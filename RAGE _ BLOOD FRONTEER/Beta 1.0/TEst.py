import code.MapRandomMaker as MRM
import code.TilesToMap as TTM
import json
for i in MRM.generate_map(2000, 20, 20): print(i)
m = MRM.generate_map(2000, 20, 20)
T = TTM.Map_to_json()
T.start_pos_set(0, 0)
T.map_size_set(20, 20)
"""
척박 50%
일반 35%
비옥 3% 
용암 5%
광물 3%
물 4%
"""
for x in range(20):
	for y in range(20):
		l = ["PlanetFloor3", "PlanetFloor2", "___", "lava", "PlanetFloor1", "water"]
		T.maptileadd(imgname=l[m[x][y]-1], pos=[x,y], type="floor", IRID=0)
T.Pr()
# 딕셔너리를 JSON 파일로 저장
with open("output.json", "w") as json_file:
	json.dump(T.Pr(), json_file)
