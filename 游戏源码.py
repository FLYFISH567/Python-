import time
import pygame
import random
import math

# 初始化界面
pygame.init()
screen = pygame.display.set_mode((800, 600))  # 图框大小
pygame.display.set_caption('flyfish game')  # 游戏名字

# 添加音乐
pygame.mixer.music.load(r"")
pygame.mixer.music.play(-1)

# 添加射中音效
bao_sound = pygame.mixer.Sound(r"\exp.wav")

icon = pygame.image.load(r"\ufo.png")  # 初始图像
pygame.display.set_icon(icon)
bgimg = pygame.image.load(r"\bg.png")  # 背景图像
playerimg = pygame.image.load(r"\player.png")  # player图像
enemyimg = pygame.image.load(r"\ufo.png")  # enemy图像
enemyimg2=pygame.image.load(r"\enemy2.png")
istrue = True
is_over = False
enemynumber = 2
enemyadd = 0
score = 0

# 玩家生命值
lives = 3

# 字体初始化
font = pygame.font.SysFont('simsunnsimsun', 32)
overfont = pygame.font.SysFont('simsunnsimsun', 96)

# 显示分数
# 显示分数和敌人数量
def scoreshow():
    global score
    text = f'Score: {score}'
    score_render = font.render(text, True, (255, 0, 0))
    screen.blit(score_render, (10, 10))

    # 显示敌人数量
    enemy_count_text = f'Enemies: {len(enemies)}'  # 显示当前敌人的数量
    enemy_count_render = font.render(enemy_count_text, True, (0, 0, 255))  # 蓝色字体
    screen.blit(enemy_count_render, (10, 50))  # 位置略微下移

# 显示玩家生命
def liveshow():
    global lives
    text = f'Lives: {lives}'
    lives_render = font.render(text, True, (0, 255, 0))
    screen.blit(lives_render, (700, 10))


# 玩家位置初始化
playerstepx_ = 0  # player y轴的移动
playerstepy_ = 0  # player x轴的移动
playerstepx = 400  # player x轴的位置
playerstepy = 500  # player y轴的位置

# 玩家移动
def showplayer():
    global istrue, playerstepy, playerstepx, playerstepx_, playerstepy_, dannumber, danmax
    if event.type == pygame.QUIT:
        istrue = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            playerstepx_ = 5
        elif event.key == pygame.K_LEFT:
            playerstepx_ = -5
        elif event.key == pygame.K_UP:
            playerstepy_ = -5
        elif event.key == pygame.K_DOWN:
            playerstepy_ = 5
        elif event.key == pygame.K_SPACE:  # 发射子弹
            dan.append(Dan())

    if event.type == pygame.KEYUP:
        playerstepx_ = 0
        playerstepy_ = 0

# 玩家位置判定
def playerloc():
    global istrue, playerstepy, playerstepx, playerstepx_, playerstepy_
    playerstepx += playerstepx_
    playerstepy += playerstepy_
    if playerstepx > 725:
        playerstepx = 725
        playerstepx_ = 0
    elif playerstepx < 0:
        playerstepx = 0
        playerstepx_ = 0
    elif playerstepy > 525:
        playerstepy_ = 0
        playerstepy = 525
    elif playerstepy < 0:
        playerstepy = 0
        playerstepy_ = 0

# 敌人类
class Enemy():
    def __init__(self):
        if random. randint(1,100)>50:
          self.img =enemyimg #pygame.image.load(r"C:\Users\86138\Desktop\game\enemy.png")  # enemy图像
        else:
            self.img=enemyimg2
        self.x = random.randint(100, 600)
        self.y = random.randint(-100, 0)
        self.x_ = random.choice([-0.5, 0.5]) #* random.randint(1, 2)  # 随机x方向速度
        self.y_ = random.choice([-0.5, 0.5]) #* random.randint(1, 2)  # 随机y方向速度

    def reset(self):
        if random. randint(1,100)>50:
          self.img =enemyimg #pygame.image.load(r"C:\Users\86138\Desktop\game\enemy.png")  # enemy图像
        else:
            self.img=enemyimg2
        if score<=10:# 重置敌人位置和运动方向
          self.x = random.randint(100, 600)
          self.y = random.randint(-50, 0)
          self.x_ = random.choice([-1, 1]) #* random.randint(1, 3)
          self.y_ = random.choice([-1, 1]) #* random.randint(1, 3)
        else:
            self.x = random.randint(100, 600)
            self.y = random.randint(-20, 0)
            self.x_ = random.choice([-1, 1])   * random.randint(1, 2)
            self.y_ = random.choice([-1, 1])   * random.randint(1, 3)

