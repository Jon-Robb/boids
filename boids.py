import random
from abc import abstractmethod
# from this import d
from tkinter import Tk, ttk
from turtle import position
from PIL import Image, ImageDraw, ImageTk
from vect2d import Vect2D
import math

class Clamper():
    def clamp_max(value, max):
        return min(value, max)

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
        return (self.__r, self.__g, self.__b, self.__a)

        
    def randomize_color(self):
        self.__r = random.randint(0, 255)
        self.__g = random.randint(0, 255)
        self.__b = random.randint(0, 255)
        self.__a = random.randint(0, 255)


class Drawable():
    def __init__(self, border_color, border_width, fill_color, position:Vect2D, size:Vect2D):
        self.__border_color = border_color
        self.__border_width = border_width
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
    def width(self):
        return self.__size.x

    @property
    def height(self):
        return self.__size.y
    
    @property
    def fill_color(self):
        return self.__fill_color.rgba

    @property
    def border_color(self):
        return self.__border_color.rgba

    @property
    def border_width(self):
        return self.__border_width
    
    @property
    def position(self):
        return self.__position

    @property
    def pos_x(self):
        return self.__position.x

    @property
    def pos_y(self):
        return self.__position.y

    @pos_x.setter
    def pos_x(self, pos_x):
        self.__position.x = pos_x

    @pos_y.setter
    def pos_y(self, pos_y):
        self.__position.y = pos_y

    @position.setter
    def position(self, position):
        self.__position = position

class Movable():
    def __init__(self, acceleration, max_speed, speed):
        self.__acceleration = acceleration
        self.__speed = speed
        self.__max_speed = max_speed


    def move(self, time):
        self.position += self.speed * time + self.acceleration * 0.5 ** 2 * time
        self.speed += self.steering_force
        # self.speed.clamp_x(0, self.max_speed)
        # self.speed.clamp_y(0, self.max_speed)

    @property
    def max_speed(self):
        return self.__max_speed

    @property
    def speed(self):
        return self.__speed

    @property
    def acceleration(self):
        return self.__acceleration

    @speed.setter
    def speed(self, speed):
        self.__speed = speed
        
class Touchable():
    def __init__(self, friction_coeff, bounce_coeff):
        self.__friction_coeff = friction_coeff
        self.__bounce_coeff = bounce_coeff

    def bounce(self, sim_dim:Vect2D):
        if self.pos_x <= 0 + self.radius:
            border = 0
            self.speed.x = -self.speed.x * self.__bounce_coeff
            self.speed.y *= self.__friction_coeff
            self.pos_x = 2.0 * (border + self.radius) - self.pos_x

        elif self.pos_x >= sim_dim.x - self.radius :
            border = sim_dim.x
            self.speed.x = -self.speed.x * self.__bounce_coeff
            self.speed.y *= self.__friction_coeff
            self.pos_x = 2.0 * (border - self.radius) - self.pos_x

        if self.pos_y <= 0 + self.radius :
            border = 0
            self.speed.y = -self.speed.y * self.__bounce_coeff
            self.speed.x *= self.__friction_coeff
            self.pos_y = 2.0 * (border + self.radius) - self.pos_y

        elif self.pos_y >= sim_dim.y - self.radius :
            border = sim_dim.y
            self.speed.y = -self.speed.y * self.__bounce_coeff
            self.speed.x *= self.__friction_coeff
            self.pos_y = 2.0 * (border - self.radius) - self.pos_y

    @property
    def bounce_coeff(self):
        return self.__bounce_coeff

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
        self.__size = Vect2D(Tk.winfo_screenwidth(self) * 0.5, Tk.winfo_screenheight(self) * 0.8)
        self.__gui = GUI(size=Vect2D(self.__size.x, self.__size.y), fill_color=RGBAColor(0 ,0, 0)) 
        self.title('Boids')
        self.geometry("{}x{}+{}+{}".format(int(self.width), (int(self.height)), int(Tk.winfo_screenwidth(self) * 0.5 - self.width * 0.5), 0 + int(Tk.winfo_screenwidth(self) * 0.50 - self.height)))
        self.geometry()
        self.iconbitmap('boids.ico')
        # self.mouse_pos = MousePos()
        self.__simulation = Simulation(nb_circles=2, size=Vect2D(self.__gui.view_window.width, self.__gui.view_window.height))

        self.__gui.view_window.image_label.bind('<Motion>', self.__simulation.move_mouse)
        self.__gui.view_window.image_label.bind('<Leave>', self.__simulation.move_left)

        self.tick()
        
        # self.bind('<Motion>', self.mouse_pos.move_mouse)
        
        self.mainloop()

    @property
    def size(self):
        return self.__size


    def tick(self):
        #self.__simulation.tick(time=0.1, sim_dim=Vect2D(500,500))

        self.__simulation.tick(time=0.1, sim_dim=Vect2D(self.__simulation.width, self.__simulation.height))
        self.__gui.view_window.update_view(self.__simulation)
        self.after(10, self.tick)
                   
    # APP getters #    
    @property
    def width(self):
        return self.__size.x

    @property
    def height(self):
        return self.__size.y
     
