import krpc
import math
import time

conn = krpc.connect(name="Orbital Test")
vessel = conn.space_center.active_vessel
srf_frame = vessel.orbit.body.reference_frame
orb_frame = vessel.orbital_reference_frame

semi_major = vessel.orbit.semi_major_axis
current_radius = vessel.orbit.radius
gm = vessel.orbit.body.gravitational_parameter

# print(f"SM: {semi_major}, R: {current_radius}, GM: {gm}")

current_velocity = math.sqrt(gm*((2/current_radius)-(1/semi_major)))

print(f"Current Velocity = {current_velocity}")


body = vessel.orbit.body
position = vessel.position(srf_frame)
velocity = vessel.velocity(srf_frame)
longitude_theta = vessel.flight().longitude

# print(f"Position: {position}")
# print(f"Velocity: {velocity}")

test_position = (-455327.7883170786, 0, 428781.4531900575)
test_velocity = (-1172.9277956788721, -0.9998800602363062, -1595.6175622169937)

aero_forces = vessel.flight().simulate_aerodynamic_force_at(body, test_position, test_velocity)

print(f"Aero Forces: {aero_forces}")

# Aero Forces: (1241697.381862863, -33261.73632646327, 320030.1770709742)