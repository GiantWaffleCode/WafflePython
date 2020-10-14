import krpc
import time

conn = krpc.connect(name="Orbital Test")
vessel = conn.space_center.active_vessel
# srf_frame = vessel.surface_reference_frame

# vessel.auto_pilot.engage()
# vessel.auto_pilot.reference_frame = srf_frame
# vessel.auto_pilot.target_direction
# vessel.auto_pilot.wait()

# vessel.control.sas = True
# time.sleep(.1)
# vessel.control.sas_mode = conn.space_center.SASMode.prograde
# print(dir(vessel.orbital_reference_frame))
# vessel.auto_pilot.target_heading = vessel.orbital_reference_frame[1]
# print(vessel.rotation(vessel.reference_frame)[1])

ref_frame = vessel.orbital_reference_frame
conn.drawing.add_direction((0, 1, 0), ref_frame)
vessel.auto_pilot.engage()
vessel.auto_pilot.reference_frame = ref_frame
vessel.auto_pilot.target_direction = 1, 0, 0
while True:
    pass