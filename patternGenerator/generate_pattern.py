import networkx as nx
import copy
from graph_manipulator import visualization as vis
import networkx.algorithms.isomorphism as iso
import itertools
from graph.nodes import * 
import os
import unittest
import random
import numpy
import pickle
import time
import sys


"""This is a method that given a list of possible labels in patterns
generates patterns up to depth n starting from the graphs of size n-1. Restrictions say when certain 
nodes cannot connect. For example, interaction cannot connect to only one
node (protein), but represents connection between two proteins.
also, some attributes (like, phenotype) can only be connected to proteins and
not other possible objects """
def generate_patterns_of_depth_n(nodes,graphs_n_minus_1,depth,relation_predicate_names,max_number_heads,max_sampled_patterns,max_number_target_predicates):
   all_graphs=[]
   previous_graphs=graphs_n_minus_1
   d_depth_graphs=[]
   number_of_graphs=len(previous_graphs)
   print "Need to extend: ",number_of_graphs
   counter=1
   for prev_graph in previous_graphs:    
       print "Extending: ",counter,"th out of ",number_of_graphs
       counter+=1
       d_depth_graphs.extend(get_all_d_depth_extensions(prev_graph,nodes))
       print "Removing isomophic of: ",len(d_depth_graphs)," graphs"         
       previous_graph=remove_isomorphic_graphs(d_depth_graphs)
   previous_graph=remove_invalid_graphs(previous_graph,relation_predicate_names)
   resulting_graphs=[]
   for pattern in previous_graph:
        if(len(pattern.nodes())==1):
            resulting_graphs.append(pattern)
            continue
        else:      
            heads=randomly_sample_up_to_n_heads(max_number_heads, pattern)
            if(len(heads)==0):
                resulting_graphs.append(pattern) 
 
            for head in heads:
                annotated_patterns=sample_dependencies_in_the_patterns(pattern, pattern.node[head], head,max_sampled_patterns,max_number_target_predicates)
                resulting_graphs.extend(annotated_patterns)
   print "Finished sampling dependencies in the graph... resulted in ",len(resulting_graphs),"graphs of size",len(resulting_graphs[0].nodes())
   return resulting_graphs

"""This is a method that given a list of possible labels in patterns
generates patterns up to depth n starting from the graphs of size n-1. Restrictions say when certain 
nodes cannot connect. For example, interaction cannot connect to only one
node (protein), but represents connection between two proteins.
also, some attributes (like, phenotype) can only be connected to proteins and
not other possible objects """
def generate_patterns_of_depth_n_version_2(nodes,graphs_n_minus_1,depth,relation_predicate_names,output_path,flag_randomly_sample,select_N_patterns):
   if(len(graphs_n_minus_1)==0):
       raise Exception(" No graphs loaded from previous level!!")
   print "Number of graphs from the previous version: ",len(graphs_n_minus_1)
   all_graphs=[]
   previous_graphs=graphs_n_minus_1
   d_depth_graphs=[]
   number_of_graphs=len(previous_graphs)
   print "Need to extend: ",number_of_graphs, "from level: "
   counter=1
   for prev_graph in previous_graphs:    
       print "Extending: ",counter,"th out of ",number_of_graphs
       counter+=1
       d_depth_graphs.extend(get_all_d_depth_extensions(prev_graph,nodes))
   previous_graph=d_depth_graphs
   print "Nr graphs: ",len(previous_graph)
   resulting_graphs=remove_invalid_graphs(previous_graph,relation_predicate_names)
   #sample dependencies
   #resulting_graphs=sample_dependencies(previous_graph_double_edges,previous_graph,max_number_heads,max_sampled_patterns,max_number_target_predicates)
   print "Number of resulting graphs: ",len(resulting_graphs)
   print "Selecting: ",select_N_patterns,"patterns"
   
   #If the randomly sample flag is set, or the number of resulting graphs is bigger than 1000 then create batches
   if flag_randomly_sample==True:
      if len(resulting_graphs)>=select_N_patterns: #if we want to create batches of 1000 graphs, than do it. And pickle the rest!
          print "Sampling ...."
          result,the_rest=randomly_sample_N_non_isomorphic_patterns(resulting_graphs,select_N_patterns) #PROMIJENI OVDJE UPOZORENJE
          print "Need to pickle! Too large to detect isomorphisms"
          print "The rest: ",len(the_rest)
          with open(output_path+'/all_patterns_'+str(depth)+'.pickle','w') as f:
            pickle.dump(the_rest,f)
          print "Pickling finished..."
          print "Resulting graphs ",len(result)
          return result
      else: #else,  return all resulting graphs
          print "DON't sample : just return all non isomorphic"
          result,smth_else=remove_isomorphic_graphs_version2(resulting_graphs)
   else:
       result,smth_else=remove_isomorphic_graphs(resulting_graphs)
   
    
   return result


