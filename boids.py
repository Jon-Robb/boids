import random
from abc import abstractmethod
import tkinter as tk
# from this import d
from tkinter import Tk, ttk
from turtle import position
from PIL import Image, ImageDraw, ImageTk
from vect2d import Vect2D
import math

#  __    __  .___________. __   __       __  .___________. __   _______     _______.
# |  |  |  | |           ||  | |  |     |  | |           ||  | |   ____|   /       |
# |  |  |  | `---|  |----`|  | |  |     |  | `---|  |----`|  | |  |__     |   (----`
# |  |  |  |     |  |     |  | |  |     |  |     |  |     |  | |   __|     \   \    
# |  `--'  |     |  |     |  | |  `----.|  |     |  |     |  | |  |____.----)   |   
#  \______/      |__|     |__| |_______||__|     |__|     |__| |_______|_______/    


                                                                                                                                                   
class Utils():
    """
    This class contains two static methods. One is used to clamp a value between a min and max value and
    one  is used to reads a file and returns a list of strings to populate the scenario combobox.
    """          

    def clamp_max(value, max):
        return min(value, max)
    
    def readfile(filename:str)->list:
        data = []
        with open(filename, 'r') as file:
            for line in file:
                data.append(line)
        return data

class RGBAColor():


    """
    This class is used to create a color object that can be used to draw shapes on the image.
    It can be used to create a random color or a specific color. To create a random color, use the
    randomize_color() method. To create a specific color, use the RGBAColor(r, g, b, a) constructor.
    """


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
    
    @rgba.setter
    def rgba(self, rgba):
        self.r = rgba[0]
        self.g = rgba[1]
        self.b = rgba[2]
        self.a = rgba[3]

        
    def randomize_color(self):
        self.__r = random.randint(0, 255)
        self.__g = random.randint(0, 255)
        self.__b = random.randint(0, 255)
        self.__a = random.randint(0, 255)
    """randomize_color() returns None and randomizes the color values of the object."""
#      _______.___________. _______  _______ .______       __  .__   __.   _______    .______    _______  __    __       ___   ____    ____  __    ______   .______          _______.
#     /       |           ||   ____||   ____||   _  \     |  | |  \ |  |  /  _____|   |   _  \  |   ____||  |  |  |     /   \  \   \  /   / |  |  /  __  \  |   _  \        /       |
#    |   (----`---|  |----`|  |__   |  |__   |  |_)  |    |  | |   \|  | |  |  __     |  |_)  | |  |__   |  |__|  |    /  ^  \  \   \/   /  |  | |  |  |  | |  |_)  |      |   (----`
#     \   \       |  |     |   __|  |   __|  |      /     |  | |  . `  | |  | |_ |    |   _  <  |   __|  |   __   |   /  /_\  \  \      /   |  | |  |  |  | |      /        \   \    
# .----)   |      |  |     |  |____ |  |____ |  |\  \----.|  | |  |\   | |  |__| |    |  |_)  | |  |____ |  |  |  |  /  _____  \  \    /    |  | |  `--'  | |  |\  \----.----)   |   
# |_______/       |__|     |_______||_______|| _| `._____||__| |__| \__|  \______|    |______/  |_______||__|  |__| /__/     \__\  \__/     |__|  \______/  | _| `._____|_______/    
                                                                                                                                                                                   
class SteeringBehavior():
    """
    This class is used to create a steering behavior object that can be used to steer an entity.
    It is an abstract class. It contains a abstract method called behave() that is used to steer an entity (dynamicCircles).
    """
    def __init__(self, target_entities:type['Entity']=None, attraction_repulsion_force:Vect2D=None, distance_to_target:Vect2D=None):
        self.__attraction_repulsion_force = attraction_repulsion_force
        self.__distance_to_target = distance_to_target
        self.__resulting_direction = Vect2D(0, 0)
        self.__target_entities = [] if target_entities is None else target_entities

    @abstractmethod    
    def behave(self, origin_entity:type['Entity']):
        pass  
    
    @property
    def attraction_repulsion_force(self):
        return self.__attraction_repulsion_force
    
    @property
    def resulting_direction(self):
        return self.__resulting_direction
    
    @resulting_direction.setter
    def resulting_direction(self, resulting_direction):
        self.__resulting_direction = resulting_direction

    @property
    def target_entities(self):
        return self.__target_entities
    
    @target_entities.setter
    def target_entities(self, target_entities):
        self.__target_entities = target_entities
        
    def add_target_entity(self, target_entity):
        self.__target_entities.append(target_entity)
        
    def remove_target_entity(self, target_entity):
        self.__target_entities.remove(target_entity)
    
class Seek(SteeringBehavior):
    """
    This class is used to create a seek steering behavior object.
    It is a child class of the SteeringBehavior class.
    """

    def __init__(self, target_entities:type['Entity']=None, attraction_repulsion_force=1, distance_to_target=None):
        SteeringBehavior.__init__(self, target_entities, attraction_repulsion_force, distance_to_target)

    def behave(self, origin_entity: type['Entity']):
        sum_of_forces = Vect2D(0, 0)
        for target_entity in self.target_entities:
            if target_entity is not None:
                if isinstance(target_entity, Entity):
                    desired_speed = (target_entity.position - origin_entity.position).normalized * origin_entity.max_speed
                    sum_of_forces += desired_speed - origin_entity.speed * self.attraction_repulsion_force
                elif isinstance(target_entity, Vect2D) and (target_entity.x != -1 and target_entity.y != -1):
                    desired_speed = (target_entity - origin_entity.position).normalized * origin_entity.max_speed
                    sum_of_forces += (desired_speed - origin_entity.speed) * self.attraction_repulsion_force
        return sum_of_forces
     
            
class Wander(Seek):
    def __init__(self, radius:float=50, circle_distance:float=100, is_in:bool=True, attraction_repulsion_force=1):
        super().__init__(attraction_repulsion_force=attraction_repulsion_force)
        '''radius will increase the turning distance
        circle_distance will increase the distance before turning
        '''        
        self.__circle_distance = circle_distance
        self.__radius = radius
        self.__is_in = is_in
        self.__circle_center = None
   
   
    def behave(self, origin_entity: type['Entity'])->Vect2D:     
        '''Returns a vector that points in a random direction

        Args:
            origin_entity (Entity): the sprite that is wandering

        Returns:
            Vect2D: displacement vector
        '''        
         
        circle_center_sprite_relative = origin_entity.speed.normalized * self.__circle_distance
        self.__circle_center = origin_entity.position + circle_center_sprite_relative
        displacement = Vect2D.from_random_normalized()
        
        if self.__is_in:
            displacement *= random.random() * self.__radius
        else:
            displacement *= self.__radius
        
        #not sure if this is correct
        self.target_entities = []
        self.target_entities.append(self.__circle_center + displacement)
        
        return super().behave(origin_entity)
        
    def draw(self, draw):
        for target_entity in self.target_entities:
            draw.ellipse([self.__circle_center.x - self.radius, self.__circle_center.y - self.radius, self.__circle_center.x + self.radius, self.__circle_center.y  + self.radius], outline="blue")
            draw.ellipse([target_entity.x - 5, target_entity.y - 5, target_entity.x + 5, target_entity.y + 5], fill="cyan")
        
    @property
    def circle_distance(self):
        return self.__circle_distance
    
    @property
    def radius(self):
        return self.__radius
        
