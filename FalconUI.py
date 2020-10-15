import krpc
import time

#Init
conn = krpc.connect(name="UI Test")
vessel = conn.space_center.active_vessel
srf_frame = vessel.orbit.body.reference_frame

# Start Streams
current_met = conn.add_stream(getattr, vessel, 'met')
current_roll = conn.add_stream(getattr, vessel.flight(), 'roll')
current_pitch = conn.add_stream(getattr, vessel.flight(), 'pitch')
current_heading = conn.add_stream(getattr, vessel.flight(), 'heading')
current_roll_ap = conn.add_stream(getattr, vessel.auto_pilot, 'target_roll')
current_pitch_ap = conn.add_stream(getattr, vessel.auto_pilot, 'target_pitch')
current_heading_ap = conn.add_stream(getattr, vessel.auto_pilot, 'target_heading')
# Setup Canvas and UI Space
canvas = conn.ui.add_canvas()
screen_size = canvas.rect_transform.size
panel = canvas.add_panel()
rect = panel.rect_transform
rect.size = (300, 600)
rect.position = ((-screen_size[0]/2)+250, (screen_size[1]/2)-450)
white = (1, 1, 1)
green = (0, 1, 0)
orange = (1, .5, 0)
red = (1, 0, 0)


def write_text(name, cord, color, size, alignment=conn.ui.TextAnchor.middle_center):  # Text Function
    panel_text = panel.add_text(name)
    panel_text.rect_transform.position = cord
    panel_text.color = color
    panel_text.size = size
    panel_text.alignment = alignment
    return panel_text


def deviation_color(d_input):
    if 0 <= d_input <= 3:
        return green
    if 3 < d_input <= 10:
        return orange
    if d_input > 10:
        return red


# Text Information
text_mission_name = write_text("Powered Landing", (0, 270), white, 20,)
text_mission_time_label = write_text("Mission Time", (20, 240), white, 20,)
text_mission_time = write_text("T: 0:00:00", (32, 220), white, 20,)

text_roll = write_text("A      AP          D", (35, 0), white, 20,)

text_roll = write_text("ROL", (-150, -20), white, 20, conn.ui.TextAnchor.middle_right)
text_pitch = write_text("PIT", (-150, -40), white, 20, conn.ui.TextAnchor.middle_right)
text_heading = write_text("HED", (-150, -60), white, 20, conn.ui.TextAnchor.middle_right)

text_roll_current = write_text("", (-100, -20), white, 20, conn.ui.TextAnchor.middle_right)
text_pitch_current = write_text("", (-100, -40), white, 20, conn.ui.TextAnchor.middle_right)
text_heading_current = write_text("", (-100, -60), white, 20, conn.ui.TextAnchor.middle_right)

text_roll_ap = write_text("", (-40, -20), white, 20, conn.ui.TextAnchor.middle_right)
text_pitch_ap = write_text("", (-40, -40), white, 20, conn.ui.TextAnchor.middle_right)
text_heading_ap = write_text("", (-40, -60), white, 20, conn.ui.TextAnchor.middle_right)

text_roll_d = write_text("", (35, -20), white, 20, conn.ui.TextAnchor.middle_right)
text_pitch_d = write_text("", (35, -40), white, 20, conn.ui.TextAnchor.middle_right)
text_heading_d = write_text("", (35, -60), white, 20, conn.ui.TextAnchor.middle_right)

vessel.auto_pilot.target_pitch = 90
vessel.auto_pilot.target_roll = -85

while True:
    text_mission_time.content = f"T: {time.strftime('%H:%M:%S', time.gmtime(current_met()))}"
    text_roll_current.content = f"{int(round(current_roll(),1))}"
    text_pitch_current.content = f"{int(round(current_pitch(), 0))}"
    text_heading_current.content = f"{int(round(current_heading(), 0))}"
    text_roll_ap.content = f"{int(round(current_roll_ap(), 0))}"
    text_pitch_ap.content = f"{int(round(current_pitch_ap(), 0))}"
    text_heading_ap.content = f"{int(round(current_heading_ap(), 0))}"
    text_roll_d.content = f"{abs(int(round(current_roll(),1)) - int(round(current_roll_ap(), 0)))}"
    text_pitch_d.content = f"{abs(int(round(current_pitch(),1)) - int(round(current_pitch_ap(), 0)))}"
    text_heading_d.content = f"{abs(int(round(current_heading(),1)) - int(round(current_heading_ap(), 0)))}"
    text_roll_d.color = deviation_color(int(text_roll_d.content))
    text_pitch_d.color = deviation_color(int(text_pitch_d.content))
    text_heading_d.color = deviation_color(int(text_heading_d.content))



    time.sleep(.1)
#     vessel_twr = Orbit.twr()
#     text_twr.content = "TWR: " + str(round(vessel_twr, 3))
#     text_mission_time.content = "T: " + time.strftime('%H:%M:%S', time.gmtime(vessel.met))
#     vessel_ap_roll = vessel.auto_pilot.target_roll  # AP Heading
#     text_ap_roll.content = "AP Roll: " + str(round(vessel_ap_roll, 1))
#     vessel_ap_pitch = vessel.auto_pilot.target_pitch
#     text_ap_pitch.content = "AP Pitch: " + str(round(vessel_ap_pitch, 1))
#     vessel_ap_heading = vessel.auto_pilot.target_heading
#     text_ap_heading.content = "AP Yaw: " + str(round(vessel_ap_heading, 1))
