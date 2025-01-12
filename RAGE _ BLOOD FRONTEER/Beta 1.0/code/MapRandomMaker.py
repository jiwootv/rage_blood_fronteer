import random, json

def generate_map(seed, width, height):
    random.seed(seed)  # 시드 설정
    # 맵의 종류를 나타내는 숫자
    """
    척박 50%
    일반 35%
    비옥 3% 
    용암 5%
    광물 3%
    물 4%
    """
    tile_types = []
    for i in range(50):
        tile_types.append(1)
    for i in range(35):
        tile_types.append(2)
    for i in range(3):  # 비옥인데 잠시 광물로 해둠
        tile_types.append(5)
    for i in range(5):
        tile_types.append(4)
    for i in range(3):
        tile_types.append(5)
    for i in range(4):
        tile_types.append(6)

    # 2차원 리스트로 맵 생성
    map_data = [[random.choice(tile_types) for _ in range(width)] for _ in range(height)]

    return map_data

def made_seed():
    l = ""
    l += str(random.randint(1,9))
    for i in range(5):
        l += str(random.randint(1, 10)-1)
    print(l)
    return int(l)



if __name__ == "__main__":
    made_seed()
    # 예제 사용법
    seed = int(input("Enter seed: "))  # 시드 입력받기
    width, height = 100, 100  # 맵의 크기 설정
    game_map = generate_map(seed, width, height)

    # 생성된 맵 출력
    for row in game_map:
        print(row)

    a = made_seed()
    game_map = generate_map(a, width, height)
    print("SEED:", a)
    print("--_- map -_--")
    for row in game_map:
        print(row)

