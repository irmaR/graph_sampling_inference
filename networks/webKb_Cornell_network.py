
from graph.nodes import * 
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
import graph_manipulator.graph_analyzer as graph_ana
import random,os
import experiments.sampling_utils as utils

class WEBKB_Cornell(object):
    
    mapping_to_associated_predicates={}
    labels=None
    relation_labels=None
    
    
    def __init__(self,path_to_data_graph,output):
        print "Creating WEBKB network ..."
        #general nodes
        self.labels=[]
        self.page=Object_class({'label':'page','predicate':'page','target':1,'valueinpattern':1})
        self.label_references=Relation({'label':'ref','predicate':'ref','target':0,'valueinpattern':0},self.page.predicate,self.page.predicate)
        self.label_direction=Relation({'label':'dir','predicate':'dir','target':0,'valueinpattern':0},self.page.predicate,self.page.predicate)
        self.label_references.first_object_predicate=self.label_direction.predicate
        self.label_references.second_object_predicate=self.page.predicate
        #self.label_references.special=True
        self.label_direction.first_object_predicate=self.page.predicate
        self.label_direction.second_object_predicate=self.label_references.predicate
        
        self.relation_labels=[self.label_direction,self.label_references]
        self.labels.append(self.page)
        self.labels.append(self.label_references)
        self.labels.append(self.label_direction)
        self.mapping_to_associated_predicates['page']=self.page
                 
        page_values=['student','project','course','faculty','department','staff']        
         
        for cit in page_values:
            rt=Randvar_value_test({'label':'page = '+cit,'predicate':'page','target':0,'valueinpattern':1}, cit,self.page.predicate)
            rt.unique_value[self.page.predicate]=True
            rt.object_predicate.append(self.label_direction.predicate)
            rt.object_predicate.append(self.label_references.predicate)
            self.labels.append(rt)
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
    
    def turn_gml_graph_to_type_graph_yeast(self,gml_graph):
            for node in gml_graph.nodes():
                node=gml_graph.node[node]
                
                node_predicate=node['predicate']
                label_predicate=node['label']
               
                if node['valueinpattern']==1:
                    value=self.get_value(label_predicate)
                    node['value']=value
                    node_type=self.create_randvar_value_test(node,self.mapping_to_associated_predicates[node_predicate])
                    node['type']=node_type            
                else:
                    if node_predicate == 'page':
                         node['type']=self.page
            return gml_graph
        
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
                    if node_predicate == 'page':
                        node['type']=self.page
                    elif node_predicate == 'dir':
                        node['type']=self.label_direction
                    elif node_predicate == 'ref':
                        node['type']=self.label_references
            return gml_graph

if __name__ == '__main__':
    dblp_path='/home/irma/workspace/some_scripts_martin_sampling/DATA/webkb/.gpickle'
    
    