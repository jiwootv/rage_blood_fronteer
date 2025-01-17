import os

# 현재 파일의 절대 경로
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(current_dir, '..', 'data'))
hangul_often_used_text_dir = os.path.join(data_dir, "asdfasdf_hangul_often_used.txt")
with open(hangul_often_used_text_dir, "rb") as file:
    hangul_often_used_text = file.read().decode('utf-8')
    hangul_often_used_list = hangul_often_used_text.split(" ")

hangul_almost_no_used_list = []
# 한글 유니코드 범위: U+AC00 ~ U+D7A3
start = 0xAC00
end = 0xD7A3

# 한글 유니코드 출력
for code in range(start, end + 1):
    if chr(code) not in hangul_often_used_list:
        hangul_almost_no_used_list.append(chr(code))

hangul_almost_no_used_text = ""
for char in hangul_almost_no_used_list:
    hangul_almost_no_used_text += char + " "

hangul_almost_no_used_text_dir = os.path.join(data_dir, "hangul_almost_no_used.txt")
with open(hangul_almost_no_used_text_dir, "w", encoding='utf8') as file:
    file.write(hangul_almost_no_used_text)
