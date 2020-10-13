import krpc
import time

conn = krpc.connect(name="Orbital Test")
vessel = conn.space_center.active_vessel
srf_frame = vessel.orbit.body.reference_frame
surface_gravity = vessel.orbit.body.surface_gravity

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
        vessel.auto_pilot.target_pitch_and_heading(pitch, 90)
        if vessel.available_thrust == 0:  # stage if out of fuel
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
    while vessel.orbit.time_to_apoapsis > 10:
        vessel.auto_pilot.target_pitch_and_heading(2, 90)
        vessel.auto_pilot.wait()
        time.sleep(1)
    while vessel.orbit.periapsis_altitude < orbit_alt:
        vessel.control.throttle = 1
    vessel.control.throttle = 0


launch()
gravity_turn()
vessel.control.activate_next_stage()
vessel.control.activate_next_stage()
orbit_burn()
print("Done!")
