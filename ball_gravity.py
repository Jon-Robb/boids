from abc import abstractmethod
from copy import deepcopy
import math
import random
from tkinter import ttk, Tk
from typing import overload 
from vect2d import Vect2D
from PIL import Image, ImageTk, ImageDraw

# Mathématique:
    # rad * 180/PI = degrés
    # degré * PI/180 = rad 
    

class Updatable():

    @abstractmethod
    def tick(self):
        """Méthode abstraite qui sera redéfinie pour les balles et le jeu
        """
        pass

class Gravitational():
    def __init__(self, masse):
        self.__masse = masse
        
    @property
    def masse(self):
        return self.__masse
     
    @abstractmethod
    def pulled_by(self, ball):
        pass
    
class GravityMagnet(Gravitational, Updatable):
    def __init__(self):
        Gravitational.__init__(self, masse=100)
        self.__direction = Vect2D()
        self.__directions = {
            "UP": Vect2D(0,-1),
            #"UR": Vect2D(1,-1),
            "RIGHT": Vect2D(1,0),
            #"RD": Vect2D(1,1),
            "DOWN": Vect2D(0,1),
            #"DL": Vect2D(-1,1),
            "LEFT": Vect2D(-1,0)
            #"UL": Vect2D(-1,-1)
        }
        
    
    def set_direction(self, event):
        if not event.send_event:
            self.__direction = Vect2D()
        elif event.keysym.upper() in self.__directions:
            if event.keysym.upper() in ("UP", "DOWN"):
                self.__direction.y = self.__directions[event.keysym.upper()].y
            else:
                self.__direction.x = self.__directions[event.keysym.upper()].x

    def pulled_by(self):
        return self.masse * self.__direction

class Trail(Updatable):
    def __init__(self, length=15):
        self.__length = length
        self.__points = ([])
        
    def tick(self, ball):
        self.update_trail(ball)
        
    def update_trail(self, ball):
        if len(self.__points) == self.__length:
            self.__points.pop(0)
        
        self.__points.append(Vect2D(ball.position.x, ball.position.y))

    @property
    def points(self):
        return self.__points
    

class Ball(Updatable, Gravitational):
    def __init__(self, radius=random.randrange(5,10), fill_color=(random.randint(0,255),random.randint(0,255), random.randint(0,255)), border_color=(random.randint(0,255),random.randint(0,255), random.randint(0,255)), density=random.randrange(0,10), position:Vect2D=Vect2D(random.randrange(0,100),random.randrange(0,100)), speed:Vect2D=Vect2D(random.randrange(-10,10),random.randrange(-10,10)), acceleration:Vect2D=Vect2D(0,0), bounce=0.95, friction=0.95):
        Gravitational.__init__(self, masse=(density * (math.pi * radius ** 2)))
        self.__radius = radius
        self.__fill_color = fill_color
        self.__border_color = border_color
        self.__density = density
        self.__position = position
        self.__initial_speed = deepcopy(speed)
        self.__speed = deepcopy(speed)
        self.__acceleration = acceleration
        self.__bounce = bounce
        self.__friction = friction
        self.__trail = Trail();

    def move(self, time):
        self.__position.x += self.__speed.x + 0.5 * self.__acceleration.x * time **2
        self.__position.y += self.__speed.y + 0.5 * self.__acceleration.y * time **2
        self.__speed.x += self.__acceleration.x * time
        self.__speed.y += self.__acceleration.y * time
        

    def bounce(self, game_dimension:Vect2D):
        if self.__position.x <= 0 + self.__radius:
            border = 0
            self.__speed.x = -self.__speed.x * self.__bounce
            self.__speed.y *= self.__friction
            self.__position.x = 2.0 * (border + self.__radius) - self.__position.x

        elif self.__position.x >= game_dimension.x - self.__radius :
            border = game_dimension.x
            self.__speed.x = -self.__speed.x * self.__bounce
            self.__speed.y *= self.__friction
            self.__position.x = 2.0 * (border - self.__radius) - self.__position.x

        if self.__position.y <= 0 + self.__radius :
            border = 0
            self.__speed.y = -self.__speed.y * self.__bounce
            self.__speed.x *= self.__friction
            self.__position.y = 2.0 * (border + self.__radius) - self.__position.y

        elif self.__position.y >= game_dimension.y - self.__radius :
            border = game_dimension.y
            self.__speed.y = -self.__speed.y * self.__bounce
            self.__speed.x *= self.__friction
            self.__position.y = 2.0 * (border - self.__radius) - self.__position.y

    def tick(self, time, game_dimensions, acceleration, game):
        
        self.__acceleration = acceleration
        
        if not game.hand_of_god == Vect2D(-1, -1):
            self.pushed_by(game.hand_of_god)
            
        if game.gravity_field_active:
                self.pulled_by(game.balls)
                
        # if acceleration == Vect2D(0, 0):
        #     self.reset_speed()
        #     pass

        self.move(time)
        self.bounce(game_dimensions)
         
            
    def pulled_by(self, balls):
        for ball in balls:
            if ball is not self:
                self.__acceleration += ball.masse * (ball.position - self.position) / ((ball.position - self.position).length_squared + 100 ** 2) ** 1.5            

    def pushed_by(self, hand_of_god):
        self.__acceleration += -10000000 * (hand_of_god - self.position) / ((hand_of_god - self.position).length_squared + 100 ** 2) ** 1.5
        print(self.__acceleration) 
        pass  
    
    def reset_speed(self):
        self.__speed.x = self.__initial_speed.x
        self.__speed.y = self.__initial_speed.y
        

    @property
    def position(self):
        return self.__position

    @property
    def radius(self):
        return self.__radius

    @property
    def fill_color(self):
        return self.__fill_color
        
    @property
    def border_color(self):
        return self.__border_color

    @property
    def density(self):
        return self.__density
    
    @property
    def trail(self):
        return self.__trail
        
