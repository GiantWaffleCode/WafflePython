import krpc
import time
import math
 #  change

conn = krpc.connect(name="Orbital Test")
vessel = conn.space_center.active_vessel
srf_frame = vessel.orbit.body.reference_frame
orb_frame = vessel.orbital_reference_frame
surface_gravity = vessel.orbit.body.surface_gravity
ut = conn.add_stream(getattr, conn.space_center, 'ut')


gravity = 9.81
orbit_alt = 100000

parm1 = [10000, 87, 1.4,  "Below 10k"]  # Launch Profile
parm2 = [25000, 55, 2.0, "10k to 25k"]
parm3 = [35000, 35, 2.0, "25k to 35k"]
parm4 = [50000, 20, 2.0, "35k to 50K"]
parm5 = [70000,  0, 2.0, "50k to 70K"]
stage_parm = [parm1, parm2, parm3, parm4, parm5]


def twr():
    return vessel.thrust / (vessel.mass * surface_gravity)


def launch_control(altitude, pitch, target_twr):  # Altitude Pitch TWR
    while vessel.flight().mean_altitude < altitude:  # 10k to 20k
        # vessel.auto_pilot.target_roll = 90
        vessel.auto_pilot.target_pitch_and_heading(pitch, 90)
        if vessel.available_thrust <= 10:  # stage if out of fuel
            vessel.control.activate_next_stage()
        if vessel.orbit.apoapsis_altitude > orbit_alt:
            vessel.control.throttle = 0
            time.sleep(1)
            break
        if twr() < target_twr:
            vessel.control.throttle += .05
            time.sleep(.1)
        else:
            vessel.control.throttle -= .05
            time.sleep(.1)


def launch():
    vessel.control.throttle = 1
    print("T-3")
    time.sleep(1)
    print("T-2")
    time.sleep(1)
    print("T-1")
    time.sleep(.5)
    vessel.control.activate_next_stage()
    time.sleep(.5)
    print("LIFTOFF")
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()


def gravity_turn():
    for profile in stage_parm:
        print("Entering Gravity Profile:", profile[3])
        launch_control(profile[0], profile[1], profile[2])


def orbit_burn():
    while vessel.flight().mean_altitude < 75000:
        print(f"Altitude:{vessel.flight().mean_altitude}")
        time.sleep(.1)
    print("Calc Velocities")
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu * ((2. / r) - (1. / a1)))
    v2 = math.sqrt(mu * ((2. / r) - (1. / a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    print("Calc Delta V")
    f = vessel.available_thrust
    isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v / isp)
    flow_rate = f / isp
    burn_time = (m0 - m1) / flow_rate

    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time / 2.)
    lead_time = 10
    conn.space_center.warp_to(burn_ut - lead_time)

    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time / 2.) > 0:
        print((time_to_apoapsis() - (burn_time / 2.)))
        pass
    print("Start Burn")
    vessel.control.throttle = 1
    time.sleep(burn_time - .2)
    vessel.control.throttle = .05
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)
    while remaining_burn()[1] > 0.1:
        print(remaining_burn())
        pass
    print("Stop Burn")
    vessel.control.throttle = 0
    node.remove()
    vessel.auto_pilot.reference_frame = orb_frame
    vessel.auto_pilot.target_direction = 0, 1, 0
    vessel.auto_pilot.wait()


def main_sequence(clicked):
    if clicked:
        print(clicked)
        launch()
        gravity_turn()
        vessel.control.activate_next_stage()
        vessel.control.activate_next_stage()
        orbit_burn()
        print("Done!")
    else:
        print("Waiting for Button")
