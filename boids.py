import random
from abc import abstractmethod
import tkinter as tk
# from this import d
from tkinter import Tk, ttk
from turtle import position
from PIL import Image, ImageDraw, ImageTk
from vect2d import Vect2D
import math

class Utils():
    def clamp_max(value, max):
        return min(value, max)
    
    def readfile(filename:str)->list:
        data = []
        with open(filename, 'r') as file:
            for line in file:
                data.append(line)
        return data


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
        
        self.speed.clamp_x(-self.max_speed, self.max_speed)
        self.speed.clamp_y(-self.max_speed, self.max_speed)

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


class App(Tk, Updatable):
    
    def __init__(self):
        Tk.__init__(self)
        self.__size = Vect2D(Tk.winfo_screenwidth(self) * 0.5, Tk.winfo_screenheight(self) * 0.8)
        self.__gui = GUI(size=Vect2D(self.__size.x, self.__size.y), fill_color=RGBAColor(0 ,0, 0)) 
        self.title('Boids')
        self.geometry("{}x{}+{}+{}".format(int(self.width), (int(self.height)), int(Tk.winfo_screenwidth(self) * 0.5 - self.width * 0.5), 0 + int(Tk.winfo_screenwidth(self) * 0.50 - self.height)))
        self.geometry()
        self.iconbitmap('boids.ico')
        self.__simulation = Simulation(nb_circles=1, size=Vect2D(self.__gui.view_window.width, self.__gui.view_window.height))

        self.__gui.view_window.image_label.bind('<Enter>', self.__simulation.mouse_entered)
        self.__gui.view_window.image_label.bind('<Motion>', self.__simulation.move_mouse)
        self.__gui.view_window.image_label.bind('<Leave>', self.__simulation.mouse_left)
        self.__gui.main_panel.control_panel.start_stop_button.bind('<Button-1>', self.toggle_simulation)
        self.__gui.main_panel.control_panel.next_button.bind('<Button-1>', self.tick_simulation)
        self.__gui.main_panel.param_panel.combobox.bind('<<ComboboxSelected>>', self.param_changed)

        self.tick()
                
        self.mainloop()

    def param_changed(self, event):
        print("Param changed : " + self.__gui.main_panel.param_panel.param_selected)

    @property
    def size(self):
        return self.__size

    def tick_simulation(self, event=None):
        self.__simulation.tick(time=0.1)

    def tick(self):
        if self.__simulation.is_running:
            self.tick_simulation()
        self.__gui.view_window.update_view(self.__simulation)
        self.after(10, self.tick)
        
    def toggle_simulation(self, event):
        self.__simulation.toggle_running(event)
        if self.__simulation.is_running:
            self.__gui.main_panel.control_panel.start_stop_button.config(text="Stop")
            self.__gui.main_panel.control_panel.next_button.config(state="disabled")
        else:
            self.__gui.main_panel.control_panel.start_stop_button.config(text="Start")
            self.__gui.main_panel.control_panel.next_button.config(state="normal")
            
                   
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
        self.__mouse_pos = None
        self.__is_running = True
        
        # random_radius = random.randrange(5,50)

        self.sprites.append(DynamicCircle(
                        border_color=RGBAColor(randomize=True),
                        border_width=random.randrange(0, 100),
                        fill_color=RGBAColor(randomize=True),
                        #position=Vect2D(random.randrange(0,501),200),
                        radius=10,
                        position=Vect2D(random.randrange(0 + random.randrange(5,50), int(self.width) - random.randrange(5,50)),random.randrange(0 + random.randrange(5,50), int(self.height) - random.randrange(5,50))),
                        acceleration=Vect2D(0,0),
                        max_speed=100,
                        #speed=Vect2D(0,0),
                        speed=Vect2D(100,100),
                        max_steering_force=15,
                        slowing_distance=10,
                        steering_force=Vect2D(0,0),
                        steering_behaviors=[Wander(is_in=True, radius=50, circle_distance=300), BorderRepulsion(attraction_repulsion_force=10000, sim_dim=self.__size)]))

        for _ in range(nb_circles):
            random_radius = random.randrange(5,50)
            random_steering_behavior = random.choice([Seek(), Flee(), Pursuit(), Evade(), BorderRepulsion(attraction_repulsion_force=random.randrange(10,1000), sim_dim=self.__size), PseudoWander(), Wander()])

            self.__sprites.append(DynamicCircle(
                                                border_color=RGBAColor(randomize=True),
                                                # border_color=RGBAColor(r=255,g=0,b=0,a=255) if isinstance(random_steering_behavior, Seek) else RGBAColor(r=0,g=0,b=255,a=255),
                                                border_width=random.randrange(0, random_radius),
                                                # fill_color=RGBAColor(randomize=True),
                                                fill_color= RGBAColor(128, 0, 0, 255) if not isinstance(random_steering_behavior, Flee) else RGBAColor(0, 128, 0, 255),
                                                radius=random_radius,
                                                position=Vect2D(random.randrange(0 + random_radius, int(self.width) - random_radius),random.randrange(0 + random_radius, int(self.height) - random_radius)),
                                                acceleration=Vect2D(0,0),
                                                max_speed=100,
                                                #speed=Vect2D(0,0),
                                                speed=Vect2D(random.randrange(-50,50),random.randrange(-50,50)),
                                                max_steering_force=5,
                                                slowing_distance=10,
                                                steering_force=Vect2D(0,0),
                                                steering_behaviors=[Pursuit(self.sprites[0]), BorderRepulsion(attraction_repulsion_force=10000, sim_dim=self.__size)]))
    
    def tick(self, time):
        if self.__sprites:
            for sprite in self.__sprites:
                sprite.tick(time)

    def move_mouse(self, event):
        self.__mouse_pos = Vect2D(event.x, event.y)
        
    def mouse_left(self, event):
        self.__mouse_pos = None
        
        for sprite in self.__sprites:
            sprite.steering_force = Vect2D(0,0)

    def mouse_entered(self, event):
        self.__mouse_pos = Vect2D(event.x, event.y)
        
    def toggle_running(self, event):
        self.__is_running = not self.__is_running

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
    
    @property
    def is_running(self):
        return self.__is_running

