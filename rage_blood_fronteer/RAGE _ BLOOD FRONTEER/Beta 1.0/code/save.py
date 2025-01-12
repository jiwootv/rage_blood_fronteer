# 메인 세이브 파일을 조정하는 모듈입니다.
import time


def list_to_str(l):
	r = ""
	for i in l: r += i
	return r
class MainSave:
	def __init__(self):
		self.save_data = open("../data/save/MF", "r")
		self.SD_list = self.save_data.readlines()
		oh = 0
		for i in self.SD_list:
			t = []
			for k in i:
				if k != "\n": t.append(k)

			self.SD_list[oh] = list_to_str(t)
			oh += 1
		print(self.SD_list)
		self.save_data.close()
		self.save_data = open("../data/save/MF", "w")
		self.now_time = time.time()

	def all_save_write(self):
		print(time.time() - float(self.SD_list[1]))

		self.SD_list[1] = str(time.time())
		for i in self.SD_list[:-1]:
			self.save_data.write(i)
			self.save_data.write("\n")
		self.save_data.write(self.SD_list[len(self.SD_list)-1])

	def get_data(self, _index):
		print(self.SD_list[_index-1])
		return self.SD_list[_index-1]

M = MainSave()
M.all_save_write()
M.get_data(1)