'''
Created on May 17, 2015

@author: irma
'''
'''
Created on Mar 6, 2015

@author: irma
'''
from graph.nodes import * 
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
import graph_manipulator.graph_analyzer as graph_ana
import random,os
import experiments.sampling_utils as utils

class DBLP_GRAPH(object):
    
    mapping_to_associated_predicates={}
    labels=None
    relation_labels=None
    
    
    def __init__(self,path_to_data_graph,output):
        print "Creating DBLP network ..."
        #general nodes
        self.labels=[]
        self.label_paper=Object_class({'label':'constant:paper','predicate':'constant','target':0,'valueinpattern':0})
        self.label_direction=None
        self.label_references=Relation({'label':'references','predicate':'references','target':0,'valueinpattern':0},None,None)
        self.label_direction=Relation({'label':'dir','predicate':'dir','target':0,'valueinpattern':0},self.label_paper.predicate,self.label_references.predicate)
        self.label_references.first_object_predicate=self.label_direction.predicate
        self.label_references.second_object_predicate=self.label_paper.predicate
        #self.label_references.special=True
        self.label_direction.second_object_predicate=self.label_references.predicate
        #self.label_direction.special=True
        self.label_coauthored=Relation({'label':'coauthored','predicate':'coauthored','target':0,'valueinpattern':0},self.label_paper.predicate,self.label_paper.predicate)
        self.label_citations=Attribute({'label':'citations','predicate':'citations','target':0,'valueinpattern':0},self.label_paper.predicate)
       
        self.relation_labels=[self.label_direction,self.label_references,self.label_coauthored]
        self.labels.append(self.label_paper)
        self.labels.append(self.label_direction)
        self.labels.append(self.label_coauthored)
        self.labels.append(self.label_references)
        self.labels.append(self.label_citations)
        
        #self.label_paper.unique_value[self.label_citations.predicate]=True
        #self.label_citations.unique=True
        
        for label in self.labels:
            print label
        
        #write statistics of the data graph
        dirname=os.path.dirname
        f = open(os.path.join(output,'info_data.txt'), 'w')
        f_labels = open(os.path.join(output,'labels_info.txt'), 'w')
              
        #D=nx.read_gpickle(path_to_data_graph)
        
        #nr_distinct_paper=graph_ana.getNumberOfDistinctNodeValue(D,'paper')
        #nr_distinct_direction=graph_ana.getNumberOfDistinctNodeValue(D,'dir')
        #nr_distinct_coauthored=graph_ana.getNumberOfDistinctNodeValue(D,'coauthored')
        #nr_distinct_references=graph_ana.getNumberOfDistinctNodeValue(D,'enzyme')
        #nr_distinct_citations=graph_ana.getNumberOfDistinctNodeValue(D,'citations')
        
        self.mapping_to_associated_predicates['citations']=self.label_paper
        
         
        #paper_constant_objects=graph_ana.get_N_nodes_with_the_highest_degree(D, 'constant',2)              
        citations_values=['low','mid','high']        
        #for prot in paper_constant_objects:
        #    prot['valueinpattern']=1
        #    self.labels.append(Randr_distinct_constant=graph_ana.getNumberOfDistinctNodeValue(D,'constant'))
             
        for cit in citations_values:
            rt=Randvar_value_test({'label':'citations = '+cit,'predicate':'citations','target':0,'valueinpattern':1}, cit,self.label_paper.predicate)
            rt.unique_value[self.label_citations.predicate]=True
            self.labels.append(rt)
        print "Number of possible labels: ",len(self.labels)
        print "Writing info to: ",f
        for label in self.labels:
            f_labels.write(str(label)+"\n")
          
#         f.write(" Nr distinct nodes for papers: "+str(nr_distinct_paper)+"\n")
#         f.write(" Nr distinct nodes for direction: "+str(nr_distinct_direction)+"\n")
#         f.write(" Nr distinct nodes for coauthored: "+str(nr_distinct_coauthored)+"\n")
#         f.write(" Nr distinct nodes for references: "+str(nr_distinct_references)+"\n")
#         f.write(" Nr distinct nodes for citations: "+str(nr_distinct_citations)+"\n")
#     
#         f.close()
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
                    if node_predicate == 'constant':
                        node['type']=self.label_protein
                    elif node_predicate == 'interaction':
                        node['type']=self.label_interaction
                    elif node_predicate == 'function':
                        node['type']=self.label_function
                    elif node_predicate == 'location':
                        node['type']=self.label_location
                    elif node_predicate == 'phenotype':
                        node['type']=self.label_phenotype
                    elif node_predicate == 'enzyme':
                        node['type']=self.label_enzyme
                    elif node_predicate == 'protein_class':
                        node['type']=self.label_class
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
                    if node_predicate == 'constant':
                        node['type']=self.label_paper
                    elif node_predicate == 'dir':
                        node['type']=self.label_direction
                    elif node_predicate == 'references':
                        node['type']=self.label_references
                    elif node_predicate == 'citations':
                        node['type']=self.label_citations
                    elif node_predicate == 'coauthored':
                        node['type']=self.label_coauthored      
            return gml_graph


  
 
            



if __name__ == '__main__':
    dblp_path='/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/DBLP/Dblp/DBLP_2001-2_discretized.gpickle'
    predicate_names=[]
    dblp=DBLP_GRAPH(dblp_path,'/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/DBLP/Dblp/')
    graph=nx.read_gpickle(dblp_path)
    #utils.turn_graph_into_prolog_format_dblp(graph, '/home/irma/workspace/Data/Martin/Dblp/dblp.prolog', ['constant'],['coauthored','references','dir'],['citations'])
    #yeast_graph=YEAST_GRAPH('/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/YEAST.gpickle','/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/')
    #gml_graph=nx.read_gml('/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/patterns_size_2_proba/patterns_size_2/yeastpattern_52936976/yeastpattern_52936976.gml')
    #graph=yeast_graph.turn_gml_graph_to_type_graph(gml_graph)
    