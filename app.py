from tkinter import ttk, Tk
from abc import abstractmethod
import math
from PIL import Image, ImageTk, ImageDraw
from vect2d import Vect2D


## Vue ##

class GUI(Tk):
    def __init__(self, control_panel, param_panel, view_window, size:tuple):
        self.__control_panel = control_panel
        self.__param_panel = param_panel
        self.__view_window = view_window
        self.__width = size[0]
        self.__height = size[1]
    
    # GUI getters #    
    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

class App(GUI):
    def __init__(self):
        pass

class ControlPanel(GUI):
    def __init__(self):
        pass

    
class StartStopPanel(ControlPanel):
    def __init__(self):
        pass

class ViewWindow(GUI):
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

class ParamPanel(GUI):
    def __init__(self):
        pass

class VisualParamPanel(ParamPanel):
    def __init__(self):
        pass

class SimParamPanel(ParamPanel):
    def __init__(self):
        pass    



## Modele ##
class Simulation(App):
    def __init__(self):
        pass

class Drawable():
    def __init__(self):
        pass

    @abstractmethod
    def draw(self):
        pass


class Circle():
    def __init__(self, position, color, radius):
        self.__position = position
        self.__color = color
        self.__radius = radius


class StaticCircle(Circle):
    def __init__(self):
        pass
    
class Movable():
    def __init__(self):
        pass
    
class DynamicCircle(Circle, Movable):
    def __init__(self, vitesse, vitesse_max):
        self.__vitesse = vitesse
        self.__vitesse_max = vitesse_max
    
class Piloted(DynamicCircle):
    def __init__(self):
        pass



    @abstractmethod
    def move(self):
        pass

class Updatable():
    def __init__(self):
        pass

    @abstractmethod
    def tick(self):
        pass






def main():
    GUI()


if __name__ == '__main__':
    main()