class PseudoWander(SteeringBehavior):
    def __init__(self, radius:float=100, circle_distance:float=100, angle_change:float=0.5):
        super().__init__()
        '''radius will increase the turning distance
        circle_distance will increase the distance before turning
        angle_change will increase the turning rate
        '''        
        self.__circle_distance = circle_distance
        self.__radius = radius
        self.__angle_change = angle_change
        self.__on_or_in = False
        self.__wander_angle = random.random() * 2 * math.pi
        
    def set_angle(self, vector:Vect2D, angle:float)->Vect2D:
        length = vector.length
        vector.x = math.cos(angle) * length
        vector.y = math.sin(angle) * length
        return vector
        
    def behave(self, origin_entity: type['Entity'])->Vect2D:     
        '''Retruns a vector that points in a random direction

        Args:
            origin_entity (Entity): the sprite that is wandering

        Returns:
            Vect2D: displacement vector
        '''        
         
        circle_center = origin_entity.speed.copy()
        circle_center.normalize()
        circle_center *= self.__circle_distance
        
        displacement = Vect2D.from_random_normalized()
        displacement *= self.__radius
        
        self.set_angle(displacement, self.__wander_angle)
        
        self.__wander_angle += (random.random() * self.__angle_change) - (self.__angle_change * .5)
        
        desired_speed = circle_center + displacement
        
        return desired_speed - origin_entity.speed
            
class Flee(Seek):
    def __init__(self, target_entities:type['Entity']=None, attraction_repulsion_force:int= 1):
        super().__init__(target_entities, attraction_repulsion_force)
        
    def behave(self, origin_entity: type['Entity'])-> Vect2D:
        return super().behave(origin_entity) * -1
    
class Pursuit(SteeringBehavior):
    def __init__(self, target_entities:type['Entity']=None, ratio:int = 1, attraction_repulsion_force:int=1):
        super().__init__(target_entities, attraction_repulsion_force=attraction_repulsion_force)
        self.__ratio = ratio
        
    def behave(self, origin_entity: type['Entity']) -> Vect2D:
        sum_of_forces = Vect2D(0, 0)
        for target_entity in self.target_entities:
            if target_entity is not None:
                estimated_position = target_entity.position + target_entity.speed  * self.__ratio 
                desired_speed = (estimated_position - origin_entity.position).normalized * origin_entity.max_speed
                sum_of_forces += (desired_speed - origin_entity.speed) * self.attraction_repulsion_force
        return sum_of_forces
            
class BorderRepulsion(SteeringBehavior): 

    def __init__(self, attraction_repulsion_force=50000, sim_dim:Vect2D=None):       
        SteeringBehavior.__init__(self, attraction_repulsion_force=attraction_repulsion_force)
        self.__sim_dim = sim_dim

    def behave(self, origin_entity:type['Entity']):
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
  
  
class EntityRepulsion(SteeringBehavior):
    def __init__(self, target_entities:list[type['Entity']|type['Vect2D']], attraction_repulsion_force=50):
        SteeringBehavior.__init__(self, attraction_repulsion_force=attraction_repulsion_force)
    
        self.__target_entities = target_entities
    def behave(self, origin_entity:type['Entity']):
        force = self.attraction_repulsion_force
        for target_entity in self.__target_entities:
            if target_entity is not origin_entity:
                if isinstance(target_entity, Entity):
                    orientation = (origin_entity.position - target_entity.position).normalized
                    distance = (origin_entity.position - target_entity.position).length - origin_entity.radius - target_entity.radius
                elif isinstance(target_entity, Vect2D):
                    orientation = (origin_entity.position - target_entity).normalized
                    distance = (origin_entity.position - target_entity).length - origin_entity.radius
                
                self.resulting_direction += orientation/distance ** 2 * force
                
        return self.resulting_direction
                    
class Evade(Pursuit):
    def __init__(self, target_entity:type['Entity']=None, ratio:int = 1, attraction_repulsion_force:int=1):
        super().__init__(target_entity, ratio, attraction_repulsion_force)
        
    def behave(self, origin_entity: type['Entity'])-> Vect2D:
        return super().behave(origin_entity) * - 1   
            
class Cohesion(SteeringBehavior):
    def __init__(self, target_entities:list[type['Entity']|type['Vect2D']], attraction_repulsion_force=5):
        super().__init__(target_entities, attraction_repulsion_force)

    def behave(self, origin_entity: type['Entity']):
        center_of_gravity = Vect2D()
        sum_of_positions = Vect2D()
        sum_of_forces = Vect2D()
        for target_entity in self.target_entities:
            if target_entity is not None:
                if isinstance(target_entity, Entity):
                    sum_of_positions.set(sum_of_positions.x + target_entity.position.x, sum_of_positions.y + target_entity.position.y)
        center_of_gravity.set(sum_of_positions.x / len(self.target_entities), sum_of_positions.y / len(self.target_entities)) 
        desired_speed = (center_of_gravity - origin_entity.position).normalized * origin_entity.max_speed
        sum_of_forces += desired_speed - origin_entity.speed * self.attraction_repulsion_force
        return sum_of_forces
    

class Separation(SteeringBehavior):
    def __init__(self, target_entities:list[type['Entity']|type['Vect2D']], attraction_repulsion_force=50):
        super().__init__(target_entities, attraction_repulsion_force)
        
        def behave(self, origin_entity: type['Entity']):
            sum_of_forces = Vect2D()
            for target_entity in self.target_entities:
                if target_entity is not None:
                    if isinstance(target_entity, Entity):
                        behavior = EntityRepulsion(target_entity, self.attraction_repulsion_force)
                        sum_of_forces += behavior.behave(origin_entity)
            return sum_of_forces