# 敌人移动以及位置生成
# 敌人移动以及位置生成
def showenemy():
    global lives
    for e1 in enemies:
        screen.blit(e1.img, (e1.x, e1.y))  # 显示敌人
        e1.x += e1.x_  # 更新x方向
        e1.y +=0.2

        # 碰到屏幕边界反弹
        if e1.x < 0 or e1.x > 736:
            e1.x_ *= -1
            e1.y_ *= -1

        if e1.y>600:
            e1.reset()
        # 判断敌人是否与玩家碰撞
        if distance(e1.x, e1.y, playerstepx, playerstepy) < 40:
            lives -= 1  # 减少玩家生命
            e1.reset()
            if lives <= 0:
                gameover()

            # 检测敌人之间的碰撞
        for e2 in enemies:
            if e1 != e2:  # 不和自己碰撞
                dist = distance(e1.x, e1.y, e2.x, e2.y)
                if dist < 35:  # 如果距离小于阈值

                    # 反转敌人之间的运动方向（模拟弹开）
                    e1.x_ *= -1
                    e1.y_ *= -1
                    e2.x_ *= -1
                    e2.y_ *= -1
                    if dist<20:
                        e1.reset()
                        e2.reset()

# 创建敌人
enemies = []
def enemiesbuild():
    global enemynumber
    for enemyadd in range(int(enemynumber)):
        enemies.append(Enemy())

def enemiesadd():
    enemies.append(Enemy())

# 敌人数量调整
enemynumber_ = 5
def enemynuberchange():
    global enemynumber, enemyadd, score, enemynumber_
    if score <= 4:
        pass
    else:
        enemynumber = int(score / 2)
    if enemynumber < 6:
        if enemynumber_ != enemynumber:
            enemynumber_ = enemynumber
            enemiesadd()

danmax=2
# 子弹类
class Dan:
    def __init__(self):
        self.img = pygame.image.load(r"C:\Users\86138\Desktop\game\bullet.png")  # dan图像
        self.x = playerstepx + 16
        self.y = playerstepy + 10
        self.step = 5

    def hit(self):
        global score
        for e in enemies:
            if distance(self.x, self.y, e.x, e.y) < 30:
                bao_sound.play()
                score += 1
                try:
                    dan.remove(self)
                except ValueError:
                    break
                e.reset()

    def add(self):
        global danmax
        if self.y < 0:
            danmax += 1

# 创建子弹
dan = []

# 子弹和敌人距离判断
def distance(dx, dy, ex, ey):
    a = dx - ex
    b = dy - ey
    return math.sqrt(a * a + b * b)

def fashe():
    for bumb in dan:
        screen.blit(bumb.img, (bumb.x, bumb.y))
        bumb.hit()
        bumb.add()
        bumb.y -= bumb.step

# 游戏结束
def gameover():
    global istrue, is_over
    overtext = 'Game Over'
    over_render = overfont.render(overtext, True, (255, 0, 0))
    istrue = False  # 停止游戏
    screen.blit(over_render, (220, 210))
    pygame.display.update()
    time.sleep(3)

# 初始化敌人
enemiesbuild()

# 游戏主循环
while istrue:
    screen.blit(bgimg, (0, 0))
    scoreshow()
    liveshow()  # 显示玩家生命
    showenemy()  # 敌人移动
    enemynuberchange()

    for event in pygame.event.get():
        showplayer()  # 玩家移动

    screen.blit(playerimg, (playerstepx, playerstepy))  # player的位置
    playerloc()  # 玩家位置判定
    fashe()  # 发射子弹

    pygame.display.update()
