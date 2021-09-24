
class Entity:
####################################################################################################################
# define Entity, which locates at a place in the world
####################################################################################################################
    def __init__(self, world):
        self.world = world
        self.x = None
        self.y = None
        self.region = None # which region is the entity located
        self.map = world.world_map

    def get_region(self):
        entity_region = ''
        for region in self.map:
            region_range = self.map[region]
            left_boundary = region_range[0][0] * self.world.world_size
            right_boundary = region_range[0][1] * self.world.world_size
            bottom_boundary = region_range[1][0] * self.world.world_size
            top_boundary = region_range[1][1] * self.world.world_size
            if self.x >= left_boundary and self.x < right_boundary and \
                self.y >= bottom_boundary and self.y < top_boundary:
                entity_region = region
                break
        return entity_region