def sample_dependencies(graphs,previous_graph,max_number_heads,max_sampled_patterns,max_number_target_predicates):
    counter=1
    resulting_graphs=[]
    for pattern in graphs: #PROMIJENI OVDJE UPOZORENJE
        print "processing ",counter,' th pattern from ',len(previous_graph),'graphs'
        counter+=1
        if(len(pattern.nodes())==1):
            resulting_graphs.append(pattern)
            continue
        else:    
            heads=[]
            for node in pattern.nodes():
                if 'head' in pattern.node[node]:
                    heads.append(node)    
            heads.extend(randomly_sample_up_to_n_heads(max_number_heads, pattern,node))  
            if len(heads)==0:
                resulting_graphs.append(pattern)
                continue      
            for head in heads:
                annotated_patterns=sample_dependencies_in_the_patterns(pattern, pattern.node[head], head,max_sampled_patterns,max_number_target_predicates)
                resulting_graphs.extend(annotated_patterns)
                if len(annotated_patterns)==0:
                    resulting_graphs.append(pattern)
    return resulting_graphs


"""This is a method that given a list of possible labels in patterns
generates patterns up to depth n."""
def generate_patterns_up_to_depth_n(nodes,depth,relation_predicate_names):
   size_1_graphs=initialize_graph_generator_procedure(nodes) 
   previous_graph=size_1_graphs
   previous_size_of_patterns=0
   if(depth==1):
        return size_1_graphs
   for d in range(1,depth):  
       d_depth_graphs=[]
       previous_size_of_patterns=len(previous_graph)
       print "Extending: ",len(previous_graph),"graphs"
       for index,prev_graph in enumerate(previous_graph):
           d_depth_graphs.extend(get_all_d_depth_extensions(prev_graph,nodes))
           previous_graph=d_depth_graphs
           print "Extension made: ",len(d_depth_graphs),"graphs"
           #print "Non-isomorphic graphs: ",len(previous_graph)
           #print "Finished extending :",index,"th graph of size",len(previous_graph[0].nodes())," out of ",previous_size_of_patterns    
   
   previous_graph_isomorph,rest=remove_isomorphic_graphs_version2(d_depth_graphs)
   print "Isomorphic graphs removed...."
   print "number of graphs to handle: ",len(previous_graph_isomorph)
   for g in previous_graph_isomorph:
       print "graph"
       for n in g.nodes():
           print g.node[n]
   previous_graph_double_edge=remove_invalid_graphs(previous_graph_isomorph,relation_predicate_names)
   #previous_graph_double_edge=previous_graph_isomorph
   print "Graphs where relation nodes not properly connected removed.... resulted in: ",len(previous_graph_double_edge)
   print "Resulting graphs: ",len(previous_graph_double_edge)
   #print "Finished sampling dependencies in the graph... resulted in ",len(resulting_graphs),"graphs of size",len(resulting_graphs[0].nodes())
   return previous_graph_double_edge


def randomly_sample_N_non_isomorphic_patterns(pattern_list,N):
    '''
    Randomly sample N (with replacement) patterns from the patterns list
    return:
    - updated pattern list (without the sampled patterns)
    - list of sampled patterns
    '''
    print "NUMBER OF PATTERNS TO SAMPLE FROM :",len(pattern_list)
    new_list=copy.deepcopy(pattern_list)
    random.shuffle(new_list)
    added_samples_non_isomorphic=[]
    counter=0
    the_rest=[]
    while True:
        print "ALREADY ADDED SAMPLES: ",len(added_samples_non_isomorphic)
        #add new patterns in the list for removing isomoprhic graphs
        cutoff=new_list[counter:counter+N]   
        the_rest=new_list[counter+N:]
        #remove isomorphic from cutoff
        if cutoff==[]:
            return remove_isomorphic_graphs_version2(new_list)[0],[]
        cutoff.extend(added_samples_non_isomorphic)
        added_samples_non_isomorphic,filtered_out_indices=remove_isomorphic_graphs_version2(cutoff)
        if len(added_samples_non_isomorphic)>=N:
            the_rest.extend(added_samples_non_isomorphic[N:])
            return added_samples_non_isomorphic[0:N],the_rest
        else:
            counter+=N
            
"""Calculate the number of edges in an undirected graph for a given number of nodes"""
def get_number_of_edges_in_undirected_graph(number_of_nodes):
    return number_of_nodes*(number_of_nodes-1)/2

