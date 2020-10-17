import krpc

conn = krpc.connect(name="UI Test")
vessel = conn.space_center.active_vessel


print(len(vessel.parts.legs))