import krpc
import time
import Orbit
import Landing
import datetime

conn = krpc.connect(name="UI Test")
vessel = conn.space_center.active_vessel
srf_frame = vessel.orbit.body.reference_frame
canvas = conn.ui.add_canvas()

# Get the size of the game window in pixels
screen_size = canvas.rect_transform.size
# screen_top_left = screen_size * 2
print(screen_size)
# Add a panel to contain the UI elements
panel = canvas.add_panel()

rect = panel.rect_transform
rect.size = (300, 600)
rect.position = ((-screen_size[0]/2)+250, (screen_size[1]/2)-850)


def make_button(name, cord):  # Creates Text Objects
    panel_button = panel.add_button(name)
    panel_button.rect_transform.position = cord
    panel_button.color = (1, 1, 1)
    panel_button.size = 18
    return panel_button


button_launch = make_button("Launch", (0, rect.size[1]/2 - 50))
button_landing = make_button("Land", (0, rect.size[1]/2 - 100))


def write_text(name, cord):  # Creates Text Objects
    panel_text = panel.add_text(name)
    panel_text.rect_transform.position = cord
    panel_text.color = (1, 1, 1)
    panel_text.size = 20
    return panel_text


# def quick_load(clicked):
#     print(clicked)
#     if clicked:
#         print("RESET WAS PUSHED")
#         conn.space_center.quickload()
#         button_launch_clicked.start()
#         # button_reset.clicked = False


text_roll = write_text("Roll", (0, -20))  # Text Objects i want
text_pitch = write_text("Pitch", (0, -40))
text_heading = write_text("Heading", (0, -60))
text_twr = write_text("TWR: Fix this Alan", (0, -80))
text_ap_roll = write_text("AP Roll", (0, -120))  # Text Objects i want
text_ap_pitch = write_text("AP Pitch", (0, -140))
text_ap_heading = write_text("AP Heading", (0, -160))

text_mission_time_label = write_text("Mission Time", (0, 100))
text_mission_time = write_text("T ", (0, 75))

# Set up a stream to monitor the throttle button
button_launch_clicked = conn.add_stream(getattr, button_launch, 'clicked')
button_launch_clicked.add_callback(Orbit.main_sequence)
button_launch_clicked.start()

button_landing_clicked = conn.add_stream(getattr, button_landing, 'clicked')
button_landing_clicked.add_callback(Landing.main_sequence)
button_landing_clicked.start()

while True:
    vessel_roll = vessel.flight().roll  # Update Nav Object Text
    text_roll.content = "Roll: " + str(round(vessel_roll, 1))
    vessel_pitch = vessel.flight().pitch
    text_pitch.content = "Pitch: " + str(round(vessel_pitch, 1))
    vessel_heading = vessel.flight().heading
    text_heading.content = "Yaw: " + str(round(vessel_heading, 1))
    vessel_twr = Orbit.twr()
    text_twr.content = "TWR: " + str(round(vessel_twr, 3))
    text_mission_time.content = "T: " + time.strftime('%H:%M:%S', time.gmtime(vessel.met))
    vessel_ap_roll = vessel.auto_pilot.target_roll  # AP Heading
    text_ap_roll.content = "AP Roll: " + str(round(vessel_ap_roll, 1))
    vessel_ap_pitch = vessel.auto_pilot.target_pitch
    text_ap_pitch.content = "AP Pitch: " + str(round(vessel_ap_pitch, 1))
    vessel_ap_heading = vessel.auto_pilot.target_heading
    text_ap_heading.content = "AP Yaw: " + str(round(vessel_ap_heading, 1))
    time.sleep(0.1)