# #  __  .__   __. .___________. _______ .______       _______    ___       ______  _______     _______.
# |  | |  \ |  | |           ||   ____||   _  \     |   ____|  /   \     /      ||   ____|   /       |
# |  | |   \|  | `---|  |----`|  |__   |  |_)  |    |  |__    /  ^  \   |  ,----'|  |__     |   (----`
# |  | |  . `  |     |  |     |   __|  |      /     |   __|  /  /_\  \  |  |     |   __|     \   \    
# |  | |  |\   |     |  |     |  |____ |  |\  \----.|  |    /  _____  \ |  `----.|  |____.----)   |   
# |__| |__| \__|     |__|     |_______|| _| `._____||__|   /__/     \__\ \______||_______|_______/   
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

    @fill_color.setter
    def fill_color(self, fill_color):
        self.__fill_color = fill_color

class Movable():
    def __init__(self, acceleration, max_speed, speed):
        self.__acceleration = acceleration
        self.__speed = speed
        self.__max_speed = max_speed


    def move(self, time):
        self.position.set(self.position.x + self.speed.x * time + self.acceleration.x * 0.5 ** 2 * time, self.position.y + self.speed.y * time + self.acceleration.y * 0.5 ** 2 * time)
        self.speed.set(self.speed.x + self.steering_force.x, self.speed.y + self.steering_force.y)
        
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
        
class Piloted():
    def __init__(self, max_steering_force:int, slowing_distance:int, steering_force:Vect2D, steering_behaviors:list[SteeringBehavior]):
        self.__max_steering_force = max_steering_force
        self.__slowing_distance = slowing_distance
        self.steering_force = steering_force
        self.__steering_behaviors = steering_behaviors

    def steer(self):
        if self.__steering_behaviors is not None:
            for steering_behavior in self.__steering_behaviors:
                self.steering_force.set(self.steering_force.x + steering_behavior.behave(origin_entity=self).x, self.steering_force.y + steering_behavior.behave(origin_entity=self).y)
        self.steering_force.set_polar(length= Utils.clamp_max(self.steering_force.length, self.__max_steering_force), orientation=self.steering_force.orientation)
        
    
    @property
    def max_steering_force(self):
        return self.__max_steering_force

    @property
    def steering_force(self):
        return self.__steering_force
    
    @property
    def steering_behaviors(self):
        return self.__steering_behaviors

    @steering_force.setter
    def steering_force(self, steering_force):
        self.__steering_force = steering_force
         
class Updatable():
    def __init__(self):
        pass

    @abstractmethod
    def tick(self):
        pass


#   ______   ______   .___  ___. .______     ______   .__   __.  _______ .__   __. .___________.    _______.
#  /      | /  __  \  |   \/   | |   _  \   /  __  \  |  \ |  | |   ____||  \ |  | |           |   /       |
# |  ,----'|  |  |  | |  \  /  | |  |_)  | |  |  |  | |   \|  | |  |__   |   \|  | `---|  |----`  |   (----`
# |  |     |  |  |  | |  |\/|  | |   ___/  |  |  |  | |  . `  | |   __|  |  . `  |     |  |        \   \    
# |  `----.|  `--'  | |  |  |  | |  |      |  `--'  | |  |\   | |  |____ |  |\   |     |  |    .----)   |   
#  \______| \______/  |__|  |__| | _|       \______/  |__| \__| |_______||__| \__|     |__|    |_______/    
                                                                                                          
class Brain():
    def __init__(self, owner, environment, behavior_patterns=None):
        self.__owner = owner
        self.__environment = environment

        if behavior_patterns is None:
            self.__behavior_patterns = {    "DynamicCircle": { "Behavior": Evade, "Target_type" : "single" }, 
                                            "SentientCircle": { "Behavior": Separation, "Target_type" : "single" },
                                            "Unknown": { "Behavior": Evade, "Target_type" : "single" },
                                            "No_target": { "Behavior": Wander, "Target_type" : "none" }
                                        }
            self.__permanent_patterns = [BorderRepulsion(sim_dim=environment.size)]
        else: self.__behavior_patterns = behavior_patterns

        self.__seen_entities = []
        self.__active_behaviors = self.__permanent_patterns

    def process(self):
        self.__seen_entities = []
        self.__active_behaviors = []
        self.__active_behaviors.extend(self.__permanent_patterns)
        for eye in self.__owner.eyes:
            self.__seen_entities = eye.look(self.__environment)

        if self.__seen_entities:
            for key in self.__behavior_patterns:
                values = self.__behavior_patterns[key]
                if values["Target_type"] == "single":
                    for seen_entity in self.__seen_entities:
                        if self.__behavior_patterns[seen_entity.__class__.__name__] == key:
                            behavior = self.__behavior_patterns[seen_entity.__class__.__name__]["Behavior"]
                            self.__active_behaviors.append(behavior([seen_entity]))
                elif values["Target_type"] == "group":
                    target_group = []
                    behavior = values["Behavior"]
                    for seen_entity in self.__seen_entities:
                        if seen_entity.__class__.__name__ == key:
                            target_group.append(seen_entity)
                    if target_group:
                        self.__active_behaviors.append(behavior(target_group))
        else: 
            behavior = self.__behavior_patterns["No_target"]["Behavior"]
            self.__active_behaviors.append(behavior())
        self.behave()

    def draw_line_to_seen_entities(self, draw):
        halo_radius = self.__owner.radius * 1.25
        for seen_entity in self.__seen_entities:
            draw.ellipse([self.__owner.position.x - halo_radius, self.__owner.position.y -  halo_radius, self.__owner.position.x +  halo_radius, self.__owner.position.y +  halo_radius], fill="cyan")
            draw.line([self.__owner.position.x, self.__owner.position.y, seen_entity.position.x, seen_entity.position.y], fill="cyan", width=5)
            
    def behave(self):
        for behavior in self.__active_behaviors:
                self.__owner.steering_force.set(self.__owner.steering_force.x + behavior.behave(origin_entity=self.__owner).x, self.__owner.steering_force.y + behavior.behave(origin_entity=self.__owner).y)

        self.__owner.steering_force.set_polar(length= Utils.clamp_max(self.__owner.steering_force.length, self.__owner.max_steering_force), orientation=self.__owner.steering_force.orientation)     


    @property
    def active_behaviors(self):
        return self.__active_behaviors
