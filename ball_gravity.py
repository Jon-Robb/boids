from abc import abstractmethod
import math
import random
from tkinter import ttk, Tk 
from vect2d import Vect2D
from PIL import Image, ImageTk, ImageDraw

# Mathématique:
    # rad * 180/PI = degrés
    # degré * PI/180 = rad 
    

class Updatable():
    def __init__(self):
        pass
    
    @abstractmethod
    def tick(self):
        """Méthode abstraite qui sera redéfinie pour les balles et le jeu
        """
        pass

class Gravitational():
    def __init__(self, masse):
        self._masse = masse
     
    @abstractmethod
    def pull(self, ball):
        pass
        

class Ball(Updatable, Gravitational):
    def __init__(self, radius=random.randrange(5,10), fill_color=(random.randint(0,255),random.randint(0,255), random.randint(0,255)), border_color=(random.randint(0,255),random.randint(0,255), random.randint(0,255)), density=1, position:Vect2D=(random.randrange(0,100),random.randrange(0,100)), speed:Vect2D=(0,0), acceleration:Vect2D=(0,0), bounce=0.95, friction=0.95):
        Gravitational.__init__(self, masse=(density * (math.pi * radius ** 2)))
        self.__radius = radius
        self.__fill_color = fill_color
        self.__border_color = border_color
        self.__density = density
        self.__position = position
        self.__initial_speed = speed
        self.__speed = speed
        self.__acceleration = acceleration
        self.__bounce = bounce
        self.__friction = friction

             
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

    def tick(self, time, game_dimensions):
        self.move(time)
        self.bounce(game_dimensions)
            
    def pull(self, ball):
        pass

    def reset_speed(self):
        self.__speed = self.__initial_speed

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
        
class Game(Updatable):

    def __init__(self, size, nb_balls=36, ball_min_radius=1, ball_max_radius=64, ball_min_speed=1, ball_max_speed=16):
        super().__init__()
        self.__size = size
        self.__nb_balls = nb_balls
        self.__balls = []
        self.__ball_min_radius = ball_min_radius
        self.__ball_max_radius = ball_max_radius
        self.__ball_min_speed = ball_min_speed
        self.__ball_max_speed = ball_max_speed
        for _ in range(self.__nb_balls):
            self.__balls.append(Ball(random.randrange(self.__ball_min_radius, self.__ball_max_radius), (random.randint(0,255),random.randint(0,255), random.randint(0,255)), (random.randint(0,255),random.randint(0,255), random.randint(0,255)), random.randrange(5, 50), Vect2D(random.randrange(0, self.__size.x), random.randrange(0, self.__size.y)), Vect2D(random.randrange(self.__ball_min_speed, self.__ball_max_speed), random.randrange(self.__ball_min_speed, self.__ball_max_speed)), Vect2D(0, 0)))
            #self.__balls.append(Ball())

    def tick(self):
        for ball in self.__balls:
            ball.tick(0.01, self.__size)

    @property
    def balls(self):
        return self.__balls

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

        self.tick()

    def tick(self):
        self.g.tick()
        self.update_view()

        self.after(10, self.tick)
    
    def update_view(self):
        i = Image.new(mode='RGB', size=(self.width, self.height), color=(0,0,0))
        draw = ImageDraw.Draw(i)

        for ball in self.g.balls:
            draw.ellipse([(ball.position.x - ball.radius, ball.position.y - ball.radius), (ball.position.x + ball.radius, ball.position.y + ball.radius)], ball.fill_color, ball.border_color,2)
       
        self.tki = ImageTk.PhotoImage(i)
        self.w["image"] = self.tki

def main():
    
    app = Application(1200,600)
    app.mainloop()
    
if __name__ == '__main__':
    main()