'''
Created on May 26, 2015

@author: irma
'''
from graph.nodes import * 
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
import graph_manipulator.graph_analyzer as graph_ana
import random,os
import experiments.sampling_utils as utils


class YEAST_GRAPH(object):
    mapping_to_associated_predicates={}
    labels=None
    relation_labels=None
    
    def __init__(self,path_to_data_graph,output,nr_randvar_value_tests,subset):
        print "Creating YEAST network ..."
        #general nodes
        self.labels=[]
        self.label_protein=Object_class({'label':'constant:protein','predicate':'constant','target':0,'valueinpattern':0})
        self.label_interaction=Relation({'label':'interaction','predicate':'interaction','target':0,'valueinpattern':0},self.label_protein.predicate,self.label_protein.predicate)
        self.label_function=Attribute({'label':'function','predicate':'function','target':0,'valueinpattern':0},self.label_protein.predicate)
        self.label_phenotype=Attribute({'label':'phenotype','predicate':'phenotype','target':0,'valueinpattern':0},self.label_protein.predicate)
        self.label_location=Attribute({'label':'location','predicate':'location','target':0,'valueinpattern':0},self.label_protein.predicate)
        self.label_protein_class=Attribute({'label':'protein_class','predicate':'protein_class','target':0,'valueinpattern':0},self.label_protein.predicate)
        self.label_enzyme=Attribute({'label':'enzyme','predicate':'enzyme','target':0,'valueinpattern':0},self.label_protein.predicate)

        self.relation_labels=[self.label_interaction]
        self.labels.append(self.label_protein)
        self.labels.append(self.label_function)
        self.labels.append(self.label_location)
        self.labels.append(self.label_protein_class)
        self.labels.append(self.label_enzyme)
        self.labels.append(self.label_interaction)
        self.labels.append(self.label_phenotype)
        
        self.mapping_to_associated_predicates['function']=self.label_protein
        self.mapping_to_associated_predicates['constant']=self.label_protein
        self.mapping_to_associated_predicates['location']=self.label_protein
        self.mapping_to_associated_predicates['enzyme']=self.label_protein
        self.mapping_to_associated_predicates['protein_class']=self.label_protein
        self.mapping_to_associated_predicates['phenotype']=self.label_protein

        #write statistics of the data graph
        dirname=os.path.dirname
        f = open(os.path.join(output,'info_data.txt'), 'w')
        f_labels = open(os.path.join(output,'labels_info.txt'), 'w')
        
        D=nx.read_gpickle(path_to_data_graph)
        #extract randvar values for function, location, proteinc class and enzyme
        phenotype_values=graph_ana.get_all_possible_nodes_wtih_values_in_data_graph(D, "phenotype",subset)
        function_values=graph_ana.get_all_possible_nodes_wtih_values_in_data_graph(D, "function",subset)
        location_values=graph_ana.get_all_possible_nodes_wtih_values_in_data_graph(D, "location",subset)
        enzyme_values=graph_ana.get_all_possible_nodes_wtih_values_in_data_graph(D, "enzyme",subset)
        protein_class_value=graph_ana.get_all_possible_nodes_wtih_values_in_data_graph(D, "protein_class",subset)
        
        if nr_randvar_value_tests==-1:
            for f in function_values:
                rt=Randvar_value_test({'label':'function = '+f['value'],'predicate':'function','target':0,'valueinpattern':1},f['value'],self.label_protein.predicate)
                self.labels.append(rt)
            for l in location_values:
                rt=Randvar_value_test({'label':'location = '+l['value'],'predicate':'location','target':0,'valueinpattern':1},l['value'],self.label_protein.predicate)
                self.labels.append(rt)
            for e in enzyme_values:
                rt=Randvar_value_test({'label':'enzyme = '+e['value'],'predicate':'enzyme','target':0,'valueinpattern':1},e['value'],self.label_protein.predicate)
                self.labels.append(rt)
            for pc in protein_class_value:
                rt=Randvar_value_test({'label':'protein_class = '+pc['value'],'predicate':'protein_class','target':0,'valueinpattern':1},pc['value'],self.label_protein.predicate)
                self.labels.append(rt)
            for phen in phenotype_values:
                rt=Randvar_value_test({'label':'phenotype = '+phen['value'],'predicate':'phenotype','target':0,'valueinpattern':1},phen['value'],self.label_protein.predicate)
                self.labels.append(rt) 
        #extract top 2 protein objects
        proteins=graph_ana.get_N_nodes_with_the_highest_degree(D, "constant",2)
        for p in proteins:
             rt=Randvar_value_test({'label':'constant = '+p['name'],'predicate':'constant','target':0,'valueinpattern':1},p['name'],None)
             self.labels.append(rt)
          
        for label in self.labels:
            f_labels.write(label.to_string_representation()+"\n")
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
                    node['type']=self.label_protein_class
        return gml_graph
    
    