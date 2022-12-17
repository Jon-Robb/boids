import random
from abc import abstractmethod
import tkinter as tk
from tkinter import Tk, ttk
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
        """r is a property that returns the red value of the color object."""
        return self.__r
        
    @property
    def g(self):
        """g is a property that returns the green value of the color object."""
        return self.__g
        
    @property
    def b(self):
        """b is a property that returns the blue value of the color object."""
        return self.__b
        
    @property
    def a(self):
        """a is a property that returns the alpha value of the color object."""
        return self.__a
    
    @property
    def rgba(self):
        """rgba is a property that returns the rgba values of the color object."""
        return (self.__r, self.__g, self.__b, self.__a)
    
    @rgba.setter
    def rgba(self, rgba):
        """rgba is a property that sets the rgba values of the color object."""
        self.r = rgba[0]
        self.g = rgba[1]
        self.b = rgba[2]
        self.a = rgba[3]
        
    def randomize_color(self):
        """randomize_color() returns None and randomizes the color values of the object."""
        self.__r = random.randint(0, 255)
        self.__g = random.randint(0, 255)
        self.__b = random.randint(0, 255)
        self.__a = random.randint(0, 255)


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
    def __init__(self, target_entities:type['Entity']=None, attraction_repulsion_force:Vect2D=None):
        self.__attraction_repulsion_force = attraction_repulsion_force
        self.__resulting_direction = Vect2D(0, 0)
        self.__target_entities = [] if target_entities is None else target_entities

    @abstractmethod    
    def behave(self, origin_entity:type['Entity']):
        pass  
    
    @property
    def attraction_repulsion_force(self):
        """attraction_repulsion_force is a property that returns the attraction repulsion force of the steering behavior object."""
        return self.__attraction_repulsion_force
    
    @property
    def resulting_direction(self):
        """resulting_direction is a property that returns the resulting direction of the steering behavior object."""
        return self.__resulting_direction
    
    @resulting_direction.setter
    def resulting_direction(self, resulting_direction):
        """resulting_direction is a property that sets the resulting direction of the steering behavior object."""
        self.__resulting_direction = resulting_direction

    @property
    def target_entities(self):
        """target_entities is a property that returns the target entities of the steering behavior object."""
        return self.__target_entities
    
    @target_entities.setter
    def target_entities(self, target_entities):
        """target_entities is a property that sets the target entities of the steering behavior object."""
        self.__target_entities = target_entities
        
    def add_target_entity(self, target_entity):
        """add_target_entity() returns None and adds a target entity to the steering behavior object."""
        self.__target_entities.append(target_entity)
        
    def remove_target_entity(self, target_entity):
        """remove_target_entity() returns None and removes a target entity from the steering behavior object."""
        self.__target_entities.remove(target_entity)


class Seek(SteeringBehavior):
    """
    This class is used to create a seek steering behavior object.
    It is a child class of the SteeringBehavior class.
    """
    def __init__(self, target_entities:type['Entity']=None, attraction_repulsion_force:int=1): 
        SteeringBehavior.__init__(self, target_entities, attraction_repulsion_force)

    def behave(self, origin_entity: type['Entity']) -> Vect2D:
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
     

class FollowBiggestBoidSeen(SteeringBehavior):
    """
    This class is used to create a follow biggest boid steering behavior object.
    It is a child class of the SteeringBehavior class.
    It will follow the biggest boid in the field of view or will not apply any force if the biggest boid is too small.
    """
    def __init__(self, target_entities:type['Entity']=None, attraction_repulsion_force:int=1, minimum_boids_radius:float=5.0): 
        SteeringBehavior.__init__(self, target_entities, attraction_repulsion_force)
        self.minimum_boids_radius = minimum_boids_radius

    """
    This function is used to calculate the force to apply to the boid.
    It is a child function of the SteeringBehavior class.
    """
    def behave(self, origin_entity: type['Entity']) -> Vect2D:
        sum_of_forces = Vect2D(0, 0)
        biggest_boid = None
        for target_entity in self.target_entities:
            if target_entity is not None:
                if biggest_boid is None:
                    biggest_boid = target_entity
                elif biggest_boid.radius < target_entity.radius:
                    biggest_boid = target_entity
        if biggest_boid is not None:
            if biggest_boid.radius > self.minimum_boids_radius:
                target_position = biggest_boid.position - biggest_boid.speed.normalized * 1.5 * biggest_boid.radius
                distance = (target_position - origin_entity.position).length
                new_maximum_speed = biggest_boid.original_max_speed * (1 + min(100, distance) / 100.0 * 0.25)
                origin_entity.max_speed = new_maximum_speed
                desired_speed = (target_position - origin_entity.position).normalized * origin_entity.max_speed
                sum_of_forces += desired_speed - origin_entity.speed * self.attraction_repulsion_force
            else:
                origin_entity.max_speed = origin_entity.original_max_speed
        return sum_of_forces


class Wander(Seek):
    def __init__(self, radius:float=50, circle_distance:float=100, is_in:bool=True, attraction_repulsion_force:int=1):
        super().__init__(attraction_repulsion_force=attraction_repulsion_force)
        '''radius will increase the turning distance
        circle_distance will increase the distance before turning
        '''        
        self.__circle_distance = circle_distance
        self.__radius = radius
        self.__is_in = is_in
        self.__circle_center = None
   
    def behave(self, origin_entity: type['Entity']) -> Vect2D:
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
        
        self.target_entities = []
        self.target_entities.append(self.__circle_center + displacement)
        
        return super().behave(origin_entity)
        
    def draw(self, draw):
        for target_entity in self.target_entities:
            draw.ellipse([self.__circle_center.x - self.radius, self.__circle_center.y - self.radius, self.__circle_center.x + self.radius, self.__circle_center.y  + self.radius], outline="blue")
            draw.ellipse([target_entity.x - 5, target_entity.y - 5, target_entity.x + 5, target_entity.y + 5], fill="purple")
        
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
        self.__wander_angle = random.random() * 2 * math.pi
        
    def set_angle(self, vector:Vect2D, angle:float) -> Vect2D:
        length = vector.length
        vector.x = math.cos(angle) * length
        vector.y = math.sin(angle) * length
        return vector
        
    def behave(self, origin_entity: type['Entity']) -> Vect2D:     
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
    def __init__(self, target_entities:type['Entity']=None, attraction_repulsion_force:int=1):
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

    def behave(self, origin_entity:type['Entity']) -> Vect2D:
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
    def __init__(self, target_entities:list[type['Entity']|type['Vect2D']], attraction_repulsion_force:int=2000000000):
        SteeringBehavior.__init__(self, attraction_repulsion_force=attraction_repulsion_force)
    
        self.__target_entities = target_entities

    def behave(self, origin_entity:type['Entity']) -> Vect2D:
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
    def __init__(self, target_entities:list[type['Entity']|type['Vect2D']], attraction_repulsion_force:int=50):
        super().__init__(target_entities, attraction_repulsion_force)

        self.__center_of_gravity = Vect2D()
        
        self.__origin_entity = None

    def behave(self, origin_entity: type['Entity']) -> Vect2D:
        if not self.__origin_entity:
            self.__origin_entity = origin_entity
        sum_of_positions = Vect2D()
        for target_entity in self.target_entities:
            if target_entity is not None:
                if isinstance(target_entity, Entity):
                    sum_of_positions.set(sum_of_positions.x + target_entity.position.x, sum_of_positions.y + target_entity.position.y)
                else: 
                    sum_of_position += target_entity
        self.__center_of_gravity.set(sum_of_positions.x / len(self.target_entities), sum_of_positions.y / len(self.target_entities)) 
        desired_speed = (self.__center_of_gravity - origin_entity.position).normalized * origin_entity.max_speed
        sum_of_forces = (desired_speed - origin_entity.speed) * self.attraction_repulsion_force
        return sum_of_forces
    
    def draw(self,draw):
        draw.line([self.__origin_entity.position.x, self.__origin_entity.position.y, self.__center_of_gravity.x, self.__center_of_gravity.y], (0, 255, 0))
        draw.ellipse([self.__center_of_gravity.x -5 , self.__center_of_gravity.y -5, self.__center_of_gravity.x + 5 , self.__center_of_gravity.y + 5], (0, 255, 0))    


