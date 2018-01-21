'''
Created on Apr 20, 2015

Use as an initial pattern level

@author: irma
'''
import argparse
import os
import dblp_network.dblp_experimenter as dblp
import networks.imdb_network as imdb
import networks.facebook_network as fb
import networks.enron_network as enron
import networks.amazon_network as amazon
import yeast_network.yeast_experimenter as yeast
import networks.webKb_Cornell_network as webkb
import graph_manipulator
from graph.nodes import *
from patternGenerator import  generate_pattern
from report_results import directory_manager
import networkx as nx
from graph_manipulator import visualization as vis

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-data_graph',help='path to data file')
    parser.add_argument('-exp',help='yeast,dblp, webkb,imdb,fb,enron,amazon')
    parser.add_argument('-png',default=False,action='store_true',help='whether to make or not a png')
    parser.add_argument('-output',help='output path - path where patterns will be stored (ending with patterns_SIZE')
    parser.add_argument('-pattern_size',type=int,help='desired patterns size')
    parser.add_argument('-data_set_short_label',help='short name for the dataset considered - will be in the name of generated patterns')
    parser.add_argument('-nr_values_max',type=int,default=-1,help='0 or -1: none or all, max number of randvar test values that will be used as labels. The most frequent ones in the data graph will be chosen')

    args = parser.parse_args()
    data_graph=args.data_graph
    final_pattern_size=args.pattern_size
    data_set_short_label=args.data_set_short_label
    nr_randvar_test_values=args.nr_values_max
    
    output_dir=os.path.join(args.output)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    file_containing_parameter_info=os.path.join(output_dir,'patterns.info')
    with open(file_containing_parameter_info,'w') as info_file:
        info_file.write(str(args))
    
    network=None
    labels=[]
    relation_predicates=[]
    if args.exp=='yeast':
        network=yeast.YEAST_GRAPH(data_graph,output_dir,args.nr_values_max)
    if args.exp=='dblp':
        network=dblp.DBLP_GRAPH(data_graph,output_dir)
    if args.exp=='webkb':
        print "Creating WEBKB network"
        network=webkb.WEBKB_Cornell(data_graph,output_dir)
    if args.exp=='imdb':
        print "Creating IMDB network"
        network=imdb.IMDB(data_graph,output_dir)
    if args.exp=='fb':
        print "Creating Facebook network"
        network=fb.Facebook(data_graph,output_dir)
    if args.exp=='enron':
        print "Creating Enron network"
        network=enron.Enron_network(data_graph,output_dir)
    if args.exp=='amazon':
        print "Creating Amazon network"
        network=amazon.Amazon_network(data_graph,output_dir)
        
    labels=network.labels
    relation_predicates=network.relation_labels
    print "Number of labels: ",len(labels)
    for l in labels:
        print l         
    relation_predicate_names=[]
    for r in labels:
        if(isinstance(r,Relation)):
            relation_predicate_names.append(r.predicate)
     
    #create all patterns up to size of initial_pattern_size. This is where we start from        
    patterns=generate_pattern.generate_patterns_up_to_depth_n(labels, final_pattern_size, relation_predicate_names)
    
    directory_manager.write_patterns_in_list(patterns, data_set_short_label, output_dir,args.png)
     