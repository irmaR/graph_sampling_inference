'''
Created on Apr 21, 2015

@author: irma
'''
import argparse
import os
import yeast_network.yeast_experimenter as yeast
import graph_manipulator
from graph.nodes import *
from patternGenerator import  generate_pattern
from report_results import directory_manager
import dblp_network.dblp_experimenter as dblp
import patternGenerator.generate_pattern as gen_pat
import networks.webKb_Cornell_network as webkb
import networks.imdb_network as imdb
import networks.facebook_network as fb
import networks.enron_network as enron
import networks.amazon_network as amazon


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-data_graph',help='path to data file')
    parser.add_argument('-output',help='output path - you have to specify exactly which directory or batch it is. not created by itself')
    parser.add_argument('-exp',help='yeast or dblp')
    parser.add_argument('-png',default=False,action='store_true',help='whether to make or not a png')
    parser.add_argument('-patterns_previous_level',help='path! patterns from previous level')
    parser.add_argument('-previous_level',type=int,help='number of previous level (nr nodes)')
    parser.add_argument('-create_batches',default=True,action='store_false',help='')
    parser.add_argument('-data_set_short_label',help='short name for the dataset considered - will be in the name of generated patterns')
    parser.add_argument('-nr_values_max',type=int,default=-1,help='max number of randvar test values that will be used as labels. The most frequent ones in the data graph will be chosen')
    parser.add_argument('-N',type=int,default=400,help='select N patterns for a batch (batch size)')

    
    args = parser.parse_args()
    data_graph=args.data_graph
    path_to_previous_level=args.patterns_previous_level
    previous_level_size=args.previous_level
    final_pattern_size=previous_level_size+1
    #max_sampled_patterns=args.max_sampled_patterns
    #max_number_heads=args.max_heads
    #max_number_target_predicates=args.max_target_predicates
    data_set_short_label=args.data_set_short_label
    nr_randvar_test_values=args.nr_values_max
    
    output_dir=args.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    file_containing_parameter_info=os.path.join(output_dir,'patterns_at_'+str(final_pattern_size)+'.info')
    with open(file_containing_parameter_info,'w') as info_file:
        info_file.write(str(args))
    
        network=None
    labels=[]
    relation_predicates=[]
    if args.exp=='yeast':
        print "CREATING YEAST GRAPH"
        network=yeast.YEAST_GRAPH(data_graph,output_dir,args.nr_values_max)
    if args.exp=='dblp':
        network=dblp.DBLP_GRAPH(data_graph,output_dir)
    if args.exp=='webkb':
        print "Creating WEBKB network"
        network=webkb.WEBKB_Cornell(data_graph,output_dir)
    if args.exp=='imdb':
        print "Creating IMDB network"
        network=imdb.IMDB(data_graph,output_dir)
    if args.exp=='facebook':
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
    graphs_n_minus_1=directory_manager.load_graphs_in_folder(network,path_to_previous_level)   
    print "Number of labels: ",len(labels)
    hist=graph_manipulator.graph_analyzer.get_sorted_labels_by_occurence_frequency_in_graph(data_graph)
    print "HIST:",hist
    relation_predicate_names=[]
    for r in labels:
        if(isinstance(r,Relation)):
            relation_predicate_names.append(r.predicate)
             
            
    #create all patterns up to size of initial_pattern_size. This is where we start from
    patterns=generate_pattern.generate_patterns_of_depth_n_version_2(labels,graphs_n_minus_1,final_pattern_size,relation_predicate_names,output_dir,args.create_batches,args.N)
    print "WRITING: ",len(patterns),"patterns"
    
    directory_manager.write_patterns_in_list(patterns, data_set_short_label, output_dir,args.png)
     