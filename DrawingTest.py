import krpc
import time

conn = krpc.connect(name="DrawingTest")
vessel = conn.space_center.active_vessel
ship_frame = vessel.reference_frame
start = [0, 0, 0]
end = [0, 0, 0]

while True:
    for i in range(0, 59, 5):
        conn.drawing.clear(True)
        start[2] = i
        end[2] = i + 5
        conn.drawing.add_line(start, end, ship_frame, visible=True)
        conn.drawing.add_text("X", ship_frame, (0, 0, 0), (0, 1, 0, 0), True)
        time.sleep(.1)


# 000 005
# 005 0010
# 0010 0015
