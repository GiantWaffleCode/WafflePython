import krpc

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

