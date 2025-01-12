import math

def radius_detect(pos1: tuple, pos2: tuple, r):
	d = math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
	return d <= r

def distance(pos1: list | tuple, pos2: list | tuple):
	return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

def generate_path(pos1, pos2, steps=100):
	path = []
	x1, y1 = pos1
	x2, y2 = pos2

	for i in range(steps):
		t = i / (steps - 1)
		x = x1 + (x2 - x1) * t
		y = y1 + (y2 - y1) * t
		path.append((x, y))

	return path


def calculate_angle(P1, P2):
	# P1과 P2의 좌표를 가져옴
	x1, y1 = P1
	x2, y2 = P2

	# 벡터 P1P2의 방향
	dx = x2 - x1
	dy = y2 - y1

	# 각도를 라디안으로 계산하고, 이를 360도 스케일로 변환
	angle_radians = math.atan2(dy, dx)
	angle_degrees = math.degrees(angle_radians)+90

	# 각도가 음수일 경우, 360도를 더하여 양수로 변환
	if angle_degrees < 0:
		angle_degrees += 360

	return angle_degrees
# print(radius_detect((0, 0), (3, 0), 3))