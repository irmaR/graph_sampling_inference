'''
Created on Feb 9, 2015

@author: irma
'''
import random

#returns 
def extend_sample(graph,objects,  relations,  attributes):
    newgraph=enlarge_pattern(graph,objects,relations,attributes)
    return newgraph
    
    

def enlarge_pattern(G, objects,  relations,  attributes):
    if  len(G.nodes()) == 0:     #initial state --- empty graph
        id = 0      # initial id
        obj = random.choice(objects)    # we start with one object
        G.add_node(id,  predicate=obj,  label=obj,  target=0)
    else:   # increase of the pattern graph from a random object
        #--------- determining the extension point
        all_object_nodes = [x for x in G.nodes() if G.node[x]['predicate'] in objects]
        print "existing objects",all_object_nodes
        print "attributes",attributes
        extension_node = random.choice(all_object_nodes)
        #----------------------------------------------------------
        #--------- creating extension
        id = max(G.nodes()) + 1     # id is always just increased by 1
        newnode = random.choice(objects + attributes)    # random pick from objects and attributes
        print "New node",newnode
        if newnode in objects:     # object is connected to an object only through a relation, so it has to be added as well
            relation = random.choice(relations)
            G.add_node(id+1,  predicate=relation,  label=relation,  target=0)   # relation node added
            G.add_edge(extension_node, id+1)     # connect pattern with relation node
            G.add_node(id,  predicate=newnode,  label=newnode,  target=0)   # new object node added
            G.add_edge(id+1,  id)       # connect relation to new object node
        else:   # new node is attribute --- simpler case
                G.add_node(id,  predicate=newnode,  label=newnode,  target=0)   # new object node added
                G.add_edge(extension_node,  id)       # connect selected existing object node to the new attribute node
        return G