class Eye(Drawable):
    def __init__(self, owner:type['Entity'], fov:float=45, range:float=150, vector:Vect2D=None):
        self.__owner = owner
        Drawable.__init__(self, border_color=RGBAColor(), border_width=1, fill_color=None, position=self.__owner.position, size=Vect2D(range, range))
        self.__fov = fov
        self.__range = range
        if vector is None:
            self.__vector = owner.speed

    def look(self, simulation):
        seen_sprites = []
        for sprite in simulation.sprites:
            if sprite is not self.__owner and self.sees(sprite):
                seen_sprites.append(sprite)
        return seen_sprites

    def is_in_range(self, target:Vect2D)->bool:
        test= self.__owner.position.distance_from(target.position) - target.radius
        return self.__owner.position.distance_from(target.position) - target.radius <= self.__range

    def is_in_fov(self, target:Vect2D)->bool:
        distance_to_target = target.position - self.__owner.position
        if distance_to_target.is_defined:
            return self.__vector.angle_between_degrees(distance_to_target) <= self.__fov
        else:
            return False
        
    def sees(self, target:type['Entity'])->bool:
        return self.is_in_range(target) and self.is_in_fov(target)

    def draw(self, draw):
        
        draw.pieslice(
                [self.__owner.position.x - self.__range,
                self.__owner.position.y - self.__range,
                self.__owner.position.x + self.__range,
                self.__owner.position.y + self.__range],
                start=self.__vector.orientation_degrees - self.__fov,
                end=self.__vector.orientation_degrees + self.__fov,
                width=self.border_width,
                outline=self.border_color)
       

    @property
    def fov(self):
        return self.__fov

    @property
    def range(self):
        return self.__range

    @property
    def position(self):
        return self.__position

    @property
    def orientation(self):
        return self.__orientation

    @fov.setter
    def fov(self, fov):
        self.__fov = fov

    @range.setter
    def range(self, range):
        self.__range = range

    @position.setter
    def position(self, position):
        self.__position = position

    @orientation.setter
    def orientation(self, orientation):
            self.__orientation = orientation

# .___  ___.   ______    _______   _______  __      
# |   \/   |  /  __  \  |       \ |   ____||  |     
# |  \  /  | |  |  |  | |  .--.  ||  |__   |  |     
# |  |\/|  | |  |  |  | |  |  |  ||   __|  |  |     
# |  |  |  | |  `--'  | |  '--'  ||  |____ |  `----.
# |__|  |__|  \______/  |_______/ |_______||_______|  
class Entity(Drawable, Updatable):
    def __init__(self, border_color, border_width, fill_color, position, size):
        Drawable.__init__(self, border_color, border_width, fill_color, position, size)
        Updatable.__init__(self)
        
        self.available_names = ["William", "Logan", "Liam", "Noah", "Jacob", "Thomas", 
                                "Raphael", "Nathan", "Leo", "Alexis", "Emile", "Edouard",
                                "Felix", "Samuel", "Olivier", "Gabriel", "Charles", "Antoine",
                                "Adam", "Victor", "Benjamin", "Elliot", "Jayden", "Arthur",
                                "James", "Louis", "Theo", "Xavier", "Zack", "Arnaud",
                                "Lucas", "Ethan", "Nolan", "Henri", "Loic", "Milan", "Mathis",
                                "Zachary", "Dylan", "Alexandre", "Tristan", "Laurent", "Eli",
                                "Mayson", "Justin", "Anthony", "Ryan", "Isaac", "Jules", "Jackson",
                                "Eliott", "Evan", "Leonard", "Philippe", "Caleb", "Nicolas",
                                "Damien", "Jake", "Theodore", "Eliot", "Eloi", "Ludovic",
                                "Malik", "Matheo", "Louka", "Alex", "Hayden", "Zackary",
                                "Hugo", "Rafael", "Matteo", "David", "Hubert", "Derek",
                                "Etienne", "Vincent", "Rayan", "Axel", "Leon", "Tyler",
                                "Mathias", "Albert", "Maxime", "Enzo", "Jordan", "Julien",
                                "Simon", "Loik", "Michael", "Ayden", "Daniel", "Tom", "Jack",
                                "Joshua", "Maverick", "Adrien", "Lyam", "Mateo", "Remi", "Elias",
                                "Gertrude", "Denis", "Donald", "Jonathan", "Andrejz"]
        
        #get a random name from the list
        self.__name = random.choice(self.available_names)

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def tick(self):
        pass
    
    @property
    def name(self):
        return self.__name
     
class Circle(Entity):
    def __init__(self, border_color, border_width, fill_color, position:Vect2D, radius:int):
        Entity.__init__(self, border_color=border_color, border_width=border_width, fill_color=fill_color, position=position, size=Vect2D(radius*2, radius*2))
        self.__fill_color = fill_color
        self.__border_color = border_color
        self.__radius = radius

    
    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, radius):
        self.__radius = radius

    def draw(self, draw):
        self.fill_color
        draw.ellipse(
                [self.position.x - self.__radius,
                self.position.y - self.__radius,
                self.position.x + self.__radius,
                self.position.y + self.__radius],
                fill=self.fill_color,
                width=self.border_width,
                outline=self.border_color)

    @abstractmethod
    def tick(self, time):
        pass
    
class DynamicCircle(Circle, Movable, Piloted):
    def __init__(   self,
                    border_color=RGBAColor(randomize=True),
                    border_width=5,
                    fill_color=RGBAColor(randomize=True),
                    position=Vect2D(random.randrange(0,1000),random.randrange(0,500)),
                    radius=random.randint(10, 50),
                    acceleration=Vect2D(0,0),
                    speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)),
                    max_speed= 100,
                    max_steering_force=5,
                    slowing_distance=10,
                    steering_force=Vect2D(0,0),
                    steering_behaviors=None,
                ):
    
        Circle.__init__(self, border_color, border_width, fill_color, position, radius)
        Movable.__init__(self, acceleration, max_speed, speed)
        Piloted.__init__(self, max_steering_force, slowing_distance, steering_force, steering_behaviors)
        
    def draw(self, draw):
        Circle.draw(self, draw)
        # draw.line([self.position.x, self.position.y, abs(self.speed.x + self.position.x), abs(self.speed.y + self.position.y)], fill="red", width=5)
        # draw.line([self.position.x, self.position.y, abs(self.steering_force.x * 5 + self.position.x), abs(self.steering_force.y * 5 + self.position.y)], fill="green", width=5)
        
        # for steering_behavior in self.steering_behaviors:
        #     # if isinstance(steering_behavior, Wander):
        #     if hasattr(steering_behavior, "draw"):
        #         steering_behavior.draw(draw)

    def draw_circle_speed(self, draw):
        draw.line([self.position.x, self.position.y, self.position.x + self.speed.x, self.position.y + self.speed.y], fill="red", width=5)
        # draw.line([self.position.x, self.position.y, abs(self.speed.x + self.position.x), abs(self.speed.y + self.position.y)], fill="red", width=5)
        
    def draw_circle_steering_force(self, draw):
        draw.line([self.position.x, self.position.y, self.position.x + self.steering_force.x * 10, self.position.y + self.steering_force.y * 10], fill="darkgoldenrod", width=5)
        # draw.line([self.position.x, self.position.y, abs(self.steering_force.x * 10 + self.position.x), abs(self.steering_force.y * 10 + self.position.y)], fill="darkgoldenrod", width=5)
        for steering_behavior in self.steering_behaviors:
            if hasattr(steering_behavior, "draw"):
                    steering_behavior.draw(draw)

    def move(self, time):
        Movable.move(self, time)

    def tick(self, time):
        self.steer()
        self.move(time)