class GUI(ttk.Frame, Drawable):
    def __init__(self, border_color=None, border_width=None, fill_color=None, position=None, size:Vect2D=None):
        ttk.Frame.__init__(self, root=None, text=None)
        Drawable.__init__(self, border_color,  border_width, fill_color, position, size)
        self.__main_panel = ControlBar()
        self.__view_window = ViewWindow(size=Vect2D(size.x * 0.82, size.y * 0.99), fill_color=fill_color)   
        self.__main_panel.grid(row=0, column=0, rowspan=3, sticky='nsew')
        self.__view_window.grid(row=0, column=1, rowspan=3, sticky="nsew") 

    @property
    def main_panel(self):
        return self.__main_panel

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

    @property
    def param_panel(self):
        return self.__param_panel
    
    @property
    def control_panel(self):
        return self.__control_panel


class StartStopPanel(ttk.LabelFrame):
    def __init__(self, text): 
        ttk.LabelFrame.__init__(self, root=None, text=text)
        self.__start_stop_button = ttk.Button(self, text="Stop")
        self.__next_button = ttk.Button(self, text="Next Step", state="disabled")
        self.__start_stop_button.pack()
        self.__next_button.pack()
        
    @property
    def start_stop_button(self):
        return self.__start_stop_button
    
    @property
    def next_button(self):
        return self.__next_button


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
        self.__param_selected = tk.StringVar()
        self.__param_selected.set("Votre scénario")
        self.__options_list = Utils.readfile("scenarios.txt")
        self.__combobox = ttk.Combobox(self, values=self.__options_list, textvariable=self.__param_selected, cursor="hand2", style="TCombobox",state="readonly")
    
        self.__combobox.pack()

        # self.__combobox.bind("<<ComboboxSelected>>", self.param_changed)

        # self__test_btn = ttk.Button(self, text="Test")
        # self__test_btn.pack()
        
    @property
    def param_selected(self):
        return self.__param_selected.get()
        
    @property
    def combobox(self):
        return self.__combobox


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
    def __init__(self, target_entity:Entity=None, attraction_repulsion_force:Vect2D=None, distance_to_target:Vect2D=None):
        self.__attraction_repulsion_force = attraction_repulsion_force
        self.__distance_to_target = distance_to_target
        self.__resulting_direction = None
        self.__target_entity = target_entity

    @abstractmethod    
    def behave(self, origin_entity:Entity):
        pass  
    
    @property
    def attraction_repulsion_force(self):
        return self.__attraction_repulsion_force

    @property
    def target_entity(self):
        return self.__target_entity
    
