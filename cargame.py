
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

from funcs import scale_image, blit_rotate_center

#[(118, 666), (103, 121), (275, 117), (603, 128), (674, 393), (300, 423), (316, 554), 
#(767, 569), (804, 131), (1086, 104), (1129, 321), (932, 348), (947, 507), (1119, 523), (1108, 729), (363, 751)]  
PATH = [(118, 666), (103, 121), (275, 117), (603, 128), (674, 393), (300, 423), (316, 554), 
(767, 569), (804, 131), (1086, 104), (1129, 321), (932, 348), (947, 507), (1119, 523), (1108, 729), (363, 751),]  
class Game:
    def __init__(self):
        a = 1.23
        self.grass = scale_image(pygame.image.load("imgs/grass.jpg"), 2*a)
        self.heart1 = scale_image(pygame.image.load("imgs/heart.png"),0.08*a)
        self.heart1_mask = pygame.mask.from_surface(self.heart1)
        self.heart1_position = (750,700)
        self.track = scale_image(pygame.image.load("imgs/ourtrack.png"), a)
        self.track_border = scale_image(pygame.image.load("imgs/ourtrack_border.png"),a)
        self.track_border_mask = pygame.mask.from_surface(self.track_border)
        self.red_car = scale_image(pygame.image.load("imgs/RedBull.png"), 0.13*a)
        self.green_car = scale_image(pygame.image.load("imgs/green-car.png"), (a*0.6)/a)
        self.score = scale_image(pygame.image.load("imgs/score.png"),(a*0.2)/a)
        self.finish = scale_image(pygame.image.load("imgs/finish.png"),1.6*a)
        self.finish_mask = pygame.mask.from_surface(self.finish)
        self.finish_position = (350,650)
        self.speed1 = scale_image(pygame.image.load("imgs/speed.png"),a*0.1/a)
        self.speed_mask = pygame.mask.from_surface(self.speed1)
        self.speed_position = (125,250)
        self.barrier1 = scale_image(pygame.image.load("imgs/barrier1.png"),(a*0.05)/a)
        self.barrier1_mask = pygame.mask.from_surface(self.barrier1)
        self.barrier1_position = (613,500)
        self.resume2 = scale_image(pygame.image.load("imgs/resume.png"),a/2)
        self.resume_position = (500,300)
        self.quitgame = scale_image(pygame.image.load("imgs/exitgame.png"),a/2)
        self.quitgame_position =(380,360)
        self.bullet = scale_image(pygame.image.load("imgs/bullet.png"),(a*0.2)/a)
        self.FPS = 60
        self.run = True
        WIDTH, HEIGHT = self.track.get_width(), self.track.get_height()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Car Race Game")

    def play(self):
        
        y = True #bariyer için
        x = False #bullet için
        z = True #speed için
        t = True
        while self.run:
            clock.tick(game.FPS)
            our_car.score+=0.1
            draw(game.WIN, images, our_car, opponent_car)
            our_car.movecar()
            opponent_car.move()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    opponent_car.path.append(pos)
            
            #opponent_car.movecar()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_x]:
                bullet1 = Bullet()
                bullet1.draw(game.WIN)
                bullet1.fire()
                firstspeed_x = our_car.horizontal
                firstspeed_y = our_car.vertical
                x = True
            if x == True: 
                bullet1.draw(game.WIN)   
                bullet1.position_x -= firstspeed_x
                bullet1.position_y -= firstspeed_y
                if y == True: #bu sayede eğer barrier öldüyse ateş tekrar aynı yerden geçerse hata vermiyor.
                    if (barrier.x-15) <= bullet1.position_x <= (barrier.x + 15) and  (barrier.y-50)<= bullet1.position_y <=(barrier.y+50):            
                        print(images)
                        barrier.die()
                        x = False
                        y = False
                    
                pygame.display.update()
                        
            finish_poi_collide = our_car.collusion(game.finish_mask,*game.finish_position)
            finish_poi_collide2 = opponent_car.collusion(game.finish_mask, *game.finish_position)
            speed_poi_collide = our_car.collusion(game.speed_mask,*game.speed_position)
            #######speed_poi_collide2 = opponent_car.collusion(game.speed_mask,*game.speed_position)
            barrier_poi_collide = our_car.collusion(game.barrier1_mask,*game.barrier1_position)
            ###barrier_poi_collide2 = opponent_car.collusion(game.barrier1_mask,*game.barrier1_position)
            heart_poi_collide = our_car.collusion(game.heart1_mask, *game.heart1_position)
            if heart_poi_collide != None:
                if t == True:
                    our_car.increase_HP()
                    heart.die()
                    t = False
            if barrier_poi_collide != None:
                if y == True:
                    our_car.stop()
                    our_car.decreaseHP()
                    
            if our_car.collusion(game.track_border_mask) != None :
                our_car.stop()
                our_car.decreaseHP()
            #if opponent_car.collusion(game.track_border_mask) != None:
             #   opponent_car.stop()

            if speed_poi_collide != None:
                if z == True:
                    our_car.increase_max_speed()
                    our_car.instant_speed()
                    speed.die()
                    z = False
            else:
                our_car.maxspeed = 5
            
            #if speed_poi_collide2 != None:
             #   opponent_car.increase_max_speed()
              #  opponent_car.instant_speed()
            #else:
             #   opponent_car.maxspeed = 5
            

            if finish_poi_collide != None: 
                if finish_poi_collide[0] ==0:
                    our_car.stop()
                else:
                    opponent_car.current_point = 0
                    our_car.restart()                  
                    opponent_car.restart()
                    opponent_car.move()
                    heart.restartobjects()
                    barrier.restartobjects()
                    speed.restartobjects()
                    t = True
                    z = True
                    y = True
            if finish_poi_collide2 != None: 
                if finish_poi_collide2[0] == 0:
                    opponent_car.stop()
                else:
                    opponent_car.current_point = 0
                    opponent_car.restart()
                    opponent_car.move()
                    our_car.restart()
                    heart.restartobjects()
                    barrier.restartobjects()
                    speed.restartobjects()
                    t = True
                    z = True
                    y = True
            if keys[pygame.K_p]:  
                self.pause()
            if keys[pygame.K_r]:
                self.resume()
            if keys[pygame.K_ESCAPE]:
                self.exitgame()
            if our_car.HP ==0:
                self.exitgame()
                print("game over")
        pygame.quit()
    def pause(self):
        images.append((self.resume2,self.resume_position))
        images.append((self.quitgame,self.quitgame_position))
        our_car.speed = 0
        ######opponent_car.speed = 0
    def resume(self):
        images.pop()
        images.pop()
    def exitgame(self):
        self.run = False
    
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
        

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotationspeed
        elif right:
            self.angle -= self.rotationspeed

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.speed = min(self.speed + self.acceleration, self.maxspeed)
        self.move()
    def move_backward(self):
        self.speed = max(self.speed - self.acceleration, -self.maxspeed/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        self.vertical = math.cos(radians) * self.speed
        self.horizontal = math.sin(radians) * self.speed

        self.y -= self.vertical
        self.x -= self.horizontal

    def reduce_speed(self):
        if self.speed-self.acceleration > 0:
            self.speed = self.speed - self.acceleration
        else:
            self.speed=0
        self.move()
    
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
        # opponent_car.maxspeed +=1

    def speed_up(self):
        pass

    def decreaseHP(self):
        our_car.HP -= 1

    def increase_max_speed(self):
        our_car.maxspeed += 3
    
    def instant_speed(self):
        our_car.speed += 3

    def DidYouTouch(self):
        pass

    def increase_HP(self):
        our_car.HP += 1
        
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

class Opponent_Car(Vehicle):
    IMG = game.green_car
    START_POS = (300,730)

    '''def movecar(self):
        keys = pygame.key.get_pressed()
        moved = False 
        if keys[pygame.K_a]:
            self.rotate(left=True)
        if keys[pygame.K_d]:
            self.rotate(right=True)
        if keys[pygame.K_s]:
            self.move_backward()
            moved = True
        if keys[pygame.K_w]: 
            moved = True
            self.move_forward()

        if not moved:
            self.reduce_speed()
            '''
    def __init__(self, maxspeed, rotationspeed, path=[]):
        super().__init__(maxspeed, rotationspeed)
        self.path = path
        self.current_point = 0
        self.speed = maxspeed

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        #self.draw_points(win)
    
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
class Road_Objects:
    
    def __init__(self,x_coordinate,y_coordinate,img):
        self.x = x_coordinate
        self.y = y_coordinate
        self.img = img
    
    def die(self):
        images.pop(images.index((self.img, (self.x,self.y))))

    def restartobjects(self):
        images.append((self.img,(self.x,self.y)))
class Boost(Road_Objects):
    pass   
class Barrier(Road_Objects):  
    pass  
class Heart(Road_Objects):
    pass
class Bullet:
    IMG = game.bullet
    
    def __init__(self):
        self.position_x = our_car.x
        self.position_y = our_car.y
        self.img = self.IMG
        self.angle = our_car.angle
        
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.position_x, self.position_y), self.angle)
    
    def fire(self):
        
        radians = math.radians(our_car.angle)
        vertical_speed = math.cos(radians) * 1
        horizontal_speed = math.sin(radians) * 1
        self.position_x -= horizontal_speed*1
        self.position_y -= vertical_speed*1
        
def draw(win, images, our_car, opponent_car):
    for img, pos in images:
        win.blit(img, pos)
    opponent_car.draw(win)
    our_car.draw(win)
    
    pygame.display.update()

clock = pygame.time.Clock()
our_car = OurCar(5, 4)
opponent_car = Opponent_Car(4, 4,PATH)
barrier = Barrier(613,500,game.barrier1)
speed = Boost(125,250,game.speed1)
heart = Heart(750,700,game.heart1)

images = [(game.grass, (0, 0)), (game.track, (0, 0)),(game.score, (0, 0)),(game.finish, game.finish_position),
(speed.img, (speed.x,speed.y)),(barrier.img, (barrier.x,barrier.y)),(game.track_border,(0,0)),(heart.img,(heart.x,heart.y))]

game.play()

#print(opponent_car.path)
print(our_car.score)