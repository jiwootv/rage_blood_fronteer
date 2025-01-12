import time
import json
import os

# 시간 저장 파일 경로
SAVE_FILE = 'save_data.json'

# 게임 종료 시 현재 시간을 저장하는 함수
def save_game():
    save_data = {
        'last_played': time.time()
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(save_data, f)

# 게임 재개 시 저장된 시간을 불러와서 경과 시간을 계산하는 함수
def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            save_data = json.load(f)
            last_played = save_data['last_played']
            elapsed_time = time.time() - last_played
            print(f"Elapsed time since last play: {elapsed_time} seconds")
            # 여기에 경과 시간에 따른 게임 로직을 추가
    else:
        print("No save data found.")

# 예제 실행
load_game()  # 게임 재개 시 호출
save_game()  # 게임 종료 시 호출