class Game(Updatable):

    def __init__(self, size, nb_balls=90):
        super().__init__()
        self.__gravity_magnet = GravityMagnet()
        self.__size = size
        self.__nb_balls = nb_balls
        self.__balls = []
        self.__gravity_field_active = False
        self.__hand_of_god = Vect2D(-1, -1)
        for _ in range(self.__nb_balls):
            self.__balls.append(Ball(radius=random.randrange(5,50), fill_color=(random.randint(0,255),random.randint(0,255), random.randint(0,255)), border_color=(random.randint(0,255),random.randint(0,255), random.randint(0,255)), density=50, position=Vect2D(random.randrange(0,self.__size.x),random.randrange(0,self.__size.y)), speed=Vect2D(random.randrange(-10,10),random.randrange(-10,10)), acceleration=Vect2D(0,0), bounce=0.95, friction=0.95))
            #self.__balls.append(Ball())

    def tick(self):
        for ball in self.__balls:
            ball.tick(0.01, self.__size, self.gravity_magnet.pulled_by(), self)
                    

    def toggle_gravity_field(self, event):
        if self.__gravity_field_active:
            self.__gravity_field_active = False
        else:
            self.__gravity_field_active = True
            
    def move_hand_of_god(self, event):
        self.__hand_of_god.x = event.x
        self.__hand_of_god.y = event.y

    @property
    def gravity_field_active(self):
        return self.__gravity_field_active

    @property
    def gravity_magnet(self):
        return self.__gravity_magnet
    
    @property
    def balls(self):
        return self.__balls
    
    @property
    def hand_of_god(self):
        return self.__hand_of_god

class Application(Tk, Updatable):
    
    def __init__(self, width=500, height=500):
        super().__init__()

        self.width = width
        self.height = height

        self.title('Balls gravity')
        self.geometry(f'{width}x{height}')

        self.w = ttk.Label(self)
        self.w.grid(column=0, row=0)
        
        
        self.g = Game(Vect2D(width, height))
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.bind('<KeyPress-Left>', self.g.gravity_magnet.set_direction)
        self.bind('<KeyPress-Right>', self.g.gravity_magnet.set_direction)
        self.bind('<KeyPress-Down>', self.g.gravity_magnet.set_direction)
        self.bind('<KeyPress-Up>', self.g.gravity_magnet.set_direction)
        self.bind('<KeyPress-Left')
        self.bind('<KeyRelease-Left>', self.g.gravity_magnet.set_direction)
        self.bind('<KeyRelease-Right>', self.g.gravity_magnet.set_direction)
        self.bind('<KeyRelease-Down>', self.g.gravity_magnet.set_direction)
        self.bind('<KeyRelease-Up>', self.g.gravity_magnet.set_direction)

        self.bind('<KeyPress-Return>', self.g.toggle_gravity_field)
        
        self.bind('<Motion>', self.g.move_hand_of_god)

        self.tick()

    def log(self, event):
        return event.keysym
    
    def tick(self):
        self.g.tick()
        self.update_view()

        self.after(10, self.tick)
    
    def update_view(self):
        i = Image.new(mode='RGB', size=(self.width, self.height), color=(0,0,0))
        draw = ImageDraw.Draw(i)

        for ball in self.g.balls:
            draw.ellipse([(ball.position.x - ball.radius, ball.position.y - ball.radius), (ball.position.x + ball.radius, ball.position.y + ball.radius)], ball.fill_color, ball.border_color)
            ball.trail.tick(ball)
            for point in ball.trail.points:
                draw.point((point.x, point.y), ball.fill_color)
       
        self.tki = ImageTk.PhotoImage(i)
        self.w["image"] = self.tki

def main():
    
    app = Application(1000,1000)
    app.mainloop()
    
if __name__ == '__main__':
    main()