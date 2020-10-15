import krpc
import time
import datetime

#Init
conn = krpc.connect(name="UI Test")
vessel = conn.space_center.active_vessel
kerbin_frame = vessel.orbit.body.reference_frame
orb_frame = vessel.orbital_reference_frame
srf_frame = vessel.surface_reference_frame
surface_gravity = vessel.orbit.body.surface_gravity

# Start Streams
current_met = conn.add_stream(getattr, vessel, 'met')
current_roll = conn.add_stream(getattr, vessel.flight(), 'roll')
current_pitch = conn.add_stream(getattr, vessel.flight(), 'pitch')
current_heading = conn.add_stream(getattr, vessel.flight(), 'heading')
current_roll_ap = conn.add_stream(getattr, vessel.auto_pilot, 'target_roll')
current_pitch_ap = conn.add_stream(getattr, vessel.auto_pilot, 'target_pitch')
current_heading_ap = conn.add_stream(getattr, vessel.auto_pilot, 'target_heading')
current_alt = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
lowest = conn.add_stream(vessel.bounding_box, srf_frame)
current_apo = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
current_per = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
current_time_to_apo = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
current_time_to_per = conn.add_stream(getattr, vessel.orbit, 'time_to_periapsis')

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


def deviation_color_ap(d_input):
    if 0 <= d_input <= 3:
        return green
    if 3 < d_input <= 10:
        return orange
    if d_input > 10:
        return red


def deviation_color_twr(d_input):
    if 0 <= d_input < 1:
        return red
    if 1 <= d_input <= 2:
        return green
    if d_input > 2:
        return orange


def twr():
    return vessel.thrust / (vessel.mass * surface_gravity)


# Text Information
text_mission_name = write_text("Powered Landing", (0, 270), white, 20,)
text_mission_time_label = write_text("Mission Time", (0, 240), white, 20,)
text_mission_time = write_text("T: 0:00:00", (0, 220), white, 20,)

text_label = write_text("A      AP          D", (35, 0), white, 20,)

text_roll = write_text("ROL", (-150, -20), white, 20, conn.ui.TextAnchor.middle_right)
text_pitch = write_text("PIT", (-150, -40), white, 20, conn.ui.TextAnchor.middle_right)
text_heading = write_text("HDG", (-150, -60), white, 20, conn.ui.TextAnchor.middle_right)

text_roll_current = write_text("", (-100, -20), white, 20, conn.ui.TextAnchor.middle_right)
text_pitch_current = write_text("", (-100, -40), white, 20, conn.ui.TextAnchor.middle_right)
text_heading_current = write_text("", (-100, -60), white, 20, conn.ui.TextAnchor.middle_right)

text_roll_ap = write_text("", (-40, -20), white, 20, conn.ui.TextAnchor.middle_right)
text_pitch_ap = write_text("", (-40, -40), white, 20, conn.ui.TextAnchor.middle_right)
text_heading_ap = write_text("", (-40, -60), white, 20, conn.ui.TextAnchor.middle_right)

text_roll_d = write_text("", (35, -20), white, 20, conn.ui.TextAnchor.middle_right)
text_pitch_d = write_text("", (35, -40), white, 20, conn.ui.TextAnchor.middle_right)
text_heading_d = write_text("", (35, -60), white, 20, conn.ui.TextAnchor.middle_right)

text_alt = write_text("ALT:", (-100, 180), white, 20, conn.ui.TextAnchor.middle_right)

text_apo_alt_text = write_text("APO", (-100, -140), white, 20,)
text_per_alt_text = write_text("PER", (-100, -160), white, 20,)

text_apo_alt = write_text("", (-60, -140), white, 20, conn.ui.TextAnchor.middle_right)
text_per_alt = write_text("", (-60, -160), white, 20, conn.ui.TextAnchor.middle_right)

text_apo_time = write_text("", (30, -140), white, 20, conn.ui.TextAnchor.middle_right)
text_per_time = write_text("", (30, -160), white, 20, conn.ui.TextAnchor.middle_right)

text_twr_label = write_text("TWR:", (-100, -220), white, 20,)
text_twr = write_text("", (20, -220), white, 20, conn.ui.TextAnchor.middle_left)


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
    text_roll_d.color = deviation_color_ap(int(text_roll_d.content))
    text_pitch_d.color = deviation_color_ap(int(text_pitch_d.content))
    text_heading_d.color = deviation_color_ap(int(text_heading_d.content))
    text_alt.content = f"ALT: {max(0, int(current_alt() - abs(lowest()[0][0])))}"
    text_apo_alt.content = f"{int(round(current_apo(), 0))}"
    text_per_alt.content = f"{int(round(current_per(), 0))}"
    text_apo_time.content = f"{(datetime.timedelta(seconds=int(current_time_to_apo())))}"
    text_per_time.content = f"{(datetime.timedelta(seconds=int(current_time_to_per())))}"
    text_twr.content = f"{float(round(twr(), 2))}"
    text_twr.color = deviation_color_twr(float(text_twr.content))

    time.sleep(.1)

