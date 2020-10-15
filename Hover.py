import krpc
import time
from simple_pid import PID


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

# def twr():
#     return vessel.thrust / (vessel.mass * surface_gravity)

vessel.control.activate_next_stage()
vessel.control.sas = True
time.sleep(.1)
vessel.control.sas_mode = conn.space_center.SASMode.radial

pid1 = PID(.01, 0.005, .1, setpoint=500)
pid1.output_limits = (0, 1)
pid1.sample_time = 0.01

vessel.control.throttle = 1

while current_apo() < 600:
    print(current_apo())
    pass
vessel.control.throttle = 0
while current_alt() < 300:
    print(current_alt())
    pass
for i in range(400):
    bottom_alt = max(0, current_alt() - abs(lowest()[0][0]))
    vessel.control.throttle = pid1(bottom_alt)
    time.sleep(.01)
while True:
    bottom_alt = max(0, current_alt() - abs(lowest()[0][0]))
    vessel.control.throttle = pid1(bottom_alt)
    pid1.setpoint *= .995

g_o = 9.82

delta_v_available = vessel.kerbin_sea_level_specific_impulse\
                    * g_o * math.log(vessel.mass/vessel.dry_mass)

# vessel.max_thrust in N

