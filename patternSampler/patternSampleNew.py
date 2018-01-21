
# from sampler_general_ex import *
# import OBDsearch
import time
import os
import pickle
import json
import numpy
import networkx as nx # @UndefinedVariable
#import sampling_utils as su
import matplotlib.pyplot as plt
import random
from scipy import stats


def writepattern_GML(G,  filename):
    f = open(filename, 'w')
    f.write("graph [\n")
    for n in G.nodes():
        f.write("node [\n")
        f.write("node [\n")
        
##########    id 0
##########    label "references"
##########    predicate "references"
##########    target 0
##########    valueinpattern 0
        
        pass
    
    f.write("]\n")
    f.close()

def enlarge_pattern(G, objects,  relations,  attributes,  size):
    if  len(G.nodes()) == 0:     #initial state --- empty graph
        id = 0      # initial id
        obj = random.choice(objects)    # we start with one object
        if size > 0:
            G.add_node(id,  predicate=obj,  label=obj,  target=0)
    else:   # increase of the pattern graph from a random object
        #--------- determining the extension point
        all_object_nodes = [x for x in G.nodes() if G.node[x]['predicate'] in objects]
        extension_node = random.choice(all_object_nodes)
        #----------------------------------------------------------
        #--------- creating extension
        id = max(G.nodes()) + 1     # id is always just increased by 1
        newnode = random.choice(objects + attributes)    # random pick from objects and attributes
        if newnode in objects:     # object is connected to an object only through a relation, so it has to be added as well
            relation = random.choice(relations)
            if len(G.nodes()) < size:
                G.add_node(id+1,  predicate=relation,  label=relation,  target=0)   # relation node added
                G.add_edge(extension_node, id+1)     # connect pattern with relation node
            if len(G.nodes()) < size:
                G.add_node(id,  predicate=newnode,  label=newnode,  target=0)   # new object node added
                G.add_edge(id+1,  id)       # connect relation to new object node
        else:   # new node is attribute --- simpler case
            if len(G.nodes()) < size:
                G.add_node(id,  predicate=newnode,  label=newnode,  target=0)   # new object node added
                G.add_edge(extension_node,  id)       # connect selected existing object node to the new attribute node



# ---- MAIN ----

size = 5    # this is the size of the generated random pattern (this limit is strictly respected)
mode = 'YEAST'
objects = None; relations = None; attributes = None
if mode == 'YEAST':
    objects = ['protein']
    relations = ['interaction']
    attributes =  ['location',  'function',  'phenotype',  'complex', 'protein_class',  'enzyme']
elif mode == 'DBLP':
    pass # do it later for DBLP also!

G=nx.MultiGraph()
while len(G.nodes()) < size:
    enlarge_pattern(G, objects,  relations,  attributes,  size)


plotlabels = {}     # dictionary of labels - for plotting
for n in G.nodes():
    plotlabels[n] = G.node[n]['label']
#drawing with pyplot
nx.draw_networkx(G, labels = plotlabels,  node_size=1000,  alpha=0.3,  node_color='blue')
nx.draw(G)
nx.draw(G,pos=nx.spring_layout(G))
plt.show()
#plt.axis('off')
#plt.savefig('YEAST_pattern_test.png')
#plt.savefig('YEAST_pattern_test.pdf')
#plt.close()
print "done."