class Alignment(SteeringBehavior):
    def __init__(self, target_entities:list[type['Entity']|type['Vect2D']], attraction_repulsion_force:int=50000):
        super().__init__(target_entities, attraction_repulsion_force)
        
        self.__origin_entity = None
        
        self.__sum_of_forces = Vect2D()
        
    def behave(self, origin_entity: type['Entity'] = None) -> Vect2D:
        if not self.__origin_entity:
            self.__origin_entity = origin_entity
            for target_entity in self.target_entities:
                if target_entity is not None:
                    if isinstance(target_entity, Entity):
                        self.__sum_of_forces += target_entity.speed
        self.__sum_of_forces /= len(self.target_entities)
        return  self.__sum_of_forces
    
    def draw(self, draw):
        draw.line([self.__origin_entity.position.x, self.__origin_entity.position.y, self.__origin_entity.position.x + self.__sum_of_forces.x, self.__origin_entity.position.y +  self.__sum_of_forces.y], (255, 255, 0))
        draw.ellipse([self.__origin_entity.position.x + self.__sum_of_forces.x -5 , self.__origin_entity.position.y + self.__sum_of_forces.y -5, self.__origin_entity.position.x + self.__sum_of_forces.x + 5 , self.__origin_entity.position.y + self.__sum_of_forces.y + 5], (255, 255, 0))