class CollisionAvoidance(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, origin_entity: Entity, target_entity: Entity):
        return super().behave(origin_entity, target_entity)
  

class Seek(SteeringBehavior):
    def __init__(self, target_entity:Entity=None, attraction_repulsion_force=1, distance_to_target=None):
        SteeringBehavior.__init__(self, target_entity, attraction_repulsion_force, distance_to_target)
      
        
    def behave(self, origin_entity: Entity, target_entity: Entity | Vect2D) -> Vect2D:
        if target_entity is not None:
            if isinstance(target_entity, Entity):
                desired_speed = (target_entity.position - origin_entity.position).normalized * origin_entity.max_speed
                return desired_speed - origin_entity.speed
            else:
                desired_speed = (target_entity - origin_entity.position).normalized * origin_entity.max_speed
                return desired_speed - origin_entity.speed
            
  
class Wander(Seek):
    def __init__(self, target_entity:Entity=None, radius:float=100, circle_distance:float=100, is_in:bool=False):
        super().__init__()
        """radius will increase the turning distance
        circle_distance will increase the distance before turning
        """        
        self.__circle_distance = circle_distance
        self.__radius = radius
        self.__is_in = is_in
        self.__circle_center = None
        self.__target = None
   
   
    def behave(self, origin_entity: Entity, target_entity: Entity=None)->Vect2D:     
        """Retruns a vector that points in a random direction

        Args:
            origin_entity (Entity): the sprite that is wandering
            target_entity (Entity, optional): Must stay None. Defaults to None.

        Returns:
            Vect2D: displacement vector
        """        
         
        circle_center_sprite_relative = origin_entity.speed.normalized * self.__circle_distance
        self.__circle_center = origin_entity.position + circle_center_sprite_relative
        displacement = Vect2D.from_random_normalized()
        
        if self.__is_in:
            displacement *= random.random() * self.__radius
        else:
            displacement *= self.__radius
            
        self.__target = self.__circle_center + displacement
        
        return super().behave(origin_entity, self.__target)
        
        
    def draw(self, draw):
        draw.ellipse([self.__circle_center.x - self.radius, self.__circle_center.y - self.radius, self.__circle_center.x + self.radius, self.__circle_center.y  + self.radius], outline="cyan")
        draw.ellipse([self.__target.x - 5, self.__target.y - 5, self.__target.x + 5, self.__target.y + 5], fill="cyan")
        
        
        
    @property
    def circle_distance(self):
        return self.__circle_distance
    
    @property
    def radius(self):
        return self.__radius
        
class PseudoWander(SteeringBehavior):
    def __init__(self, radius:float=100, circle_distance:float=100, angle_change:float=0.5):
        super().__init__()
        """radius will increase the turning distance
        circle_distance will increase the distance before turning
        angle_change will increase the turning rate
        """        
        self.__circle_distance = circle_distance
        self.__radius = radius
        self.__angle_change = angle_change
        self.__on_or_in = False
        self.__wander_angle = random.random() * 2 * math.pi
        
    def setAngle(self, vector:Vect2D, angle:float)->Vect2D:
        length = vector.length
        vector.x = math.cos(angle) * length
        vector.y = math.sin(angle) * length
        return vector
        
    def behave(self, origin_entity: Entity, target_entity: Entity=None)->Vect2D:     
        """Retruns a vector that points in a random direction

        Args:
            origin_entity (Entity): the sprite that is wandering
            target_entity (Entity, optional): Must stay None. Defaults to None.

        Returns:
            Vect2D: displacement vector
        """        
         
        circle_center = origin_entity.speed.copy()
        circle_center.normalize()
        circle_center *= self.__circle_distance
        
        displacement = Vect2D.from_random_normalized()
        displacement *= self.__radius
        
        self.setAngle(displacement, self.__wander_angle)
        
        self.__wander_angle += (random.random() * self.__angle_change) - (self.__angle_change * .5)
        
        desired_speed = circle_center + displacement
        
        return desired_speed - origin_entity.speed
        
        