"""Given a current graph of depth-1, possible labels and desired depth, get all possible extensions"""
def get_all_d_depth_extensions(current_graph,labels):
    #if isinstance(current_graph, pattern):
    #        current_graph=current_graph.graph
    number_of_edges=get_number_of_edges_in_undirected_graph(len(current_graph.nodes())+1)
    #print "Number of possible edges: ",number_of_edges
    tmp=[]
    for node in labels:
           new_node=copy.deepcopy(node)
           #check if node can be the target: if yes, make it a target (SKIPPING SAMPLING)!
           #print "**********************************************************\n"
           #print "Can this new node be a target: ",new_node.can_be_target()
           if new_node.can_be_target():
                new_node.setTarget()
           #time.sleep(2)
           for nr_edges in range(0,number_of_edges):  
                print "Adding for: ",nr_edges+1  
                new_node.setId()
                extended_patterns=make_n_edges_with_nodes_in_the_graph(current_graph,new_node,nr_edges+1)
                print "RESULTS IN PATTERNS: ",len(extended_patterns)
                #for e in extended_patterns:
                #    for n in e.nodes():
                #        print e.node[n]
                #time.sleep(2+2*len(extended_patterns))
                #print "Extended patterns: ",len(extended_patterns),vis.visualize_multiple_graphs(extended_patterns),"existing: ",vis.visualize_multiple_graphs(tmp)
                #filtered_patterns=get_non_isomorphic_graph_already_added(extended_patterns,tmp)
                tmp.extend(extended_patterns) 
                  
    return tmp

"""Make all possible number_of_edges edges of the new_node to the other nodes in the graph"""
def make_n_edges_with_nodes_in_the_graph(graph,new_node,number_of_edges):  
    tmp=[]
    nodes=graph.nodes()
    subsets=list(itertools.combinations(nodes, number_of_edges))
    print "subsets: ",subsets
    for subs in subsets:
        new_graph=nx.Graph()
        #I know it's stupid, but I put parent's path into this variable "name". Remember that
        new_graph.name=graph.name
        new_graph=copy.deepcopy(graph)
        if allowed_to_connect_to_all_nodes(subs,new_node,graph):
            for node in subs:
                if isinstance(new_node,Randvar_value_test):
                 new_graph.add_node(new_node.id,value=new_node.value,label=new_node.label,predicate=new_node.predicate,target=new_node.target,type=new_node,valueinpattern=new_node.value_in_pattern)
                else:
                 new_graph.add_node(new_node.id,label=new_node.label,predicate=new_node.predicate,target=new_node.target,type=new_node,valueinpattern=new_node.value_in_pattern)
                new_graph.add_edge(node,new_node.id)
                tmp.append(new_graph)          
    return tmp       

'''
Check if the new node is allowed to connect to all the nodes in the subset of the graph
'''
def allowed_to_connect_to_all_nodes(subs,new_node,graph):
    tmp=True
    for node in subs:
        if(not(new_node.is_allowed_to_connect(node,graph.node[node]['type'],graph))):
            return False
    return tmp


def get_non_isomorphic_graph_already_added(extended_patterns,tmp):
    nm = iso.categorical_node_match('label', 'label')
    indices_for_removal=[]
    filtered_list=[]
    for counter1 in xrange(len(extended_patterns)):
        for counter2 in xrange(len(tmp)):
            if((counter1 not in indices_for_removal) & nx.is_isomorphic(extended_patterns[counter1],tmp[counter2],nm)):
                   indices_for_removal.append(counter1)
    for ind in range(0,len(extended_patterns)):
        if(ind not in indices_for_removal):
            filtered_list.append(extended_patterns[ind])
    return filtered_list

def is_isomorphic(graph,existing_patterns):
    nm = iso.categorical_node_match('label', 'label')
    for counter1 in xrange(len(existing_patterns)):
        if(nx.is_isomorphic(graph,existing_patterns[counter1],nm)):
            return True
    return False
            
        
    
    
""""Given labels this function initializes a one node graph for each of the labels"""
def initialize_graph_generator_procedure(labels_of_interest):
    tmp=[]
    for node in labels_of_interest:
        if(isinstance(node,Object) or isinstance(node,Randvar_value_test)):
            continue
        graph=nx.Graph()
        new_node=copy.deepcopy(node)
        new_node.setId()
        if new_node.can_be_target():
            new_node.setTarget()
        if isinstance(new_node,Randvar_value_test):
          graph.add_node(new_node.id,value=new_node.value,label=new_node.label,predicate=new_node.predicate,target=new_node.target,type=new_node,valueinpattern=new_node.value_in_pattern)
        else:
          graph.add_node(new_node.id,label=new_node.label,predicate=new_node.predicate,target=new_node.target,type=new_node,valueinpattern=new_node.value_in_pattern)
        tmp.append(graph)
    return tmp

def find_most_frequent_label_in_the_graph(pattern):
    for node in pattern.graph.nodes():
        print node