class Separation(SteeringBehavior):
    def __init__(self, target_entities:list[type['Entity']|type['Vect2D']], attraction_repulsion_force:int=50):
        super().__init__(target_entities, attraction_repulsion_force)
        
    def behave(self, origin_entity: type['Entity']) -> Vect2D:
        sum_of_forces = Vect2D()
        for target_entity in self.target_entities:
            if target_entity is not None:
                if isinstance(target_entity, Entity):
                    behavior = EntityRepulsion([target_entity], self.attraction_repulsion_force)
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
        self.__original_max_speed = max_speed

    def move(self, time):
        self.position.set(self.position.x + self.speed.x * time + self.acceleration.x * 0.5 ** 2 * time, self.position.y + self.speed.y * time + self.acceleration.y * 0.5 ** 2 * time)
        self.speed.set(self.speed.x + self.steering_force.x, self.speed.y + self.steering_force.y)
        
        self.speed.clamp_x(-self.max_speed, self.max_speed)
        self.speed.clamp_y(-self.max_speed, self.max_speed)

    @property
    def max_speed(self):
        return self.__max_speed

    @max_speed.setter
    def max_speed(self, max_speed):
        self.__max_speed = max_speed

    @property
    def original_max_speed(self):
        return self.__original_max_speed

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
    '''
    Thomas Pelletier
    Piloted représente la capacité à un cercle dynamique d'être influencé par un Steering Behaviour.

    Args:
    self.__max_steering_force (int): la force maximal de direction .
    self.steering_force (Vect2D): la force de direction.
    self.__steering_behaviors (list[SteeringBehavior]): la liste des Steering Behaviors.     
    
    Example:
        >>> dynamiccircle = DynamicCircle( border_color=RGBAColor(randomize=True),
                                                            border_width=5,
                                                            fill_color=RGBAColor(randomize=True),
                                                            position=Vect2D(random.randrange(0,1000),random.randrange(0,500)),
                                                            radius=random.randint(10, 50),
                                                            acceleration=Vect2D(0,0),
                                                            speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)),
                                                            max_speed= 100,
                                                            max_steering_force=5,
                                                            steering_force=Vect2D(0,0),
                                                            steering_behaviors=[BorderRepulsion(sim_dim=self.__size)])
        >>> dynamiccircle.steer()
        >>> print(dynamicircle is not None)
        True
    
    '''
    def __init__(self, max_steering_force:int, steering_force:Vect2D, steering_behaviors:list[SteeringBehavior]):
        self.__max_steering_force = max_steering_force
        self.steering_force = steering_force
        self.__steering_behaviors = steering_behaviors

   
    def steer(self) -> None:
        '''   The steer function helps to set the steering force for each boids.
        '''

        
        if self.__steering_behaviors is not None:
            for steering_behavior in self.__steering_behaviors:
                self.steering_force.set(self.steering_force.x + steering_behavior.behave(origin_entity=self).x, self.steering_force.y + steering_behavior.behave(origin_entity=self).y)
        self.steering_force.set_polar(length= Utils.clamp_max(self.steering_force.length, self.__max_steering_force), orientation=self.steering_force.orientation)

    @property
    def max_steering_force(self):
        '''Retourne la force de direction maximale '''
        return self.__max_steering_force

    @property
    def steering_force(self):
        '''Retourne la force de direction actuelle '''
        return self.__steering_force
    
    @property
     
    def steering_behaviors(self):
        '''Retourne la liste des comportements de direction'''
        return self.__steering_behaviors

    @steering_force.setter
    def steering_force(self, steering_force):
        '''permet de donner une force de direction'''
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
    """
    Commentée par Andrzej Wisniowski

    Cette classe représente un cerveau appartenant à un objet propriétaire. 
    Elle est responsable de la collecte d'informations en provenance des capteurs du propriétaire, et de la prise de décision de l'entité.
    Elle est composés de patterns de comportement, qui sont principalement des couples (cible, comportement) qui sont appliqués à l'entité en fonction de la cible que le cerveau détecte. Il existe également des patterns de comportement qui ne sont pas liés à une cible, et qui sont toujours ou conditionnellement appliqués à l'entité.
    
    Il existe plusieurs façons de **créer** un `Brain` :
    
    - `Brain(owner, environment, behavior_patterns)`
    - `Brain(owner, environment)`

    Les **propriétés** (accesseurs et mutateurs) sont :

    - `Brain.active_behaviors` [lecture] : retourne la liste des comportements actifs
    - `Brain.seen_entities` [lecture] : retourne la liste des entités vues par le cerveau
    - `Brain.behavior_patterns` [lecture/écriture] : la liste des patterns de comportement

    Les **méthodes** sont :

    - `Brain.process()` : traite les informations collectées par les capteurs du propriétaire, et applique les patterns de comportement correspondants
    - `Brain.behave()` : applique les comportements actifs sur le propriétaire
    - `Brain.draw_line_to_seen_entities()` : dessine une ligne entre le propriétaire et les entités vues par le cerveau, et surligne l'entité propriétaire avec un halo bleu

    Les **attributs** sont :

    - `Brain.__owner` : l'entité propriétaire
    - `Brain.__environment` : l'environnement dans lequel évolue l'entité
    - `Brain.__behavior_patterns` : la liste des patterns de comportement
    - `Brain.__seen_entities` : la liste des entités vues par le cerveau
    - `Brain.__active_behaviors` : la liste des comportements actifs
    - `Brain.__permanent_patterns` : la liste des patterns de comportement permanents

    Exemple d'utilisation :
        >>> brain = Brain(SentientCircle(), Simulation())
        >>> print(isinstance(brain, Brain))
        True
    """
    def __init__(self, owner:type["Entity"], environment:type["Simulation"], behavior_patterns:dict[dict[str]]=None):
        """
        Création d'un objet `Brain` utilisant les patterns de comportement passés en paramètre.
        Si aucun pattern n'est passé en paramètre, les patterns par défaut sont utilisés.

        Args:
            owner (Entity): l'entité propriétaire
            environment (Environment): l'environnement dans lequel évolue l'entité
            behavior_patterns (dict, optional): la liste des patterns de comportement. Defaults to None.
        """
        self.__owner = owner
        """
        L'entité propriétaire. Il s'agit dans ce cas-ci d'un **SentientCircle**.
        """
        self.__environment = environment
        """
        L'environnement dans lequel évolue l'entité. Il s'agit dans ce cas-ci de la **Simulation**.
        """
        if behavior_patterns is None:
            self.__behavior_patterns = {    "DynamicCircle": { "Behavior": Evade, "Target_type" : "single" }, 
                                            "SentientCircle": { "Behavior": Cohesion, "Target_type" : "grouping" },
                                            "Circle": { "Behavior": EntityRepulsion, "Target_type" : "single" },
                                            "Unknown": { "Behavior": Evade, "Target_type" : "single" },
                                            "No_target": { "Behavior": Wander, "Target_type" : "none" }
                                        }
            """
            La liste des patterns de comportement
            Si aucun pattern n'est passé en paramètre, les patterns par défaut sont utilisés.
            """
        else: self.__behavior_patterns = behavior_patterns
        self.__permanent_patterns = [BorderRepulsion(sim_dim=environment.size)]
        """
        La liste des patterns de comportement permanents
        """

        self.__seen_entities = []
        """
        La liste des entités vues par le cerveau
        
        """
        self.__active_behaviors = self.__permanent_patterns
        """
        La liste des comportements actifs
        """

    def process(self) -> None:
        """
        Traite les informations collectées par les capteurs du propriétaire, et applique les patterns de comportement correspondants.
        """
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
                        if seen_entity.__class__.__name__ == key:
                            behavior = self.__behavior_patterns[seen_entity.__class__.__name__]["Behavior"]
                            self.__active_behaviors.append(behavior([seen_entity]))
                elif values["Target_type"] == "grouping":
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

    def draw_line_to_seen_entities(self, draw) -> None:
        """
        Dessine une ligne entre le propriétaire et les entités vues par le cerveau, et surligne l'entité propriétaire avec un halo bleu.
        """
        halo_radius = self.__owner.radius * 1.25
        for seen_entity in self.__seen_entities:
            draw.ellipse([self.__owner.position.x - halo_radius, self.__owner.position.y -  halo_radius, self.__owner.position.x +  halo_radius, self.__owner.position.y +  halo_radius], fill="cyan")
            draw.line([self.__owner.position.x, self.__owner.position.y, seen_entity.position.x, seen_entity.position.y], fill="cyan", width=5)
            
    def behave(self) -> None:
        """
        Applique les comportements actifs sur l'entité propriétaire.
        """
        for behavior in self.__active_behaviors:
                self.__owner.steering_force.set(self.__owner.steering_force.x + behavior.behave(origin_entity=self.__owner).x, self.__owner.steering_force.y + behavior.behave(origin_entity=self.__owner).y)

        self.__owner.steering_force.set_polar(length= Utils.clamp_max(self.__owner.steering_force.length, self.__owner.max_steering_force), orientation=self.__owner.steering_force.orientation)     

    @property
    def active_behaviors(self):
        """
        Renvoie la liste des comportements actifs.
        """
        return self.__active_behaviors
    
    @property
    def seen_entities(self):
        """
        Retourne la liste des entités vues par le cerveau.
        """
        return self.__seen_entities

    @property
    def behavior_patterns(self):
        """
        Retourne la liste des patterns de comportement.
        """
        return self.__behavior_patterns

    @behavior_patterns.setter
    def behavior_patterns(self, value):
        """
        Définit la liste des patterns de comportement.
        """
        self.__behavior_patterns = value


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
        return self.__owner.position.distance_from(target.position) - target.radius <= self.__range

    def is_in_fov(self, target:Vect2D)->bool:
        distance_to_target = target.position - self.__owner.position
        if distance_to_target.is_defined:
            return self.__vector.angle_between_degrees(distance_to_target) <= self.__fov
        else:
            return True
        
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
        
        """L'entity est un objet qui peut être dessiné et qui peut être mis à jour
        
        Args:
            border_color (RGBAColor): Couleur de la bordure
            border_width (int): Epaisseur de la bordure
            fill_color (RGBAColor): Couleur de remplissage
            position (Vect2D): Position de l'entity
            size (Vect2D): Taille de l'entity
            
            >>> entity = Entity(RGBAColor(255, 0, 0), 1, RGBAColor(0, 0, 255), Vect2D(0, 0), Vect2D(100, 100))
            >>> print(entity)        
            
        """
    
        self.__available_names = ["William", "Logan", "Liam", "Noah", "Jacob", "Thomas", 
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
                                "Gertrude", "Denis", "Donald", "Jonathan", "Andrzej", "Marius",
                                "Marek", "Marcin", "Maciej", "Piotr", "Pawel", "Piotrek", "Pawel",
                                "Julie", "Juliette", "Juliet", "Julia", "Juliana", "June", "Valerie",
                                "Valeria", "Zoe", "Chanel", "Chloe", "Charlotte", "Celine", "Cecile",
                                "Martha", "Marie", "Marion", "Marina", "Marine", "Maria", "Marianne",
                                "Diana", "Diane", "Gertrude", "Geraldine", "Alexandra", "Alexandria",
                                "Alexandrine", "Alexia", "Huguette", "Marguerite", "Margot", "Molly"]
        
        #get a random name from the list
        self.__name = random.choice(self.__available_names)

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
    def __init__(self, border_color = RGBAColor(randomize=True), border_width = 5, fill_color = RGBAColor(0,0,0,255),  position=Vect2D(random.randrange(0,1000),random.randrange(0,500)), radius:int=50):
        Entity.__init__(self, border_color=border_color, border_width=border_width, fill_color=fill_color, position=position, size=Vect2D(radius*2, radius*2))
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
    
    """Création d'un cercle dynamique, c'est à dire un cercle qui peut se déplacer et qui peut être piloté par des forces de déplacement
        
        Args:
            - border_color (RGBAColor, optional): Couleur de la bordure. Defaults to RGBAColor(randomize=True).
            - border_width (int, optional): Epaisseur de la bordure. Defaults to 5.
            - fill_color (RGBAColor, optional): Couleur de remplissage. Defaults to RGBAColor(randomize=True).
            - position (Vect2D, optional): Position du cercle. Defaults to Vect2D(random.randrange(0,1000),random.randrange(0,500)).
            - radius (int, optional): Rayon du cercle. Defaults to random.randint(10, 50).
            - acceleration (Vect2D, optional): Accélération du cercle. Defaults to Vect2D(0,0).
            - speed (Vect2D, optional): Vitesse du cercle. Defaults to Vect2D(random.randrange(-50,50), random.randrange(-50,50)).
            - max_speed (int, optional): Vitesse maximale du cercle. Defaults to 100.
            - max_steering_force (int, optional): Force de déplacement maximale. Defaults to 50.
            - steering_force (Vect2D, optional): Force de déplacement. Defaults to Vect2D(0,0).
            - steering_behaviors (list, optional): Liste des forces de déplacement. Defaults to None.
            
        Exemple:
            >>> dynamic_circle = DynamicCircle(position=Vect2D(100,100), radius=50, speed=Vect2D(10,10), max_speed=100, max_steering_force=50)
            >>> print(isinstance(dynamic_circle, DynamicCircle))
            True
            >>> print(dynamic_circle.position.x, dynamic_circle.position.y)
            100.0 100.0
            >>> print(dynamic_circle.speed.x, dynamic_circle.speed.y)
            10.0 10.0
            >>> print(dynamic_circle.max_speed)
            100     
            >>> print(dynamic_circle.max_steering_force)
            50
            >>> print(dynamic_circle.radius)
            50
            >>> print(isinstance(dynamic_circle, DynamicCircle))
            True
            >>> print(isinstance(dynamic_circle, Circle))
            True
            >>> print(isinstance(dynamic_circle, Movable))
            True  
        """
            
    
    def __init__(   self,
                    border_color=RGBAColor(randomize=True),
                    border_width=5,
                    fill_color=RGBAColor(randomize=True),
                    position=Vect2D(random.randrange(0,1000),random.randrange(0,500)),
                    radius=random.randint(10, 50),
                    acceleration=Vect2D(0,0),
                    speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)),
                    max_speed= 100,
                    max_steering_force=50,
                    steering_force=Vect2D(0,0),
                    steering_behaviors=None,
                ):
        Circle.__init__(self, border_color, border_width, fill_color, position, radius)
        Movable.__init__(self, acceleration, max_speed, speed)
        Piloted.__init__(self, max_steering_force, steering_force, steering_behaviors)
        
        
    def draw(self, draw:ImageDraw):
        """Methode generique de dessin d'un cercle dynamique

        Args:
            draw (ImageDraw): Objet necessaire pour dessiner sur une image
        """
        Circle.draw(self, draw)

    def draw_circle_speed(self, draw:ImageDraw):
        """Methode de dessin de la vitesse du cercle dynamique

        Args:
            draw (ImageDraw): Objet necessaire pour dessiner sur une image
        """
        draw.line([self.position.x, self.position.y, self.position.x + self.speed.x, self.position.y + self.speed.y], fill="red", width=5)
        
    def draw_circle_steering_force(self, draw:ImageDraw):
        """Methode de dessin de la force de déplacement du cercle dynamique

        Args:
            draw (ImageDraw): Objwet necessaire pour dessiner sur une image
        """
        draw.line([self.position.x, self.position.y, self.position.x + self.steering_force.x * 10, self.position.y + self.steering_force.y * 10], fill="darkgoldenrod", width=5)
        for steering_behavior in self.steering_behaviors:
            if hasattr(steering_behavior, "draw"):
                    steering_behavior.draw(draw)
            
    def move(self, time):
        """Method qui permet de déplacer le cercle dynamique

        Args:
            time (float): Unité de temps
        """
        Movable.move(self, time)

    def tick(self, time):
        """Methode qui permet de faire évoluer le cercle dynamique

        Args:
            time (float): Unité de temps
        """
        self.steer()
        self.move(time)


