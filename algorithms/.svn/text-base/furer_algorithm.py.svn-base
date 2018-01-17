'''
Created on Apr 17, 2015

@author: irma
'''
#!/usr/bin/env python
import time,copy,random,math,sched,threading
import experiments.sampler_general_ex as smplr
import experiments.globals,os
from decimal import Decimal, getcontext

class Furer:
   D=None
   P=None
   root_nodes=None
   #short_graph_file_name=None
   output_path=None
   nodes_observed=-1
   lock=None
   nlimitlist=-1
   OBdecomp=None
   globalist_furer=None
   globaltimes_furer=None
   current_iteration=-1
   abort=False
   iteration_counter=0
   Zlist_dict=None
   report_flag=False
   freq_dict={}
   nr_embeddings_exhaustive=-1
   max_rec_fit_time=300
   running_bug_fixed_code=True
   ordering_of_target_nodes=None
   nr_targets=None
   
   def __init__(self,D, P, OBdecomp, root_nodes,NLIMIT,output_path,lock,current_iteration,nr_embeddings):
          self.D=D
          self.P=P
          self.OBdecomp=OBdecomp
          self.root_nodes=root_nodes
          self.output_path=output_path
          self.start_time_monitor=0
          self.end_time_monitor=0
          self.lock=lock
          self.nlimitlist=NLIMIT
          self.current_iteration=current_iteration
          self.nr_embeddings_exhaustive=nr_embeddings
          smplr.output_bug=output_path
          nr_target=0
          for n in P.nodes():
              if P.node[n]['target']==True:
                  nr_target+=1
          self.nr_targets=nr_target;
          with open(os.path.join(self.output_path,"furer_version.info"),'w') as f:
            if(self.running_bug_fixed_code):
                f.write("Running bug fix version of Furer.")
            else:
                f.write("Running old (no bug fix) version of Furer.")   
            f.close()   
       
   def run(self):
        """
        OBdecomp : ordered bipartite decomposition on P, which is given. First element is list with a root node. # [ [2] , [1,3] , [4] , [5, 6] ]
        """
        if(self.running_bug_fixed_code):
            print "Running bug fixed furer algorithm"
        else:
            print "Rning original furer code (no bug fix)"
        experiments.globals.globaltimes_furer[self.current_iteration] = [time.time()]
        experiments.globals.cqi[self.current_iteration] = 0
        experiments.globals.globalist_furer[self.current_iteration] = []
        freq_dict={}    # dictionary with tuples of values as keys and frequency as value
        self.Zlist_dict = {}     # Furer will result in a list of estimations for each tuple -> average of this list must be taken as frequency
        # out of debug we do not use a list actually: an integer is kept for every tuple, and divided by number of iterations at the end
        number_of_targets = 0
        for node in self.P.nodes():
            if self.P.node[node]['target'] == True:
                number_of_targets += 1
        # number_of_targets holds the number of target nodes that we are after
        self.nodes_observed = 0
        self.iteration_counter = 0
        matchings_found=0
        getcontext().prec = 100
        root_nodes_already_observed=[]
        nr_iterations=1
     
        seed_counter=1
        while True: 
            if(self.abort==True):
                for k in self.Zlist_dict.keys():
                    freq_dict[k] = (self.Zlist_dict[k])/float(self.iteration_counter)
                nr_emb=0
                for k in freq_dict.keys():
                    nr_emb+=freq_dict[k]
                with open(os.path.join(self.output_path,"final_embeddings.info"),'w') as f:
                    f.write(str(nr_emb))   
                return 
            #print "Observed: ",self.nodes_observed  
            #if self.nodes_observed>=2:
            #   self.abort=True
            if experiments.globals.same_seed:
                random.seed(seed_counter)
                seed_counter+=1
            if self.nodes_observed in self.nlimitlist:# and experiments.globals.cqi[self.current_iteration]<len(self.nlimitlist) and self.nodes_observed > self.nlimitlist[experiments.globals.cqi[self.current_iteration]]:
                experiments.globals.cqi[self.current_iteration] = experiments.globals.cqi[self.current_iteration]+1    # we increase the index of position of quota to check upon
                total_Zlist_dict_copy = copy.deepcopy(self.Zlist_dict)
                smplr.handle_quota_Furer(self.D,  self.P, total_Zlist_dict_copy,  [0,None], self.iteration_counter,self.current_iteration)
            rand_nr=random.randrange(len(self.root_nodes))
            n = self.root_nodes[rand_nr]
            #print "ROOT NODE: ",self.D.node[n]
            self.iteration_counter = self.iteration_counter +1
            self.nodes_observed = self.nodes_observed + 1
            list_for_spent = []
            list_for_spent.append(self.nodes_observed)

            if(self.running_bug_fixed_code):
               result = smplr.rec_fit_Furer_bug_fix([n], self.D,  self.P,  self.OBdecomp,  0,  [],  self.nlimitlist,  list_for_spent,  self.Zlist_dict,  self.iteration_counter,  0,self.current_iteration)
            else:
               result = smplr.rec_fit_Furer([n], self.D,  self.P,  self.OBdecomp,  0,  [],  self.nlimitlist,  list_for_spent,  self.Zlist_dict,  self.iteration_counter,  0,self.current_iteration)
            self.nodes_observed = list_for_spent[0]
            matches_found_root_node=0
            if result[1] != None:
                actualX = result[0] * len(self.root_nodes)
                matches_found_root_node=actualX
                mapping = result[1]     # this is mapping for OBdecomp FLAT.
                OBd_flat = [item for sublist in self.OBdecomp for item in sublist]
                target_values = [None]*self.nr_targets
                for i in range(len(OBd_flat)):
                    if self.P.node[OBd_flat[i]]['target'] == True:
                        if 'value' in self.D.node[mapping[i]]:
                            value=self.D.node[mapping[i]]['value']
                            value_tuple = (self.P.node[OBd_flat[i]]['label'] , value)
                            if self.ordering_of_target_nodes!=None:
                                target_values[self.ordering_of_target_nodes[OBd_flat[i]]]=value_tuple
                            else:
                                target_values.append(value_tuple)                
                target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.    
                with self.lock:
                    if target_tuple in self.Zlist_dict:   # this checks for KEYS in Zlist_dict
                        self.Zlist_dict[target_tuple] = self.Zlist_dict[target_tuple]+ actualX
                    else:
                        self.Zlist_dict[target_tuple] = 0
                        self.Zlist_dict[target_tuple] = self.Zlist_dict[target_tuple] + actualX
            nr_emb=get_nr_embeddings(self.Zlist_dict,self.iteration_counter)
            nr_extra_embeddings=(Decimal(nr_emb)-Decimal(experiments.globals.sum_number_of_embeddings))
            experiments.globals.sum_number_of_embeddings+=Decimal(nr_emb)
            experiments.globals.sum_of_the_square_embeddings+=Decimal(math.pow((nr_emb),2))
            experiments.globals.sum_number_of_extra_embeddings+=Decimal(matches_found_root_node)
            experiments.globals.sum_of_the_square_extra_embeddings+=Decimal(math.pow((matches_found_root_node),2))
            experiments.globals.embeddings_estimate=nr_emb
            experiments.globals.nr_iterations=self.iteration_counter

            
        if (experiments.globals.cqi[self.current_iteration] < len(self.nlimitlist)) and (self.nodes_observed >= self.nlimitlist[experiments.globals.cqi[self.current_iteration]]):
            experiments.globals.cqi[self.current_iteration] = experiments.globals.cqi[self.current_iteration] +1    # we increase the index of position of quota to check upon
            total_Zlist_dict_copy = copy.deepcopy(self.Zlist_dict)
            smplr.handle_quota_Furer(self.D,  self.P, total_Zlist_dict_copy,  [0,None], self.iteration_counter,self.current_iteration)
        
        return [experiments.globals.globalist_furer[self.current_iteration],  experiments.globals.globaltimes_furer[self.current_iteration]]

def get_nr_embeddings(Zlist,current_iteration):
    nr_emb=0
    for k in Zlist.keys():
        nr_emb+=Zlist[k]/float(current_iteration)
    return nr_emb
        