"""Given a list of graphs, remove graphs under vertex isomorphism"""
def find_isomorphic_graphs(graphs):
    print "Removing isomorphic graphs from ",len(graphs),' graphs'
    pairs={}
    nm = iso.categorical_node_match('label', 'label')
    indices_for_removal=[]
    filtered_list=[]
    for counter1 in xrange(len(graphs)):
        for counter in xrange(len(graphs)):
           if(counter1==counter):
               continue
           else:
               if((counter1 not in indices_for_removal) & nx.is_isomorphic(graphs[counter],graphs[counter1],nm)):
                   indices_for_removal.append(counter)
                   pairs[counter]=counter1
    for ind in range(0,len(graphs)):
        if(ind not in indices_for_removal):
            filtered_list.append(graphs[ind])

    return filtered_list,indices_for_removal,pairs

       

"""Given a list of graphs, remove graphs under vertex isomorphism"""
def remove_isomorphic_graphs(graphs):
    print "Removing isomorphic graphs from ",len(graphs),' graphs'
    nm = iso.categorical_node_match('label', 'label')
    indices_for_removal=[]
    filtered_list=[]
    for counter1 in xrange(len(graphs)):
        for counter in xrange(len(graphs)):
           if(counter1==counter):
               continue
           else:
               if((counter1 not in indices_for_removal) & nx.is_isomorphic(graphs[counter],graphs[counter1],nm)):
                   indices_for_removal.append(counter)
    for ind in range(0,len(graphs)):
        if(ind not in indices_for_removal):
            filtered_list.append(graphs[ind])
    print "returning:",len(filtered_list),len(indices_for_removal)
    return filtered_list,indices_for_removal

"""Given a list of graphs, remove graphs under vertex isomorphism"""
def remove_isomorphic_graphs_version2(graphs):
    if(len(graphs)==0):
        return
    print "Removing isomorphic graphs from ",len(graphs), 'graphs'
    nm = iso.categorical_node_match('label', 'label')
    length=len(graphs)
    counter=0
    added=[]
    filtered_out=[]
    while counter<length:
        element=graphs[counter]
        added.append(element)
        the_rest=graphs[counter+1:]
        filtered_list,indices_filtered_out_patterns=filter_isomorphic(element,the_rest,nm)
        filtered_out.extend(indices_filtered_out_patterns)
        print "Still to check:",len(filtered_list)
        graphs=added+filtered_list
        length=len(graphs)
        counter+=1      
    return added,filtered_out 
    
def filter_isomorphic(elem,list,nm):
    res=[]
    indices=[]
    counter=0
    for e in list:
        counter+=1
        if not nx.is_isomorphic(elem,e,nm):
            res.append(e)
        else:
            indices.append(counter)
    return res,indices
    
"""Given a list of graphs, remove graphs under vertex isomorphism"""
def remove_invalid_graphs(graphs,relation_predicates):
    result=[]
    for graph in graphs:
        #print "---------------New graph -------------------"
        if is_disallowed_edges_for_relation_node(graph,relation_predicates):
            continue
        #if has_zero_target_nodes(graph):
        #    continue
        else:
            result.append(graph) 
    return result


def has_zero_target_nodes(graph):
    for node in graph.nodes():
       if 'target' in graph.node[node].keys() and graph.node[node]['target']==1:
           return False
       
    return True
           

def is_disallowed_edges_for_relation_node(graph,relation_predicates):
   print "----------------------------------------------------------"
   return_value=False
   for relation_node in relation_predicates:
         print "RELATION NODE: ",relation_node 
         return_value=disallowed_edges_for_relation_node(graph,relation_node)
         if return_value==True:
             print "DISALLOWED"
             return True
   return return_value
'''
Given a list of patterns, generate N random samples
'''
def select_n_random_patterns(pattern_list,N):
    patterns=[]
    indices=random.sample(range(1, len(pattern_list)), N)
    for i in indices:
        patterns.apend(pattern_list[i])
    return patterns

'''
Given a pattern, check if the relation nodes actually has 
two outgoing edges. If it has less than two edges, or more than two edges, it doesn't make sense for the pattern,
because the relation node is the relation between two objects
'''
def disallowed_edges_for_relation_node(pattern_graph,relation_node):
    for node in pattern_graph.nodes():
        if(pattern_graph.node[node]['predicate']==relation_node):
            if(len(nx.neighbors(pattern_graph, node))<2): #warning: allowed this here!!!
                return False
            if(len(nx.neighbors(pattern_graph, node))>2):
                print "More than two neighbours!"
                return True
            else:
                neighbours=nx.neighbors(pattern_graph, node)
                node1=neighbours[0]
                node2=neighbours[1]
                
                if not pattern_graph.node[node]['type'].are_allowed_to_connect_undirected(pattern_graph.node[node1]['predicate'],pattern_graph.node[node2]['predicate']):
                    return True
                else:
                    print "Node: ",pattern_graph.node[node]
                    print "Neighbours: ",pattern_graph.node[node1],pattern_graph.node[node2]
                    print "ALLOWED"
                    return False
    
            

                