class SentientCircle(DynamicCircle):
    def __init__(self, border_color=RGBAColor(randomize=True), border_width=5, fill_color=RGBAColor(randomize=True), position=Vect2D(random.randrange(0,1000),random.randrange(0,500)), radius=random.randint(10, 50), acceleration=Vect2D(0,0), speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)), max_speed= 100, max_steering_force=5, steering_force=Vect2D(0,0), steering_behaviors=None, environment=None, brain=None, eyes=None):
        DynamicCircle.__init__(self, border_color, border_width, fill_color, position, radius, acceleration, speed, max_speed, max_steering_force, steering_force, steering_behaviors)

        """Création d'un cercle intelligent, c'est à dire un cercle qui peut se déplacer et qui peut être piloté par des forces de déplacement et qui peut voir et interagir avec son environnement
        """

        self.__brain = brain if brain else Brain(self, environment)  
        self.__eyes = eyes if eyes else [Eye(self)]

    def tick(self, time):
        DynamicCircle.tick(self, time)
        self.__brain.process()

    def draw_fov(self, draw):
        for eye in self.__eyes:
            eye.draw(draw)    
        self.__brain.draw_line_to_seen_entities(draw)

    def draw_circle_steering_force(self, draw):
        draw.line([self.position.x, self.position.y, self.position.x + self.steering_force.x * 10, self.position.y + self.steering_force.y * 10], fill="darkgoldenrod", width=5)
        for steering_behavior in self.__brain.active_behaviors:
            if hasattr(steering_behavior, "draw"):
                    steering_behavior.draw(draw)
                    
    @property
    def eyes(self):
        return self.__eyes
    
    @property
    def brain(self):
        return self.__brain
    
    @eyes.setter
    def eyes(self, eyes):
        self.__eyes = eyes
        
    @brain.setter
    def brain(self, brain):
        self.__brain = brain


