import networkx as nx
from Programs.World import config
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


####################################################################################################################
# define event_tree generating function
# The structure of a tree is uniquely determined by the coordinate of all its leaves thus we generate the
# tree from the leave information in the leave file.
# There are leave files corresponding to different agent categories in the directory.
####################################################################################################################

tree = 'World/event_human_crafting.txt'

def initialize_event_tree(leave_file, show_tree):
    f = open(leave_file)
    line_list = []
    for line in f:
        text = line.strip('\n')
        if len(text) > 0:
            item = eval(text)
            line_list.append(item)
    parallel = line_list[0] # the first line of leave file specify parallel nodes(parallel combination of sub events)
    prob_parallel = line_list[1]  # the 2nd line specify which of the parallel nodes choose child by random assignment
    sub_trees = line_list[2] # the 3rd line specify nodes representing subtree structures, which are connected to other
                            # tree files
    leaves = line_list[3:]  # read the leaves
    tree = {} # store tree information
    depth = 0
    t = nx.DiGraph() # the actual tree object
    for leave in leaves:
        code = leave[-1]
        if depth < len(code):
            depth = len(code)
        if code in sub_trees:
            tree[code] = ['subtree',leave[0],1] # specify the node is a subtree, with leave[0] refering to the address
        else:
            tree[code] = [leave[0], 1]
        for i in range(len(code)-1, -1, -1):
            parent_code = code[:i]
            child_code = code[:i+1]
            if parent_code not in tree:
                if parent_code in parallel:
                    if parent_code in prob_parallel:  # generating tree dictionary which specify type of the node with
                        # initial state 1(unfinished)
                        tree[parent_code] = ['pp', 1]  # probabilistic parallel nodes
                    else:
                        tree[parent_code] = ['op', 1]  # parallel nodes determining child by computing scores
                else:
                    tree[parent_code] = ['s', 1]  # serial nodes
                t.add_edge(parent_code, child_code)
            else:
                t.add_edge(parent_code, child_code)
                break

    for node in t:
        num = t.out_degree(node)
        if num > 0 and tree[node][0] == 's':
            tree[node][1] = len([n for n in t.neighbors(node)]) # set specialized state for serial node, as the number
            # of its children

    if show_tree:
        pos = graphviz_layout(t, prog='dot')
        nx.draw(t, pos, arrows=False, with_labels=True)
        plt.show()

    return tree, t

####################################################################################################################
# The event tree gives the event structure for agnets.
# Each node of the event tree is an event, where the leaves are simple events. The information for the tree is stores
# in a tree dictionary, which get updated as the world is running. The key for the dictionary is the coordinates of the
# nodes, and the values are the corresponding information of the event on that node.
# For simple events, the values is a trinary value: 0,1,or -1. 0 means the event is completed, 1 means the event has not been
# completed, -1 means just failed the event.
# At each time, the agent knows where he/she is on the event tree.
####################################################################################################################


def show_tree_here(tree_file):
    tree, t = initialize_event_tree(tree_file[6:],0) # testing locally requires truncating the directory
    print(tree)
    pos = graphviz_layout(t, prog='dot')
    nx.draw(t, pos, arrows=False, with_labels=True)
    plt.show()


#show_tree_here(tree)