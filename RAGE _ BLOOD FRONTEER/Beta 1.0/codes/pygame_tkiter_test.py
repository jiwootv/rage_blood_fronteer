import tkinter as tk
import pygame
import os

# Tkinter 초기화
root = tk.Tk()
root.title("Tkinter 안의 Pygame")  # 창 제목 설정
root.geometry("800x600")  # Tkinter 창 크기 설정
root.resizable(False, False)  # 창 크기 조절 불가능 설정

# 메뉴바 생성
menubar = tk.Menu(root)

# 기본적으로 아무 동작도 하지 않는 함수
def donothing():
    filewin = tk.Toplevel(root)
    button = tk.Button(filewin, text="Do nothing button")
    button.pack()

# 파일 메뉴 생성 및 추가
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# 편집 메뉴 생성 및 추가
editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)
editmenu.add_separator()
editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)
menubar.add_cascade(label="Edit", menu=editmenu)

# 도움말 메뉴 생성 및 추가
helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

# 메뉴바를 Tkinter 창에 설정
root.config(menu=menubar)

# Tkinter에서 Pygame을 포함할 프레임 생성
pygame_frame = tk.Frame(root, width=640, height=480, bg="black")  # Pygame이 렌더링될 영역
pygame_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Tkinter 창 중앙에 위치

# Pygame 창을 Tkinter 프레임에 임베딩
os.environ['SDL_WINDOWID'] = str(pygame_frame.winfo_id())  # SDL 창 ID 설정
os.environ['SDL_VIDEODRIVER'] = 'windib'  # Windows에서 제대로 동작하도록 드라이버 설정
root.update()  # 창을 업데이트하여 ID가 반영되도록 함

# Pygame 초기화 및 화면 설정
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pygame in Tkinter")  # Pygame 창 제목

# 프로그램 종료 플래그
running = True

def stop_running():
    global running
    running = False  # 종료 플래그 설정
    root.quit()  # Tkinter 루프 종료

# Tkinter 창 닫기 이벤트 처리
root.protocol("WM_DELETE_WINDOW", stop_running)

# Pygame 이벤트 처리 및 화면 업데이트
def handle_pygame_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Pygame 종료 이벤트 처리
        if event.type == pygame.KEYDOWN:  # 키가 눌렸을 때
            if event.key == pygame.K_ESCAPE:  # ESC 키를 눌렀을 때
                stop_running()  # 프로그램 종료
            print(f"키가 눌렸습니다: {pygame.key.name(event.key)}")

    # Pygame 화면 업데이트 (흰색 사각형 그리기)
    screen.fill((0, 0, 0))  # 화면을 검정색으로 채움
    pygame.draw.rect(screen, (255, 255, 255), [10, 10, 100, 100])  # 흰색 사각형
    pygame.display.flip()  # Pygame 화면 갱신

    # Tkinter 이벤트 처리
    root.after(10, handle_pygame_events)  # 10ms 후에 이 함수를 다시 호출

# Pygame 이벤트 처리 시작
handle_pygame_events()

# Tkinter 루프 시작
root.mainloop()

# Pygame 종료
pygame.quit()
