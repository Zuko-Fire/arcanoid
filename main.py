import pygame
from pygame import *

font.init()
blue = (200,255,255)
mw = display.set_mode((500,500))
mw.fill(blue)
clock = time.Clock()


class Area():
   def __init__(self, x=0, y=0, width=10, height=10, color=None):
       self.rect = Rect(x, y, width, height)
       self.fill_color = blue
       if color:
           self.fill_color = color


   def color(self, new_color):
       self.fill_color = new_color


   def fill(self):
       pygame.draw.rect(mw, self.fill_color, self.rect)


   def collidepoint(self, x, y):
       return self.rect.collidepoint(x, y)


   def colliderect(self, rect):
       return self.rect.colliderect(rect)


class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = image.load(filename)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Label(Area):
  def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
      self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
  def draw(self, shift_x=0, shift_y=0):
      self.fill()
      mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

racket_x = 200
racket_y = 330

ball = Picture('ball_1615463127.png',160,200,50,50)
platform = Picture('platform.png',racket_x,racket_y,100,30)


start_x = 5 #координаты создания первого монстра
start_y = 5
count = 9 #количество монстров в верхнем ряду
monsters = [] #список для хранения объектов-монстров
for j in range(3): #цикл по столбцам
    y = start_y + (55 * j) #координата монстра в каждом след. столбце будет смещена на 55 пикселей по y
    x = start_x + (27.5 * j) #и 27.5 по x
    for i in range (count):#цикл по рядам (строкам) создаёт в строке количество монстров, равное count
        d = Picture('enemy_1615463121.png', x, y, 50, 50) #создаём монстра
        monsters.append(d) #добавляем в список
        x = x + 55 #увеличиваем координату следующего монстра
    count = count - 1  #для следующего ряда уменьшаем кол-во монстров

FPS = 40

game = True
move_right = False
move_left = False
speed_x = 3
speed_y = 3
game_over = False

while not game_over:

    for m in monsters:
        m.draw()
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.fill()
            speed_y *= -1
    ball.fill()
    platform.fill()

    for even in event.get():
        if even.type == QUIT:
            game_over = True
        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_RIGHT:
                move_right = True
            if even.key == pygame.K_LEFT:
                move_left = True
        elif even.type == pygame.KEYUP:
            if even.key == pygame.K_RIGHT:
                move_right = False
            if even.key == pygame.K_LEFT:
                move_left = False
    if move_right:
        platform.rect.x += 3
    if move_left:
        platform.rect.x -= 3
    ball.rect.x += speed_x
    ball.rect.y += speed_y
    ball.draw()
    platform.draw()
    for i in monsters:
        i.draw()
    if ball.colliderect(platform):
        speed_y *= -1
    if ball.rect.y < 0:
        speed_y *= -1

    if ball.rect.x > 450 or ball.rect.x < 0:
        speed_x *= -1
    if ball.rect.y > (platform.rect.y + 20):
        time_text = Label(150, 150, 50, 50, blue)
        time_text.set_text('YOU LOSE', 60, (255, 0, 0))
        time_text.draw(10, 10)
        game_over = True
    if len(monsters) == 0:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text('YOU WIN', 60, (0, 200, 0))
        time_text.draw(10, 10)
        game_over = True


    pygame.display.update()
    clock.tick(FPS)