class SentientCircle(DynamicCircle):
    def __init__(self, border_color=RGBAColor(randomize=True), border_width=5, fill_color=RGBAColor(randomize=True), position=Vect2D(random.randrange(0,1000),random.randrange(0,500)), radius=random.randint(10, 50), acceleration=Vect2D(0,0), speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)), max_speed= 100, max_steering_force=5, slowing_distance=10, steering_force=Vect2D(0,0), steering_behaviors=None, fov=math.pi/2, range=100, environment=None):
        DynamicCircle.__init__(self, border_color, border_width, fill_color, position, radius, acceleration, speed, max_speed, max_steering_force, slowing_distance, steering_force, steering_behaviors)

        self.__brain = Brain(self, environment)
        _id = id(self.__brain)
        
        self.__eyes = [Eye(self),]

    def tick(self, time):
        DynamicCircle.tick(self, time)
        self.__brain.process()

    def draw_fov(self, draw):
        for eye in self.__eyes:
            eye.draw(draw)    
        self.__brain.draw_line_to_seen_entities(draw)

    def draw_circle_steering_force(self, draw):
        draw.line([self.position.x, self.position.y, self.position.x + self.steering_force.x * 10, self.position.y + self.steering_force.y * 10], fill="darkgoldenrod", width=5)
        # draw.line([self.position.x, self.position.y, abs(self.steering_force.x * 10 + self.position.x), abs(self.steering_force.y * 10 + self.position.y)], fill="darkgoldenrod", width=5)
        for steering_behavior in self.__brain.active_behaviors:
            if hasattr(steering_behavior, "draw"):
                    steering_behavior.draw(draw)
    @property
    def eyes(self):
        return self.__eyes