'''Function for extracting the randvar-values from data graph for a particular predicate. Constants such as proteind
are denoted with 'constant' predicate'''
def extract_randvar_value_nodes_for_predicate_name(data_graph,predicate_names):
        nodes=[]
        for pred in predicate_names:    
            for node in nx.get_node_attributes(data_graph,'predicate'):
                cur_node=data_graph.node[node]
                if(cur_node['predicate']==pred):
                    nodes.append(cur_node)
        return nodes        

'''
Given a pattern and a desired number n, randomly select n nodes that can be head predicates
returns: head (returns graph node IDs)
'''
def randomly_sample_up_to_n_heads(n,pattern,ignore):
    #select only nodes that can be heads
    possible_heads=[]
    
    for n in pattern.nodes():
        if pattern.node[n]['type'].can_be_head():
            possible_heads.append(n)
    
    indices=random.sample(range(0, len(possible_heads)), len(possible_heads))
    res=[]
    for ind in indices:
        if(pattern.node[possible_heads[ind]]['type'].can_be_head() or not ignore==possible_heads[ind]):
            res.append(possible_heads[ind])
            if(len(res)==n):
                break
    return res
            


''' Given a pattern, a head predicate, and N representing the number of desired patterns and N_pr representing the
number of desired probabilistic predicates in the dependency body, create N patterns that contain target predicates
that are randomly sampled from the overall number of nodes'''
'''patterns is a networkx graph. Each node should have "type" key, where it's corresponding node representation
    with some extra data can be found'''
def sample_dependencies_in_the_patterns(pattern,head_node,head_node_id,N,N_pr):
    #print "Annotating pattern, with head: nr_predicates ",head_node,vis.visualize_graph(pattern)
    result_patterns=[]    
    nodes=pattern.nodes()
    nodes.remove(head_node_id) #remove head node
    
    #delete all existing head notatios
    for node in pattern.nodes():
        if 'head' in pattern.node[node]:
            pattern.node[node]['head']=0
    
    
    #when we load previous pattern, there are also target nodes already present in it
    #we first have to load those target nodes, and then add maybe a new one if needed
    existing_targets_in_pattern=[]
    
    for node in pattern.nodes():
        if node==head_node_id:
            continue
        if 'target' in pattern.node[node] and pattern.node[node]['target']==1 and not('head' in pattern.node[node]) :
            existing_targets_in_pattern.append(node)
    
    sublists=[]
    #remove existing target nodes --- they are alyready marked with target=1 from the
    #previous level   
    for t in existing_targets_in_pattern:
        nodes.remove(t)
    
    for i in xrange(1,((N_pr+1)-len(existing_targets_in_pattern))):
        sublists.extend(list(itertools.combinations(nodes, i)))
    
    random.shuffle(sublists)

    for n in range(0,len(sublists)):
        fail=False
        node_ids=sublists[n]
        new_pattern=copy.deepcopy(pattern)
        new_pattern.node[head_node_id]['head']=1
        new_pattern.node[head_node_id]['target']=1
        for node_id in node_ids:
         if(not(new_pattern.node[node_id]['type'].can_be_target_to(new_pattern.node[head_node_id]))):
             fail=True
             break
         else:
             new_pattern.node[node_id]['target']=1
        if(fail==True):
            continue
        else:
            head_nodes=0
            for node in new_pattern:
                if 'head' in new_pattern.node[node] and new_pattern.node[node]['head']==1:
                    head_nodes+=1
            
            if head_nodes>1:
                print "Pattern issue: has",head_nodes," heads"
                for node in new_pattern.nodes():
                    print new_pattern.node[node]
                raise MoreThanOneHeadNode("More than one head nodes! Attention!")
                sys.exit()
                
            
            result_patterns.append(new_pattern)
            if(float(N)!=float("inf") and int(len(result_patterns))==int(N)):
                break

    if(len(result_patterns)==0):
        return []
    return result_patterns

