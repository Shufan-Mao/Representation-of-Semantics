import random
import numpy as np
from Programs.World import config
from Programs.World.entity import Entity


class Plant_resource(Entity):

    ####################################################################################################################
    # define plant_resource class, now including 3 subclasses: Plant (eaten by herbivores); Nut and Fruit (eaten by
    # human)

    # A plant is an object, that produce plant resource. The resource can be collected, and the object never die. The
    # plant grows so that resources are accumulated, and once collected/consumed by agents, the amount of the resource
    # decrease, yet it recovers, as time pass by.

    # all plant item has a 'size', it stops growing once the size is reached
    ####################################################################################################################

    def __init__(self, world):
        Entity.__init__(self,world)
        self.type = 'plant_r'
        self.size = random.randint(1000,2000)
        self.remain_size = self.size
        self.gather_size = 0
        self.category = None
        self.x = random.randint(-config.World.world_size/5, config.World.world_size/5)
        self.y = random.randint(-config.World.world_size/5, config.World.world_size/5)

    def grow(self):
        rate = self.world.grow_rate[self.category]
        self.remain_size = self.remain_size + rate * self.size
        if self.remain_size > self.size:
            self.remain_size = self.size

class Plant(Plant_resource):
    def __init__(self, world):
        Plant_resource.__init__(self,world)
        self.plant_type = 'plant'
        self.category = str(np.random.choice(self.world.plant_taxo[self.plant_type], 1, p=[0.33, 0.33, 0.34])[0])
        self.id_number = len(self.world.plant_list)

class Nut(Plant_resource):
    def __init__(self, world):
        Plant_resource.__init__(self,world)
        self.plant_type = 'nut'
        self.category = str(np.random.choice(self.world.plant_taxo[self.plant_type], 1, p=[0.33, 0.33, 0.34])[0])
        self.id_number = len(self.world.nut_list)

class Fruit(Plant_resource):
    def __init__(self, world):
        Plant_resource.__init__(self,world)
        self.plant_type = 'fruit'
        self.category = str(np.random.choice(self.world.plant_taxo[self.plant_type], 1, p=[0.33, 0.33, 0.34])[0])
        self.id_number = len(self.world.fruit_list)


class Instrument:
    ####################################################################################################################
    # define instrument class, now including 2 subclasses: Tool (eaten by herbivores); Appliance (eaten by
    # human)

    # An instrument can be either a tool or an appliance, which accumulates 'damages' while being used. An instrument
    # will be discarded when the damage reach 1.

    ####################################################################################################################
    def __init__(self, world):
        self.world = world
        self.type = None
        self.category = None
        self.damage = 0

class Tool(Instrument):
    ####################################################################################################################
    # a tool is an instrumment that may only be used by one individual(at a time), it is usually small, and can be
    # carried

    ####################################################################################################################
    def __init__(self, world, category):
        Instrument.__init__(self,world)
        self.category = category
        self.size = self.world.tool_size[category]
        self.id_number = len(self.world.tool_list)


class Appliance(Instrument):
    ####################################################################################################################
    # a tool is an instrumment that may only be used by one individual(at a time), it is usually small, and can be
    # carried

    ####################################################################################################################
    def __init__(self, world, category):
        Instrument.__init__(self,world)
        self.category = category
        self.id_number = len(self.world.appliance_list)