class PredatorCircle(SentientCircle):
    def __init__(self, border_color=RGBAColor(randomize=True), border_width=5, fill_color=RGBAColor(randomize=True), position=Vect2D(random.randrange(0,1000),random.randrange(0,500)), radius=random.randint(10, 50), acceleration=Vect2D(0,0), speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)), max_speed= 100, max_steering_force=5, steering_force=Vect2D(0,0), steering_behaviors=None, fov=math.pi/2, range=100, environment=None):
        SentientCircle.__init__(self, border_color, border_width, fill_color, position, radius, acceleration, speed, max_speed, max_steering_force, steering_force, steering_behaviors, fov, range, environment)

        predator_dict = {                   "DynamicCircle": { "Behavior": Pursuit, "Target_type" : "single" }, 
                                            "SentientCircle": { "Behavior": Pursuit, "Target_type" : "grouping" },
                                            "Circle": { "Behavior": EntityRepulsion, "Target_type" : "single" },
                                            "Unknown": { "Behavior": Evade, "Target_type" : "single" },
                                            "PredatorCircle": { "Behavior": Alignment, "Target_type" : "grouping" },
                                            "PreyCircle": { "Behavior": Seek, "Target_type" : "single" },
                                            "No_target": { "Behavior": PseudoWander, "Target_type" : "none" }
                        }

        self.brain = Brain(self, environment, predator_dict)    
        self.eyes = [Eye(self, fov = 20, range = 400)]
        

class PreyCircle(SentientCircle):
    def __init__(self, border_color=RGBAColor(randomize=True), border_width=5, fill_color=RGBAColor(randomize=True), position=Vect2D(random.randrange(0,1000),random.randrange(0,500)), radius=random.randint(10, 50), acceleration=Vect2D(0,0), speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)), max_speed= 100, max_steering_force=5, steering_force=Vect2D(0,0), steering_behaviors=None, fov=math.pi/2, range=100, environment=None):
        SentientCircle.__init__(self, border_color, border_width, fill_color, position, radius, acceleration, speed, max_speed, max_steering_force, steering_force, steering_behaviors, fov, range, environment)

        prey_dict = {                   "DynamicCircle": { "Behavior": Evade, "Target_type" : "single" }, 
                                        "SentientCircle": { "Behavior": Evade, "Target_type" : "grouping" },
                                        "Circle": { "Behavior": EntityRepulsion, "Target_type" : "single" },
                                        "Unknown": { "Behavior": Evade, "Target_type" : "single" },
                                        "PredatorCircle": { "Behavior": Flee, "Target_type" : "grouping" },
                                        "PreyCircle": { "Behavior": Cohesion, "Target_type" : "grouping" },    
                                        "No_target": { "Behavior": Wander, "Target_type" : "none" }
                        }
        self.brain = Brain(self, environment, prey_dict)    
        self.eyes = [Eye(self, fov = 95, range = 100)]


