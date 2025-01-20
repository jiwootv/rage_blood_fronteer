import os

import codes.MAP_Ver2 as GameMap
import codes.KeyEventTkinterToPygame as KeyTk2Pygame
import tkinter as tk
from tkinter import ttk
import pygame
import json

DEBUG = False
pygame.init()  # pygame 모듈 초기화


def center_window(window):
    window.update_idletasks()  # 창의 크기 계산
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 중앙 좌표로 창 위치 설정
    position_top = int(screen_height / 2 - height / 2)
    position_left = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_left}+{position_top}')


class Main:
    def __init__(self):
        # Tkinter 초기화
        self.root = tk.Tk()
        self.root.title("1950 Map Editor")  # 창 제목 설정
        self.root.geometry("880x660")  # Tkinter 창 크기 설정
        self.root.resizable(False, False)  # 창 크기 조절 불가능 설정

        # Tkinter에서 Pygame을 포함할 프레임 생성
        pygame_frame = tk.Frame(self.root, width=880, height=660, bg="black")  # Pygame이 렌더링될 영역
        pygame_frame.pack()

        # Pygame 창을 Tkinter 프레임에 임베딩
        os.environ['SDL_WINDOWID'] = str(pygame_frame.winfo_id())  # SDL 창 ID 설정
        os.environ['SDL_VIDEODRIVER'] = 'windib'  # Windows에서 제대로 동작하도록 드라이버 설정
        self.root.update()  # 창을 업데이트하여 ID가 반영되도록 함

        # Tkinter 창 닫기 이벤트 처리
        self.root.protocol("WM_DELETE_WINDOW", self.stop_running)

        # 초기화
        pygame.init()
        pygame.mixer.init()
        self.select_SE = pygame.mixer.Sound(r'data/sound/effect/A Piano.wav')
        self.collect_SE = pygame.mixer.Sound(r'data/sound/effect/Connect.wav')

        if DEBUG:
            print("성공적으로 Main 클래스가 로드되었습니다")
        # screen, preview(메인 스크린 배경), [preview1, preview2] (서브 스크린 배경 (ui?)) clock 초기화
        self.screen = pygame.display.set_mode((880, 660))  # 640, 480의 1.375배
        self.preview = pygame.rect.Rect(0, 0, 640, 480)
        self.preview1 = pygame.rect.Rect(0, 480, 640, 180)
        self.preview2 = pygame.rect.Rect(640, 0, 240, 660)
        self.clock = pygame.time.Clock()

        # tile_size, map_max 초기화 (아마도 타일 하나당 width, height 크기랑, 한 맵에 있는 타일의 개수 말하는 듯)
        self.tile_size = 60
        self.map_max = 30

        self.Map_c = GameMap.Map(self.screen, pygame_in_game=pygame)
        self.file_index = 1
        self.select_IRID = 0
        self.mouserect = 0
        self.select_tileType = 1
        self.map_load_onoff = 0
        self.is_wall = 1
        # 현재 map list 생성
        self.now_map = self.Map_c.get_all_map()
        self.text = lambda size, text, color, x, y: self.screen.blit(
            pygame.font.Font(r"data/font/DungGeunMo.otf", size).render(text, 1, color), (x, y))
        self.pos_x, self.pos_y = 0, 0

        self.tile_name_list = list(self.Map_c.assets.keys())
        self.tile_name_list.insert(0, "삭제 모드")
        if DEBUG:
            print(self.tile_name_list)
        self.running = True

        KeyTk2Pygame.add_key_event_from_tk_to_pygame(self.root, pygame)

        # 메뉴바 생성
        menubar = tk.Menu(self.root)

        def donothing():
            filewin = tk.Toplevel(self.root)
            button = tk.Button(filewin, text="Do nothing button")
            button.pack()

        def new():
            new_win = tk.Toplevel(self.root)
            new_win.title("New")

            new_win.columnconfigure(0, weight=1)
            new_win.columnconfigure(1, weight=1)
            new_win.columnconfigure(2, weight=1)

            # 1. 첫 번째 행: 레이블
            label = tk.Label(new_win, text="생성할 맵 이름을 적어주세요.")
            label.grid(row=0, column=0, columnspan=3, pady=10)

            # 2. 두 번째 행: room 레이블, 입력 필드, .json 레이블
            label_room = tk.Label(new_win, text="room")
            label_room.grid(row=1, column=0, sticky="e", padx=(5, 0))

            entry_num = tk.Entry(new_win)
            entry_num.grid(row=1, column=1)

            label_json = tk.Label(new_win, text=".json")
            label_json.grid(row=1, column=2, sticky="w", padx=(0, 5))

            # 3. 세 번째 행: 확인 버튼
            button_get_input = tk.Button(
                new_win,
                text="확인",
                width=10,
                command=lambda: new1(f"room{entry_num.get()}.json", new_win),
            )
            button_get_input.grid(row=2, column=0, columnspan=3, pady=10)

        def new1(file_name, last_window):
            last_window.destroy()
            new_win = tk.Toplevel(self.root)
            new_win.title("New")

            # 창의 모든 열을 균등하게 확장 가능하도록 설정
            new_win.columnconfigure(0, weight=1)
            new_win.columnconfigure(1, weight=1)
            new_win.columnconfigure(2, weight=1)
            new_win.columnconfigure(3, weight=1)

            label = tk.Label(new_win, text="생성할 맵 사이즈를 적어주세요.")
            label.grid(row=0, column=0, columnspan=2, pady=10)
            # 'room' 레이블
            label_width = tk.Label(new_win, text="width:")
            label_width.grid(row=1, column=0)

            # 입력 필드
            entry_size_w = tk.Entry(new_win)
            entry_size_w.grid(row=1, column=1)

            # 'room' 레이블
            label_height = tk.Label(new_win, text="height:")
            label_height.grid(row=2, column=0)

            # 입력 필드
            entry_size_h = tk.Entry(new_win)
            entry_size_h.grid(row=2, column=1)

            button_get_input = tk.Button(
                new_win,
                text="확인",
                width=10,
                command=lambda:
                self.make_new_map(file_name, [int(entry_size_w.get()), int(entry_size_h.get())], new_win)
            )
            button_get_input.grid(row=3, column=0, columnspan=2, pady=10)

        def open():
            open_win = tk.Toplevel(self.root)
            open_win.title("열 맵을 선택해주세요.")
            listbox = tk.Listbox(open_win, height=0, selectmode="extended")
            for map in self.Map_c.get_map_list():
                listbox.insert(tk.END, map)
            listbox.pack()

            # 버튼 추가 (선택된 항목 반환)
            button = tk.Button(open_win, text="선택하기", command=lambda: self.map_load_in_listbox(listbox, open_win))
            button.pack()

            # Toplevel 창을 중앙에 배치하는 함수
            center_window(open_win)

        def save():
            self.save(f"room{self.file_index}.json")

        def save_as():
            new_win = tk.Toplevel(self.root)
            new_win.title("Save As...")

            new_win.columnconfigure(0, weight=1)
            new_win.columnconfigure(1, weight=1)
            new_win.columnconfigure(2, weight=1)

            # 1. 첫 번째 행: 레이블
            label = tk.Label(new_win, text="저장할 맵 이름을 적어주세요.")
            label.grid(row=0, column=0, columnspan=3, pady=10)

            # 2. 두 번째 행: room 레이블, 입력 필드, .json 레이블
            label_room = tk.Label(new_win, text="room")
            label_room.grid(row=1, column=0, sticky="e", padx=(5, 0))

            entry_num = tk.Entry(new_win)
            entry_num.grid(row=1, column=1)

            label_json = tk.Label(new_win, text=".json")
            label_json.grid(row=1, column=2, sticky="w", padx=(0, 5))

            # 3. 세 번째 행: 확인 버튼
            button_get_input = tk.Button(
                new_win,
                text="확인",
                width=10,
                command=lambda:
                self.save_as_map(f"room{entry_num.get()}.json", self.Map_c.mapGet(self.file_index), new_win),
            )
            button_get_input.grid(row=2, column=0, columnspan=3, pady=10)

        # 파일 메뉴 생성 및 추가
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=new)
        filemenu.add_command(label="Open", command=open)
        filemenu.add_command(label="Save", command=save)
        filemenu.add_command(label="Save as...", command=save_as)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # 메뉴바를 Tkinter 창에 설정
        self.root.config(menu=menubar)

    def draw_preview(self):
        """
        메인 화면 배경 그리는 함수
        """
        pygame.draw.rect(self.screen, (0, 0, 0), self.preview)

    def draw_hider(self):
        """
        화면 ui 배경 그리는 함수
        """
        pygame.draw.rect(self.screen, (0, 0, 70), self.preview1)
        pygame.draw.rect(self.screen, (0, 0, 70), self.preview2)

    def lines(self):
        """
        메인 배경 격자 그리는 함수
        """
        for k in range(0, self.Map_c.get_size()[0] * self.tile_size + 1, self.tile_size):  # 가로선
            x, y = self.Map_c.moveposGet()
            pygame.draw.line(self.screen, (255, 255, 255), start_pos=(x, k + y),
                             end_pos=(x + self.Map_c.get_size()[0] * self.tile_size, k + y))

        for k in range(0, self.Map_c.get_size()[1] * self.tile_size + 1, self.tile_size):  # 가로선
            x, y = self.Map_c.moveposGet()
            pygame.draw.line(self.screen, (255, 255, 255), start_pos=(k + x, y),
                             end_pos=(k + x, self.Map_c.get_size()[1] * self.tile_size + y))

    def event(self):
        """
        이벤트 다루는 함수
        """
        # 마우스 pos 가져오기
        x, y = pygame.mouse.get_pos()
        # 마우스를 기준으로 해서 10x10 사각형 만들기
        # 좌측 상단보다 중앙이 나을 것 같아서 조금 바꿈
        self.mouserect = pygame.rect.Rect(x - 5, y - 5, 10, 10)
        # 마우스 렉트 그리기
        pygame.draw.rect(self.screen, (255, 255, 255), self.mouserect)  # 마우스에 Rect개체 덮어 씨우기

        x, y = self.Map_c.moveposGet()  # 맵의 이동 좌표 얻기
        x1, y1 = pygame.mouse.get_pos()  # 마우스 좌표얻기
        self.pos_x, self.pos_y = (x * -1 + x1) // self.tile_size, (
                y * -1 + y1) // self.tile_size  # 그걸 Tile size로 나누어 커서가 위치한 pos 계산

        # print(self.now_map[self.file_index - 1]["tilemap"][f"{self.pos_x};{self.pos_y}"])
        # print(self.pos_x, self.pos_y)  # 그 pos 출력
        # 지금 당장 savefile 저장
        # noinspection PyTypeChecker
        # 위 주석은 무시하셈.

        # 단축기
        pressed_keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_running()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.select_IRID += 1
                    self.select_SE.play()
                if event.key == pygame.K_k and not self.select_IRID == 0:
                    self.select_IRID -= 1
                    self.select_SE.play()
                if event.key == pygame.K_f and not self.select_tileType == 0:
                    if DEBUG:
                        print("POPIPOPIPO")
                    self.select_tileType -= 1
                    self.select_SE.play()
                if event.key == pygame.K_r and len(self.tile_name_list) != self.select_tileType + 1:
                    self.select_tileType += 1
                    self.select_SE.play()

                if event.key == pygame.K_l:
                    self.select_SE.play()
                    self.is_wall = not self.is_wall

                if pressed_keys[pygame.K_RCTRL] or pressed_keys[pygame.K_LCTRL]:
                    if event.key == pygame.K_s:
                        self.save(f"room{self.file_index}.json")

            if (event.type == pygame.MOUSEBUTTONDOWN and
                    event.button == 3 and
                    self.pos_x >= 0 and self.pos_y >= 0 and
                    self.pos_x < self.Map_c.get_size()[0] and
                    self.pos_y < self.Map_c.get_size()[1]):
                # 메인 ui에 마우스가 있는 경우
                if self.mouserect.colliderect(self.preview):
                    OptionTopLevel(self.root, self.pos_x + 1, self.pos_y + 1, self.Map_c,
                                   self.now_map, self.file_index)
            # print("WALL or FLOOR : {}".format(self.is_wall))

        # 마우스 클릭 감지 및, 맵 에디터 설정
        if (pygame.mouse.get_pressed()[0] and
                self.pos_x >= 0 and self.pos_y >= 0 and
                self.pos_x < self.Map_c.get_size()[0] and
                self.pos_y < self.Map_c.get_size()[1]):  # 마우스 좌클릭 감지
            # 메인 ui에 마우스가 있는 경우
            if self.mouserect.colliderect(self.preview):
                try:
                    # select_tileType가 0(Delete)가 아닌 경우
                    if self.select_tileType != 0:
                        if DEBUG:
                            print(["floor", "wall"][self.is_wall])
                        # file_index번 맵에서 tilemap을 가져와 pos_x와 pos_y에 있는 타일의 이미지를
                        # tile_name_list[select_tileType]로 설정하고
                        # type를 floor, wall중에 선택되어있는걸로 설정한다.
                        if not self.now_map[f"room{self.file_index}.json"]["tilemap"].get(
                                f"{self.pos_x + 1};{self.pos_y + 1}"):
                            self.now_map[f"room{self.file_index}.json"]["tilemap"][
                                f"{self.pos_x + 1};{self.pos_y + 1}"] = {
                                "event": 0,
                                "img": "",
                                "pos": [
                                    0,
                                    0
                                ],
                                "type": ""
                            }
                        self.now_map[f"room{self.file_index}.json"]["tilemap"][f"{self.pos_x + 1};{self.pos_y + 1}"][
                            "img"] = self.tile_name_list[self.select_tileType]
                        self.now_map[f"room{self.file_index}.json"]["tilemap"][f"{self.pos_x + 1};{self.pos_y + 1}"][
                            "pos"] = [self.pos_x + 1, self.pos_y + 1]
                        self.now_map[f"room{self.file_index}.json"]["tilemap"][f"{self.pos_x + 1};{self.pos_y + 1}"][
                            "type"] = ["floor", "wall"][self.is_wall]
                    # 아니면
                    else:
                        if DEBUG:
                            print('Delete')
                        # 지워버린다.
                        del self.now_map[f"room{self.file_index}.json"]["tilemap"][f"{self.pos_x + 1};{self.pos_y + 1}"]
                    # 이걸로 다시 맵 로딩을 한다.
                    self.Map_c.load_to_list(self.now_map[f"room{self.file_index}.json"])
                except KeyError:
                    if DEBUG:
                        print("None")

    def nowMapGet(self):
        """
        현재 맵을 반환합니다.
        (아직 안씀)
        :return: self.now_map
        """
        return self.now_map

    def save(self, file_name):
        """
        맵을 파일로 저장합니다.
        """
        print("SAVING...")
        a = str(json.dumps(self.now_map[file_name], indent=4, sort_keys=True))
        # print(a)
        with open(f"data\\map_Ver2\\{file_name}", "w") as file:
            if DEBUG:
                print(self.now_map[file_name])
            file.write(a)
            if DEBUG:
                print("GAY")

    def save_all(self):
        """
        맵을 파일로 저장합니다.
        """
        print("SAVING...")
        for file_name in self.Map_c.get_map_list():
            if DEBUG: print(file_name)
            a = str(json.dumps(self.now_map[file_name], indent=4, sort_keys=True))
            # print(a)
            with open(f"data\\map_Ver2\\{file_name}", "w") as file:
                if DEBUG:
                    print(self.now_map[file_name])
                file.write(a)
                if DEBUG:
                    print("GAY")

    def run(self):
        self.Map_c.load_to_list(self.Map_c.mapGet(1))
        self.Map_c.draw_set()
        self.Map_c.brickPassSet(1)
        while self.running:
            pygame.event.pump()

            self.screen.fill((0, 0, 0))
            a = "존재하지 않는 IRID"

            self.draw_preview()

            self.Map_c.draw()
            self.Map_c.event()

            self.lines()
            self.draw_hider()
            self.event()
            self.text(30, "현재 맵 파일 번호: %d" % int(self.file_index), (255, 255, 255), 500, 600)
            self.text(30, a, (255, 255, 255), 600, 550)
            self.text(30, "현재 IRID: %d" % self.select_IRID, (255, 255, 255), 600, 500)
            self.text(30, "현재 좌표: %d;%d" % (self.pos_x + 1, self.pos_y + 1), (255, 255, 255), 300, 500)
            try:
                self.text(30,
                          "현재 타일:" +
                          self.now_map[f"room{self.file_index}.json"]["tilemap"][f"{self.pos_x + 1};{self.pos_y + 1}"][
                              "img"], (255, 255, 255), 300, 550)
            except KeyError:
                self.text(30, "현재 타일: 없음", (255, 255, 255), 300, 550)
            self.text(30, f"현재 선택 타일", (255, 255, 255), 650, 0)
            self.text(30, f"벽 여부: {bool(self.is_wall)}", (255, 255, 255), 650, 100)

            try:
                self.text(19,
                          f"현재 타일 벽 여부: {self.now_map[f"room{self.file_index}.json"]["tilemap"][f"{self.pos_x + 1};{self.pos_y + 1}"]["type"]}",
                          (255, 255, 255), 650, 150)
            except KeyError:
                self.text(19, f"현재 타일 벽 여부: None", (255, 255, 255), 650, 150)
            self.text(20, f"{self.tile_name_list[self.select_tileType]}", (255, 255, 255), 700, 80)
            # 미리보기 드로우
            if self.select_tileType != 0:
                self.screen.blit(
                    pygame.transform.scale(self.Map_c.assets[self.tile_name_list[self.select_tileType]], (40, 40)),
                    (750, 40))
            pygame.display.update()

            self.clock.tick(60)

            # Tkinter 이벤트 처리 (화면 업데이트 및 이벤트 처리)
            self.root.update_idletasks()
            self.root.update()

    # print(self.now_map[f"room{self.file_index}.json"])
    # print(json.dumps(self.now_map[f"room{self.file_index}.json"], indent=4, separators=("{", "="), sort_keys=True))

    def make_new_map(self, file_name, size=None, window=None):
        if size is None:
            size = [20, 20]
        map_dir = "data/map_Ver2/"
        with open(map_dir + file_name, "w+", encoding="utf8") as file:
            file.write(json.dumps({"size": size, "startpos": [0, 0], "tilemap": {}}, indent=4, sort_keys=True))
        self.Map_c.reload_file()
        self.now_map = self.Map_c.get_all_map()
        self.map_load_with_file_name(file_name)
        window.destroy()

    def save_as_map(self, file_name, map, window=None):
        map_dir = "data/map_Ver2/"
        with open(map_dir + file_name, "w+", encoding="utf8") as file:
            file.write(json.dumps(map, indent=4, sort_keys=True))
        self.Map_c.reload_file()
        self.now_map = self.Map_c.get_all_map()
        self.map_load_with_file_name(file_name)
        window.destroy()

    def stop_running(self):
        self.running = False  # 플래그를 False로 설정하여 루프 종료
        self.root.quit()  # Tkinter 루프 종료

    def map_load_in_listbox(self, listbox, window):
        # 선택된 항목의 인덱스를 얻음
        selected_indices = listbox.curselection()

        # 선택된 항목이 있을 경우 반환
        if selected_indices:
            selected_item = listbox.get(selected_indices[0])
            print(f"선택된 항목: {selected_item}")
            window.destroy()
            self.map_load_with_file_name(selected_item)
        else:
            print("선택된 항목이 없습니다.")

    def map_load_with_file_name(self, file_name):
        self.file_index = int(file_name[4:-5])
        self.Map_c.load_to_list(self.now_map[f"room{self.file_index}.json"])


