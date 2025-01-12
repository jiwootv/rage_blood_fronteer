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
	print(pos2)

	for i in range(steps):
		t = i / (steps - 1)
		x = x1 + (x2 - x1) * t
		y = y1 + (y2 - y1) * t
		path.append((x, y))

	return path

# print(radius_detect((0, 0), (3, 0), 3))