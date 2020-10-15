import krpc
import time



conn = krpc.connect(name="UI Test")
vessel = conn.space_center.active_vessel
kerbin_frame = vessel.orbit.body.reference_frame
orb_frame = vessel.orbital_reference_frame
srf_frame = vessel.surface_reference_frame
surface_gravity = vessel.orbit.body.surface_gravity

current_roll = conn.add_stream(getattr, vessel.flight(), 'roll')
current_pitch = conn.add_stream(getattr, vessel.flight(), 'pitch')
current_heading = conn.add_stream(getattr, vessel.flight(), 'heading')
current_alt = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
current_apo = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
current_per = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
lowest = conn.add_stream(vessel.bounding_box, srf_frame)

bottom_alt = max(0, int(current_alt() - abs(lowest()[0][0])))


def engine_amount(number_of_engines):
    if number_of_engines == 1:
        vessel.control.toggle_action_group(1)
        vessel.control.toggle_action_group(3)
    elif number_of_engines == 3:
        vessel.control.toggle_action_group(1)
        vessel.control.toggle_action_group(2)
    elif number_of_engines == 9:
        vessel.control.toggle_action_group(4)
    else:
        print(f"Not a Valid Engine Request")

def twr():
    return vessel.thrust / (vessel.mass * surface_gravity)


engine_amount(9)
vessel.control.throttle = 1
vessel.control.activate_next_stage()
vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch = 85
vessel.auto_pilot.target_heading = 270
vessel.auto_pilot.target_roll = 0

while current_apo() < 10000:
    if twr() > 3:
        vessel.control.throttle -= .1
    elif twr() <= 2:
        vessel.control.throttle += .1
    time.sleep(.1)

vessel.control.throttle = 0
vessel.auto_pilot.disengage()
vessel.control.sas = True
vessel.control.rcs = True
time.sleep(.1)
vessel.control.sas_mode = conn.space_center.SASMode.prograde

while vessel.flight(kerbin_frame).vertical_speed > 0:
    time.sleep(1)

time.sleep(5)
vessel.control.sas_mode = conn.space_center.SASMode.retrograde
vessel.control.brakes = True
engine_amount(3)

while current_alt() > 1250:
    time.sleep(.1)

vessel.control.throttle = 1

while vessel.flight(kerbin_frame).vertical_speed < -50:
    time.sleep(.1)

vessel.control.gear = True
while max(0, int(current_alt() - abs(lowest()[0][0]))) > 10:
    if vessel.flight(kerbin_frame).vertical_speed < -5:
        vessel.control.throttle += .1
    else:
        vessel.control.throttle -= .1
    time.sleep(.05)

vessel.control.throttle = 0

# throttle < 10 and TWR > 2
# Go to 3 engines


