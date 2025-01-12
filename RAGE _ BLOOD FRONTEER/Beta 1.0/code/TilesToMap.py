import json
class Map_to_json:
	def __init__(self):
		self.m = {"tilemap":{}}
	def map_size_set(self, w, h):
		self.m["size"] = [w, h]

	def start_pos_set(self, w, h):
		self.m["startpos"] = [w, h]

	def maptileadd(self, imgname, pos, type, IRID=0):
		self.m["tilemap"][f"{pos[0]};{pos[1]}"] = {"IRID" : IRID, "img":imgname, "pos" : pos, "type":"type"}
	def Pr(self):
		print(self.m)
		return self.m
if __name__ == "__main__":
	M = Map_to_json()
	M.map_size_set(20, 20)
	M.start_pos_set(0, 0)
	M.maptileadd("채민이 게이", [1, 5], "wall", 1)
	M.Pr()