class Simulation(Updatable):
    """ 
        Commentée par Alexis Provost
        
        La classe Simulation correspond à la simulation elle-même. 
        Elle contient les sprites, la taille de l'image, la position de la souris, et la boucle de jeu qui bouge les Entities.
        Elle contient aussi les fonctions de dessin, qui sont appelées par la fonction draw() de la classe Window.
       
        Args:
            - :param size: Vect2D, la taille de la fenêtre
            - :param sprites: list, la liste des sprites
            - :param mouse_pos: Vect2D, la position de la souris
            - :param is_running: bool, True si la simulation est en cours, False sinon
            - :param seed: int, le seed pour la génération aléatoire
            - :param selected_entity: Entity, l'entité sélectionnée par le click de la souris
        
        Exemples: Créé une simulation et l'initialise un scénario
        >>> sim = Simulation()
        >>> sim.initialize_scenario(key="Seek, Flee or Wander")
        >>> print(len(sim.sprites))
        256
    """
    def __init__(self, size=Vect2D(100,100)):
        self.__size = size
        self.__sprites = []
        self.__mouse_pos = Vect2D(-1, -1)
        self.__is_running = True
        self.__seed = 0
        self.__selected_entity = None
        
        self.initialize_scenario()

    def initialize_scenario(self, key:str="Red chasing Green"): 
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
                                                            steering_force=Vect2D(0,0),
                                                            environment=self
                                                            ))
        
            case 'Alignment':
                nb_balls = 50

                behavior_patterns =  {  "DynamicCircle": { "Behavior": Evade, "Target_type" : "single" }, 
                                        "SentientCircle": { "Behavior": Alignment, "Target_type" : "grouping" },
                                        "Circle": { "Behavior": EntityRepulsion, "Target_type" : "single" },
                                        "Unknown": { "Behavior": Evade, "Target_type" : "single" },
                                        "No_target": { "Behavior": Wander, "Target_type" : "none" }
                                    }

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
                                                            steering_force=Vect2D(0,0),
                                                            environment=self
                                                            ))
                for sprite in self.__sprites:
                    sprite.brain.behavior_patterns = behavior_patterns


            case 'Follow Biggest Boid Seen':
                nb_balls = 50

                behavior_patterns =  {  "DynamicCircle": { "Behavior": Evade, "Target_type" : "single" }, 
                                        "SentientCircle": { "Behavior": FollowBiggestBoidSeen, "Target_type" : "grouping" },
                                        "Circle": { "Behavior": EntityRepulsion, "Target_type" : "single" },
                                        "Unknown": { "Behavior": Evade, "Target_type" : "single" },
                                        "No_target": { "Behavior": Wander, "Target_type" : "none" }
                                    }
                eye_fov = 500
                eye_range = 150

                for i in range(nb_balls):
                                self.__sprites.append(SentientCircle(border_color=RGBAColor(randomize=True),
                                                            border_width=5,
                                                            fill_color=RGBAColor(randomize=True),
                                                            position=Vect2D(random.randrange(0,1000),random.randrange(0,500)),
                                                            radius=random.randint(5, 50),
                                                            acceleration=Vect2D(0,0),
                                                            speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)),
                                                            max_speed= 100,
                                                            max_steering_force=5,
                                                            steering_force=Vect2D(0,0),
                                                            environment=self
                                                            ))

                for sprite in self.__sprites:
                    sprite.brain.behavior_patterns = behavior_patterns
                    sprite.eye.fov = eye_fov
                    sprite.eye.range = eye_range

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
                                                        steering_force=Vect2D(0,0),
                                                        steering_behaviors=[Wander(), BorderRepulsion(sim_dim=self.__size)]))


            case 'Predator Chasing Prey': # Default
                nb_obstacles = 0
                nb_predators = 1
                nb_preys = 50
                for _ in range(nb_predators):
                    self.__sprites.append(PredatorCircle(position=Vect2D(random.randrange(0, int(self.width)),random.randrange(0, int(self.height))),
                                                        speed=Vect2D(random.randrange(-50,50),random.randrange(-50,50)),
                                                        border_color=RGBAColor(randomize=True),
                                                        border_width=5,
                                                        radius=25,
                                                        acceleration=Vect2D(0,0),
                                                        max_speed= 100,
                                                        max_steering_force=5,
                                                        steering_force=Vect2D(0,0),
                                                        environment=self,
                                                        fill_color=RGBAColor(255,0,0,255)
                                                       ))
                for _ in range(nb_preys):
                    self.__sprites.append(PreyCircle(border_color=RGBAColor(randomize=True),
                                                            border_width=5,
                                                            fill_color=RGBAColor(0,255,0,255),
                                                            position=Vect2D(random.randrange(0,1000),random.randrange(0,500)),
                                                            radius=random.randint(5, 10),
                                                            acceleration=Vect2D(0,0),
                                                            speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)),
                                                            max_speed= 100,
                                                            max_steering_force=5,
                                                            steering_force=Vect2D(0,0),
                                                            environment=self
                                                       ))
                for _ in range(nb_obstacles):
                    self.__sprites.append(Circle(position=Vect2D(random.randrange(0, int(self.width)),random.randrange(0, int(self.height)))))
            
            case 'Avoid Obstacles':
                nb_obstacles = 20
                nb_sentient_circles = 10
                        
                for _ in range(nb_obstacles):
                    self.__sprites.append(Circle(   position=Vect2D(random.randrange(0, int(self.width)),random.randrange(0, int(self.height))),
                                                    radius=25))

                for _ in range(nb_sentient_circles):
                    self.__sprites.append(SentientCircle(border_color=RGBAColor(randomize=True),
                    border_width=5,
                    radius=10,
                    fill_color=RGBAColor(randomize=True),
                    position=Vect2D(random.randrange(0,1000),random.randrange(0,500)),
                    acceleration=Vect2D(0,0),
                    speed=Vect2D(random.randrange(-50,50), random.randrange(-50,50)),
                    max_speed= 100,
                    max_steering_force=5,
                    steering_force=Vect2D(0,0),
                    environment=self
                    ))


            case 'Red chasing Green': # Default
                nb_balls = 6
                for i in range(nb_balls):
                    self.__sprites.append(DynamicCircle(position=Vect2D(random.randrange(0, int(self.width)),random.randrange(0, int(self.height))),
                                                        speed=Vect2D(random.randrange(-50,50),random.randrange(-50,50)),
                                                        border_color=RGBAColor(randomize=True),
                                                        border_width=5,
                                                        acceleration=Vect2D(0,0),
                                                        max_speed= 100,
                                                        max_steering_force=5,
                                                        steering_force=Vect2D(0,0),
                                                        steering_behaviors=[Wander(), BorderRepulsion(sim_dim=self.__size)] if i%2 == 0 else [Pursuit([self.sprites[i-1]]), BorderRepulsion(sim_dim=self.__size)]))

                for i, sprite in enumerate(self.__sprites):
                    sprite.fill_color = RGBAColor(128, 0, 0, 255) if type(sprite.steering_behaviors[0]) is Pursuit else RGBAColor(0, 128, 0, 255)
                    sprite.radius = 60 if type(sprite.steering_behaviors[0]) is Pursuit else 30
                    if i%2 == 0 and i != len(self.__sprites) - 1:
                        self.__sprites[i].steering_behaviors.append(Evade([self.__sprites[i+1]]))

    def tick(self, time):
        """Fait bouger les Entities, est appelée par la fonction update() de la classe App"""
        if self.__sprites:
            for sprite in self.__sprites:
                sprite.tick(time)

    def reset(self, key:str="Red chasing Green"):
        """Remet la simulation à zéro"""
        self.__is_running = True
        self.__sprites = []
        self.initialize_scenario(key)

    def move_mouse(self, event):
        """Met à jour la position de la souris"""
        self.__mouse_pos.set(event.x, event.y)
        
    def mouse_left(self, event):
        """Gère la sortie de la souris de la fenêtre"""
        self.__mouse_pos.set(-1, -1)
        
        for sprite in self.__sprites:
            sprite.steering_force = Vect2D(0,0)

    def mouse_entered(self, event):
        """Gère l'entrée de la souris dans la fenêtre"""
        self.__mouse_pos.set(event.x, event.y)
        
    def toggle_running(self, event):
        """Met en pause ou en reprend la simulation"""
        self.__is_running = not self.__is_running
        
    def check_entity_clicked(self, event):
        """Vérifie si une entité a été cliquée avec un offset de 20 pixels pour le miss click"""
        radius_offset = 20
        for sprite in reversed(self.__sprites):
            if sprite.position.x - (sprite.radius + radius_offset) < event.x < sprite.position.x + (sprite.radius + radius_offset) and sprite.position.y - (sprite.radius + radius_offset) < event.y < sprite.position.y + (sprite.radius + radius_offset):
                return sprite

    @property
    def selected_entity(self):
        """Retourne l'entité sélectionnée"""
        return self.__selected_entity
    
    @selected_entity.setter
    def selected_entity(self, value):
        """Définit l'entité sélectionnée"""
        self.__selected_entity = value

    @property
    def sprites(self):
        """Retourne la liste des sprites"""
        return self.__sprites
    
    @property
    def mouse_pos(self):
        """Retourne la position de la souris"""
        return self.__mouse_pos
    
    @property
    def size(self):
        """Retourne la taille de la fenêtre"""
        return self.__size

    @property
    def width(self):
        """Retourne la largeur de la fenêtre"""
        return self.__size.x

    @property
    def height(self):
        """Retourne la hauteur de la fenêtre"""
        return self.__size.y
    
    @property
    def is_running(self):
        """Retourne True si la simulation est en cours, False sinon"""
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
        self.__start_stop_button = ttk.Button(self, text="Stop", width = 40)
        self.__next_button = ttk.Button(self, text="Next Step", state="disabled", width = 40)
        self.__reset_button = ttk.Button(self, text="Reset", width = 40)
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
        self.__info_label = tk.Text(self, width=30, height=20)
        self.__set_text("Click on a boid to show the infomations about it")
        self.__info_label.grid(row=0, column=0)
        
        self.__info_entity = None
        self.__info_string = ""

    @property
    def info_label(self):
        return self.__info_label
    
    def __set_text(self, text):
        self.__info_label.config(state=tk.NORMAL)
        self.__info_label.delete(1.0, tk.END)
        self.__info_label.insert(tk.END, text)
        self.__info_label.config(state=tk.DISABLED)
        
    @property
    def info_entity(self):
        return self.__info_entity
    
    @property
    def info_string(self):
        return self.__info_string

    def update(self):
        if self.__info_entity is not None and not type(self.__info_entity) is Circle:
            self.__info_string = "Name: " + self.__info_entity.name + "\n"
            self.__info_string += "Position: ({}, {})".format(math.trunc(self.__info_entity.position.x), math.trunc(self.__info_entity.position.y)) + "\n"
            self.__info_string += "Speed: ({}, {})".format(math.trunc(self.__info_entity.speed.x), math.trunc(self.__info_entity.speed.y)) + "\n"
            self.__info_string += "Steering force: ({}, {})".format(math.trunc(self.__info_entity.steering_force.x), math.trunc(self.__info_entity.steering_force.y)) + "\n"
            if isinstance(self.__info_entity, Circle):
                self.__info_string += "Radius: {}".format(self.__info_entity.radius) + "\n"
            self.__info_string += "Steering forces: " + "\n"
            if self.__info_entity.steering_behaviors is not None:
                for steering_behavior in self.__info_entity.steering_behaviors:
                    self.__info_string += "    " + steering_behavior.__class__.__name__ + "\n"
                    if steering_behavior.target_entities is not None:
                        for target_entity in steering_behavior.target_entities:
                            if isinstance(target_entity, Entity):
                                self.__info_string += "        " + target_entity.name + "\n"
            elif hasattr(self.__info_entity, 'brain') and self.__info_entity.brain is not None and self.__info_entity.brain.active_behaviors is not None and hasattr(self.__info_entity.brain, 'active_behaviors'):
                for steering_behavior in self.__info_entity.brain.active_behaviors:
                    self.__info_string += "    " + steering_behavior.__class__.__name__ + "\n"
                    if steering_behavior.target_entities is not None:
                        for target_entity in steering_behavior.target_entities:
                            if isinstance(target_entity, Entity):
                                self.__info_string += "        " + target_entity.name + "\n"
                
            else:
                self.__info_string += "    None\n"
            
            if hasattr(self.__info_entity, 'eyes') and hasattr(self.__info_entity, 'brain') and self.__info_entity.eyes is not None:
                self.__info_string += "Eyes: " + "\n"
                for eye in self.__info_entity.eyes:
                    self.__info_string += "    " + str(self.__info_entity.eyes.index(eye)) +" (FOV: " + str(math.trunc(eye.fov)) + ", Range: " + str(eye.range) + "): " + "\n"
                    for seen_entity in self.__info_entity.brain.seen_entities:
                        self.__info_string += "        " + seen_entity.name + ":" + seen_entity.__class__.__name__ + "\n"

            self.__info_string += "\nClick again to hide info."
            
            self.__set_text(self.__info_string)
        else:
            self.__set_text("Click on an entity to show it's informations")
    
    @info_entity.setter
    def info_entity(self, entity):
        self.__info_entity = entity
        self.update()


