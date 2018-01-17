'''
Created on Apr 15, 2015

@author: irma
'''
import timeit
import experiments.sampler_general_ex as smplr
import time,threading
import experiments
from multiprocessing.pool import ThreadPool
import sched
import multiprocessing as mp
from multiprocessing import Process, Queue

def find_nr_emb(D, P,Plist,  root_nodes,output_path,lock):
        """A procedure that is GENERAL and can sample general graphs for patterns
        D : domain graph (networkx graph with 'predicate' and 'value' attributes)
        P : pattern graph (networkx graph with 'predicate' and 'value' attributes, and 'target' boolean value)
        Plist : ordered list of P nodes
        root_nodes: list of nodes of D that match the root node of P, given in advance, not considered part of sampling procedure
        """
        start = timeit.timeit()
        print "exhaustive approach"
        experiments.globals.fdict_exhaustive_limited={}
        number_of_targets = 0
        for node in P.nodes():
            if P.node[node]['target'] == True:
                number_of_targets += 1
        # number_of_targets holds the number of target nodes that we are after
        nodes_observed = 0
        
        print "Number of root nodes: ",len(root_nodes)
        for n in root_nodes: 
            nodes_observed = nodes_observed + 1
            list_for_spent = []
            list_for_spent.append(nodes_observed)
            infinity = float("inf")
            mappings_list = smplr.rec_fit_limited_basic(n, D,  P, Plist,  0,  [],  [infinity],  list_for_spent,experiments.globals.fdict_exhaustive_limited,1)
            nodes_observed = list_for_spent[0]
            if(nodes_observed==1):
                raise Wrong_root_node('cannot use this one as a root node')
            #print "mappings list: ",mappings_list
            for mapping in mappings_list:
                #print  "well get the target indices accoding to Plist and collect the values"
                target_values = []
                for i in range(len(Plist)):
                    if P.node[Plist[i]]['target'] == True:
                        value_tuple = (P.node[Plist[i]]['label'] ,D.node[mapping[i]]['value'])
                        target_values.append(value_tuple)
                # now target_values contains all combinations of target nodes' label-value as tuples
                target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.            
                #print "Target tuple: ",target_tuple
                
            
                if target_tuple in experiments.globals.fdict_exhaustive_limited:
                        experiments.globals.fdict_exhaustive_limited[target_tuple] += 1
                        experiments.globals.fdict_exhaustive_limited=experiments.globals.fdict_exhaustive_limited
                else:
                        experiments.globals.fdict_exhaustive_limited[target_tuple] = 1
              
        return (experiments.globals.fdict_exhaustive_limited,nodes_observed)


