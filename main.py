import pygame, sys, random, time, pyautogui
from functools import cmp_to_key
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui

class SetCount(QWidget):
    def __init__(self):
        super().__init__()

        try:
            font = QtGui.QFont('NanumGothic', 11)
        except:
            font = QtGui.QFont('Malgun Gothic', 11)

        self.label1 = QLabel('점 개수 입력(3개 ~ 99개)')
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setFont(font)

        self.count = QSpinBox()
        self.count.setRange(3, 99)
        self.count.setFont(font)
        self.count.setValue(30)

        self.label2 = QLabel('속도(0.1s ~ 2s)')
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setFont(font)

        self.speed = QDoubleSpinBox()
        self.speed.setRange(0.1, 2)
        self.speed.setSingleStep(0.01)
        self.speed.setFont(font)
        self.speed.setValue(0.5)

        self.btn = QPushButton(self)
        self.btn.setText('입력')
        self.btn.setFont(font)
        self.btn.clicked.connect(self.fin)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label1)
        self.vbox.addWidget(self.count)
        self.vbox.addWidget(self.label2)
        self.vbox.addWidget(self.speed)
        self.vbox.addWidget(self.btn)
        self.setLayout(self.vbox)

        self.setWindowTitle('설정(✿◡‿◡))')
        self.setGeometry(300, 300, 300, 200)
        self.show()
    
    def fin(self):
        self.close()

pygame.init()
WIDTH = pygame.display.Info().current_w - 100
HEIGHT = pygame.display.Info().current_h - 100
BTN_WIDTH = 300
POINT_AREA = (20, 80, WIDTH - 20, HEIGHT - 20)

point_count = 30
speed = 0.5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Convex Hull Algorithm(Graham's Scan) Visualizer")

class GameButton:
    def __init__(self, txt, rect, color):
        self.x, self.y, self.w, self.h = rect
        self.color = color
        try:
            self.font = pygame.font.Font('Typo_SsangmundongGulimB.ttf', 20)
        except:
            self.font = pygame.font.SysFont('Malgun Gothic', 20)
        self.font_color = (255, 255, 255)
        self.txt = txt
        self.onclick = None

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        txt_info = self.font.render(self.txt, True, self.font_color)
        screen.blit(txt_info, txt_info.get_rect(center=(self.x + self.w / 2, self.y + self.h / 2)))

    def is_collide(self, pos):
        return self.x <= pos[0] <= self.x + self.w and self.y <= pos[1] <= self.y + self.h

class Line:
    def __init__(self, s, e):
        self.start = s
        self.end = e
        self.color = (255, 0, 0)
        self.thickness = 3

    def draw(self):
        pygame.draw.line(screen, self.color, self.start, self.end, self.thickness)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f'{self.x} {self.y}'
    
    def draw(self):
        pygame.draw.circle(screen, (0,0,0), (self.x, self.y), 5)

    def to_tuple(self):
        return self.x, self.y

btn_list = [
    GameButton(f'설정', (WIDTH / 4 - BTN_WIDTH / 2, 10, BTN_WIDTH, 40), '#060D13'), 
    GameButton('볼록 껍질 구하기', (WIDTH / 4 * 2 - BTN_WIDTH / 2, 10, BTN_WIDTH, 40), '#060D13'),
    GameButton('점 다시 찍기', (WIDTH / 4 * 3 - BTN_WIDTH / 2, 10, BTN_WIDTH, 40), '#060D13')
]
line_list = []
point_list = []

def draw_screen():
    screen.fill('#ece6cc')
    for btn in btn_list:
        btn.draw()
    for l in line_list:
        l.draw()
    for point in point_list:
        point.draw()
    pygame.display.update()

def remake_point():
    global point_count, point_list, line_list

    point_list = []
    line_list = []
    tmp = set()
    for i in range(point_count):
        while True:
            new_coord = (random.randint(POINT_AREA[0], POINT_AREA[2]), random.randint(POINT_AREA[1], POINT_AREA[3]))
            if new_coord not in tmp:
                tmp.add(new_coord)
                break
    for i in tmp:
        point_list.append(Point(*i))

app = QApplication(sys.argv)
gui = SetCount()
gui.close()
def get_count(): 
    global point_count, speed

    gui.show()
    app.exec_()
    point_count = int(gui.count.value())
    speed = float(gui.speed.value())
    remake_point()

def get_convex_hull():
    global point_count, point_list, line_list, speed

    def ccw(a, b, c):
        ret = (b.x - a.x) * (c.y - b.y) - (c.x - b.x) * (b.y - a.y)
        if ret: return ret // abs(ret)
        return 0
    
    def dist(a, b):
        return (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)

    _start_point = None
    def cmp(a, b):
        if ccw(_start_point, a, b):
            return -ccw(_start_point, a, b)
        return dist(a, _start_point) - dist(b, _start_point)

    mi = 0
    for i in range(1, len(point_list)):
        if point_list[mi].x > point_list[i].x or point_list[mi].x == point_list[i].x and point_list[mi].y > point_list[i].y: 
            mi = i
    point_list[mi], point_list[0] = point_list[0], point_list[mi]
    _start_point = point_list[0]
    pp = sorted(point_list[1:], key=cmp_to_key(cmp))

    stk = [point_list[0]]
    line_list = []
    for i in pp:
        while len(stk) >= 2 and ccw(stk[-2], stk[-1], i) <= 0:
            time.sleep(speed)
            line_list.append(Line(stk[-1].to_tuple(), i.to_tuple()))
            draw_screen()
            stk.pop()
            line_list.pop()
            line_list.pop()
        time.sleep(speed)
        stk.append(i)
        line_list.append(Line(stk[-2].to_tuple(), stk[-1].to_tuple()))
        draw_screen()
    
    time.sleep(speed)
    line_list.append(Line(stk[-1].to_tuple(), stk[0].to_tuple()))
    draw_screen()
    pyautogui.alert('볼록 껍질을 성공적으로 구했습니다.')

btn_list[0].onclick = get_count
btn_list[1].onclick = get_convex_hull
btn_list[2].onclick = remake_point

draw_screen()
get_count()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for b in btn_list:
                if b.is_collide(pos):
                    b.onclick()
                    break
    draw_screen()
    pygame.display.update()