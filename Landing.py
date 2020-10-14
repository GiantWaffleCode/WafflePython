import krpc
import math
import time

# center_lat = vessel.orbit.body.latitude_at_position((0, 1, 0), vessel.reference_frame)
# center_long = vessel.orbit.body.longitude_at_position((0, 1, 0), vessel.reference_frame)

# print(f"KSC Latitude: {center_lat}")
# print(f"KSC Longitude: {center_long}")
# print('(%.1f, %.1f, %.1f)' % vessel_pos)

# r = math.sqrt(vessel_pos[0]**2 + vessel_pos[1]**2 + vessel_pos[2]**2)
# theta_lat = math.atan((math.sqrt(vessel_pos[0] ** 2 + vessel_pos[2] ** 2) / vessel_pos[1]))

# print(f"Latitude Angle: {round(math.degrees(theta_lat), 3)}")


def main_sequence(clicked):
    if clicked:
        print(clicked)

        conn = krpc.connect(name="Orbital Test")
        vessel = conn.space_center.active_vessel
        kerbin_ref = vessel.orbit.body.reference_frame

        target_theta_long = -125

        while True:
            vessel_pos = vessel.position(kerbin_ref)
            theta_long = math.atan2(vessel_pos[2], vessel_pos[0])
            theta_long_dif = math.degrees(theta_long) - target_theta_long
            print(f"Longitude Angle: {round(math.degrees(theta_long), 3)}, Angle Difference ={theta_long_dif}")
            if 1 > theta_long_dif > 0:
                break
            time.sleep(1)

        vessel.control.sas = True
        time.sleep(1)
        vessel.control.sas_mode = conn.space_center.SASMode.retrograde
        time.sleep(2)
        vessel.control.throttle = 1
        time.sleep(10)
        vessel.control.throttle = 0
        vessel.control.sas_mode = conn.space_center.SASMode.radial
        time.sleep(1)
        vessel.control.activate_next_stage()
        vessel.control.sas_mode = conn.space_center.SASMode.retrograde
        while vessel.flight().mean_altitude > 5000:
            time.sleep(1)
        vessel.control.activate_next_stage()
        print(f"Landed!")
    else:
        print("Waiting for Button")

