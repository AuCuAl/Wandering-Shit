# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 14:03:09 2021

@author: Administrator
"""
import json
import os
import queue
import random
import socket
import sys
from socket import *

import pygame
import select
from pygame.color import *
from pygame.locals import *

from bf_button import BFButton
from imputbox import InputBox

# 设置窗口位置:
wherex = 100
wherey = 50

# 设置窗口大小:
screenx = 1130
screeny = 700

# 界面初始化
pygame.init()  # 初始化pygame
font = pygame.font.SysFont("SimHei", 30)

# 音效音乐系统
pygame.mixer.init()
pygame.mixer.music.load(r'audio/bgm/bgm.mp3')
heng_1 = pygame.mixer.Sound(r'audio/sounds/heng1.mp3')
heng_2 = pygame.mixer.Sound(r'audio/sounds/heng2.mp3')
heng_3 = pygame.mixer.Sound(r'audio/sounds/heng3.mp3')
ah_1 = pygame.mixer.Sound(r'audio/sounds/ah1.mp3')
ah_2 = pygame.mixer.Sound(r'audio/sounds/ah2.mp3')
ah_3 = pygame.mixer.Sound(r'audio/sounds/ah3.mp3')
ah_4 = pygame.mixer.Sound(r'audio/sounds/ah4.mp3')
ah_5 = pygame.mixer.Sound(r'audio/sounds/ah5.mp3')
ah_6 = pygame.mixer.Sound(r'audio/sounds/ah6.mp3')
gasping_1 = pygame.mixer.Sound(r'audio/sounds/gasping1.mp3')
gasping_2 = pygame.mixer.Sound(r'audio/sounds/gasping2.mp3')
gasping_3 = pygame.mixer.Sound(r'audio/sounds/gasping3.mp3')
gasping_4 = pygame.mixer.Sound(r'audio/sounds/gasping4.mp3')

fire = heng_1
hit = ah_5
kill = heng_1
died = ah_1
resolve = gasping_2

# 创建窗口:
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (wherex, wherey)
# screen = pygame.display.set_mode(flags=pygame.FULLSCREEN, depth=0)
screen = pygame.display.set_mode((screenx, screeny), pygame.DOUBLEBUF, 32)
clock = pygame.time.Clock()
pygame.display.set_caption("多体运动")
screenx = screen.get_width()
screeny = screen.get_height()

# 按钮
button_x = screenx / 3
button_y = screeny / 8
button2_x = screenx / 6
button2_y = screeny / 10
input_box_x = screenx / 2
input_box_y = screeny * 0.1

# 颜色
white = (255, 255, 255)
black = (0, 0, 0)
gray = (127, 127, 127)

dev = False

# 数据缓冲区
queue_len = 20
roaming = queue.Queue(queue_len)
rear_len = 200

FPS = 120

def menu(btn):
    global dev
    global break_signal
    break_signal = True
    dev = False
    button1.visible = True
    button2.visible = True
    button3.visible = True
    button4_menu.visible = False
    input_box.visible = False
    button1.text = '单人游戏'
    button2.text = '多人游戏'
    button3.text = '退出'
    button1.click = single
    button2.click = multiplayer
    button3.click = pygame_quit


def single(btn):
    button1.text = '三体壁纸'
    button2.text = '训练场'
    button3.text = '返回'
    button1.click = start_0
    button2.click = start_1
    button3.click = menu


def multiplayer(btn):
    button1.text = '创建房间'
    button2.text = '加入房间'
    button3.text = '返回'
    button1.click = start_2
    button2.click = start_3
    button3.click = menu
    pass


def pygame_quit(btn):
    pygame.quit()
    exit()


def start_0(btn):
    button1.visible = False
    button2.visible = False
    button3.visible = False
    button4_menu.visible = True
    main(0)


def start_1(btn):
    button1.visible = False
    button2.visible = False
    button3.visible = False
    button4_menu.visible = True
    main(1)


def start_2(btn):
    screen.fill((0, 0, 0))
    button4_menu.visible = True
    draw_text('正在等待连接……', screenx / 2, screeny / 2, 50, screen)
    main(2)


def start_3(btn):
    break_signal_2 = False
    button4_menu.visible = True
    input_box.visible = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            button4_menu.update(event)
            input_box.dealEvent(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    break_signal_2 = True

        if break_signal_2:
            break
        screen.fill((0, 0, 0))
        draw_text('服务器地址：', screenx / 2, screeny * 0.4, 50, screen)
        button4_menu.draw()
        input_box.draw(screen)
        pygame.display.update()
        time_passed_2 = clock.tick(FPS)  # 帧率过高会发生闪烁

    button4_menu.visible = False
    input_box.visible = False
    screen.fill((0, 0, 0))
    draw_text('正在连接至服务器……', screenx / 2, screeny / 2, 50, screen)
    pygame.display.update()
    main(3)


def developing(btn):
    global dev
    button1.visible = False
    button2.visible = False
    button3.text = '返回'
    button3.click = menu
    dev = True


def draw_text(text, x, y, font_size, surface):
    pygame.font.init()
    fontObj = pygame.font.SysFont('SimHei', font_size)
    textSurfaceObj = fontObj.render(text, True, white, black)
    textSurfaceObj.set_alpha(255)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x, y)
    surface.blit(textSurfaceObj, textRectObj)


def draw_statistics_list(statistics_list):
    statistics_list_Obj = pygame.Surface((screenx, screeny))
    statistics_list_Obj.fill(black)
    statistics_list_Obj.set_alpha(180)
    for i in range(len(statistics_list)):
        name = statistics_list[i][0].split('|')
        data = statistics_list[i][1]
        text = ''
        for j in range(len(name)):
            text += name[j] + str(data[j])
        draw_text(text, screenx / 2, screeny / 20 * (i + 1), screenx // 50, statistics_list_Obj)
    screen.blit(statistics_list_Obj, (0, 0, screenx, screeny))
break_signal = False


# def darken_screen():
#     dark_img = screen.convert_alpha()
#     #  透明度（opacity）等于零0为完全不透明，等于255时为完全透明
#     opacity = 127
#     #  fill方法的第一个color参数需传入元组
#     #  元组的前三个整数控制RGB数值，最后一个为透明度
#     dark_img.fill((*(255, 255, 255),opacity))
#     screen.blit(dark_img,(0,0))

# mode:0 - 三体壁纸  1 - 练习场  2 - 多人游戏（房主）  3 - 多人游戏（房客）
def main(mode):
    global FPS
    global break_signal
    break_signal = False
    print_statistics_list = False
    # 图片导入
    # 用于传送的数据
    msg = []

    # 参数
    M = 1.9891 * 10 ** 30  # 太阳质量
    Me = 5.97 * 10 ** 24  # 地球质量
    AU = 149597870700.0  # 天文单位
    G = 6.67 / (10 ** 11)  # 万有引力常数
    dt = 1200  # 时间步长(每隔多少秒计算一次轨迹)
    d_day = 1  # 每隔多少天绘制一次轨迹
    p = 10 ** 9 * 2  # 一像素表示多少米
    day = 0
    year = 0
    n = round(24 * 3600 * d_day / dt)

    # 加速度
    engine_acceleration = 0.002
    key = [0, 0, 0, 0]

    # 限速
    v_upper_lim = 100000
    v_lower_lim = 100000

    # 限加速
    a_upper_lim = 1
    a_lower_lim = 1

    link = False

    class Star(object):
        def __init__(self, star_m, star_pos, star_v, star_color, star_r, star_name):
            self.star_m = star_m
            self.star_pos = star_pos
            self.star_v = star_v
            self.star_a = [0, 0]
            self.star_color = star_color
            self.star_r = star_r
            self.star_name = star_name

            self.live = 1  # 0为死亡，1为存活，2为即将死亡，3为无敌状态
            self.count = 0
            self.star_rear_len = rear_len
            self.star_rear = []
            self.star_rear_size = star_r / 2

            self.master = None

            # 战斗系统
            self.blood = 100
            self.attack = 200  # 撞击
            self.remaining_cannonball = 0  # 剩余弹药
            self.kill = 0
            self.death = 0

            self.statistics = []

        def calculate(self):
            # 限加速系统
            scale = (self.star_a[0] * self.star_a[0] + self.star_a[1] * self.star_a[1]) / (a_upper_lim * a_upper_lim)
            if scale > 1:
                scale = (self.star_a[0] * self.star_a[0] + self.star_a[1] * self.star_a[1]) / (
                        a_lower_lim * a_lower_lim)
                self.star_a[0] /= scale ** 0.5
                self.star_a[1] /= scale ** 0.5

            # 速度计算
            self.star_v[0] += 0.5 * self.star_a[0] * dt
            self.star_v[1] += 0.5 * self.star_a[1] * dt

            # 限速系统
            scale = (self.star_v[0] * self.star_v[0] + self.star_v[1] * self.star_v[1]) / (v_upper_lim * v_upper_lim)
            if scale > 1:
                scale = (self.star_v[0] * self.star_v[0] + self.star_v[1] * self.star_v[1]) / (
                        v_lower_lim * v_lower_lim)
                self.star_v[0] /= scale ** 0.5
                self.star_v[1] /= scale ** 0.5

            # 位移、速度计算
            d_pos_x = self.star_v[0] * dt + 0.5 * self.star_a[0] * dt ** 2
            d_pos_y = self.star_v[1] * dt + 0.5 * self.star_a[1] * dt ** 2
            self.star_v[0] += 0.5 * self.star_a[0] * dt
            self.star_v[1] += 0.5 * self.star_a[1] * dt

            # 限速系统
            scale = (self.star_v[0] * self.star_v[0] + self.star_v[1] * self.star_v[1]) / (v_upper_lim * v_upper_lim)
            if scale > 1:
                scale = (self.star_v[0] * self.star_v[0] + self.star_v[1] * self.star_v[1]) / (
                        v_lower_lim * v_lower_lim)
                self.star_v[0] /= scale ** 0.5
                self.star_v[1] /= scale ** 0.5

            # 位置计算
            self.star_pos[0] += d_pos_x
            self.star_pos[1] += d_pos_y

            # 限位（反弹）系统
            if self.star_pos[0] >= screenx / 2 * p:
                self.star_pos[0] = screenx * p - self.star_pos[0]
                self.star_v[0] = - self.star_v[0]
            elif self.star_pos[0] <= - screenx / 2 * p:
                self.star_pos[0] = - screenx * p - self.star_pos[0]
                self.star_v[0] = - self.star_v[0]

            if self.star_pos[1] >= screeny / 2 * p:
                self.star_pos[1] = screeny * p - self.star_pos[1]
                self.star_v[1] = - self.star_v[1]
            elif self.star_pos[1] <= - screeny / 2 * p:
                self.star_pos[1] = - screeny * p - self.star_pos[1]
                self.star_v[1] = - self.star_v[1]

        def draw(self):
            if not star_list[star_num1].master:
                self.statistics = ['|: 剩余血量:|% 剩余弹药:| k/d:|/',
                                   [self.star_name, self.blood, self.remaining_cannonball, self.kill, self.death]]
            pygame.draw.circle(screen, self.star_color,
                               (int(self.star_pos[0] / p + screenx / 2), int(-self.star_pos[1] / p + screeny / 2)),
                               self.star_r)
            # 尾迹
            if len(self.star_rear) == self.star_rear_len:
                self.star_rear.pop(0)
            self.star_rear.append([int(self.star_pos[0] / p + screenx / 2), int(-self.star_pos[1] / p + screeny / 2)])
            for j in range(len(self.star_rear)):
                pygame.draw.circle(screen, self.star_color, self.star_rear[j], self.star_rear_size)

    class Cannonball(Star):
        def __init__(self, star_m, star_pos, star_v, star_color, star_r, star_master):
            Star.__init__(self, star_m, star_pos, star_v, star_color, star_r, '加农炮')
            self.master = star_master

            # 战斗系统
            self.blood = 1
            self.attack = 60
            self.remaining_cannonball = None

    star1 = Star(0.5 * M, [0.0, 3 * AU], [20430.0, 0.0], (255, 255, 100), 10, '黄')
    star2 = Star(0.5 * M, [0.0, 4.5 * AU], [-7226.0, 0.0], (255, 100, 100), 10, '红')
    star3 = Star(M, [0.0, -3.75 * AU], [-6652.0, 0.0], (255, 255, 255), 10, '白')
    star4 = Star(Me, [AU, -3.75 * AU], [-6652.0, 27000.0], (100, 250, 255), 5, '蓝')
    star_list = [star1, star2, star3, star4]

    # 服务端参数定义
    if mode == 2:
        # 定义服务器名称
        HOST = '127.0.0.1'
        PORT = 55555
        BUFSIZE = 1024
        ADDR = (HOST, PORT)

        # 定义服务器属性
        tcpsersock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsersock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 对socket的配置重用ip和端口号
        tcpsersock.bind(ADDR)
        tcpsersock.listen(1)
        inputs = [tcpsersock]

        pos = ''
        test = True
        i = 0
        key_1 = [0, 0, 0, 0]
    # 客户端参数定义
    elif mode == 3:
        # 定义客户端名称
        if ':' in button4_menu.text:
            ADDR = tuple(button4_menu.text.rsplit(':', -1))
        else:
            HOST = 'sh.s2.6net.plus'
            PORT = 55555
            BUFSIZE = 1024 * 1024
            ADDR = (HOST, PORT)

        test = not ADDR[0] == 'localhost'

        # 连接服务器
        tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        inputs = [tcpCliSock]

        pos = ''
        tmp = -1
        i = 0
    else:
        link = True

    while True:
        if break_signal:
            break
        if not pygame.mixer.music.get_busy():  # 检查是否正在播放音乐
            pygame.mixer.music.play()  # 开始播放音乐流
        if mode == 2 or mode == 3:
            rs, ws, es = select.select(inputs, [], [], 0)
            button4_menu.draw()
            for r in rs:
                if mode == 2:
                    if r is tcpsersock:
                        link = True
                        print('new ser')
                        tcpcliscock, addr = tcpsersock.accept()
                        print('addr={0}'.format(addr))
                        if test:
                            tcpcliscock, addr = tcpsersock.accept()
                            print('addr={0}'.format(addr))
                            test = False
                        inputs.append(tcpcliscock)
                    else:
                        data, addr = r.recvfrom(BUFSIZE)
                        '''反丢包系统'''
                        pos += str(data)
                        pos = pos.replace('b', '')
                        pos = pos.replace('\'', '')
                        while True:
                            try:
                                end = pos.index(']')
                            except ValueError:
                                break
                            else:
                                data = pos[:end + 1]
                                if end + 1 == len(pos):
                                    pos = ''
                                else:
                                    pos = pos[end + 1:]
                                if data:
                                    try:
                                        data = json.loads(data)
                                        key_1 = data
                                    except (json.decoder.JSONDecodeError, ValueError):
                                        print('丢包')
                                    else:
                                        key_1 = data
                        '''反丢包系统结束'''
                        disconnected = not data
                        if disconnected:
                            inputs.remove(r)
                            while True:
                                for event in pygame.event.get():
                                    if event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()
                        '''else:
                            key_1 = json.loads(data)
                            print(key_1)'''
                elif mode == 3:
                    if r is tcpCliSock:
                        data, addr = r.recvfrom(BUFSIZE)
                        link = True
                        '''反丢包系统'''
                        pos += str(data)
                        pos = pos.replace('b', '')
                        pos = pos.replace('\'', '')
                        while True:
                            try:
                                end = pos.index(']')
                            except ValueError:
                                break
                            else:
                                data = pos[:end + 1]
                                if end + 1 == len(pos):
                                    pos = ''
                                else:
                                    pos = pos[end + 1:]
                                if data:
                                    try:
                                        data = json.loads(data)
                                        [x1, y1, x2, y2, x3, y3, x4, y4, year, day] = data
                                    except (json.decoder.JSONDecodeError, ValueError):
                                        print('丢包')
                                    else:
                                        if roaming.qsize() == roaming.maxsize:
                                            roaming.get()
                                        roaming.put(data)
                        '''反丢包系统结束'''
                        while not roaming.empty():
                            [x1, y1, x2, y2, x3, y3, x4, y4, year, day] = roaming.get()
                            screen.fill((0, 0, 0))  # 刷新画面,并设置背景颜色
                            screen.blit(font.render(str(year) + "年 " + str(round(day)) + "日", True, THECOLORS["gray"]),
                                        (20, screeny - 60))

                            # 绘制天体:
                            pygame.draw.circle(screen, (255, 255, 100),
                                               (int(x1 / p + screenx / 2), int(-y1 / p + screeny / 2)), 10)
                            pygame.draw.circle(screen, (255, 100, 100),
                                               (int(x2 / p + screenx / 2), int(-y2 / p + screeny / 2)), 10)
                            pygame.draw.circle(screen, (255, 255, 255),
                                               (int(x3 / p + screenx / 2), int(-y3 / p + screeny / 2)), 10)
                            pygame.draw.circle(screen, (100, 250, 255),
                                               (int(x4 / p + screenx / 2), int(-y4 / p + screeny / 2)), 5)

                            if print_statistics_list:
                                star_statistics_list = []
                                for star in star_list:
                                    if not star.master:
                                        star_statistics_list.append(star.statistics)
                                draw_statistics_list(star_statistics_list)

                            pygame.display.update()
                            time_passed = clock.tick(FPS)  # 画面帧率

        if link:
            if mode == 3:
                i += 1
                if i == 1:
                    i = 0
                    msg = key
                    msg1 = json.dumps(msg)
                    tcpCliSock.sendto(msg1.encode(), ADDR)
                    # time_passed = clock.tick(FPS)  # 画面帧率

            else:
                # 运算阶段
                for k in range(n):
                    # 计算各个天体间的万有引力加速度:
                    for star_num1 in range(len(star_list)):
                        if star_list[star_num1].live and star_list[star_num1].live != 2:
                            star_list[star_num1].star_a[0] = star_list[star_num1].star_a[1] = 0
                    for star_num1 in range(len(star_list)):
                        for star_num2 in range(star_num1 + 1, len(star_list)):
                            if star_list[star_num1].live and star_list[star_num1].live != 2 and star_list[
                                star_num2].live and star_list[star_num2].live != 2:
                                dr_x = star_list[star_num1].star_pos[0] - star_list[star_num2].star_pos[0]
                                dr_y = star_list[star_num1].star_pos[1] - star_list[star_num2].star_pos[1]
                                r = pow(dr_x * dr_x + dr_y * dr_y, 0.5)
                                if r / p <= star_list[star_num1].star_r + star_list[star_num2].star_r:
                                    if star_list[star_num1].live == 3:
                                        if not star_list[star_num2].live == 3:
                                            if star_list[star_num2].blood > star_list[star_num1].attack:
                                                star_list[star_num2].blood -= star_list[star_num1].attack
                                            else:
                                                star_list[star_num2].blood = 0
                                                star_list[star_num2].live = 2
                                                star_list[star_num2].death += 1
                                                if not star_list[star_num2].master:
                                                    if not star_list[star_num1].master:
                                                        star_list[star_num1].kill += 1
                                                    else:
                                                        star_list[star_num1].master.kill += 1
                                    else:
                                        if star_list[star_num1].blood > star_list[star_num2].attack:
                                            star_list[star_num1].blood -= star_list[star_num2].attack
                                        else:
                                            star_list[star_num1].blood = 0
                                            star_list[star_num1].live = 2
                                            star_list[star_num1].death += 1
                                            if not star_list[star_num1].master:
                                                if not star_list[star_num2].master:
                                                    star_list[star_num2].kill += 1
                                                else:
                                                    star_list[star_num2].master.kill += 1

                                        if not star_list[star_num2].live == 3:
                                            if star_list[star_num2].blood > star_list[star_num1].attack:
                                                star_list[star_num2].blood -= star_list[star_num1].attack
                                            else:
                                                star_list[star_num2].blood = 0
                                                star_list[star_num2].live = 2
                                                star_list[star_num2].death += 1
                                                if not star_list[star_num2].master:
                                                    if not star_list[star_num1].master:
                                                        star_list[star_num1].kill += 1
                                                    else:
                                                        star_list[star_num1].master.kill += 1

                                star_list[star_num1].star_a[0] += - G * star_list[star_num2].star_m * dr_x / r / r / r
                                star_list[star_num1].star_a[1] += - G * star_list[star_num2].star_m * dr_y / r / r / r
                                star_list[star_num2].star_a[0] += G * star_list[star_num1].star_m * dr_x / r / r / r
                                star_list[star_num2].star_a[1] += G * star_list[star_num1].star_m * dr_y / r / r / r
                    star_list[0].star_a[0] += engine_acceleration * (key[2] + key[3])
                    star_list[0].star_a[1] += engine_acceleration * (key[0] + key[1])
                    if mode == 2:
                        star_list[1].star_a[0] += engine_acceleration * (key_1[2] + key_1[3])
                        star_list[1].star_a[1] += engine_acceleration * (key_1[0] + key_1[1])
                    # 计算各个天体在dt内的运动:
                    for star_num1 in range(len(star_list)):
                        if star_list[star_num1].live:
                            star_list[star_num1].calculate()

                # 记录时间:
                day = day + d_day
                if day >= 365.2422:
                    year = year + 1
                    day = day - 365.2422

                if mode == 2:
                    msg = [star1.star_pos[0], star1.star_pos[1], star2.star_pos[0], star2.star_pos[1],
                           star3.star_pos[0],
                           star3.star_pos[1], star4.star_pos[0], star4.star_pos[1], year, day]
                    msg1 = json.dumps(msg)
                    tcpcliscock.sendto(msg1.encode(), ADDR)

                screen.fill((0, 0, 0))  # 刷新画面,并设置背景颜色
                screen.blit(font.render(str(year) + "年 " + str(round(day)) + "日", True, THECOLORS["gray"]),
                            (20, screeny - 60))

                # 绘制天体:
                star_num1 = 0
                while True:
                    if star_num1 >= len(star_list):
                        break
                    else:
                        star_list[star_num1].count += 1
                        if star_list[star_num1].live:
                            star_list[star_num1].draw()
                            if not star_list[star_num1].master:
                                if star_list[star_num1].remaining_cannonball < 5:
                                    if star_list[star_num1].count % 100 == 0:
                                        star_list[star_num1].remaining_cannonball += 1
                                else:
                                    star_list[star_num1].count -= 1  # 停止计数
                                if star_list[star_num1].live == 2:
                                    died.play()
                                    star_list[star_num1].star_rear.clear()
                                    star_list[star_num1].live = 0
                                    star_list[star_num1].count = 0
                                    star_list[star_num1].remaining_cannonball = 0
                                elif star_list[star_num1].live == 3:
                                    if star_list[star_num1].count > 300:
                                        star_list[star_num1].count = 0
                                        star_list[star_num1].live = 1
                            else:
                                if star_list[star_num1].live == 2:
                                    hit.play()
                                    del star_list[star_num1]
                                    star_num1 -= 1
                                elif star_list[star_num1].count == 100 or len(star_list) > 9:
                                    resolve.play()
                                    del star_list[star_num1]
                                    star_num1 -= 1
                        else:
                            if star_list[star_num1].count == 1000:
                                star_list[star_num1].count = 0
                                star_list[star_num1].star_pos = [(random.random() - 0.5) * screenx * p,
                                                                 (random.random() - 0.5) * screeny * p]
                                star_list[star_num1].star_v = [(random.random() - 0.5) * 5000,
                                                               (random.random() - 0.5) * 5000]
                                star_list[star_num1].live = 3
                                star_list[star_num1].blood = 100
                        star_num1 += 1

                if print_statistics_list:
                    star_statistics_list = []
                    for star in star_list:
                        if not star.master:
                            star_statistics_list.append(star.statistics)
                    draw_statistics_list(star_statistics_list)

                pygame.display.update()
                time_passed = clock.tick(FPS)  # 画面帧率

        for event in pygame.event.get():
            button4_menu.update(event)
            if event.type == QUIT:
                if mode == 2:
                    tcpsersock.close()
                elif mode == 3:
                    tcpCliSock.close()
                pygame.quit()
                sys.exit()
            if mode == 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if star_list[0].live:
                        if star_list[0].remaining_cannonball > 0:
                            star_list[0].remaining_cannonball -= 1
                            fire.play()
                            dr_x = (pygame.mouse.get_pos()[0] - screenx / 2) * p - star_list[0].star_pos[0]
                            dr_y = (pygame.mouse.get_pos()[1] - screeny / 2) * p + star_list[0].star_pos[1]
                            r = pow(dr_x * dr_x + dr_y * dr_y, 0.5)

                            cannonball_pos = [star_list[0].star_pos[0] + AU * dr_x / r,
                                              star_list[0].star_pos[1] - AU * dr_y / r]
                            cannonball = Cannonball(0.01 * M, cannonball_pos, [40000 * dr_x / r, - 40000 * dr_y / r],
                                                    (255, 0, 0), 3, star_list[0])
                            star_list.append(cannonball)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        print_statistics_list = True
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        key[0] = 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        key[1] = -1
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        key[2] = -1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        key[3] = 1
                    elif event.key == pygame.K_ESCAPE:
                        if mode == 2:
                            tcpsersock.close()
                        elif mode == 3:
                            tcpCliSock.close()
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_n:
                        print_statistics_list = False
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        key[0] = 0
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        key[1] = 0
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        key[2] = 0
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        key[3] = 0

    if (mode == 2 or mode == 3) and not break_signal:
        tcpcliscock.close()
        tcpsersock.close()


if __name__ == '__main__':
    button1 = BFButton(screen, (screenx / 2 - button_x / 2, screeny / 2 * 0.7 - button_y / 2, button_x, button_y),
                       text='单人游戏', click=single)
    button2 = BFButton(screen, (screenx / 2 - button_x / 2, screeny / 2 - button_y / 2, button_x, button_y),
                       text='Hide', click=multiplayer)
    button3 = BFButton(screen, (screenx / 2 - button_x / 2, screeny / 2 * 1.3 - button_y / 2, button_x, button_y),
                       text='Quit', click=pygame_quit)
    button4_menu = BFButton(screen, (button2_x / 5, button2_y / 5, button2_x, button2_y), text='返回主菜单', click=menu)
    input_box = InputBox(
        pygame.Rect(screenx / 2 - input_box_x / 2, screeny / 2 - input_box_y / 2, input_box_x, input_box_y))  # 输入框
    print(screenx, screeny)
    menu(button1)
    while True:
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                pygame.quit()
                exit()
            button1.update(Event)
            button2.update(Event)
            button3.update(Event)
            button4_menu.update(Event)
            input_box.dealEvent(Event)  # 输入框处理事件

        screen.fill((0, 0, 0))
        button1.draw()
        button2.draw()
        button3.draw()
        button4_menu.draw()
        input_box.draw(screen)  # 输入框显示
        if dev:
            draw_text('功能正在开发中……', screenx / 2, screeny / 2, 50)
        pygame.display.update()