class Entity(Drawable, Updatable):
    def __init__(self, border_color, border_width, fill_color, position, size):
        Drawable.__init__(self, border_color, border_width, fill_color, position, size)
        Updatable.__init__(self)

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def tick(self):
        pass
     
class Simulation(Updatable):
    def __init__(self, nb_circles:int=2, size=Vect2D(100,100)):

        self.__size = size
        self.__sprites = []
        self.__mouse_pos = Vect2D()
        for _ in range(nb_circles):
            random_radius = random.randrange(5,50)
            self.__sprites.append(DynamicCircle(
                                                border_color=RGBAColor(randomize=True),
                                                border_width=random.randrange(0, random_radius),
                                                fill_color=RGBAColor(randomize=True),
                                                #position=Vect2D(random.randrange(0,501),200),
                                                radius=random_radius,
                                                position=Vect2D(random.randrange(0 + random_radius, int(self.width) - random_radius),random.randrange(0 + random_radius, int(self.height) - random_radius)),
                                                acceleration=Vect2D(0,0),
                                                max_speed=1000,
                                                #speed=Vect2D(0,0),
                                                speed=Vect2D(random.randrange(-50,50),random.randrange(-50,50)),
                                                max_steering_force=15,
                                                slowing_distance=10,
                                                steering_force=Vect2D(0,0),
                                                steering_behaviors=[Evade()]
                                                ))

        self.sprites.append(DynamicCircle(
                            border_color=RGBAColor(randomize=True),
                            border_width=random.randrange(0, random_radius),
                            fill_color=RGBAColor(randomize=True),
                            #position=Vect2D(random.randrange(0,501),200),
                            radius=random_radius,
                            position=Vect2D(random.randrange(0 + random_radius, int(self.width) - random_radius),random.randrange(0 + random_radius, int(self.height) - random_radius)),
                            acceleration=Vect2D(0,0),
                            max_speed=1000,
                            #speed=Vect2D(0,0),
                            speed=Vect2D(100,100),
                            max_steering_force=15,
                            slowing_distance=10,
                            steering_force=Vect2D(0,0),
                            steering_behaviors=None
        ))
        
    def tick(self, time, sim_dim):
        if self.__sprites:
            for sprite in self.__sprites:
                sprite.tick(time, sim_dim, self)

    def move_mouse(self, event):
        self.__mouse_pos = Vect2D(event.x, event.y)
        
    def move_left(self, event):
        self.__mouse_pos = None
        
        for sprite in self.__sprites:
            sprite.steering_force = Vect2D(0,0)

    @property
    def sprites(self):
        return self.__sprites
    
    @property
    def mouse_pos(self):
        return self.__mouse_pos
    
    @property
    def size(self):
        return self.__size

    @property
    def width(self):
        return self.__size.x

    @property
    def height(self):
        return self.__size.y

class GUI(ttk.Frame, Drawable):
    def __init__(self, border_color=None, border_width=None, fill_color=None, position=None, size:Vect2D=None):
        ttk.Frame.__init__(self, root=None, text=None)
        Drawable.__init__(self, border_color,  border_width, fill_color, position, size)
        self.__main_panel = ControlBar()
        self.__view_window = ViewWindow(size=Vect2D(size.x * 0.82, size.y * 0.99), fill_color=fill_color)   
        self.__main_panel.grid(row=0, column=0, rowspan=3, sticky='nsew')
        self.__view_window.grid(row=0, column=1, rowspan=3, sticky="nsew") 


    @property
    def view_window(self):
        return self.__view_window  


