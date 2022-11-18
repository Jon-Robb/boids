import math
import random
from abc import abstractmethod
from tkinter import Tk, ttk
from PIL import Image, ImageDraw, ImageTk
from vect2d import Vect2D


class RGBAColor():
    def __init__(self, r:int=255, g:int=255, b:int=255, a:int=255, randomize:bool=False):
        self.__r = r
        self.__g = g
        self.__b = b
        self.__a = a

        if randomize:
            self.randomize_color()
        
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
    
    @property
    def rgba(self):
        return (self.__r, self.__b, self.__g, self.__a)

        
    def randomize_color(self):
        self.__r = random.randint(0, 255)
        self.__g = random.randint(0, 255)
        self.__b = random.randint(0, 255)
        self.__a = random.randint(0, 255)


class Drawable():
    def __init__(self, border_color, fill_color, position:Vect2D, size:Vect2D):
        self.__border_color = border_color
        self.__fill_color = fill_color
        self.__position = position
        self.__size = size


    @abstractmethod
    def draw(self):
        pass

    @property
    def size(self):
        return self.__size
    
    @property
    def fill_color_(self):
        return self.__fill_color.rgba

    @property
    def border_color_(self):
        return self.__border_color.rgba
    
    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position

class Movable():
    def __init__(self, acceleration, max_speed, speed):
        self.__acceleration = acceleration
        self.__speed = speed
        self.__max_speed = max_speed


    def move(self, time):
        self.position += self.__speed * time + self.__acceleration * 0.5 ** 2

    @property
    def max_speed(self):
        return self.__max_speed
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

# class App(Updatable):
# def __init__(self):
    
#     self.__gui = GUI()



class App(Tk, Updatable):
    
    def __init__(self):
        Tk.__init__(self)
        self.__size = Vect2D(Tk.winfo_screenwidth(self), Tk.winfo_screenheight(self))

        self.__gui = GUI(size=Vect2D(self.__size.x * 0.5,self.__size.y * 0.8), fill_color=RGBAColor(0 ,0, 0)) 
        self.title('Boids')
        self.geometry(str(int(self.__size.x * 0.5)) + 'x' + str(int(self.__size.y * 0.8)))
        self.iconbitmap('boids.ico')

        self.__simulation = Simulation()

        # self.tick()

        self.mainloop()


    def tick(self):
        for sprite in self.__simulation.sprites:
            print(sprite.position)

        self.__simulation.tick(time=0.1, draw=self.__gui.view_window.image_draw) 

        self.after(10, self.tick)

               
    # GUI getters #    
    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height
     
class Entity(Drawable, Updatable):
    def __init__(self, border_color, fill_color, position, size):
        Drawable.__init__(self, border_color, fill_color, position, size)
        Updatable.__init__(self)

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def tick(self):
        pass
     
class Simulation(Updatable):
    def __init__(self, nb_sprites:int=2):

        self.__sprites = []

        for _ in range(nb_sprites):
            self.__sprites.append(DynamicCircle())

    def tick(self, time, draw):
        if self.__sprites:
            for sprite in self.__sprites:
                sprite.tick(time, draw)

    @property
    def sprites(self):
        return self.__sprites

class GUI(ttk.Frame, Drawable):
    def __init__(self, border_color=None, fill_color=None, position=None, size:Vect2D=None):
        ttk.Frame.__init__(self, root=None, text=None)
        Drawable.__init__(self, border_color,  fill_color, position, size)
        self.__main_panel = ControlBar("Main Panel")
        self.__view_window = ViewWindow(size=(size.x * 0.8, size.y * 0.9), fill_color=fill_color)   
        self.__main_panel.grid(row=0, column=0, sticky='nsew')
        self.__view_window.grid(row=0, column=1, rowspan=3, sticky="nsew") 
        
    
    @property
    def view_window(self):
        return self.__view_window
        