class ViewWindow(ttk.Label, Drawable):
    def __init__(self, border_color=None, border_width=None, fill_color=None, position=None, size=None):
        ttk.Label.__init__(self, root=None, text=None, width=size.x)
        Drawable.__init__(self, border_color, border_width, fill_color, position, size)
        self.__background = Image.open("tropicalforest.jpg")
        self.sizex = size.x
        self.sizey = size.y
        self.__resized = self.__background.resize((int(size.x), int(size.y)))
        self.__image_draw = ImageDraw.Draw(self.__resized)
        self.__image_tk = ImageTk.PhotoImage(self.__resized)
        self.__image_label = ttk.Label(self, image=self.__image_tk)
        self.__image_label.grid(row=0, column=0, sticky='ns')
        self.__image_label.columnconfigure(0, minsize=600, weight=1)
        self.__speed_is_drawn = False
        self.__steering_force_is_drawn = False
        self.__circle_is_drawn = True
        self.__fov_is_drawn = False
        self.__crazy_mode = False
        self.__jungle_background = False

    def update_view(self, simulation):
            if self.__crazy_mode:
                i = self.__resized
                draw = ImageDraw.Draw(i)
            else:
                if self.__jungle_background:
                    self.__newbackground = Image.open("tropicalforest.jpg")
                else :
                    self.__newbackground = Image.new('RGBA', (int(self.sizex), int(self.sizey)), (0, 0, 0))
                i = self.__newbackground.resize((int(self.sizex), int(self.sizey)))
                draw = ImageDraw.Draw(i)
            
            if self.__speed_is_drawn and self.__steering_force_is_drawn and self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw)                     
                    sprite.draw(draw)
                    if hasattr(sprite, "draw_circle_speed"):
                        sprite.draw_circle_speed(draw)
                        sprite.draw_circle_steering_force(draw)
                   
            elif self.__speed_is_drawn and self.__steering_force_is_drawn and self.__circle_is_drawn and not self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    sprite.draw(draw)
                    if hasattr(sprite, "draw_circle_speed"):
                        sprite.draw_circle_speed(draw)
                        sprite.draw_circle_steering_force(draw)
            elif self.__speed_is_drawn and self.__steering_force_is_drawn and not self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw)   
                    if hasattr(sprite, "draw_circle_speed"):
                        sprite.draw_circle_speed(draw)
                        sprite.draw_circle_steering_force(draw)                 
            elif self.__speed_is_drawn and self.__steering_force_is_drawn and not self.__circle_is_drawn and not self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, "draw_circle_speed"):
                        sprite.draw_circle_speed(draw)
                        sprite.draw_circle_steering_force(draw)
            elif self.__speed_is_drawn and not self.__steering_force_is_drawn and self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw)                         
                    sprite.draw(draw)
                    if hasattr(sprite, "draw_circle_speed"):
                        sprite.draw_circle_speed(draw)
            elif self.__speed_is_drawn and not self.__steering_force_is_drawn and self.__circle_is_drawn and not self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    sprite.draw(draw)
                    if hasattr(sprite, "draw_circle_speed"):
                        sprite.draw_circle_speed(draw)
            elif self.__speed_is_drawn and not self.__steering_force_is_drawn and not self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw)
                    if hasattr(sprite, "draw_circle_speed"):
                        sprite.draw_circle_speed(draw)
            elif self.__speed_is_drawn and not self.__steering_force_is_drawn and not self.__circle_is_drawn and not self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, "draw_circle_speed"):
                        sprite.draw_circle_speed(draw)
            elif not self.__speed_is_drawn and self.__steering_force_is_drawn and self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw)
                    sprite.draw(draw)
                    if hasattr(sprite, "draw_circle_speed"):
                        sprite.draw_circle_steering_force(draw)
            elif not self.__speed_is_drawn and self.__steering_force_is_drawn and self.__circle_is_drawn and not self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    sprite.draw(draw)
                    if hasattr(sprite, "draw_circle_speed"):
                        sprite.draw_circle_steering_force(draw)
            elif not self.__speed_is_drawn and self.__steering_force_is_drawn and not self.__circle_is_drawn and self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, 'draw_fov'):
                        sprite.draw_fov(draw) 
                    if hasattr(sprite, "draw_circle_speed"):                   
                        sprite.draw_circle_steering_force(draw)
            elif not self.__speed_is_drawn and self.__steering_force_is_drawn and not self.__circle_is_drawn and not self.__fov_is_drawn:
                for sprite in simulation.sprites:
                    if hasattr(sprite, "draw_circle_speed"):
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
                        
            if simulation.selected_entity:
                simulation.selected_entity.draw(draw)
                if hasattr(simulation.selected_entity, "draw_circle_speed"):
                    simulation.selected_entity.draw_circle_speed(draw)                
                    simulation.selected_entity.draw_circle_steering_force(draw)    
                if hasattr(simulation.selected_entity, 'draw_fov'):
                    simulation.selected_entity.draw_fov(draw)
        
            self.__image_tk = ImageTk.PhotoImage(i)
            self.__image_label["image"] = self.__image_tk 
            
    def toggle_draw_fov(self, event):
        self.__fov_is_drawn = not self.__fov_is_drawn
    
    def toggle_draw_circle(self, event):
        self.__circle_is_drawn = not self.__circle_is_drawn
            
    def toggle_draw_steering_force(self, event):
        self.__steering_force_is_drawn = not self.__steering_force_is_drawn

    def toggle_draw_speed(self, event):
        self.__speed_is_drawn = not self.__speed_is_drawn

    def toggle_crazy_mode(self, event):
        self.__crazy_mode = not self.__crazy_mode

    def toggle_jungle_background(self, event):
        self.__jungle_background = not self.__jungle_background

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
        self.__param_selected.set("Red chasing Green")
        self.__options_list = Utils.readfile("scenarios.txt")
        self.__combobox = ttk.Combobox(self, values=self.__options_list, textvariable=self.__param_selected, cursor="hand2", style="TCombobox",state="readonly", width=37)
    
        self.__combobox.pack()
        
    @property
    def param_selected(self):
        return self.__param_selected.get()
        
    @property
    def combobox(self):
        return self.__combobox


