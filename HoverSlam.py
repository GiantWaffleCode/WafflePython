import krpc
import time
import math
from simple_pid import PID

conn = krpc.connect(name="UI Test")
vessel = conn.space_center.active_vessel
kerbin_frame = vessel.orbit.body.reference_frame
orb_frame = vessel.orbital_reference_frame
srf_frame = vessel.surface_reference_frame
surface_gravity = vessel.orbit.body.surface_gravity

current_met = conn.add_stream(getattr, vessel, 'met')
current_roll = conn.add_stream(getattr, vessel.flight(), 'roll')
current_pitch = conn.add_stream(getattr, vessel.flight(), 'pitch')
current_heading = conn.add_stream(getattr, vessel.flight(), 'heading')
current_alt = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
lowest = conn.add_stream(vessel.bounding_box, srf_frame)
current_drag = conn.add_stream(getattr, vessel.flight(), 'drag')
current_aero = conn.add_stream(getattr, vessel.flight(), 'aerodynamic_force')
current_speed = conn.add_stream(getattr, vessel.flight(kerbin_frame), 'speed')

vessel.control.activate_next_stage()
vessel.control.sas = True
time.sleep(.2)
vessel.control.sas_mode = conn.space_center.SASMode.retrograde


def bottom_altitude():
    return max(0, current_alt() - abs(lowest()[0][0]))


for engine in vessel.parts.engines:
    engine.gimbal_locked = True

while True:
    aero_amp = math.sqrt(current_aero()[0] ** 2
                         + current_aero()[1] ** 2
                         + current_aero()[2] ** 2)
    time_to_zero = current_speed() / ((((vessel.max_thrust * .9) + aero_amp) / vessel.mass)
                                      + vessel.orbit.body.surface_gravity)
    if (time_to_zero * current_speed()) >= bottom_altitude() - current_speed():
        print(current_speed())
        print(f"Start Hover Slam Burn")
        vessel.control.throttle = .9
        break
while current_speed() > 50:
    print(current_speed())
    time.sleep(.01)
    pass
print(f"Switch to Stab")

for leg in vessel.parts.legs:
    leg.deployed = True

pid1 = PID(.15, 0, .5, setpoint=0)
pid1.output_limits = (0, 1)
pid1.sample_time = 0.01

while bottom_altitude() > 1:
    vessel.control.throttle = pid1(bottom_altitude())
    # pid1.setpoint *= .98
    time.sleep(.01)
vessel.control.sas_mode = conn.space_center.SASMode.radial
vessel.control.throttle = 0
