import math
import random
from abc import abstractmethod
from tkinter import Tk, ttk
from PIL import Image, ImageDraw, ImageTk
from vect2d import Vect2D


class RGBAColor():
    def __init__(self, r:int=255, g:int=255, b:int=255, a:int=255):
        self.__r = r
        self.__g = g
        self.__b = b
        self.__a = a
        
        @property
        def r(self):
            return self.__r
        
        @property
        def g(self):
            return self.__g
        
        @property
        def b(self):
            return self.__b
        
        @property
        def a(self):
            return self.__a


class Drawable():
    def __init__(self, size:Vect2D, color:RGBAColor, position:Vect2D):
        self.__size = size
        self.__color = color
        self.__position = position


    @property
    def size(self):
        return self.__size
    
    @property
    def color(self):
        return self.__color
    
    @property
    def position(self):
        return self.__position


class Movable():
    def __init__(self, speed, max_speed):
        self.__speed = speed
        

    @abstractmethod
    def move(self):
        pass
class Touchable():
    def __init__(self):
        pass

    @abstractmethod
    def checkCollision(self):
        pass

class Updatable():
    def __init__(self):
        pass

    @abstractmethod
    def tick(self):
        pass

class App():
    def __init__(self):
        self.__gui = GUI(500,500)
        #self.__simulation = Simulation()
    
    
class GUI(Tk):
    
    def __init__(self, width, height):
        Tk.__init__(self)
        self.__main_frame = MainFrame(Vect2D(500,500), RGBAColor(0 ,0, 0), Vect2D(0,0)) 
        self.title('Boids')
        self.__width = width
        self.__height = height
        self.geometry(str(int(self.__width)) + 'x' + str(int(self.__height)))
        self.iconbitmap('boids.ico')
        
        self.mainloop()
               
    # GUI getters #    
    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

     
class Entity():
    def __init__(self):
        pass
     
class Simulation(Updatable):
    def __init__(self, sprites:list[Entity]):
        self.__sprites = sprites

    def tick(self):
        for sprite in self.__sprites:
            sprite.tick()


class MainFrame(ttk.Frame, Drawable):
    def __init__(self, size:Vect2D, color, position=None):
        ttk.Frame.__init__(self, root=None, text=None)
        Drawable.__init__(self, size, color, position)
        self.__main_panel = ControlBar("Main Panel")
        self.__view_window = ViewWindow(size, color)   
        self.__main_panel.grid(row=0, column=0, sticky='nsew')
        self.__view_window.grid(row=0, column=1, sticky="nsew") 
        
        


class ControlBar(ttk.Frame):
    def __init__(self, title):
        ttk.Frame.__init__(self, title=None)
        self.__control_panel = StartStopPanel("Control")
        self.__param_panel = ParamPanel("Paramètre")
        self.__visual_param_panel = VisualParamPanel("Paramètre visuel")
        self.__control_panel.grid(row=0, column=0)
        self.__param_panel.grid(row=1, column=0)
        self.__visual_param_panel.grid(row=2, column=0)
        self.__control_panel.rowconfigure(0, minsize=200, weight=1)
        self.__control_panel.columnconfigure(0, minsize=200, weight=1)
        self.__param_panel.rowconfigure(1, minsize=200, weight=1)
        self.__param_panel.columnconfigure(1, minsize=200, weight=1)
        self.__visual_param_panel.rowconfigure(2, minsize=200, weight=1)
        self.__visual_param_panel.columnconfigure(2, minsize=200, weight=1)
        self.grid(row=0, column=0, sticky='ns')
        


class StartStopPanel(ttk.LabelFrame):
    def __init__(self, text): 
        ttk.LabelFrame.__init__(self, root=None, text=text)
        self.__start_button = ttk.Button(self, text="Start")
        self.__stop_button = ttk.Button(self, text="Stop")
        self.__next_button = ttk.Button(self, text="Next Step")
        self.__start_button.pack()
        self.__stop_button.pack()
        self.__next_button.pack()