class VisualParamPanel(ttk.LabelFrame):
    def __init__(self, title):
        ttk.LabelFrame.__init__(self, root=None, text=title)
        self.__width_var = 28
        self.__speed_var = tk.IntVar()
        self.__speed_checkbutton = ttk.Checkbutton(self, text="Show Speed", variable=self.__speed_var, onvalue=1, offvalue=0, width=self.__width_var)
        self.__speed_checkbutton.pack(padx=(50, 0))
        self.__steering_force_var = tk.IntVar()
        self.__steering_force_checkbutton = ttk.Checkbutton(self, text="Show Steers", variable=self.__steering_force_var, onvalue=1, offvalue=0, width=self.__width_var)
        self.__steering_force_checkbutton.pack(padx=(50, 0))
        self.__show_circle_var = tk.IntVar()
        self.__show_circle_checkbutton = ttk.Checkbutton(self, text="Show Circles", variable=self.__show_circle_var, onvalue=0, offvalue=1, width=self.__width_var)  
        self.__show_circle_checkbutton.pack(padx=(50, 0))
        self.__show_fov_var = tk.IntVar()
        self.__show_fov_checkbutton = ttk.Checkbutton(self, text="Show F-o-V", variable=self.__show_fov_var, onvalue=1, offvalue=0, width=self.__width_var)
        self.__show_fov_checkbutton.pack(padx=(50, 0))
        self.__jungle_background_var = tk.IntVar()
        self.__jungle_background_checkbutton = ttk.Checkbutton(self, text="Jungle background", variable=self.__jungle_background_var, onvalue=1, offvalue=0, width=self.__width_var)
        self.__jungle_background_checkbutton.pack(padx=(50, 0))
        self.__crazy_mode_var = tk.IntVar()
        self.__crazy_mode_checkbutton = ttk.Checkbutton(self, text="Crazy Mode", variable=self.__crazy_mode_var, onvalue=1, offvalue=0, width=self.__width_var)
        self.__crazy_mode_checkbutton.pack(padx=(50, 0))

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

    @property
    def crazy_mode_checkbutton(self):
        return self.__crazy_mode_checkbutton

    @property
    def jungle_background_checkbutton(self):
        return self.__jungle_background_checkbutton


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
        
        self.__gui.main_panel.visual_param_panel.speed_checkbutton.bind('<Button-1>', self.__gui.view_window.toggle_draw_speed)
        self.__gui.main_panel.visual_param_panel.steering_force_checkbutton.bind('<Button-1>', self.__gui.view_window.toggle_draw_steering_force)
        self.__gui.main_panel.visual_param_panel.show_circle_checkbutton.bind('<Button-1>', self.__gui.view_window.toggle_draw_circle)
        self.__gui.main_panel.visual_param_panel.show_fov_checkbutton.bind('<Button-1>', self.__gui.view_window.toggle_draw_fov)
        self.__gui.main_panel.visual_param_panel.crazy_mode_checkbutton.bind('<Button-1>', self.__gui.view_window.toggle_crazy_mode)
        self.__gui.main_panel.visual_param_panel.jungle_background_checkbutton.bind('<Button-1>', self.__gui.view_window.toggle_jungle_background)
        self.__gui.view_window.image_label.bind('<Enter>', self.__simulation.mouse_entered)
        self.__gui.view_window.image_label.bind('<Motion>', self.__simulation.move_mouse)
        self.__gui.view_window.image_label.bind('<Leave>', self.__simulation.mouse_left)
        self.__gui.main_panel.control_panel.start_stop_button.bind('<Button-1>', self.toggle_simulation)
        self.__gui.main_panel.control_panel.next_button.bind('<Button-1>', self.tick_simulation)
        self.__gui.main_panel.control_panel.next_button.bind('<space>', self.tick_simulation)
        self.__gui.main_panel.control_panel.reset_button.bind('<Button-1>', self.reset_simulation)
        self.__gui.main_panel.param_panel.combobox.bind('<<ComboboxSelected>>', self.param_changed)
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
            if clicked_entity is self.__gui.main_panel.info_panel.info_entity:
                self.__gui.main_panel.info_panel.info_entity = None
                self.__simulation.selected_entity = None
            else:
                self.__gui.main_panel.info_panel.info_entity = clicked_entity
                self.__simulation.selected_entity = clicked_entity

    def tick_simulation(self, event=None):
        self.__simulation.tick(time=0.1)
        
    def reset_simulation(self, event=None) -> None:
        key = self.__gui.main_panel.param_panel.param_selected
        self.__gui.main_panel.control_panel.start_stop_button.config(text="Stop")
        self.__gui.main_panel.control_panel.next_button.config(state="disabled")
        self.__simulation.reset(key)
        self.__simulation.selected_entity = None
        self.__gui.main_panel.info_panel.info_entity = None

    def update_info_panel(self):
        self.__gui.main_panel.info_panel.set_text(self.__info_string)

    def tick(self):
        if self.__simulation.is_running:
            self.tick_simulation()
        self.__gui.main_panel.info_panel.update()
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
             
    @property
    def width(self):
        return self.__size.x

    @property
    def height(self):
        return self.__size.y


def main():
    App()


def __main_doctest():
    if bool(__debug__): # do not work
        import doctest
        doctest.testmod()#verbose=True)
def __main_doctest():
    import doctest
    doctest.testmod()#verbose=True)

if __name__ == '__main__':
    __main_doctest()
    main()