class Flee(Seek):
    def __init__(self, target_entity:Entity=None):
        super().__init__(target_entity)
        
    def behave(self, origin_entity: Entity, target_entity: Vect2D )-> Vect2D:
        return super().behave(origin_entity, target_entity) * -1   
    
class Pursuit(SteeringBehavior):
    def __init__(self, target_entity:Entity=None, ratio:int = 1):
        super().__init__(target_entity)
        self.__ratio = ratio
        
    def behave(self, origin_entity: Entity) -> Vect2D:
        if self.target_entity is not None:
            estimated_position = self.target_entity.position + self.target_entity.speed  * self.__ratio 
            desired_speed = (estimated_position - origin_entity.position).normalized * origin_entity.max_speed
            return desired_speed - origin_entity.speed
        
            
class BorderRepulsion(SteeringBehavior):
    def __init__(self, target_entity:Entity=None, attraction_repulsion_force=1, sim_dim:Vect2D=None):       
        SteeringBehavior.__init__(self, target_entity, attraction_repulsion_force=attraction_repulsion_force)
        self.__sim_dim = sim_dim

    def behave(self, origin_entity:Entity):
        force = self.attraction_repulsion_force

        distance_from_left = origin_entity.position.x - origin_entity.width / 2
        distance_from_right = self.__sim_dim.x - origin_entity.position.x - origin_entity.width / 2
        distance_from_top = origin_entity.position.y - origin_entity.height / 2
        distance_from_bottom = self.__sim_dim.y - origin_entity.position.y - origin_entity.height / 2

        repulsive_force_left = round((Vect2D(force, 0))/(distance_from_left) ** 2, 0) if distance_from_left > 0 else Vect2D(force, 0)
        repulsive_force_right = round((Vect2D(-force, 0))/(distance_from_right) ** 2, 0) if distance_from_right > 0 else Vect2D(-force, 0)
        repulsive_force_top = round((Vect2D(0, force))/(distance_from_top) ** 2, 2) if distance_from_top > 0 else Vect2D(0, force)
        repulsive_force_bottom = round((Vect2D(0, -force))/(distance_from_bottom) ** 2, 0) if distance_from_bottom > 0 else Vect2D(0, -force)
        return repulsive_force_left + repulsive_force_right + repulsive_force_top + repulsive_force_bottom


                     
class Evade(Pursuit):
    def __init__(self):
        super().__init__()
        
    def behave(self, origin_entity: Entity, target_entity: Vect2D)-> Vect2D:
        return super().behave(origin_entity, target_entity) * -1   
    
            

           
class Piloted():
    def __init__(self, max_steering_force:int, slowing_distance:int, steering_force:Vect2D, steering_behaviors:list[SteeringBehavior]):
        self.__max_steering_force = max_steering_force
        self.__slowing_distance = slowing_distance
        self.steering_force = steering_force
        self.__steering_behaviors = steering_behaviors

    def steer(self):
        if self.__steering_behaviors is not None:
            for steering_behavior in self.__steering_behaviors:
                    self.steering_force += steering_behavior.behave(origin_entity=self)
            
        self.steering_force.set_polar(length= Utils.clamp_max(self.steering_force.length, self.__max_steering_force), orientation=self.steering_force.orientation)
        
    
    @property
    def steering_force(self):
        return self.__steering_force
    
    @property
    def steering_behaviors(self):
        return self.__steering_behaviors

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
        
    def draw(self, draw):
        Circle.draw(self, draw)
        draw.line([self.position.x, self.position.y, abs(self.speed.x + self.position.x), abs(self.speed.y + self.position.y)], fill="red", width=5)
        draw.line([self.position.x, self.position.y, abs(self.steering_force.x * 5 + self.position.x), abs(self.steering_force.y * 5 + self.position.y)], fill="green", width=5)
        
        for steering_behavior in self.steering_behaviors:
            if isinstance(steering_behavior, Wander):
                steering_behavior.draw(draw)

        pass

    def move(self, time):
        Movable.move(self, time)

    def bounce(self, sim_dim):
        Touchable.bounce(self, sim_dim)

    def tick(self, time):
        self.steer()
        self.move(time)
        # self.bounce(sim_dim)
    
def main():
    App()

if __name__ == '__main__':
    main()