class ControlBar(ttk.Frame):
    def __init__(self, title):
        ttk.Frame.__init__(self, title=None)
        self.__control_panel = StartStopPanel("Control")
        self.__param_panel = ParamPanel("Paramètre")
        self.__visual_param_panel = VisualParamPanel("Paramètre visuel")
        self.__control_panel.grid(row=0, column=0)
        self.__param_panel.grid(row=1, column=0)
        self.__visual_param_panel.grid(row=2, column=0)



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
    def __init__(self, border_color=None, fill_color=None, position=None, size=None):
        ttk.Label.__init__(self, root=None, text=None, width=size[0])
        Drawable.__init__(self, border_color, fill_color, position, size)
        self.__image = Image.new('RGBA', (int(size[0]), int(size[1])), (0, 0, 0))
        self.__image_draw = ImageDraw.Draw(self.__image)
        self.__ball = DynamicCircle()
        self.__ball.draw(self.__image_draw)
        self.__image_tk = ImageTk.PhotoImage(self.__image)
        self.__ball = DynamicCircle()
        self.__ball.draw(self.__image_draw)
        self.__image_label = ttk.Label(self, image=self.__image_tk)
        self.__image_label.grid(row=0, column=0, sticky='ns')
        self.__image_label.columnconfigure(0, minsize=600, weight=1)




    @property
    def image(self):
        return self.__image

    @property
    def image_draw(self):
        return self.__image_draw        


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
    
class Circle(Entity, Touchable):
    def __init__(self, border_color, fill_color, position:Vect2D, radius:int):
        Entity.__init__(self, border_color=border_color, fill_color=fill_color, position=position, size=(radius*2, radius*2))
        self.__fill_color = fill_color
        self.__border_color = border_color
        self.__radius = radius

    def check_collision(self):
        Touchable.check_collision() 

    def draw(self, draw):
        draw.ellipse(
        [self.position.x,
        self.position.y,
        self.position.x + self.__radius,
        self.position.y + self.__radius],
        fill=self.__fill_color.rgba,
        outline=self.__border_color.rgba)

    def tick(self, time, draw):
        self.move(time)
        self.draw(draw)

class StaticCircle(Circle):
    def __init__(self):
        Circle.init(self)


class SteeringBehavior():
    def __init__(self, attraction_repulsion_force=None, distance_to_target=None):
        self.__attraction_repulsion_force = attraction_repulsion_force
        self.__distance_to_target = distance_to_target
        self.__resulting_direction = None

    @abstractmethod    
    def behave(self, origin_entity:Entity, target_entity:Entity):
        pass  
    
class CollisionAvoidance(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, origin_entity: Entity, target_entity: Entity):
        return super().behave(origin_entity, target_entity)
 
    
class Wander(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, origin_entity: Entity, target_entity: Entity):
        return super().behave(origin_entity, target_entity)
 
    
class FleeArrival(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, this_entity: Entity, target_entity: Entity):
        return super().behave(this_entity, target_entity)
 
    
class Seek(SteeringBehavior):
    def __init__(self, attraction_repulsion_force=1, distance_to_target=None):
        SteeringBehavior.__init__(self, attraction_repulsion_force, distance_to_target)
        
    def behave(self, this_entity: Entity, target_entity: Entity):
        return super().behave(this_entity, target_entity)
    
class Piloted():
    def __init__(self, slowing_distance:int, steering_force:Vect2D, steering_behaviors:list[SteeringBehavior]):
        self.__slowing_distance = slowing_distance
        self.__steering_force = steering_force
        self.__steering_behaviors = steering_behaviors

    def steer(self, target_entity=None):
        for steering_behavior in self.__steering_behaviors:
            self.__steering_force += steering_behavior.behave(self, target_entity)
        
        if self.__steering_force.length > self.max_speed:
            self.__steering_force.length = self.max_speed
        


class DynamicCircle(Circle, Movable, Piloted):
    def __init__(   self,
                    border_color=RGBAColor(randomize=True),
                    fill_color=RGBAColor(randomize=True),
                    position=Vect2D(random.randrange(0,1000),random.randrange(0,500)),
                    radius=random.randrange(30,100),
                    acceleration=Vect2D(0,100),
                    speed=Vect2D(random.randrange(-10,10),random.randrange(-10,10)),
                    max_speed=1,
                    slowing_distance=10,
                    steering_force=Vect2D(0,0),
                    steering_behaviors=None,
                ):
    
        Circle.__init__(self, border_color, fill_color, position, radius)
        Movable.__init__(self, acceleration, max_speed, speed)
        Piloted.__init__(self, slowing_distance, steering_force, steering_behaviors)

    def move(self, time):
        Movable.move(self, time)
    


def main():
    App()


if __name__ == '__main__':
    main()