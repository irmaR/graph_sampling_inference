'''
Created on Mar 16, 2015

@author: irma
'''
import generate_pattern
import report_results 
import os
from graph.nodes import * 

def generate_and_write_N_patterns_to_files(path_to_writing,current_level_patterns,current_depth,labels,N,relation_predicate_names):
    extended_patterns=generate_pattern.generate_patterns_of_depth_n(labels,current_level_patterns,current_depth+1)
    #randomly choose N patterns
    #indices=random.sample(range(1, len(pattern_list)), N)
    
    
def initialize_experiment(path_to_writing,initial_level,labels,relation_predicate_names):
    #generate patterns for initial level
    patterns=generate_pattern.generate_patterns_up_to_depth_n(labels, initial_level, relation_predicate_names) 
    #write the patterns in the files
    report_results.directory_manager.write_patterns_in_list(patterns, 'yeast', path_to_writing)
    


if __name__ == '__main__':  
    new_node_protein=Object_class({'label':'protein','predicate':'protein','target':0})
    new_node_interaction=Relation({'label':'interaction','predicate':'interaction','target':0},new_node_protein,new_node_protein)
    new_node_function=Attribute({'label':'function','predicate':'function','target':0},new_node_protein)
    new_node_location=Attribute({'label':'location','predicate':'location','target':0},new_node_protein)
    
    
    
    
       