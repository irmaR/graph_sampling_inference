
from graph.nodes import * 
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
import graph_manipulator.graph_analyzer as graph_ana
import random,os
import experiments.sampling_utils as utils

class IMDB(object):
    
    mapping_to_associated_predicates={}
    labels=None
    relation_labels=None
    
    
    def __init__(self,path_to_data_graph,output):
        print "Creating IMDB network ..."
        #general nodes
        self.labels=[]
        self.movie=no_self_loop_object({'label':'movie','predicate':'movie','target':0,'valueinpattern':0})
        self.director=no_self_loop_object({'label':'director','predicate':'director','target':0,'valueinpattern':0})
        self.actor=no_self_loop_object({'label':'actor','predicate':'actor','target':0,'valueinpattern':0})
        self.gender=Attribute({'label':'gender','predicate':'gender','target':1,'valueinpattern':1},[self.actor.predicate,self.director.predicate])
        self.genre=Attribute({'label':'genre','predicate':'genre','target':1,'valueinpattern':1},[self.actor.predicate,self.director.predicate])
        #self.workedUnder=Relation({'label':'workedUnder','predicate':'workedUnder','target':0,'valueinpattern':0},self.actor.predicate,self.director.predicate)
        #self.workedUnder.first_object_predicate=self.actor.predicate
        #self.workedUnder.second_object_predicate=self.director.predicate
        #self.relation_labels=[self.workedUnder]
       
        self.labels.append(self.movie)
        self.labels.append(self.director)
        self.labels.append(self.actor)
        self.labels.append(self.gender)
        self.labels.append(self.genre)
        #self.labels.append(self.workedUnder)
        
        self.mapping_to_associated_predicates['movie']=self.director
        self.mapping_to_associated_predicates['movie']=self.actor
        self.mapping_to_associated_predicates['movie']=self.genre
       
        
        self.mapping_to_associated_predicates['actor']=self.movie
        self.mapping_to_associated_predicates['actor']=self.director
        self.mapping_to_associated_predicates['actor']=self.gender
   
        self.mapping_to_associated_predicates['gender']=[self.actor,self.director]
        self.mapping_to_associated_predicates['genre']=[self.actor,self.director]
        
       
        gender_values=['Male','Female'] 
        genre_values=['Adrama','Acrime','Acomedy','Amystery','Ascifi','Aromance']        
        #for prot in paper_constant_objects:
        #    prot['valueinpattern']=1
        #    self.labels.append(Randr_distinct_constant=graph_ana.getNumberOfDistinctNodeValue(D,'constant'))
             
        for g in gender_values:
            rt=Randvar_value_test({'label':'gender = '+g,'predicate':'gender','target':0,'valueinpattern':1}, g,[self.actor.predicate,self.director.predicate])
            rt.unique_value[self.gender.predicate]=True
            self.labels.append(rt)
        
        for g in genre_values:
            rt=Randvar_value_test({'label':'genre = '+g,'predicate':'genre','target':0,'valueinpattern':1}, g,[self.actor.predicate,self.director.predicate])
            rt.unique_value[self.genre.predicate]=True
            self.labels.append(rt)
            
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
                value=graph_ana.get_value(label_predicate)
                node['value']=value
                node_type=graph_ana.create_randvar_value_test(node,self.mapping_to_associated_predicates[node_predicate])
                node['type']=node_type            
            else:
                if node_predicate == 'actor':
                    node['type']=self.actor                        
                elif node_predicate == 'director':
                    node['type']=self.director
                elif node_predicate == 'movie':
                    node['type']=self.movie
                elif node_predicate == 'gender':
                    node['type']=self.gender
                elif node_predicate == 'genre':
                    node['type']=self.genre
        return gml_graph
   
if __name__ == '__main__':
    dblp_path='/home/irma/workspace/some_scripts_martin_sampling/DATA/YEAST.gpickle'
    graph=nx.read_gpickle(dblp_path)
    for n in graph.nodes():
        if graph.node[n]['predicate']=='constant':
           print graph.node[n]
    