'''
Created on Oct 25, 2016

@author: irma
'''
from graph.nodes import * 
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
import graph_manipulator.graph_analyzer as graph_ana
import random,os
import experiments.sampling_utils as utils

class Facebook(object):
    
    mapping_to_associated_predicates={}
    labels=None
    relation_labels=None
    
    
    def __init__(self,path_to_data_graph,output):
        print "Creating IMDB network ..."
        #general nodes
        self.labels=[]
        self.user=Special_Object({'label':'user','predicate':'user','target':0,'valueinpattern':0})
        self.birthday=Attribute({'label':'birthday','predicate':'birthday','target':1,'valueinpattern':0},[self.user.predicate])
        self.hometown=Attribute({'label':'hometown','predicate':'hometown','target':1,'valueinpattern':0},[self.user.predicate])
        self.education_type=Attribute({'label':'education_type','predicate':'education_type','target':1,'valueinpattern':0},[self.user.predicate])
        self.education_degree=Attribute({'label':'education_degree','predicate':'education_degree','target':1,'valueinpattern':0},[self.user.predicate])
        self.language=Attribute({'label':'language','predicate':'language','target':1,'valueinpattern':0},[self.user.predicate])
        self.gender=Attribute({'label':'gender','predicate':'gender','target':1,'valueinpattern':0},[self.user.predicate])
        
        self.labels.append(self.user)
        self.labels.append(self.birthday)
        self.labels.append(self.hometown)
        self.labels.append(self.education_type)
        self.labels.append(self.education_degree)
        self.labels.append(self.language)
        self.labels.append(self.gender)
        
        self.mapping_to_associated_predicates['gender']=self.user
        self.mapping_to_associated_predicates['birthday']=self.user
        self.mapping_to_associated_predicates['hometown']=self.user
        self.mapping_to_associated_predicates['education_type']=self.user
        self.mapping_to_associated_predicates['education_degree']=self.user
        self.mapping_to_associated_predicates['language']=self.user
        self.mapping_to_associated_predicates['user']=self.user
        
#         birthday_values=['value_unknown', 'value_6', 'value_2', 'value_1', 'value_5', 'value_7', 'value_4', 'value_377', 'value_3', 'value_210', 'value_1004', 'value_734', 'value_0', 'value_208', 'value_211', 'value_381', 'value_380', 'value_378', 'value_1006', 'value_1172', 'value_209', 'value_732', 'value_730', 'value_733', 'value_1003', 'value_207', 'value_1005', 'value_212', 'value_736', 'value_376', 'value_741', 'value_735', 'value_382', 'value_740', 'value_739', 'value_729', 'value_731', 'value_206', 'value_737', 'value_379', 'value_738']   
#         hometown_values=['value_unknown', 'value_84', 'value_79', 'value_89', 'value_81', 'value_908', 'value_88', 'value_80', 'value_43', 'value_82', 'value_87', 'value_935', 'value_1222', 'value_86', 'value_1223', 'value_134', 'value_283', 'value_65', 'value_566', 'value_176', 'value_298', 'value_1098', 'value_560', 'value_559', 'value_263', 'value_1221', 'value_1220', 'value_1087', 'value_85', 'value_911', 'value_261', 'value_902', 'value_909', 'value_904', 'value_619', 'value_1090', 'value_565', 'value_1096', 'value_1097', 'value_264', 'value_568', 'value_905', 'value_266', 'value_910', 'value_1095', 'value_149', 'value_1089', 'value_562', 'value_567', 'value_618', 'value_284', 'value_563', 'value_119', 'value_561', 'value_178', 'value_83', 'value_903', 'value_564', 'value_907', 'value_280', 'value_297', 'value_1094', 'value_1088', 'value_1086', 'value_617', 'value_1100', 'value_1092', 'value_569', 'value_1099', 'value_1091', 'value_1093', 'value_21', 'value_906']
#         education_type_values=['value_unknown', 'value_53', 'value_55', 'value_54']  
#         education_degree_values=['value_unknown', 'value_21', 'value_224', 'value_22', 'value_437', 'value_20', 'value_223', 'value_220', 'value_221', 'value_432', 'value_438', 'value_1183', 'value_436', 'value_431', 'value_774', 'value_1184', 'value_433', 'value_435', 'value_222', 'value_23', 'value_313', 'value_1182', 'value_776', 'value_775', 'value_434']   
#         language_values=['value_unknown', 'value_92', 'value_101', 'value_265', 'value_912', 'value_96', 'value_93', 'value_91', 'value_90', 'value_1225', 'value_571', 'value_97', 'value_94', 'value_266', 'value_574', 'value_573', 'value_572', 'value_100', 'value_102', 'value_98', 'value_914', 'value_913', 'value_1224', 'value_1102', 'value_99']
#         gender_values=['value_77', 'value_78', 'value_unknown']
#       
        birthday_values=['value_unknown','value_1','value_2','value_3']
        hometown_values=['value_unknown','value_1','value_2','value_3']
        education_type_values=['value_unknown','value_1','value_2','value_3']
        education_degree_values=['value_unknown','value_1','value_2','value_3']   
        language_values=['value_unknown','value_1','value_2','value_3']
        gender_values=['value_77', 'value_78', 'value_unknown']
      
        #select most frequent 3 values for birthday, 
      
        for b in birthday_values:
            rt=Randvar_value_test({'label':'birthday = '+b,'predicate':'birthday','target':0,'valueinpattern':1}, b,self.user.predicate)
            rt.unique_value[self.birthday.predicate]=True
            self.labels.append(rt)
         
        for h in hometown_values:
            rt=Randvar_value_test({'label':'hometown = '+h,'predicate':'hometown','target':0,'valueinpattern':1}, h,self.user.predicate)
            rt.unique_value[self.hometown.predicate]=True
            self.labels.append(rt)
          
        for et in education_type_values:
            rt=Randvar_value_test({'label':'education_type = '+et,'predicate':'education_type','target':0,'valueinpattern':1}, et,self.user.predicate)
            rt.unique_value[self.education_type.predicate]=True
            self.labels.append(rt)
          
        for ed in education_degree_values:
            rt=Randvar_value_test({'label':'education_degree = '+ed,'predicate':'education_degree','target':0,'valueinpattern':1}, ed,self.user.predicate)
            rt.unique_value[self.education_degree.predicate]=True
            self.labels.append(rt)
          
        for l in language_values:
            rt=Randvar_value_test({'label':'language = '+l,'predicate':'language','target':0,'valueinpattern':1}, l,self.user.predicate)
            rt.unique_value[self.language.predicate]=True
            self.labels.append(rt)
#              
        for g in gender_values:
            rt=Randvar_value_test({'label':'gender = '+g,'predicate':'gender','target':0,'valueinpattern':1}, g,self.user.predicate)
            rt.unique_value[self.gender.predicate]=True
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
                if node_predicate == 'gender':
                    node['type']=self.gender                        
                elif node_predicate == 'language':
                    node['type']=self.language
                elif node_predicate == 'birthday':
                    node['type']=self.birthday
                elif node_predicate == 'hometown':
                    node['type']=self.hometown
                elif node_predicate == 'education_type':
                    node['type']=self.education_type
                elif node_predicate == 'education_degree':
                    node['type']=self.education_degree
                elif node_predicate == 'user':
                    node['type']=self.user
        return gml_graph
   
if __name__ == '__main__':
    dblp_path='/home/irma/workspace/some_scripts_martin_sampling/DATA/YEAST.gpickle'
    graph=nx.read_gpickle(dblp_path)
    for n in graph.nodes():
        if graph.node[n]['predicate']=='constant':
           print graph.node[n]
    