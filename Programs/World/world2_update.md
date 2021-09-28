# world2 update made

## Sub event tree structure

Update: Some of the sub event trees are represented by one node in the parent tree file, with the tree
structure expanded in a separate subtree file.

In the older version, every agent (category) had the tree structure in one single text file, and the tree
structure is generated from the file whenever needed. As the event structure of agents (mostly humans)
become more and more complex in the future versions, it will become difficult to encode the events within
one single tree file (as the num of layer grows, the coordinates of nodes are becoming longer and longer).

Therefore, a recursively organized set of tree text files are constructed. Complicated substructures in
a tree file are replaced by one single node, which will be expanded (showing the exact structure) in a
separate file. The name of the sub-event node will be the directory of the sub-event text file.

A subtree file 'event_human_hunting.txt' is created, replacing the hunting subtree in the original 
'event_structure_human.txt'

## Entity taxonomy

Update: more entities are added to the world, and a hierarchical taxonomy of all entities is created.

In the older version, the entities of the world are not well organized, but in the future versions,
as there will be more and more entities added to the world, it is better to have a taxonomy of the
entities as a general set up, with new entities added to the taxonomy when added to the world.

Currently, due to the need of world 2, Instrument class is added, which contain two sub-classes:
Appliance and Tool, which both fill in the 'instrument' slot in an event structure. The current taxonomy
is:

Entity(Agent, Plant_resource, Material, Instrument)

Agent(Animal, Human)/ Plant_resource(Fruit, Nut, Plant)/ Material(Stone, Wood, Hay)/ Instrument(Tool, Appliance)

Animal(Carnivore, Herbivore)

Herbivore(Herb_s, Herb_m, Herb_l)


## World Map

Update: a world map is created and divided into regions, so that each entity has a location (coordinate, 
region) in the world. 


## Crafting and Collecting:

Update: two new subtree files: 'event_human_collecting.txt' and 'event_human_crafting.txt' are created 
accounting for more human activities in world 2.

Currently, these two events have relatively simple structure. In collecting, one have decided what to collect
therefore just goes to the place, conducts the collecting action (cracking stone, chopping wood, cutting tree),
and then gathers; and in crafting, one have decided what to make, and then go through the purely serial procedure,
which have three variations according to the tool to make. The structure of these event are preliminary and subject 
to changes.


# General goal of world 2 update

Wolrd 2 is set up to produce sentences with adjunct argument such as instrument and location (place). To
achieve this, instruments and locations are needed to be incorporated in the world. 

And more generally, as the world is growing more and more complicated, a considerably sophisticated infrastructure
of the world is needed, so that future developers may flexibly generalize and evolve the world (with regard
to respective research interests) with new add-ons, with minimal update on the infrastructure. 

 

 