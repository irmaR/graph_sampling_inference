'''
Created on Nov 15, 2016

@author: irma
'''
from graph.nodes import * 
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
import graph_manipulator.graph_analyzer as graph_ana
import random,os
import experiments.sampling_utils as utils

class Enron_network(object):
    
    mapping_to_associated_predicates={}
    labels=None
    relation_labels=None
    
    
    def __init__(self,path_to_data_graph,output):
        print "Creating ENRON network ..."
        #general nodes
        self.labels=[]
        self.user=Special_Object({'label':'user','predicate':'user','target':0,'valueinpattern':0})
        self.labels.append(self.user)
        self.mapping_to_associated_predicates['user']=self.user
        print "Number of possible labels: ",len(self.labels)
        for label in self.labels:
            print label
        
        #write statistics of the data graph
        dirname=os.path.dirname
        f = open(os.path.join(output,'info_data.txt'), 'w')
        f_labels = open(os.path.join(output,'labels_info.txt'), 'w')
        for label in self.labels:
            f_labels.write(label.to_string_representation()+"\n")
        f_labels.close()
        f_labels.close()
    

        
    def turn_gml_graph_to_type_graph(self,gml_graph):
            for node in gml_graph.nodes():
                node=gml_graph.node[node]
                
                node_predicate=node['predicate']
                label_predicate=node['label']
               
                if node['valueinpattern']==1:
                    if 'value' in node.keys():
                        value=node['value']
                    else:
                        value=self.get_value(label_predicate)
                    node['value']=value
                    node_type=graph_ana.create_randvar_value_test(node,self.mapping_to_associated_predicates[node_predicate])
                    node['type']=node_type            
                else:
                    if node_predicate == 'user':
                        node['type']=self.user
            return gml_graph

if __name__ == '__main__':
    dblp_path='/home/irma/workspace/some_scripts_martin_sampling/DATA/webkb/.gpickle'
    
    