class ViewWindow(ttk.Label, Drawable):
    def __init__(self, size, color, position=None):
        ttk.Label.__init__(self, root=None, text=None)
        Drawable.__init__(self, size, color, position)
        self.__image = Image.new('RGBA', (int(400), int(100)), (0, 0, 0))
        self.__image_draw = ImageDraw.Draw(self.__image)
        self.__image_tk = ImageTk.PhotoImage(self.__image)
        self.__image_label = ttk.Label(self, image=self.__image_tk)
        self.__image_label.grid(row=0, column=0, sticky='ns')
        self.__image_label.columnconfigure(0, minsize=600, weight=1)



class ParamPanel(ttk.LabelFrame):
    def __init__(self, title):
        ttk.LabelFrame.__init__(self, root=None, text=title)
        self__test_btn = ttk.Button(self, text="Test")
        self__test_btn.pack()
        


class VisualParamPanel(ttk.LabelFrame):
     def __init__(self, title):
        ttk.LabelFrame.__init__(self, root=None, text=title)
        self__test_btn = ttk.Button(self, text="Test")
        self__test_btn.pack()

class SimParamPanel(ParamPanel):
    def __init__(self):
        pass    

    @abstractmethod
    def draw(self):
        pass
    
    @property
    def sprites(self):
        return self.__sprites
    

    
    @abstractmethod
    def check_collision(self):
        pass
    
class Circle(Entity, Movable, Touchable):
    def __init__(self, border_color=(random.randint(0,255),random.randint(0,255), random.randint(0,255)), fill_color=(random.randint(0,255),random.randint(0,255), random.randint(0,255)), max_speed:int=1, position:Vect2D=Vect2D(random.randrange(0,100),random.randrange(0,100)), radius:int=random.randrange(5,10), speed:Vect2D=Vect2D(random.randrange(-10,10),random.randrange(-10,10))):
        Entity.__init__(self, fill_color=fill_color, border_color=border_color, position=position, size=(radius*2, radius*2))
        Movable.__init__(self, max_speed=max_speed, speed=speed)


    def check_collision(self):
        return super().check_collision()

    def move(self, time):

        self.__position.x += self.__speed.x + 0.5 * self.__acceleration.x * time **2
        self.__position.y += self.__speed.y + 0.5 * self.__acceleration.y * time **2
        self.__speed.x += self.__acceleration.x * time
        self.__speed.y += self.__acceleration.y * time
        

    def tick(self, time):
        
        self.move(time)

class StaticCircle(Circle):
    def __init__(self):
        Circle.init(self)


class SteeringBehavior():
    def __init__(self):
        self.__force_attraction_repulsion = None
        self.__resulting_direction = None
        
    @abstractmethod    
    def behave(self, this_entity:Entity, target_entity:Entity):
        return target_entity.position - this_entity.position
  
    
class CollisionAvoidance(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, this_entity: Entity, target_entity: Entity):
        return super().behave(this_entity, target_entity)
 
    
class Wander(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, this_entity: Entity, target_entity: Entity):
        return super().behave(this_entity, target_entity)
 
    
class FleeArrival(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, this_entity: Entity, target_entity: Entity):
        return super().behave(this_entity, target_entity)
 
    
class Seek(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, this_entity: Entity, target_entity: Entity):
        return super().behave(this_entity, target_entity)
    
class Piloted(Movable):
    def __init__(self, slowing_distance:int, steering_force:Vect2D, desired_speed:Vect2D, steering_behavior:list[SteeringBehavior], acceleration:Vect2D, max_steering_force:Vect2D):
        self.__slowing_distance = slowing_distance
        self.__steering_force = steering_force
        self.__desired_speed = desired_speed
        self.__steering_behavior = steering_behavior
        self.__acceleration = acceleration
        self.__max_steering_force = max_steering_force
    
    @abstractmethod
    def move(self):
        pass

class DynamicCircle(Circle, Piloted):
    def __init__(self, vitesse, vitesse_max):
        self.__vitesse = vitesse
        self.__vitesse_max = vitesse_max
    


def main():
    App()


if __name__ == '__main__':
    main()