class OptionTopLevel:
    def __init__(self, root, x, y, Map_c, now_map, file_index):
        self.setting_win = tk.Toplevel(root)
        self.setting_win.title("속성")
        self.Map_c = Map_c
        label1 = tk.Label(self.setting_win, text=f"x={x}, y={y} 타일 속성")
        label1.grid(row=0, column=0, columnspan=2)
        label_img = tk.Label(self.setting_win, text="img:")
        label_img.grid(row=1, column=0)

        assets_items = list(self.Map_c.get_assets().keys())
        combobox_img = ttk.Combobox(self.setting_win, values=assets_items)
        try:
            combobox_img.set(now_map[f"room{file_index}.json"]["tilemap"][f"{x};{y}"]["img"])
        except KeyError:
            combobox_img.set("None")
        combobox_img.grid(row=1, column=1)

        label_type = tk.Label(self.setting_win, text="type:")
        label_type.grid(row=2, column=0)

        combobox_type = ttk.Combobox(self.setting_win, values=["floor", "wall"])
        try:
            combobox_type.set(now_map[f"room{file_index}.json"]["tilemap"][f"{x};{y}"]["type"])
        except KeyError:
            combobox_type.set("None")
        combobox_type.grid(row=2, column=1)

        self.row = 4
        self.event_label_list = []
        self.event_dropdown_list = []
        self.event_dropdown_item_list = []
        self.event_button_minus_list = []
        self.event_item_list = []

        def add_label_and_dropdown(event=None, *args):
            # 새 Label 추가
            label_new = tk.Label(self.setting_win, text="이벤트")
            label_new.grid(row=self.row, column=0)
            self.event_label_list.append(label_new)

            # 새 Dropdown (Combobox) 추가
            dropdown = ttk.Combobox(self.setting_win, values=["방 이동"])
            dropdown.grid(row=self.row, column=1)
            dropdown.bind("<<ComboboxSelected>>", self.on_combobox_change)
            self.event_dropdown_list.append(dropdown)
            self.event_dropdown_item_list.append(dropdown.get())
            self.event_item_list.append([])

            button_event_minus = tk.Button(
                self.setting_win,
                text="-",
                width=1,
                height=1,
                command=lambda: self.minus(button_event_minus)
            )
            button_event_minus.grid(row=self.row, column=2)
            self.event_button_minus_list.append(button_event_minus)

            self.button_apply.grid(row=self.row + 1, column=0, columnspan=2)

            self.row += 1  # 행 번호 증가
            if event == "방 이동":
                dropdown.set("방 이동")
                self.room_move(self.row - 5, dropdown.grid_info(), args[0])

        label_event = tk.Label(self.setting_win, text="event")
        label_event.grid(row=3, column=0)
        button_event_add = tk.Button(
            self.setting_win,
            text="+",
            width=10,
            command=add_label_and_dropdown
        )
        button_event_add.grid(row=3, column=1)

        def apply_changes():
            now_map[f"room{file_index}.json"]["tilemap"][f"{x};{y}"] = {
                "pos": [x, y],
                "img": combobox_img.get(),
                "type": combobox_type.get(),
                "event": []
            }

            for i in range(len(self.event_dropdown_item_list)):
                event_name = self.event_dropdown_item_list[i]
                if event_name == "방 이동":
                    now_map[f"room{file_index}.json"]["tilemap"][f"{x};{y}"]["event"].append({
                        "type": "room_move",
                        "room": self.event_item_list[i][1].get()
                    })

            self.Map_c.load_to_list(now_map[f"room{file_index}.json"])

            self.setting_win.destroy()

        self.button_apply = tk.Button(
            self.setting_win,
            text="확인",
            width=10,
            command=apply_changes
        )
        self.button_apply.grid(row=self.row, column=0, columnspan=2)

        if now_map[f"room{file_index}.json"]["tilemap"][f"{x};{y}"].get("event"):
            for event in now_map[f"room{file_index}.json"]["tilemap"][f"{x};{y}"]["event"]:
                if event["type"] == "room_move":
                    add_label_and_dropdown("방 이동", event["room"])

    def on_combobox_change(self, event):
        combobox = event.widget
        selected_item = combobox.get()
        combobox_index = self.event_dropdown_list.index(combobox)
        if selected_item == "방 이동" and self.event_dropdown_item_list[combobox_index] != "방 이동":
            self.room_move(combobox_index, combobox.grid_info())
        elif self.event_dropdown_item_list[combobox_index] == "방 이동":
            self.remove_event_item(combobox_index)

    def room_move(self, index, grid_info, file_name=None):
        self.event_dropdown_item_list[index] = "방 이동"
        for i in range(index + 1, len(self.event_dropdown_list)):
            label = self.event_label_list[i]
            dropdown = self.event_dropdown_list[i]
            button = self.event_button_minus_list[i]
            label.grid(row=label.grid_info()["row"]+1)
            dropdown.grid(row=dropdown.grid_info()["row"]+1)
            button.grid(row=button.grid_info()["row"]+1)
        self.row += 1
        self.button_apply.grid(row=self.row, column=0, columnspan=2)
        label_new = tk.Label(self.setting_win, text="방 이름")
        label_new.grid(row=grid_info["row"] + 1, column=0)

        map_items = list(self.Map_c.get_map_list())
        combobox_new = ttk.Combobox(self.setting_win, values=map_items)
        combobox_new.grid(row=grid_info["row"] + 1, column=1)
        if file_name:
            combobox_new.set(file_name)
        self.event_item_list[index] = [label_new, combobox_new]

    def remove_event_item(self, index):
        for item in self.event_item_list[index]:
            item.destroy()

    def minus(self, button):
        button_index = self.event_button_minus_list.index(button)
        self.event_label_list[button_index].destroy()
        self.event_label_list.pop(button_index)
        self.event_dropdown_list[button_index].destroy()
        self.event_dropdown_list.pop(button_index)
        self.event_dropdown_item_list.pop(button_index)
        self.event_button_minus_list[button_index].destroy()
        self.event_button_minus_list.pop(button_index)
        self.remove_event_item(button_index)
        self.event_item_list.pop(button_index)


M = Main()
M.run()
M.save_all()
