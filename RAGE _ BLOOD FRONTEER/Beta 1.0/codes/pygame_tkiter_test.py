import tkinter as tk  # tkinter를 tk로 aliasing
import pygame
import os

# 기본적으로 아무 동작도 하지 않는 함수
def donothing():
    filewin = tk.Toplevel(root)
    button = tk.Button(filewin, text="Do nothing button")
    button.pack()

# Tkinter 초기화
root = tk.Tk()
root.title("Tkinter와 Pygame 통합 예제")  # 창 제목 추가

# 메뉴바 생성
menubar = tk.Menu(root)

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

# Pygame을 표시할 Tkinter 프레임 생성
embed = tk.Frame(root, width=640, height=480)
embed.pack()

# Pygame의 SDL 창이 Tkinter 프레임에 렌더링되도록 설정
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
root.update()  # 창이 표시되도록 업데이트

# Pygame 초기화 및 화면 설정
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pygame in Tkinter")  # Pygame 창 제목 설정

# 개선: 루프 종료를 처리하는 변수와 함수
running = True  # 프로그램 실행 상태를 나타내는 플래그
def stop_running():
    global running
    running = False  # 플래그를 False로 설정하여 루프 종료
    root.quit()  # Tkinter 루프 종료

# Tkinter 창 닫기 이벤트 처리
root.protocol("WM_DELETE_WINDOW", stop_running)

# Pygame 렌더링 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop_running()  # Pygame 종료 이벤트 처리

    # Pygame 화면 업데이트 (흰색 사각형 그리기)
    screen.fill((0, 0, 0))  # 화면을 검정색으로 채움
    pygame.draw.rect(screen, (255, 255, 255), [10, 10, 100, 100])  # 흰색 사각형
    pygame.display.flip()  # 화면 갱신

    # Tkinter 이벤트 처리 (화면 업데이트 및 이벤트 처리)
    root.update_idletasks()
    root.update()

# Pygame 종료
pygame.quit()