class MoreThanOneHeadNode(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class Test_sampling_dependencies_in_the_patterns(unittest.TestCase):    
    test_pattern1=nx.Graph()
    new_node_protein=Object_class({'label':'protein','predicate':'protein','target':0})
    new_node_interaction=Relation({'label':'interaction','predicate':'interaction','target':0},new_node_protein,new_node_protein)
    new_node_function1=Attribute({'label':'function','predicate':'function','target':0},new_node_protein)
    new_node_function2=Attribute({'label':'function','predicate':'function','target':0},new_node_protein)
    new_node_const1=Object({'label':'constant=YU11','predicate':'constant','target':0},new_node_protein)
    new_node_const2=Object({'label':'constant=YU12','predicate':'constant','target':0},new_node_protein)
    test_pattern1.add_node(new_node_const1.id,label='constant=YU11',predicate='constant',target=0, type=new_node_const1)
    test_pattern1.add_node(new_node_interaction.id,label='interaction',predicate='interaction',target=0,type=new_node_interaction)
    test_pattern1.add_node(new_node_const2.id,label='constant=YU12',predicate='constant',target=0,type=new_node_const2)
    test_pattern1.add_node(new_node_function1.id,label='function',predicate='function',target=0,type=new_node_function1)
    test_pattern1.add_node(new_node_function2.id,label='function',predicate='function',target=0,type=new_node_function2)
    test_pattern1.add_edge(new_node_interaction.id, new_node_const1.id)
    test_pattern1.add_edge(new_node_interaction.id, new_node_const2.id)
    test_pattern1.add_edge(new_node_function1.id, new_node_const1.id)
    test_pattern1.add_edge(new_node_function2.id, new_node_const2.id)
    
    test_pattern2=nx.Graph()
    new_node_protein1=Object_class({'label':'protein','predicate':'protein','target':0})
    new_node_protein2=Object_class({'label':'protein','predicate':'protein','target':0})
    new_node_interaction=Relation({'label':'interaction','predicate':'interaction','target':0},new_node_protein1,new_node_protein2)
    new_node_location=Attribute({'label':'location','predicate':'location','target':0},new_node_protein)
    new_node_function1=Attribute({'label':'function','predicate':'function','target':0},new_node_protein)
    new_node_function2=Attribute({'label':'function','predicate':'function','target':0},new_node_protein)
    
    test_pattern2.add_node(new_node_protein1.id,label=new_node_protein1.label,predicate=new_node_protein1.predicate,target=new_node_protein1.target, type=new_node_const1)
    test_pattern2.add_node(new_node_protein2.id,label=new_node_protein2.label,predicate=new_node_protein2.predicate,target=new_node_protein2.target,type=new_node_interaction)
    test_pattern2.add_node(new_node_interaction.id,label=new_node_interaction.label,predicate=new_node_interaction.predicate,target=new_node_interaction.target,type=new_node_const2)
    test_pattern2.add_node(new_node_location.id,label=new_node_location.label,predicate=new_node_location.predicate,target=new_node_location.target,type=new_node_location)
    test_pattern2.add_node(new_node_function1.id,label=new_node_function1.label,predicate=new_node_function1.predicate,target=new_node_function1.target,type=new_node_function1)
    test_pattern2.add_node(new_node_function2.id,label=new_node_function2.label,predicate=new_node_function2.predicate,target=new_node_function2.target,type=new_node_function2)
    
    test_pattern2.add_edge(new_node_protein1.id, new_node_location.id)
    test_pattern2.add_edge(new_node_protein1.id, new_node_function1.id)
    test_pattern2.add_edge(new_node_protein1.id, new_node_interaction.id)
    test_pattern2.add_edge(new_node_interaction.id, new_node_protein2.id)
    test_pattern2.add_edge(new_node_protein2.id, new_node_function2.id)
    
    
    labels=[]
    label_protein=Object_class({'label':'protein','predicate':'protein','target':0})
    label_interaction=Relation({'label':'interaction','predicate':'interaction','target':0},label_protein.predicate,label_protein.predicate)
    label_function=Attribute({'label':'function','predicate':'function','target':0},label_protein.predicate)
    labels.append(label_protein)
    labels.append(label_interaction)
    labels.append(label_function)

class Test_extending_pattern_yeast_network(unittest.TestCase):  

    def test_extending_pattern_with_possible_target_node(self):
        self.node_protein=Object_class({'label':'constant:protein','predicate':'constant','target':0,'valueinpattern':0})
        self.node_interaction=Relation({'label':'interaction','predicate':'interaction','target':0,'valueinpattern':0},None,self.node_protein.predicate)
        self.node_function=Attribute({'label':'function','predicate':'function','target':0,'valueinpattern':0},self.node_protein.predicate)
        self.node_phenotype=Attribute({'label':'phenotype','predicate':'phenotype','target':0,'valueinpattern':0},self.node_protein.predicate)
        self.node_location=Attribute({'label':'location','predicate':'location','target':0,'valueinpattern':0},self.node_protein.predicate)
        self.node_protein_class=Attribute({'label':'protein_class','predicate':'protein_class','target':0,'valueinpattern':0},self.node_protein.predicate)
        self.node_enzyme=Attribute({'label':'enzyme','predicate':'enzyme','target':0,'valueinpattern':0},self.node_protein.predicate)
        rt=Randvar_value_test({'label':'function = function_value1','predicate':'function','target':0,'valueinpattern':1},"function_value1",self.node_protein.predicate)

        test_pattern1=nx.Graph()
        test_pattern1.add_node(0,label='constant=YU11',predicate='constant',target=0, type=self.node_protein)
        test_pattern1.add_node(1,label='constant=YU12',predicate='constant',target=0, type=self.node_protein)
        test_pattern1.add_node(3,label='function',head=0,predicate='function',target=1,type=self.node_function)
        test_pattern1.add_node(4,label='interaction',head=0,predicate='interaction',target=0,type=self.node_interaction)
        test_pattern1.add_edge(3, 0)
        test_pattern1.add_edge(4, 1)
        test_pattern1.add_edge(4, 0)
        
        extension_node1=Randvar_value_test({'label':'function = function_value1','predicate':'function','target':0,'valueinpattern':1},"function_value1",self.node_protein.predicate)
        
        extended_pattern=get_all_d_depth_extensions(test_pattern1,[extension_node1])
        print len(extended_pattern)
        print "Graphs we obtained: "
        counter=1
        for graph in extended_pattern:
             print "Graph has: ",len(graph.nodes())," nodes"
             vis.visualize_graph(graph,"name"+str(counter))
             counter+=1
             nx.write_gml(graph, "name"+str(counter))
            #print "***************************"
            #for node in graph.nodes():
            #    print graph.node[node]
           
        self.assertEquals(4,len(extended_pattern))
        for node in extended_pattern[0].nodes():
            print extended_pattern[0].node[node]
            if(extended_pattern[0].node[node]['predicate']=='function' and extended_pattern[0].node[node]['type']=='attribute'):
                self.assertEqual(extended_pattern[0].node[node]['target']==1, True)
            if(extended_pattern[0].node[node]['predicate']=='function' and extended_pattern[0].node[node]['type']=='randvar_value_test'):
                self.assertEqual(extended_pattern[0].node[node]['target']==0, True)
   
   
    def test_2_PATTERNS(self):
        self.assertEqual(len(sample_dependencies_in_the_patterns(self.test_pattern1,self.test_pattern1.node[self.new_node_interaction.id],self.new_node_interaction.id,2,2)),1)
        
    def test_3_predicates(self):
        self.assertEqual(len(sample_dependencies_in_the_patterns(self.test_pattern2,self.test_pattern2.node[self.new_node_interaction.id],self.new_node_interaction.id,2,3)),2)
        
    def test_3_head_predicates(self):
        self.assertEqual(len(randomly_sample_up_to_n_heads(3,self.test_pattern2)),3)
        
    def test_3_size_patterns_with_dependency_sampling(self):
        patt=generate_patterns_up_to_depth_n(self.labels, 5, ['interaction'], 3, 3, 3)
        print "number of patterns,",len(patt)
        #self.assertEqual(len(generate_patterns_up_to_depth_n(self.labels, 3, ['interaction'], 2, 2, 2)),3)
              
class Test_pattern_filtering(unittest.TestCase):
    test_pattern=nx.Graph()
    test_pattern.add_node(0,label='constant=YU11',predicate='constant',target=0)
    test_pattern.add_node(1,label='interaction',predicate='interaction',target=0)
    test_pattern.add_node(2,label='interaction',predicate='interaction',target=0)
    test_pattern.add_edge(0, 1)
    test_pattern.add_edge(0, 2)
    
    test_pattern1=nx.Graph()
    test_pattern1.add_node(0,label='constant=YU11',predicate='constant',target=0)
    test_pattern1.add_node(1,label='interaction',predicate='interaction',target=0)
    test_pattern1.add_node(2,label='constant=YU12',predicate='constant',target=0)
    test_pattern1.add_edge(1, 0)
    test_pattern1.add_edge(1, 2)
   
    def test_False(self):
        self.assertEqual(disallowed_edges_for_relation_node(self.test_pattern1,'interaction'), False)            
            

    def test_True(self):
        self.assertEqual(disallowed_edges_for_relation_node(self.test_pattern,'interaction'), True)            
            
          

             
            



def test_randvar_value_tests():
    path=os.path.abspath(os.pardir)
    print "path",path
    #graph_name=os.path.join(path+'/test_data/YEAST_27.gpickle')
    graph_name=path+"/test_data/YEAST_27.gpickle"
    print "graph: ",graph_name
    graph=nx.read_gml(graph_name)
    
    print extract_randvar_value_nodes_for_predicate_name(graph, 'constant')
    #print extract_randvar_value_nodes_for_predicate_name(graph, 'phenotype')
    


if __name__ == '__main__':
      path_pattern='/cw/dtailocal/irma/Martin_paper/graph_sampling/exampleExperiment/patternY1.gml'
      #data_graph= pickle.load(open(('/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/PATTERNS_proba_2_brisi/patterns_size_4/all_patterns_4.pickle')))
      #data_graph=nx.read_gpickle('/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/DATA/Yeast/YEAST.gpickle')
      #data_graph=nx.read_gml(path_pattern)
      #vis.visualize_graph_standard(data_graph)
      #for node in data_graph.nodes():
      #    if(data_graph.node[node]['predicate']=='function'):
      #        print data_graph.node[node]
      
      #print (len(list))
      suite = unittest.TestSuite()
      suite.addTest(Test_extending_pattern_yeast_network('test_extending_pattern_with_possible_target_node'))
      unittest.TextTestRunner().run(suite)
#     #suite.addTest(Test_sampling_dependencies_in_the_patterns('test_3_predicates'))
#     #suite.addTest(Test_sampling_dependencies_in_the_patterns('test_3_head_predicates'))
#     suite.addTest(Test_sampling_dependencies_in_the_patterns('test_3_size_patterns_with_dependency_sampling'))
#     
#     
    
    #unittest.main()
    
#     path=os.path.abspath(os.pardir)
#     print "path",path
#     #graph_name=os.path.join(path+'/test_data/YEAST_27.gpickle')
#     graph_name=path+"/test_data/YEAST_27.gpickle"
#     print "graph: ",graph_name
#     graph=nx.read_gml(graph_name)
#       
#     nodes=extract_randvar_value_nodes_for_predicate_name(graph, ['constant','interaction','location'])
#     domain_nodes=[]
#      
#     nd_function={'predicate':'function','label':'function','target':0,'id':0}
#     protein={'predicate':'protein','label':'protein','target':0,'id':1}
#     for node in nodes:       
#          graph_node=None
#          if(node['predicate']=='constant'):
#              graph_node=Object(node,protein)
#          #if(node['predicate']=='interaction'):
#          #    graph_node=Relation(node, 'constant', 'constant')
#          #if(node['predicate']=='function'):
#          #    graph_node=Attribute(node, 'constant')
#          #if(node['predicate']=='location'):
#          #    graph_node=Attribute(node, 'constant')    
#                
#          if(graph_node!=None):
#              domain_nodes.append(graph_node)
#     
#     print "domain nodes: ",domain_nodes
#     domain_nodes.append(Attribute(nd_function, 'constant'))
#     domain_nodes.append(Object_class(protein))
#       
#     patterns=generate_patterns_up_to_depth_n(domain_nodes,None,3,['interaction'])
#     #graph=patterns[0]
#     vis.visualize_multiple_graphs(5, 8, patterns)
#     #vis.visualize_multiple_graphs(6, 6, patterns)
#                              
     #test_randvar_value_tests()
#      G1=nx.Graph()
#      
#      labels_of_interest=[]
#      a=Domain_object('a','a',0)    
#      b=Attribute('b','b',0,a)
#      labels_of_interest.append(a)
#      labels_of_interest.append(b)
#      
#      patterns=generate_patterns_up_to_depth_n(labels_of_interest,None,2)
#      extended_patterns=generate_patterns_of_depth_n(labels_of_interest, patterns, None, 3)
#      find_most_frequent_label_in_the_graph(extended_patterns[0])
     #vis.visualize_multiple_graphs(10,10,extended_patterns)
     #size_one_graph=initialize_graph_generator_procedure(labels_of_interest)
     #g=size_one_graph[0]
     #print g.node[1]['type'].__class__
     #print nx.get_node_attributes(size_one_graph[0],'target')
#      #vis.visualize_multiple_graphs(1,4,size_one_graph);
#      size_2_graphs=undirected_patterns_of_size_2(size_one_graph, labels_of_interest)
#      #vis.visualize_multiple_graphs(4,5,size_2_graphs)
#      
#      tmp=[]     
#      for g in size_2_graphs:
#        extended_3=make_n_edges_with_nodes_in_the_graph(g,'a',len(g.nodes())+1,2)
#        extended_4=make_n_edges_with_nodes_in_the_graph(g,'b',len(g.nodes())+1,2)
#        tmp.extend(extended_3)
#        tmp.extend(extended_4)
#     
#      removed_isomorphisms=remove_isomorphic_graphs(tmp)    
#      vis.visualize_multiple_graphs(4,5,removed_isomorphisms)
#     # vis.print_graph_nodes_labels(extended_3[0],'label')
#      #print "Number of graphs of size 2",len(size_2_graphs)
#      #vis.visualize_multiple_graphs(4,5,size_2_graphs);
