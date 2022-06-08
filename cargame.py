
'''yapılacaklar!!!

her şeyi game ve classların içine atmamız lazım +
bullet vurunca kaybolsun, tekrar tekrar ateş edilebilsin -
diagramlar bunlara göre ayarlanacak -
opponent car yolu çizilecek +
ara yüz geliştirilecek
level eklenecek
'''



import pygame
import time
import math


#[(118, 666), (103, 121), (275, 117), (603, 128), (674, 393), (300, 423), (316, 554), 
#(767, 569), (804, 131), (1086, 104), (1129, 321), (932, 348), (947, 507), (1119, 523), (1108, 729), (363, 751)]  
PATH = [(118, 666), (103, 121), (275, 117), (603, 128), (674, 393), (300, 423), (316, 554), 
(767, 569), (804, 131), (1086, 104), (1129, 321), (932, 348), (947, 507), (1119, 523), (1108, 729), (363, 751),]  
class Game:
    

    def __init__(self):
        a = 1.23
        self.grass = Game.scale_image(pygame.image.load("imgs/grass.jpg"), 2*a)
        self.heartimg = Game.scale_image(pygame.image.load("imgs/heart.png"),0.08*a)
        self.heartimg_mask = pygame.mask.from_surface(self.heartimg)
        self.heartimg_position = (750,700)
        self.heartimg2 = Game.scale_image(pygame.image.load("imgs/heart2.png"),0.08*a)
        self.heartimg2_mask = pygame.mask.from_surface(self.heartimg2)
        self.heartimg2_position = (750,300)
        self.track = Game.scale_image(pygame.image.load("imgs/ourtrack.png"), a)
        self.track_border = Game.scale_image(pygame.image.load("imgs/ourtrack_border.png"),a)
        self.track_border_mask = pygame.mask.from_surface(self.track_border)
        self.red_car = Game.scale_image(pygame.image.load("imgs/RedBull.png"), 0.13*a)
        self.green_car = Game.scale_image(pygame.image.load("imgs/green-car.png"), (a*0.6)/a)
        self.score = Game.scale_image(pygame.image.load("imgs/score.png"),(a*0.2)/a)
        self.finish = Game.scale_image(pygame.image.load("imgs/finish.png"),1.6*a)
        self.finish_mask = pygame.mask.from_surface(self.finish)
        self.finish_position = (350,650)
        self.speedimg = Game.scale_image(pygame.image.load("imgs/speed.png"),a*0.1/a)
        self.speedimg_mask = pygame.mask.from_surface(self.speedimg)
        self.speedimg_position = (125,250)
        self.barrierimg = Game.scale_image(pygame.image.load("imgs/barrier1.png"),(a*0.05)/a)
        self.barrierimg_mask = pygame.mask.from_surface(self.barrierimg)
        self.barrierimg_position = (613,500)
 
        self.p = True
        self.resumeimg = Game.scale_image(pygame.image.load("imgs/resume.png"),a/2)
        self.resumeimg_position = (500,300)
        self.quitgame = Game.scale_image(pygame.image.load("imgs/exitgame.png"),a/2)
        self.quitgame_position =(380,360)
        
        self.bulletimg = Game.scale_image(pygame.image.load("imgs/bullet.png"),(a*0.2)/a)
        self.FPS = 60
        self.run = True
        WIDTH, HEIGHT = self.track.get_width(), self.track.get_height()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Car Race Game")
    
    def scale_image(img, factor):
        size = round(img.get_width() * factor), round(img.get_height() * factor)
        return pygame.transform.scale(img, size)


    def blit_rotate_center(win, image, top_left, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(
            center=image.get_rect(topleft=top_left).center)
        win.blit(rotated_image, new_rect.topleft)
    

    def play(self):

        bullet = Bullet()  

        while self.run:
            
            Game.draw(game.WIN, images, our_car, opponent_car)

            if self.p:
                clock.tick(game.FPS)
                our_car.score+=0.1
                our_car.movecar()
                opponent_car.move()
                
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break
               
            keys = pygame.key.get_pressed()

            if our_car.isitfired():
                bullet = Bullet()   
                bullet.fire()
                firstspeed_x = our_car.horizontal
                firstspeed_y = our_car.vertical
                bullet.life = True
                
            if bullet.areyouout() == True: 
                bullet.draw(game.WIN)   
                bullet.position_x -= firstspeed_x
                bullet.position_y -= firstspeed_y
                if barrier.areyoualive() == True: #bu sayede eğer barrier öldüyse ateş tekrar aynı yerden geçerse hata vermiyor.
                    if bullet.didwecrush():            
                        print(images)
                        barrier.die()
                        bullet.life = False
                        barrier.life = False
                
                pygame.display.update()
            

            if heart.areyoutaken():
                if heart.areyoualive() == True:
                    our_car.increase_HP()
                    heart.die()
                    heart.life = False
                   
            if barrier.areyoutaken():
                if barrier.areyoualive() == True:
                    our_car.stop()
                    our_car.decreaseHP()
         
                    our_car.stop()
                    our_car.decreaseHP()
        
            if our_car.collusion(game.track_border_mask) != None :
                our_car.stop()
                our_car.decreaseHP()
        
            if speed.areyoutaken():
                if speed.areyoualive() == True:
                    our_car.increase_max_speed()
                    our_car.instant_speed()
                    speed.die()
                    speed.life = False
            else:
                our_car.maxspeed = 5
            
            if our_car.whofinish() != None: 
                if our_car.whofinish() == 0:
                    our_car.stop()
                else:
                    opponent_car.current_point = 0
                    our_car.restart()                  
                    opponent_car.restart()
                    opponent_car.move()
                    our_car.maxspeed-= 0.5
                    our_car.maxspeed = max(3,our_car.maxspeed)
                    if heart.areyoualive() == False:
                        heart.restartobjects()
                  
                    if barrier.areyoualive() == False:
                        barrier.restartobjects()
                   
                    if speed.areyoualive() == False:
                        speed.restartobjects()
                    heart.life = True
                    speed.life = True
                    barrier.life = True
              
            if opponent_car.whofinish() != None: 
                opponent_car.current_point = 0
                opponent_car.restart()
                opponent_car.move() 
                our_car.restart()
                our_car.maxspeed-= 0.5
                our_car.maxspeed = max(3,our_car.maxspeed)
                if heart.areyoualive() == False:
                    heart.restartobjects()
                if barrier.areyoualive() == False:
                    barrier.restartobjects()
            
                if speed.areyoualive() == False:
                    speed.restartobjects()
                heart.life = True          
                speed.life = True
                barrier.life = True
     
            
            if keys[pygame.K_p]:  
                if self.p == True:
                    self.pause()
        
            if keys[pygame.K_ESCAPE]:
                self.exitgame()
            if keys[pygame.K_c]:
                if self.p == False:
                    self.cntinue()   
            if our_car.HP ==0:
                self.exitgame()
                print("game over")
        pygame.quit()
 
    def pause(self):
        images.append((self.resumeimg,self.resumeimg_position))
        images.append((self.quitgame,self.quitgame_position))
        self.p = False
    
    def cntinue(self):
        images.remove((self.resumeimg,self.resumeimg_position))
        images.remove((self.quitgame,self.quitgame_position))
        self.p = True

    def exitgame(self):
        self.run = False
    
    def draw(win, images, our_car, opponent_car):
        for img, pos in images:
            win.blit(img, pos)
        opponent_car.drawcars(win)
        our_car.drawcars(win)
    
        pygame.display.update()
game = Game()
class Vehicle:
    def __init__(self, maxspeed, rotationspeed):
        self.img = self.IMG
        self.maxspeed = maxspeed
        self.speed = 0
        self.rotationspeed = rotationspeed
        self.angle = 90
        self.x, self.y = self.START_POS
        self.acceleration = 1
        
    def drawcars(self, win):
        Game.blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move(self):
        radians = math.radians(self.angle)
        self.vertical = math.cos(radians) * self.speed
        self.horizontal = math.sin(radians) * self.speed

        self.y -= self.vertical
        self.x -= self.horizontal

    def collusion(self,mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def stop(self):
        if self.speed >= 0:
            self.speed = -8
        else:
            self.speed = 8
        self.move()

    def restart(self):
        self.x, self.y = self.START_POS
        self.angle = 90
        self.speed = 0
        return True
        # opponent_car.maxspeed +=1

    def areyoufinish(self):
        pass

    def whofinish(self):  
        if self.collusion(game.finish_mask,*game.finish_position) != None:
            if self.collusion(game.finish_mask,*game.finish_position)[0] == 0:
                return 0
            else:
                return 1
        else:
            return None
class OurCar(Vehicle):
    
    IMG = game.red_car
    def __init__(self, maxspeed, rotationspeed):
        super().__init__(maxspeed, rotationspeed)
        self.score = 0
        self.HP = 5
    START_POS = (300, 680)

    def movecar(self):
        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_LEFT] :
            self.rotate(left=True)
        if keys[pygame.K_RIGHT] :
            self.rotate(right=True)
        if keys[pygame.K_DOWN] :
            self.move_backward()
            moved = True
        if keys[pygame.K_UP] :
            moved = True
            self.move_forward()
        if not moved:
            self.reduce_speed()
    
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotationspeed
        elif right:
            self.angle -= self.rotationspeed
    
    def move_forward(self):
        self.speed = min(self.speed + self.acceleration, self.maxspeed)
        self.move()
    def move_backward(self):
        self.speed = max(self.speed - self.acceleration, -self.maxspeed/2)
        self.move()
        
    def reduce_speed(self):
        if self.speed-self.acceleration > 0:
            self.speed = self.speed - self.acceleration
        else:
            self.speed=0
        self.move()

    def decreaseHP(self):
        our_car.HP -= 1

    def increase_max_speed(self):
        our_car.maxspeed += 3
    
    def instant_speed(self):
        our_car.speed += 3

    def increase_HP(self):
        our_car.HP += 1

    def isitfired(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            return True
    
    def didourcarfinish(self):
        if our_car.collusion(game.finish_mask,*game.finish_position) != None:
            return True
        else:
            return False

class Opponent_Car(Vehicle):
    IMG = game.green_car
    START_POS = (300,730)


    def __init__(self, maxspeed, rotationspeed, path=[]):
        super().__init__(maxspeed, rotationspeed)
        self.path = path
        self.current_point = 0
        self.speed = maxspeed

    def draw(self, win):
        super().draw(win)
    
    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotationspeed, abs(difference_in_angle))
        else:
            self.angle += min(self.rotationspeed, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        self.speed = self.maxspeed
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()

    def didopponentcarfinish(self):
        if opponent_car.collusion(game.finish_mask,*game.finish_position) != None:
            return True
        else:
            return False
class Road_Objects:
    
    def __init__(self,x_coordinate,y_coordinate,img, life = True):
        self.x = x_coordinate
        self.y = y_coordinate
        self.img = img
        self.life = life
        self.img_mask = pygame.mask.from_surface(self.img)
    def die(self):
        images.pop(images.index((self.img, (self.x,self.y))))
        

    def restartobjects(self):
        images.append((self.img,(self.x,self.y)))
    
    def areyoualive(self):
        if self.life == True:
            return True
        else:
            return False
    
    def areyoutaken(self):
        if our_car.collusion(self.img_mask,*(self.x,self.y)) != None:
            return True
        else:
            return False
class Boost(Road_Objects):
    pass
class Barrier(Road_Objects):  
    pass
class Heart(Road_Objects):
    pass

    
class Bullet:
    IMG = game.bulletimg
    
    def __init__(self, life= False):
        self.position_x = our_car.x
        self.position_y = our_car.y
        self.img = self.IMG
        self.angle = our_car.angle
        self.life = life
        
    def draw(self, win):
        Game.blit_rotate_center(win, self.img, (self.position_x, self.position_y), self.angle)
    
    def fire(self):
        
        radians = math.radians(our_car.angle)
        vertical_speed = math.cos(radians) * 1
        horizontal_speed = math.sin(radians) * 1
        self.position_x -= horizontal_speed*1
        self.position_y -= vertical_speed*1
        
    def areyouout(self):
        if self.life == True:
            return True
        else:    
            if our_car.isitfired() == True:
                return True        
            else:
                return False
            
    def didwecrush(self):
        if (barrier.x-20) <= self.position_x <= (barrier.x + 20) and  (barrier.y-40)<= self.position_y+50 <=(barrier.y+20):
            return True
       


clock = pygame.time.Clock()
our_car = OurCar(5, 4)
opponent_car = Opponent_Car(4, 4,PATH)
barrier = Barrier(613,500,game.barrierimg)
speed = Boost(125,250,game.speedimg)
heart = Heart(750,700,game.heartimg)
heart2 = Heart(750,300,game.heartimg2)

images = [(game.grass, (0, 0)), (game.track, (0, 0)),(game.score, (0, 0)),(game.finish, game.finish_position),(speed.img, (speed.x,speed.y)),
(barrier.img, (barrier.x,barrier.y)), (game.track_border,(0,0)), (heart.img, (heart.x,heart.y))]

game.play()


print(our_car.score)