class Simulation(Updatable):
    def __init__(self, size=Vect2D(100,100)):

        self.__size = size
        self.__sprites = []
        self.__mouse_pos = Vect2D(-1, -1)
        self.__is_running = True
        self.__seed = 0
        
        self.initialize_scenario()
        
    
    def initialize_scenario(self, key:str="Predator Chasing Prey"): 
        key = key.replace("\n", "")
        nb_balls = 0
                
        match key:
            case 'Seek, Flee or Wander':
                nb_balls = 250
                for i in range(nb_balls):
                    self.__sprites.append(DynamicCircle(    border_color=RGBAColor(randomize=True),
                                                            border_width=5,
                                                            fill_color=RGBAColor(randomize=True),
                                                            position=Vect2D(random.randrange(0,1000),random.randrange(0,500)),
                                                            radius=random.randint(10, 50),
                                                            acceleration=Vect2D(0,0),
                                                            speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)),
                                                            max_speed= 100,
                                                            max_steering_force=5,
                                                            slowing_distance=10,
                                                            steering_force=Vect2D(0,0),
                                                            steering_behaviors=[BorderRepulsion(sim_dim=self.__size)]))

                for sprite in self.__sprites:
                    random_sprite = random.choice(self.__sprites)
                    while random_sprite == sprite:
                        random_sprite = random.choice(self.__sprites)

                    random_steering_behavior = random.choice([Seek([random_sprite]), Flee([random_sprite]), Wander()])
                    sprite.steering_behaviors.append(random_steering_behavior)
                    sprite.fill_color = RGBAColor(0, 128, 0, 255) if type(random_steering_behavior) is Flee else RGBAColor(128, 0, 0, 255) if type(random_steering_behavior) is Seek else RGBAColor(0, 0, 128, 255)

            case 'Seek or Flee Mouse':
                nb_balls = 20
                for i in range(nb_balls):
                    random_steering_behavior = random.choice([Seek([self.__mouse_pos]), Flee([self.__mouse_pos])])

                    self.__sprites.append(DynamicCircle(    border_color=RGBAColor(randomize=True),
                                                            border_width=5,
                                                            fill_color = RGBAColor(0, 128, 0, 255) if type(random_steering_behavior) is Flee else RGBAColor(128, 0, 0, 255) if type(random_steering_behavior) is Seek else RGBAColor(0, 0, 128, 255),
                                                            position=Vect2D(random.randrange(0,1000),random.randrange(0,500)),
                                                            radius=random.randint(10, 50),
                                                            acceleration=Vect2D(0,0),
                                                            speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)),
                                                            max_speed= 100,
                                                            max_steering_force=5,
                                                            slowing_distance=10,
                                                            steering_force=Vect2D(0,0),
                                                            steering_behaviors=[Wander(), random_steering_behavior, BorderRepulsion(sim_dim=self.__size)]))

            case 'Follow the leader':
                nb_balls = 20
                for i in range(nb_balls):
                    self.__sprites.append(DynamicCircle(position=Vect2D(random.randrange(0, int(self.width)),random.randrange(0, int(self.height))),
                                                        speed=Vect2D(random.randrange(-50,50),random.randrange(-50,50)),
                                                        fill_color = RGBAColor(128, 0, 128, 255)  if len(self.__sprites) == nb_balls-1 else RGBAColor(128, 128, 0, 255),
                                                        border_color=RGBAColor(randomize=True),
                                                        border_width=5,
                                                        radius=random.randint(10, 50),
                                                        acceleration=Vect2D(0,0),
                                                        max_speed= 100,
                                                        max_steering_force=5,
                                                        slowing_distance=10,
                                                        steering_force=Vect2D(0,0),
                                                        steering_behaviors=[Wander(), BorderRepulsion(sim_dim=self.__size)] if i == nb_balls-1 else [BorderRepulsion(sim_dim=self.__size)]))

                for i, sprite in enumerate(self.__sprites):
                    if i != len(self.__sprites)-1:
                        sprite.steering_behaviors.append(Pursuit([self.__sprites[i-1]]))
                        sprite.radius = (nb_balls - i - 1) * 2
                    else: sprite.radius = nb_balls * 2
                    
            case 'Cohesion':
                nb_balls = 50
                for i in range(nb_balls):
                                self.__sprites.append(SentientCircle(border_color=RGBAColor(randomize=True),
                                                            border_width=5,
                                                            fill_color=RGBAColor(randomize=True),
                                                            position=Vect2D(random.randrange(0,1000),random.randrange(0,500)),
                                                            radius=random.randint(5, 10),
                                                            acceleration=Vect2D(0,0),
                                                            speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)),
                                                            max_speed= 100,
                                                            max_steering_force=5,
                                                            slowing_distance=10,
                                                            steering_force=Vect2D(0,0),
                                                            #steering_behaviors=[BorderRepulsion(sim_dim=self.__size)], environment=self
                                                            environment=self
                                                            ))
        
            case "Rise of Sentience":
                nb_sentients = 10
                nb_dumbs = 10
                for i in range(nb_sentients):
                    self.__sprites.append(SentientCircle(border_color=RGBAColor(randomize=True),
                            border_width=5,
                            radius=10,
                            fill_color=RGBAColor(randomize=True),
                            position=Vect2D(random.randrange(0,1000),random.randrange(0,500)),
                            acceleration=Vect2D(0,0),
                            speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)),
                            max_speed= 100,
                            max_steering_force=5,
                            slowing_distance=10,
                            steering_force=Vect2D(0,0),
                            environment=self
                            ))

                for i in range(nb_dumbs):
                    self.__sprites.append(DynamicCircle(position=Vect2D(random.randrange(0, int(self.width)),random.randrange(0, int(self.height))),
                                                        speed=Vect2D(random.randrange(-50,50),random.randrange(-50,50)),
                                                        border_color=RGBAColor(randomize=True),
                                                        border_width=5,
                                                        radius=25,
                                                        fill_color= RGBAColor(33,33,33,255),
                                                        acceleration=Vect2D(0,0),
                                                        max_speed= 100,
                                                        max_steering_force=5,
                                                        slowing_distance=10,
                                                        steering_force=Vect2D(0,0),
                                                        steering_behaviors=[Wander(), BorderRepulsion(sim_dim=self.__size)]))


            case 'Predator Chasing Prey': # Default
                nb_balls = 6
                for i in range(nb_balls):
                    self.__sprites.append(DynamicCircle(position=Vect2D(random.randrange(0, int(self.width)),random.randrange(0, int(self.height))),
                                                        speed=Vect2D(random.randrange(-50,50),random.randrange(-50,50)),
                                                        border_color=RGBAColor(randomize=True),
                                                        border_width=5,
                                                        acceleration=Vect2D(0,0),
                                                        max_speed= 100,
                                                        max_steering_force=5,
                                                        slowing_distance=10,
                                                        steering_force=Vect2D(0,0),
                                                        steering_behaviors=[Wander(), BorderRepulsion(sim_dim=self.__size)] if i%2 == 0 else [Pursuit([self.sprites[i-1]]), BorderRepulsion(sim_dim=self.__size)]))

                for i, sprite in enumerate(self.__sprites):
                    sprite.fill_color = RGBAColor(128, 0, 0, 255) if type(sprite.steering_behaviors[0]) is Pursuit else RGBAColor(0, 128, 0, 255)
                    sprite.radius = 60 if type(sprite.steering_behaviors[0]) is Pursuit else 30
                    if i%2 == 0 and i != len(self.__sprites) - 1:
                        self.__sprites[i].steering_behaviors.append(Evade([self.__sprites[i+1]]))


        # self.__sprites.append(SentientCircle(steering_behaviors=[Wander(), BorderRepulsion(sim_dim=self.__size)], environment=self, positsteering_behaviors=ion=Vect2D(random.randrange(0,1000),random.randrange(0,500))))

    def tick(self, time):
        if self.__sprites:
            for sprite in self.__sprites:
                sprite.tick(time)

    def reset(self, key:str="Predator Chasing Prey"):
        self.__is_running = True
        self.__sprites = []
        self.initialize_scenario(key)

    def move_mouse(self, event):
        self.__mouse_pos.set(event.x, event.y)
        
    def mouse_left(self, event):
        self.__mouse_pos.set(-1, -1)
        
        for sprite in self.__sprites:
            sprite.steering_force = Vect2D(0,0)

    def mouse_entered(self, event):
        self.__mouse_pos.set(event.x, event.y)
        
    def toggle_running(self, event):
        self.__is_running = not self.__is_running
        
    def check_entity_clicked(self, event):
        radius_offset = 20
        for sprite in reversed(self.__sprites):
            if sprite.position.x - (sprite.radius + radius_offset) < event.x < sprite.position.x + (sprite.radius + radius_offset) and sprite.position.y - (sprite.radius + radius_offset) < event.y < sprite.position.y + (sprite.radius + radius_offset):
                return sprite

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


#   _______  __    __   __ 
#  /  _____||  |  |  | |  |
# |  |  __  |  |  |  | |  |
# |  | |_ | |  |  |  | |  |
# |  |__| | |  `--'  | |  |
#  \______|  \______/  |__|

class GUI(ttk.Frame, Drawable):
    def __init__(self, border_color=None, border_width=None, fill_color=None, position=None, size:Vect2D=None):
        ttk.Frame.__init__(self, root=None, text=None)
        Drawable.__init__(self, border_color,  border_width, fill_color, position, size)
        self.__main_panel = ControlBar()
        # self.__view_window = ViewWindow(size=Vect2D(size.x * 0.80, size.y * 0.99), fill_color=fill_color)
        self.__view_window = ViewWindow(size=Vect2D(size.x, size.y), fill_color=fill_color)
        self.__main_panel.grid(row=0, column=1)
        self.__view_window.grid(row=0, column=1, rowspan=4, sticky="ns")

    @property
    def main_panel(self):
        return self.__main_panel

    @property
    def view_window(self):
        return self.__view_window  

class ControlBar(ttk.Frame):
    def __init__(self):
        ttk.Frame.__init__(self)
        self.__control_panel = StartStopPanel("Controls")
        self.__param_panel = ParamPanel("Scenarios")
        self.__visual_param_panel = VisualParamPanel("Visual Parameters")
        self.__Info_panel = InfoPanel("Selected Entity Informations")
        self.__control_panel.grid(row=0, column=0, sticky="N")
        self.__param_panel.grid(row=1, column=0, sticky="N")
        self.__visual_param_panel.grid(row=2, column=0, sticky="N")
        self.__Info_panel.grid(row=3, column=0, sticky="N")

    @property
    def param_panel(self):
        return self.__param_panel
    
    @property
    def control_panel(self):
        return self.__control_panel
    
    @property
    def visual_param_panel(self):
        return self.__visual_param_panel
    
    @property
    def info_panel(self):
        return self.__Info_panel

