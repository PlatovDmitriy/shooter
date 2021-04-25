from pygame import *
from random import randint
from time import time as timer
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')



font.init()
font1 = font.SysFont('Arial',36)
lost = 0
score = 0
font2 = font.SysFont('Arial',75)
finish_win = font2.render('YOU WIN',True,(0,255,255)) 
finish_lose = font2.render('YOU LOSE',True,(255,0,0)) 
#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой
# img_bullet = "bullet.png" #пуля 3

 
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)
 
       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       #self.image.set_colorkey((0,0,0))
       self.speed = player_speed
 
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self): 
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,15)
        bullets.add(bullet)




class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(0,620)
            self.rect.y = 0
            global lost
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy( "ufo.png",randint(0,620),0,80,80,randint(1,5))
    monsters.add(monster)


#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#создаем спрайты
ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

monster = Enemy( "ufo.png",randint(0,620),0,80,80,randint(1,5))

#monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
rec_time = False

finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
num_fire = 0
life = 3
while run:
   #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rec_time == False:
                    num_fire += 1
                    ship.fire()
                    fire_sound.play()
                    
                if num_fire >= 5 and rec_time == False:
                    last_time = timer()
                    rec_time = True

    monsters.add(monster)
    if not finish:
       #обновляем фон
        window.blit(background,(0,0))
       

 
       #производим движения спрайтов
        ship.update()
 
       #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.update()
        bullets.update()
        bullets.draw(window)
        monsters.draw(window)
        text_lose = font1.render('Пропущено:'+str(lost),1,(255,255,255))
        window.blit(text_lose,(10,10))
        text_score = font1.render('Сбито:'+str(score),1,(255,255,255))
        window.blit(text_score,(10,35))
        if life == 3:
            text_life = font1.render(str(life),1,(0,255,0))
            window.blit(text_life,(650,450))
        if life == 2:
            text_life = font1.render(str(life),1,(255,255,0))
            window.blit(text_life,(650,450))
        if life == 1:
            text_life = font1.render(str(life),1,(255,0,0))
            window.blit(text_life,(650,450))
        if rec_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                text_reload = font1.render('Перезарядка',1,(200,0,0)) 
                window.blit(text_reload,(260,460))
            else:
                num_fire = 0
                rec_time = False
                
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for coll in collides:
            monster = Enemy("ufo.png",randint(0,620),0,80,80,randint(1,5))
            monsters.add(monster)
            score += 1
        if lost >= 3 or sprite.spritecollide(ship,monsters,True):
            life -= 1
            monster = Enemy("ufo.png",randint(0,620),0,80,80,randint(1,5))
        if score >= 10:
            window.blit(finish_win,(225,210))
            finish = True
        if life == 0:
            window.blit(finish_lose,(225,210))
            finish = True
        display.update()
    else:
        finish = False   
        score = 0
        lost = 0
        num_fire = 0
        life = 3 
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for i in range(5):
            monster = Enemy("ufo.png",randint(0,620),0,80,80,randint(1,5))
            monsters.add(monster)
   #цикл срабатывает каждые 0.05 секунд
    time.delay(50)