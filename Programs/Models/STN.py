# This module define Stn class
import nltk
import random
import operator
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import time
import pandas
import math
import heatmapcluster
from nltk import WordNetLemmatizer
from nltk.parse.generate import generate
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from operator import itemgetter
from networkx.drawing.nx_agraph import graphviz_layout

VERBOSE = False

############################################################################################

badwords = set(stopwords.words('english'))


#########################################################################################
#########################################################################################

# Global functions used to get the corpus and transform a nested list(tuple) to a tree instance.

#########################################################################################

# read the corpus(parsed) from a txt file.

def get_parsed_corpus(corpus):
    if isinstance(corpus,list):
        parsed_corpus = corpus
    else:
        f = open(corpus)
        parsed_corpus = eval(f.read())
    return parsed_corpus


# for a given nested list, return a copy in tuple data type

def return_tuple(l):
    if flat(l) == 1:
        return tuple(l)
    else:
        return tuple(e if type(e) != list else return_tuple(e) for e in l)


#########################################################################################

# Judge if a list(tuple) is nested

def flat(l):
    t = 1
    for item in l:
        if type(item) == list or type(item) == tuple:
            t = 0
            break
    return t


#########################################################################################

# Given a nested list, return the corresponding tree data structure: including the
# node set and the edge set of the tree. where the nodes are all constituents in the
# nested list, and the edges are subconstituent relations.\

# the complete_tree function just makes sure that it works for the trivial cases
# where the tree is just a word.

def create_tree(x):
    if type(x) == str:
        return [], [x]
    else:
        if type(x) == list:
            x = return_tuple(x)
        edge_set = []
        node_set = []
        for item in x:
            edge_set.append((item, x))
            node_set.append(item)
        if flat(x) == 1:
            return edge_set, node_set
        else:
            for item in x:
                if type(item) == tuple:
                    tem_tree = create_tree(item)
                    edge_set.extend(tem_tree[0])
                    node_set.extend(tem_tree[1])
            return edge_set, node_set


def complete_tree(x):
    if type(x) == str:
        return [], [x]
    else:
        tree = create_tree(x)
        if type(x) == list:
            x = return_tuple(x)
        tree[1].append(x)
        tree1 = (tree[0], tree[1])
        return tree1


#########################################################################################

# transform an nltk POS tag to a wordnet POS tag

def nltk_tag_to_wordnet_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


# get the wordnet pos tag for a word(a string, type:str)
def get_wordnet_tag(word):
    nltk_tag = nltk.pos_tag([word])[0][1]
    wordnet_tag = nltk_tag_to_wordnet_tag(nltk_tag)
    return wordnet_tag



#########################################################################################
#########################################################################################

# This is a function that returns a neighbor (consisting of nodes) of a specified node with an assigned size.
# For example, given a graph G, and a node u in G, and let size be 2, it returns all nodes in G which are up to
# 2 edges away from u.

def get_sized_neighbor_node(G, node, size):
    i = 0
    neighbor_node_dict = {node: 0}
    neighbor_node_list = [node]

    while i < size:
        for node in neighbor_node_dict:
            if neighbor_node_dict[node] == i:
                for neighbor_node in G[node]:
                    neighbor_node_list.append(neighbor_node)
        for node in neighbor_node_list:
            if node not in neighbor_node_dict:
                neighbor_node_dict[node] = i + 1
        i = i + 1

    return neighbor_node_list


#########################################################################################

# Class Syntax tree network, generated by joining parsed trees by shared nodes(constituent)