class StartStopPanel(ttk.LabelFrame):
    def __init__(self, text): 
        ttk.LabelFrame.__init__(self, root=None, text=text)
        self.__start_stop_button = ttk.Button(self, text="Stop")
        self.__next_button = ttk.Button(self, text="Next Step", state="disabled")
        self.__reset_button = ttk.Button(self, text="Reset")
        self.__start_stop_button.grid(row=0, column=0)
        self.__next_button.grid(row=1, column=0)
        self.__reset_button.grid(row=2, column=0)
        
    @property
    def start_stop_button(self):
        return self.__start_stop_button
    
    @property
    def next_button(self):
        return self.__next_button
    
    @property
    def reset_button(self):
        return self.__reset_button

class InfoPanel(ttk.LabelFrame):
    def __init__(self, text):
        ttk.LabelFrame.__init__(self, root=None, text=text)
        self.__info_label = tk.Text(self, width=30, height=10)
        self.set_text("Click on a boid to show the infomations about it")
        self.__info_label.grid(row=0, column=0)

    @property
    def info_label(self):
        return self.__info_label
    
    def set_text(self, text):
        self.__info_label.config(state=tk.NORMAL)
        self.__info_label.delete(1.0, tk.END)
        self.__info_label.insert(tk.END, text)
        self.__info_label.config(state=tk.DISABLED)

class ViewWindow(ttk.Label, Drawable):
    def __init__(self, border_color=None, border_width=None, fill_color=None, position=None, size=None):
        ttk.Label.__init__(self, root=None, text=None, width=size.x)
        Drawable.__init__(self, border_color, border_width, fill_color, position, size)
        self.__background = Image.open("tropicalforest.jpg")
        self.sizex = size.x
        self.sizey = size.y
        #self.__canvas = Image.new('RGBA', (int(size.x), int(size.y)), (0, 0, 0))
        self.__resized = self.__background.resize((int(size.x), int(size.y)))
        self.__image_draw = ImageDraw.Draw(self.__resized)
        self.__image_tk = ImageTk.PhotoImage(self.__resized)
        self.__image_label = ttk.Label(self, image=self.__image_tk)
        # self.__ball = DynamicCircle(position=Vect2D(100,100))
        # self.__ball.draw(self.__image_label, self.__canvas, self.__image_draw)
        self.__image_label.grid(row=0, column=0, sticky='ns')
        self.__image_label.columnconfigure(0, minsize=600, weight=1)
        self.__speed_is_drawn = False
        self.__steering_force_is_drawn = False
        self.__circle_is_drawn = True
        self.__fov_is_drawn = False


    def update_view(self, simulation):
            self.__newbackground = Image.open("tropicalforest.jpg")
            i = self.__newbackground.resize((int(self.sizex), int(self.sizey)))
            draw = ImageDraw.Draw(i)
            
            # for sprite in simulation.sprites:
            #     if self.__speed_is_drawn:
            #         sprite.draw_circle_speed(draw)
                    
            #     if self.__steering_force_is_drawn:
            #         sprite.draw_circle_steering_force(draw)
                    
            #     if self.__circle_is_drawn:
            #         sprite.draw(draw)
                    
            #     if self.__fov_is_drawn:
            #         if hasattr(sprite, 'draw_fov'):
            #             sprite.draw_fov(draw)   
            
            if self.__speed_is_drawn and self.__steering_force_is_drawn and self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw)                     
                    sprite.draw(draw)
                    sprite.draw_circle_speed(draw)
                    sprite.draw_circle_steering_force(draw)
                   
            elif self.__speed_is_drawn and self.__steering_force_is_drawn and self.__circle_is_drawn and not self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    sprite.draw(draw)
                    sprite.draw_circle_speed(draw)
                    sprite.draw_circle_steering_force(draw)
            elif self.__speed_is_drawn and self.__steering_force_is_drawn and not self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw)                    
                    sprite.draw_circle_speed(draw)
                    sprite.draw_circle_steering_force(draw)
                    
            elif self.__speed_is_drawn and self.__steering_force_is_drawn and not self.__circle_is_drawn and not self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    sprite.draw_circle_steering_force(draw)
                    sprite.draw_circle_speed(draw)
            elif self.__speed_is_drawn and not self.__steering_force_is_drawn and self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw)                         
                    sprite.draw(draw)
                    sprite.draw_circle_speed(draw)
            elif self.__speed_is_drawn and not self.__steering_force_is_drawn and self.__circle_is_drawn and not self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    sprite.draw(draw)
                    sprite.draw_circle_speed(draw)
            elif self.__speed_is_drawn and not self.__steering_force_is_drawn and not self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw)
                    sprite.draw_circle_speed(draw)
            elif self.__speed_is_drawn and not self.__steering_force_is_drawn and not self.__circle_is_drawn and not self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    sprite.draw_circle_speed(draw)
            elif not self.__speed_is_drawn and self.__steering_force_is_drawn and self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw)
                    sprite.draw(draw)
                    sprite.draw_circle_steering_force(draw)
            elif not self.__speed_is_drawn and self.__steering_force_is_drawn and self.__circle_is_drawn and not self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    sprite.draw(draw)
                    sprite.draw_circle_steering_force(draw)
            elif not self.__speed_is_drawn and self.__steering_force_is_drawn and not self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw)                    
                    sprite.draw_circle_steering_force(draw)
            elif not self.__speed_is_drawn and self.__steering_force_is_drawn and not self.__circle_is_drawn and not self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    sprite.draw_circle_steering_force(draw)
            elif not self.__speed_is_drawn and not self.__steering_force_is_drawn and self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw)
                    sprite.draw(draw)
            elif not self.__speed_is_drawn and not self.__steering_force_is_drawn and self.__circle_is_drawn and not self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    sprite.draw(draw)
            elif not self.__speed_is_drawn and not self.__steering_force_is_drawn and not self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw)                       
        
            self.__image_tk = ImageTk.PhotoImage(i)
            self.__image_label["image"] = self.__image_tk

            # self.tki = ImageTk.PhotoImage(self.__gui.view_window.canvas)
            # self.__gui.view_window.image_label["image"] = self.tki

            # self.after(10, self.tick)  
            
    def toggle_draw_fov(self, event):
        self.__fov_is_drawn = not self.__fov_is_drawn
    
    def toggle_draw_circle(self, event):
        self.__circle_is_drawn = not self.__circle_is_drawn
            
    def toggle_draw_steering_force(self, event):
        self.__steering_force_is_drawn = not self.__steering_force_is_drawn

    def toggle_draw_speed(self, event):
        self.__speed_is_drawn = not self.__speed_is_drawn

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
        self.__param_selected.set("Predator Chasing Prey")
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
        self.__speed_var = tk.IntVar()
        self.__speed_checkbutton = ttk.Checkbutton(self, text="Show Speed", variable=self.__speed_var, onvalue=1, offvalue=0, width=20)
        self.__speed_checkbutton.pack(padx=(50, 0))
        self.__steering_force_var = tk.IntVar()
        self.__steering_force_checkbutton = ttk.Checkbutton(self, text="Show Steers", variable=self.__steering_force_var, onvalue=1, offvalue=0, width=20)
        self.__steering_force_checkbutton.pack(padx=(50, 0))
        self.__show_circle_var = tk.IntVar()
        self.__show_circle_checkbutton = ttk.Checkbutton(self, text="Show Circles", variable=self.__show_circle_var, onvalue=0, offvalue=1, width=20)  
        self.__show_circle_checkbutton.pack(padx=(50, 0))
        self.__show_fov_var = tk.IntVar()
        self.__show_fov_checkbutton = ttk.Checkbutton(self, text="Show F-o-V", variable=self.__show_fov_var, onvalue=1, offvalue=0, width=20)
        self.__show_fov_checkbutton.pack(padx=(50, 0))
        

    @property
    def show_fov_checkbutton(self):
        return self.__show_fov_checkbutton

    @property
    def show_circle_checkbutton(self):
        return self.__show_circle_checkbutton

    @property
    def steering_force_checkbutton(self):
        return self.__steering_force_checkbutton
    
    @property
    def speed_checkbutton(self):
        return self.__speed_checkbutton
    
