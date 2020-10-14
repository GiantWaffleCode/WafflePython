import krpc
import time
import math

conn = krpc.connect(name="DrawingTest")
vessel = conn.space_center.active_vessel

apo1 = vessel.orbit.speed
print(apo1)
apo2 = vessel.orbit.orbital_speed
print(apo2)
apo_speed_current = vessel.orbit.orbital_speed_at(700000)
print(vessel.orbit.body.name)
print(vessel.met)
print("Speed at Apo Currently", apo_speed_current)
print(vessel.orbit.body.gravitational_parameter)
print(vessel.orbit.apoapsis)

orbit_gm = vessel.orbit.body.gravitational_parameter
print("GM of Kerbin", orbit_gm)
apo_of_orbit = vessel.orbit.apoapsis
print("Apo of our Orbit from center of mass", apo_of_orbit)
apo_speed_needed = math.sqrt(orbit_gm / apo_of_orbit)
print("Velocity needed to orbit at apo", apo_speed_needed)