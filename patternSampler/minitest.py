from sampler_general_ex import *
import OBDsearch
import time
import os
import pickle
import numpy
import random
import networkx as nx # @UndefinedVariable
import sampling_utils as su # @UndefinedVariable
import extend_sample
import visualization as vs
  
  
graph_file_name = "DBLP_2001-2_discretized.gpickle"
pattern_file_name = "patternD9.gml"

objects = ['protein']
relations = ['interaction']
attributes =  ['location',  'function',  'phenotype',  'complex', 'protein_class',  'enzyme']

Yeast=nx.read_gpickle("YEAST.gpickle")

P=nx.MultiGraph()
obj = random.choice(objects)    # we start with one object
print "Random object",obj
P.add_node(0,predicate=obj,label=obj,target=0)
NewP=extend_sample.extend_sample(P, objects, relations, attributes)
vs.visualize_graph(Yeast)

#OBdecomp = OBDsearch.get_heuristic4_OBD(P, startNode = 0)
#print OBdecomp
print "Finished."