class Stn:

    def __init__(self, corpus):
        self.freq_threshold = 1
        self.corpus = get_parsed_corpus(corpus)
        self.network = self.get_network()
        self.word_dict = self.network[3]
        self.word_list = [word for word in self.word_dict]
        self.pos_list = ['n', 'v', 'a', 'r', None]
        self.tagged_word = self.get_pos_tag()
        self.diamond_list = self.network[4]
        self.freq_dict = self.network[5]
        self.constituent_net = self.get_constituent_net()
        self.network_type = 'stn'



    #########################################################################################

    # create the networkx Digraph by joining the trees of the corpus.
    # the return consits of the edge set, the node set, and also the networkx graphical object of the network.

    def get_network(self):
        network_edge = []
        network_node = []
        count = 0
        epoch = 0
        start_time = time.time()
        word_dict = {}
        freq_dict = {}
        diamond_list = []
        for sentence in self.corpus:
            tree = complete_tree(sentence)
            if type(sentence) != str:
                diamond_list.append(tree)
            edge_set = tree[0]
            node_set = tree[1]
            for node in node_set:
                if type(node) == str and node not in badwords:
                    if node not in word_dict:
                        word_dict[node] = len(word_dict)
                        freq_dict[node] = 1
                    else:
                        freq_dict[node] = freq_dict[node] + 1

            network_edge.extend(edge_set)
            network_node.extend(node_set)
            count = count + 1
            if count >= 100:
                count = 0
                epoch = epoch + 100
                if VERBOSE:
                    print("{} sentences added to the network.".format(epoch))
        end_time = time.time()
        time_joining_trees = end_time - start_time
        steven = nx.DiGraph()
        network_node_set = set(network_node)
        network_node_list = list(network_node_set)
        network_edge_dict = {}
        for edge in network_edge:
            if edge in network_edge_dict:
                network_edge_dict[edge] = network_edge_dict[edge] + 1
            else:
                network_edge_dict[edge] = 1
        weighted_network_edge = []
        for edge in network_edge_dict:
            weighted_network_edge.append(edge + (math.log10(network_edge_dict[edge]+1),))
        if VERBOSE:
            print()
            print('Weighted Edges:')
            for edge in weighted_network_edge:
                print(network_node_list.index(edge[0]), network_node_list.index(edge[1]), edge)
            print()
        steven.add_weighted_edges_from(weighted_network_edge)
        if VERBOSE:
            print()
            print('{} used to join the trees.'.format(time_joining_trees))
            print()
            print('Nodes in the network:')
            for node in network_node_list:
                print(network_node_list.index(node), node)
            print()
            print(len(word_dict),word_dict)
            print()
        final_freq_dict = {}
        for word in freq_dict:
            if freq_dict[word] >= self.freq_threshold:
                final_freq_dict[word] = freq_dict[word]
        if VERBOSE:
            print(len(final_freq_dict))

        return weighted_network_edge, network_node_list, steven, word_dict, diamond_list, final_freq_dict

    ###########################################################################################

    # get the neighborhood of a node
    # where a 'neighborhood' refers to all the trees containing the given node.

    def get_neighbor_node(self, node):
        neighborhood = [node]
        G = self.network[2]
        if G.out_degree(node) == 0 or type(G.out_degree(node)) != int:
            neighborhood = set(neighborhood)
            return neighborhood
        else:
            count = 1
            while count > 0:
                for n in neighborhood:
                    if G.out_degree(n) > 0:
                        for m in G.successors(n):
                            neighborhood.append(m)
                            if G.out_degree(m) > 0:
                                count = count + 1
                        neighborhood.remove(n)
                        count = count - 1
            real_neighborhood = [1]
            for tree in neighborhood:
                subtree_node = complete_tree(tree)[1]
                real_neighborhood.extend(subtree_node)
            real_neighborhood = set(real_neighborhood)
            real_neighborhood.difference_update({1})
            return real_neighborhood

    ###########################################################################################

    # get all open class words in the network

    # sort the words by default pos tags.

    def get_pos_tag(self):
        pos_dict = {}
        for tag in self.pos_list:
            pos_dict[tag] = []

        for word in self.word_list:
            pos_tag = get_wordnet_tag(word)
            pos_dict[pos_tag].append(word)

        return pos_dict

    ###########################################################################################

    # get the 'highest' node, which have 0 out degree (sentence or clause) in the network.

    ###########################################################################################

    # get the constituent distance between linked word pairs (with a edge)

    # for words next to each other in the constituent net, they have an edge if they are at least
    # co-occur in the same tree. Take all trees (sentences) that they co-occur, the constituent
    # distance betweeen word A and B is the average of all distances on the co-occur trees.

    # In a constituent net, the distance between any two words are defined as follow:
    # 1.If they are not connected, then infinity,
    # 2.If they have an edge, defined as above
    # 3.If they are connected, yet there is no edge between, then the distacne is the length of
    # the weighted shortest path between them, where the weight of an edge is the constituent distances
    # between the word pairs linked by the edge.

    def get_constituent_edge_weight(self):
        l = len(self.word_dict)

        weight_matrix = np.zeros((l, l), float)
        count_matrix = np.zeros((l, l), float)

        count = 0
        epoch = 0
        start_time = time.time()

        for tree_info in self.diamond_list:
            sent_node = tree_info[1]
            sent_edge = tree_info[0]
            sent_words = []
            tree = nx.Graph()
            tree.add_edges_from(sent_edge)
            for node in sent_node:
                if type(node) == str and node not in badwords:
                    sent_words.append(node)

            for word1 in sent_words:
                id1 = self.word_dict[word1]
                for word2 in sent_words:
                    id2 = self.word_dict[word2]
                    if id1 != id2:
                        weight_matrix[id1][id2] = weight_matrix[id1][id2] + .5 ** (
                                    nx.shortest_path_length(tree, word1, word2) - 1)
                        # count_matrix[id1][id2] = count_matrix[id1][id2] + 1

            count = count + 1
            if count >= 100:
                count = 0
                epoch = epoch + 100
                if VERBOSE:
                    print("{} weights added to the weight matrix.".format(epoch))

        end_time = time.time()
        time_get_w_matrix = end_time - start_time
        if VERBOSE:
            print()
            print('{} used to get the weight matrix.'.format(time_get_w_matrix))
            print()

        return weight_matrix, count_matrix

    ###########################################################################################

    # create the constituent-net, which is a lexical netowrks derived from the STN
    # The nodes of the net are the words in STN, while
    # for constituent-net, 2 words are linked if and only if they co-appear in at least one constituent

    def get_constituent_net(self):
        steven_constituent = nx.Graph()
        weight_matrix, count_matrix = self.get_constituent_edge_weight()

        l = len(self.freq_dict)
        freq_list = [word for word in self.freq_dict]

        count = 0
        epoch = 0
        start_time = time.time()

        weight_normalizer = weight_matrix.sum(0)
        # count_normalizer = count_matrix.sum(0)

        for k in range(len(self.word_dict)):
            if weight_normalizer[k] == 0:
                # count_normalizer[k] = count_normalizer[k] + 1
                weight_normalizer[k] = weight_normalizer[k] + 1

        for i in range(l - 1):
            id1 = self.word_dict[freq_list[i]]
            for j in range(i + 1, l):
                id2 = self.word_dict[freq_list[j]]
                w = weight_matrix[i][j] / (weight_normalizer[i] * weight_normalizer[j]) ** .5
                if w > 0:
                    steven_constituent.add_edge(freq_list[i], freq_list[j])
                    count = count + 1
                    if count >= 100:
                        count = 0
                        epoch = epoch + 100
                        if VERBOSE:
                            print("{} edges added to the constituent net.".format(epoch))

        end_time = time.time()
        time_get_C_net = end_time - start_time
        if VERBOSE:
            print()
            print('{} used to get the constituent net.'.format(time_get_C_net))
            print()
        return steven_constituent

    ###########################################################################################

    # showing the neighborhood of a given node

    def get_neighbor(self, node):
        G = self.network[2]
        choice_neighbor = list(self.get_neighbor_node(node))
        choice_net = G.subgraph(choice_neighbor)
        return choice_net

    def show_neighbor(self, word):
        word_neighbor = self.get_neighbor(word)

        nx.draw(word_neighbor, with_labels=True)

    ###########################################################################################

    # showing the sized neighborhood of a given node

    def get_sized_neighbor(self, node, size):
        G = self.network[2].to_undirected()
        choice_neighbor = get_sized_neighbor_node(G, node, size)
        choice_net = G.subgraph(choice_neighbor)
        return choice_net

    def show_sized_neighbor(self, word, size):
        word_neighbor = self.get_sized_neighbor(word, size)

        nx.draw(word_neighbor, with_labels=True)

    ###########################################################################################

    # ploting the STN,
    def plot_network(self):
        steven = self.network[2]
        plt.title('syntax tree network', loc= 'center')
        pos = graphviz_layout(steven, prog='dot')
        edges = steven.edges()
        weights = [steven[u][v]['weight'] for u, v in edges]
        nx.draw(steven, pos, with_labels=True, width = weights)
        plt.show()


    # together with the neighbor-net and the constituent-net
    def plot_lexical_network(self, color_list):
        steven_constituent = self.constituent_net
        plt.title('lexical network with activation dispersion on STN', loc= 'center')
        vmin = min(color_list)
        vmax = max(color_list)
        cmap = plt.cm.cool
        nx.draw(steven_constituent, with_labels=True, node_color=color_list, cmap= cmap, font_color='black')
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
        sm._A = []
        plt.colorbar(sm)


    ###########################################################################################

    # for every word pair, compute the constituent distance between the pair
    # the lengths of all paths between the word pair

    def compute_distance_matrix(self, word_list1, word_list2):
        G = self.constituent_net
        l1 = len(word_list1)
        l2 = len(word_list2)
        distance_matrix = np.zeros((l1, l2), float)

        count = 0
        epoch = 0
        for i in range(l1):
            for j in range(l2):
                pair = [word_list1[i], word_list2[j]]
                if nx.has_path(G, pair[0], pair[1]):
                    distance = nx.shortest_path_length(G, pair[0], pair[1])
                else:
                    distance = np.inf
                distance_matrix[i][j] = round(distance, 3)

                count = count + 1
                if count >= 5:
                    count = 0
                    epoch = epoch + 5
                    print("{} pairs of distance caculated".format(epoch))

        table = pandas.DataFrame(distance_matrix, word_list1, word_list2)
        return table, distance_matrix

    def compute_similarity_matrix(self, word_list, neighbor_size):
        G = self.network[2].to_undirected()
        l = len(word_list)
        graph_list = []
        for word in word_list:
            g = self.get_sized_neighbor(word, neighbor_size)
            graph_list.append(g)
            # print(word, g.nodes)
            # print()

        similarity_matrix = np.zeros((l, l), float)
        for i in range(l):
            for j in range(i, l):
                similarity_matrix[i][j] = round(1 / (1 + nx.graph_edit_distance(graph_list[i], graph_list[j])), 3)
                # print(word_list[i],word_list[j],similarity_matrix[i][j])

        table = pandas.DataFrame(similarity_matrix, word_list, word_list)
        return table, similarity_matrix