class ControlBar(ttk.Frame):
    def __init__(self):
        ttk.Frame.__init__(self)
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
    def __init__(self, border_color=None, border_width=None, fill_color=None, position=None, size=None):
        ttk.Label.__init__(self, root=None, text=None, width=size.x)
        Drawable.__init__(self, border_color, border_width, fill_color, position, size)
        self.__canvas = Image.new('RGBA', (int(size.x), int(size.y)), (0, 0, 0))
        self.__image_draw = ImageDraw.Draw(self.__canvas)
        self.__image_tk = ImageTk.PhotoImage(self.__canvas)
        self.__image_label = ttk.Label(self, image=self.__image_tk)
        # self.__ball = DynamicCircle(position=Vect2D(100,100))
        # self.__ball.draw(self.__image_label, self.__canvas, self.__image_draw)
        self.__image_label.grid(row=0, column=0, sticky='ns')
        self.__image_label.columnconfigure(0, minsize=600, weight=1)


    def update_view(self, simulation):

            i = Image.new('RGBA', (int(self.width), int(self.height)), (0, 0, 0))
            draw = ImageDraw.Draw(i)

            for sprite in simulation.sprites:
                sprite.draw(draw)
        
            self.__image_tk = ImageTk.PhotoImage(i)
            self.__image_label["image"] = self.__image_tk

            # self.tki = ImageTk.PhotoImage(self.__gui.view_window.canvas)
            # self.__gui.view_window.image_label["image"] = self.tki

            # self.after(10, self.tick)  


    @property
    def canvas(self):
        return self.__canvas

    @property
    def image_draw(self):
        return self.__image_draw     

    @property
    def image_label(self):
        return self.__image_label    

    @canvas.setter
    def canvas(self, canvas):
        self.__canvas = canvas


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
    
class Circle(Entity, Touchable):
    def __init__(self, border_color, border_width, bounce_coeff, fill_color, friction_coeff, position:Vect2D, radius:int):
        Entity.__init__(self, border_color=border_color, border_width=border_width, fill_color=fill_color, position=position, size=Vect2D(radius*2, radius*2))
        Touchable.__init__(self, bounce_coeff=bounce_coeff, friction_coeff=friction_coeff)
        self.__fill_color = fill_color
        self.__border_color = border_color
        self.__radius = radius

    def bounce(self):
        Touchable.bounce() 

    def draw(self, draw):
        
        draw.ellipse(
                [self.position.x - self.__radius,
                self.position.y - self.__radius,
                self.position.x + self.__radius,
                self.position.y + self.__radius],
                fill=self.fill_color,
                width=self.border_width,
                outline=self.border_color)
       
        # self.tki = ImageTk.PhotoImage(canvas)
        # label["image"] = self.tki

    @abstractmethod
    def tick(self, time):
        pass

    @property
    def radius(self):
        return self.__radius
    
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
   

 
class Seek(SteeringBehavior):
    def __init__(self, attraction_repulsion_force=1, distance_to_target=None):
        SteeringBehavior.__init__(self, attraction_repulsion_force, distance_to_target)
      
        
    def behave(self, local_entity: Entity, target_entity: Entity):
        if target_entity is not None:
            desired_speed = (target_entity.position - local_entity.position).normalized * local_entity.max_speed
            return desired_speed - local_entity.speed
    
    #Pour suivre le mouvement de la souris 
    def behave(self, local_entity:Entity, target_entity: Vect2D):
        if target_entity is not None:
            desired_speed = (target_entity.position - local_entity.position).normalized * local_entity.max_speed
            return desired_speed - local_entity.speed
        
class Flee(Seek):
    def __init__(self):
        super().__init__(self)
        
    # def behave(self, local_entity: Entity, target_entity: Entity):
    #     if target_entity is not None:
    #         desired_speed = (local_entity.position - target_entity.position).normalized * local_entity.max_speed
    #         return desired_speed - local_entity.speed
        
    def behave(self, local_entity: Entity, target_entity: Vect2D):
        return super().behave(local_entity, target_entity) * -1   
        