class Exhaustive_sampling_inf:
    D=None
    P=None
    Plist=None
    root_nodes=None
    short_graph_file_name=None
    output_path=None
    freq_dict=None
    nodes_observed=0
    lock=None
    abort=False
    max_time_execution_seconds=None
    all_emb=0
   
    def __init__(self,D, P,Plist,  root_nodes,output_path,lock):
      self.D=D
      self.P=P
      self.Plist=Plist
      self.root_nodes=root_nodes
      self.output_path=output_path
      self.start_time_monitor=0
      self.end_time_monitor=0
      self.lock=lock
    
    
    def update_freq_dict(self,mappings,nodes_observed,Plist,P,D,lock,freq_dict):   
        mappings_list=mappings
        nr_emb_temp=0
        list_for_spent=nodes_observed
        nodes_observed = list_for_spent[0]
        if(nodes_observed==1):
            raise Wrong_root_node('cannot use this one as a root node')
        counter=0
        for mapping in mappings_list:
            experiments.globals.nr_embeddings_exhaustive+=1
            counter+=1
            target_values = []
            for i in range(len(Plist)):
                if P.node[Plist[i]]['target'] == True:
                    value_tuple = (P.node[Plist[i]]['label'] , D.node[mapping[i]]['value'])
                    target_values.append(value_tuple)
            target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.            
            if lock!=None:
                with lock:
                    if target_tuple in freq_dict:
                        freq_dict[target_tuple] += 1
                        experiments.globals.fdict_exhaustive_limited=freq_dict
                    else:
                        freq_dict[target_tuple] = 1
                        experiments.globals.fdict_exhaustive_limited=freq_dict
            else:
                    if target_tuple in freq_dict:
                        freq_dict[target_tuple] += 1
                        experiments.globals.fdict_exhaustive_limited=freq_dict
                    else:
                        freq_dict[target_tuple] = 1
                        experiments.globals.fdict_exhaustive_limited=freq_dict
        #print "End nr emb: ",experiments.globals.nr_embeddings_exhaustive
        return freq_dict
        
    
    def run(self):
        """A procedure that is GENERAL and can sample general graphs for patterns
        D : domain graph (networkx graph with 'predicate' and 'value' attributes)
        P : pattern graph (networkx graph with 'predicate' and 'value' attributes, and 'target' boolean value)
        Plist : ordered list of P nodes
        root_nodes: list of nodes of D that match the root node of P, given in advance, not considered part of sampling procedure
        """
        start = timeit.timeit()
        print "exhaustive approach"
        experiments.globals.abort=False
        self.freq_dict={}
        experiments.globals.fdict_exhaustive_limited=self.freq_dict
        number_of_targets = 0
        for node in self.P.nodes():
            if self.P.node[node]['target'] == True:
                number_of_targets += 1
        self.nodes_observed = 0
        experiments.globals.nr_root_nodes=len(self.root_nodes)
        experiments.globals.temporary_observed=[]
        experiments.globals.temporary_observed.append(0)
        counter=0
        for n in self.root_nodes:
            experiments.globals.last_seen_root_node=self.D.node[n]
            counter+=1
            experiments.globals.nr_root_nodes_observed_so_far=counter
            if(self.abort==True):
                    print "Aborting main method... exhaustive ...timeout"
                    sum = 0
                    for k in self.freq_dict.keys():
                        sum = sum + self.freq_dict[k]
                    print "Number of embeddings: ",sum
                    return 
            if(counter==len(self.root_nodes)):
                self.abort==True
            experiments.globals.temporary_observed[0]=experiments.globals.temporary_observed[0]+1
            self.nodes_observed = experiments.globals.temporary_observed[0]
            mappings_list=[]
            infinity = float("inf")
            self.list_for_spent = []
            self.list_for_spent.append(self.nodes_observed)
            experiments.globals.temporary_embeddings=[]
            #with self.lock:
            start = timeit.default_timer()
            smplr.rec_fit_limited_global(n, self.D,  self.P,  self.Plist,  0,  [],  [infinity],  self.list_for_spent, self.freq_dict,1,self.lock,"exhaustive",self.root_nodes)
            
            end=timeit.default_timer()
            experiments.globals.root_node_embeddings.append((self.D.node[n],experiments.globals.nr_embeddings_exhaustive,(end-start)))
            if(self.abort==True):
                        print "Aborting main method... exhaustive ...timeout"
                        return 
        return (self.freq_dict, self.nodes_observed)

def update_freq_dict(mappings,nodes_observed,Plist,P,D,lock,freq_dict): 
        experiments.globals.main_exhaustive_reporting=True
        with lock:
            #print "IN MAIN Nr global emb before addition: ",experiments.globals.nr_embeddings_exhaustive 
            #print "Adding: ",len(mappings)
            mappings_list=mappings
            nr_emb_temp=0
            list_for_spent=nodes_observed
            nodes_observed = list_for_spent[0]
            if(nodes_observed==1):
                raise Wrong_root_node('cannot use this one as a root node')
            counter=0
            for mapping in mappings_list:
                experiments.globals.nr_embeddings_exhaustive+=1
                counter+=1
                target_values = []
                for i in range(len(Plist)):
                    if P.node[Plist[i]]['target'] == True:
                        value_tuple = (P.node[Plist[i]]['label'] , D.node[mapping[i]]['value'])
                        target_values.append(value_tuple)
                target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.            
                
                if target_tuple in freq_dict:
                            freq_dict[target_tuple] += 1
                            experiments.globals.fdict_exhaustive_limited=freq_dict
                else:
                            freq_dict[target_tuple] = 1
                            experiments.globals.fdict_exhaustive_limited=freq_dict
            #print "After adding: ",len(mappings)," is: ",experiments.globals.nr_embeddings_exhaustive
            experiments.globals.main_exhaustive_reporting=False
        return freq_dict
               
    
class Wrong_root_node(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

     
     

        