class SimParamPanel(ParamPanel):
    def __init__(self):
        pass    
    
#  __________   ___  _______   ______  __    __  .___________. __    ______   .__   __.
# |   ____\  \ /  / |   ____| /      ||  |  |  | |           ||  |  /  __  \  |  \ |  |
# |  |__   \  V  /  |  |__   |  ,----'|  |  |  | `---|  |----`|  | |  |  |  | |   \|  |
# |   __|   >   <   |   __|  |  |     |  |  |  |     |  |     |  | |  |  |  | |  . `  |
# |  |____ /  .  \  |  |____ |  `----.|  `--'  |     |  |     |  | |  `--'  | |  |\   |
# |_______/__/ \__\ |_______| \______| \______/      |__|     |__|  \______/  |__| \__|
class App(Tk, Updatable):
    
    def __init__(self):
        Tk.__init__(self)
        self.__size = Vect2D(Tk.winfo_screenwidth(self) * 0.8, Tk.winfo_screenheight(self) * 0.8)
        self.__gui = GUI(size=Vect2D(self.__size.x, self.__size.y), fill_color=RGBAColor(0 ,0, 0)) 
        self.title('Boids')
        self.geometry("{}x{}+{}+{}".format(int(self.width), (int(self.height)), int(Tk.winfo_screenwidth(self) * 0.5 - self.width * 0.5), 0 + int(Tk.winfo_screenwidth(self) * 0.50 - self.height)))
        self.geometry()
        self.iconbitmap('boids.ico')
        self.__simulation = Simulation(size=Vect2D(self.__gui.view_window.width, self.__gui.view_window.height))
        
        self.__info_entity = None
        self.__info_string = ""
        
        self.__gui.main_panel.visual_param_panel.speed_checkbutton.bind('<Button-1>', self.__gui.view_window.toggle_draw_speed)
        self.__gui.main_panel.visual_param_panel.steering_force_checkbutton.bind('<Button-1>', self.__gui.view_window.toggle_draw_steering_force)
        self.__gui.main_panel.visual_param_panel.show_circle_checkbutton.bind('<Button-1>', self.__gui.view_window.toggle_draw_circle)
        self.__gui.main_panel.visual_param_panel.show_fov_checkbutton.bind('<Button-1>', self.__gui.view_window.toggle_draw_fov)
        
        
        self.__gui.view_window.image_label.bind('<Enter>', self.__simulation.mouse_entered)
        self.__gui.view_window.image_label.bind('<Motion>', self.__simulation.move_mouse)
        self.__gui.view_window.image_label.bind('<Leave>', self.__simulation.mouse_left)
        self.__gui.main_panel.control_panel.start_stop_button.bind('<Button-1>', self.toggle_simulation)
        self.__gui.main_panel.control_panel.next_button.bind('<Button-1>', self.tick_simulation)
        self.__gui.main_panel.control_panel.next_button.bind('<space>', self.tick_simulation)
        self.__gui.main_panel.control_panel.reset_button.bind('<Button-1>', self.reset_simulation)
        self.__gui.main_panel.param_panel.combobox.bind('<<ComboboxSelected>>', self.param_changed)
        #bind mouse click to image
        self.__gui.view_window.image_label.bind('<Button-1>', self.mouse_clicked_on_image)

        self.tick()
                
        self.mainloop()

    def param_changed(self, event):
        self.reset_simulation()

    @property
    def size(self):
        return self.__size
    
    def mouse_clicked_on_image(self, event):
        clicked_entity = self.__simulation.check_entity_clicked(event)
        if clicked_entity is not None:
            self.__info_entity = clicked_entity
            self.update_info_panel()
            

    def tick_simulation(self, event=None):
        self.__simulation.tick(time=0.1)
        
    def reset_simulation(self, event=None) -> None:
        key = self.__gui.main_panel.param_panel.param_selected
        self.__gui.main_panel.control_panel.start_stop_button.config(text="Stop")
        self.__gui.main_panel.control_panel.next_button.config(state="disabled")
        self.__simulation.reset(key)


    def update_info_panel(self):
        self.__info_string = ""
        self.__info_string += "Name: " + self.__info_entity.name + "\n"
        self.__info_string += "Position: ({}, {})".format(math.trunc(self.__info_entity.position.x), math.trunc(self.__info_entity.position.y)) + "\n"
        self.__info_string += "Speed: ({}, {})".format(math.trunc(self.__info_entity.speed.x), math.trunc(self.__info_entity.speed.y)) + "\n"
        self.__info_string += "Steering force: ({}, {})".format(math.trunc(self.__info_entity.steering_force.x), math.trunc(self.__info_entity.steering_force.y)) + "\n"
        self.__gui.main_panel.info_panel.set_text(self.__info_string)

    def tick(self):
        if self.__simulation.is_running:
            self.tick_simulation()
            if self.__info_entity is not None:
                self.update_info_panel()
            else:
                self.__gui.main_panel.info_panel.set_text("Click on a boid to show the infomations about it")
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

def main():
    App()

if __name__ == '__main__':
    main()