class Pursuit(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        self.__ratio = 2
        
    def behave(self, origin_entity: Entity, target_entity: Entity) -> Vect2D:
        if target_entity is not None:
            estimated_position = target_entity.position + target_entity.speed  * self.__ratio 
            desired_speed = (estimated_position - origin_entity.position).normalized * origin_entity.max_speed
            return desired_speed - origin_entity.speed
            
class BorderRepulsion(SteeringBehavior):
    def __init__(self):       
        super().__init__(self) 
    
    def behave(self, origin_entity:Entity, sim_dim):
        repulsive_force_left = (Vect2D(1, 0))/origin_entity.position.x ** 2 if origin_entity.position.x > 0 else Vect2D(1, 0)
        repulsive_force_right = (Vect2D(-1, 0))/(sim_dim.x - origin_entity.position.x) ** 2 if origin_entity.position.x < sim_dim.x else Vect2D(-1, 0)
        repulsive_force_top = (Vect2D(0, 1))/origin_entity.position.y ** 2 if origin_entity.position.y > 0 else Vect2D(0, 1)
        repulsive_force_bottom = (Vect2D(0, -1))/(sim_dim.y - origin_entity.position.y) ** 2 if origin_entity.position.y < sim_dim.y else Vect2D(0, -1)
        return repulsive_force_left + repulsive_force_right + repulsive_force_top + repulsive_force_bottom

  
                    
class Evade(Pursuit):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, origin_entity: Entity, target_entity: Entity) -> Vect2D:
        return super().behave(origin_entity, target_entity) * -1
    
            

           
class Piloted():
    def __init__(self, max_steering_force:int, slowing_distance:int, steering_force:Vect2D, steering_behaviors:list[SteeringBehavior]):
        self.__max_steering_force = max_steering_force
        self.__slowing_distance = slowing_distance
        self.steering_force = steering_force
        self.__steering_behaviors = steering_behaviors

    def steer(self, target_entity:Entity=None, sim_dim = None):
        if self.__steering_behaviors is not None:
            for steering_behavior in self.__steering_behaviors:
                if (isinstance(steering_behavior, Seek) or isinstance(steering_behavior, Flee) or isinstance(steering_behavior, Pursuit)) and target_entity is not None:
                    self.steering_force += steering_behavior.behave(self, target_entity)
                elif isinstance(steering_behavior, BorderRepulsion):
                    self.steering_force += steering_behavior.behave(origin_entity = self,sim_dim=sim_dim)
            
        self.steering_force.set_polar(length= Clamper.clamp_max(self.steering_force.length, self.__max_steering_force), orientation=self.steering_force.orientation)
        
    
    @property
    def steering_force(self):
        return self.__steering_force

    @steering_force.setter
    def steering_force(self, steering_force):
        self.__steering_force = steering_force
        
class DynamicCircle(Circle, Movable, Piloted):
    def __init__(   self,
                    border_color=RGBAColor(randomize=True),
                    border_width=5,
                    bounce_coeff=0.95,
                    fill_color=RGBAColor(randomize=True),
                    friction_coeff=0.95,
                    position=Vect2D(random.randrange(0,1000),random.randrange(0,500)),
                    radius=random.randrange(30,100),
                    acceleration=Vect2D(0,0),
                    speed=Vect2D(random.randrange(-10,10),random.randrange(-10,10)),
                    max_speed= 100,
                    max_steering_force=1,
                    slowing_distance=10,
                    steering_force=Vect2D(0,0),
                    steering_behaviors=None,
                ):
    
        Circle.__init__(self, border_color, border_width, bounce_coeff, fill_color, friction_coeff, position, radius)
        Movable.__init__(self, acceleration, max_speed, speed)
        Piloted.__init__(self, max_steering_force, slowing_distance, steering_force, steering_behaviors)

    def move(self, time):
        Movable.move(self, time)

    def bounce(self, sim_dim):
        Touchable.bounce(self, sim_dim)

    def tick(self, time, sim_dim, simulation):
        self.steer(target_entity=simulation.sprites[-1].position, sim_dim=sim_dim)
        self.move(time)
        self.bounce(sim_dim)
    
def main():
    App()

if __name__ == '__main__':
    main()