############################################################################################

# Class Distributional graph, generated by joining linear sentence sequence by shared words

class Dg:

    def __init__(self, linear_corpus):
        self.freq_threshold = 1
        self.linear_corpus = linear_corpus
        self.network = self.get_graph()
        self.network_type = 'linear_doug'

    def get_graph(self):
        network_edge = []
        network_node = []
        diamond_list = []
        count = 0
        epoch = 0
        start_time = time.time()
        word_dict = {}
        freq_dict = {}
        for sentence in self.linear_corpus:
            node_set = sentence
            edge_set = []
            l = len(sentence)
            for i in range(l-1):
                edge_set.append((node_set[i],node_set[i+1]))
            for node in node_set:
                if node not in word_dict:
                    word_dict[node] = len(word_dict)
                    freq_dict[node] = 1
                else:
                    freq_dict[node] = freq_dict[node] + 1
            network_edge.extend(edge_set)
            network_node.extend(node_set)
            count = count + 1
            if count >= 1000:
                count = 0
                epoch = epoch + 1000
                if VERBOSE:
                    print("{} sentences added to the linear graph.".format(epoch))
        end_time = time.time()
        time_joining_trees = end_time - start_time
        linear_doug = nx.Graph()
        network_node_set = set(network_node)
        network_node_list = list(network_node_set)
        network_edge_dict = {}
        for edge in network_edge:
            if edge in network_edge_dict:
                network_edge_dict[edge] = network_edge_dict[edge] + 1
            else:
                network_edge_dict[edge] = 1
        weighted_network_edge = []
        for edge in network_edge_dict:
            weighted_network_edge.append(edge + (math.log10(network_edge_dict[edge] + 1),))
        if VERBOSE:
            print()
            print('Weighted Edges:')
            for edge in weighted_network_edge:
                print(network_node_list.index(edge[0]), network_node_list.index(edge[1]), edge)
            print()
        linear_doug.add_weighted_edges_from(weighted_network_edge)
        if VERBOSE:
            print()
            print('{} used to join the trees.'.format(time_joining_trees))
            print()
        final_freq_dict = {}
        for word in freq_dict:
            if freq_dict[word] >= self.freq_threshold:
                final_freq_dict[word] = freq_dict[word]
        if VERBOSE:
            print(len(final_freq_dict))

        return weighted_network_edge, network_node_list, linear_doug, word_dict, diamond_list, final_freq_dict

    def plot_lexical_network(self, color_list):
        linear_doug = self.network[2]
        plt.title('lexical network with activation dispersion on distributional graph', loc= 'center')
        vmin = min(color_list)
        vmax = max(color_list)
        cmap = plt.cm.cool
        nx.draw(linear_doug, with_labels=True, node_color=color_list, cmap= cmap)
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
        sm._A = []
        plt.colorbar(sm)