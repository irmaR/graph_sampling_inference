'''
Created on Apr 17, 2015

@author: irma
'''
import time,copy,random,math
import experiments.sampler_general_ex as smplr
import experiments.globals,os,sched,threading

class False_Furer:
   D=None
   P=None
   root_nodes=None
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
   
   def __init__(self,D, P, OBdecomp, root_nodes,NLIMIT,output_path,lock,current_iteration,nr_embeddings_exhaustive):
          self.D=D
          self.P=P
          self.OBdecomp=OBdecomp
          self.root_nodes=root_nodes
          self.output_path=output_path
          self.start_time_monitor=0
          self.end_time_monitor=0
          self.lock=lock
          self.nlimitlist=NLIMIT
          #self.detailed_result_path=detailed_result_path
          self.current_iteration=current_iteration
          self.nr_embeddings_exhaustive=nr_embeddings_exhaustive
          
   def run(self):
    """
    OBdecomp : ordered bipartite decomposition on P, which is given. First element is list with a root node. # [ [2] , [1,3] , [4] , [5, 6] ]
    """
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
    
    #while self.nodes_observed <= max(self.nlimitlist):
    while True:
        if(self.abort==True):
                #print "NR EMBEDDINGS (OVERALL):"
                for k in self.Zlist_dict.keys():
                    freq_dict[k] = (self.Zlist_dict[k])/float(self.iteration_counter)
                nr_emb=0
                for k in freq_dict.keys():
                    nr_emb+=freq_dict[k]
                print "IS : ",nr_emb
                with open(os.path.join(self.output_path,"final_embeddings.info"),'w') as f:
                    f.write(str(nr_emb))
                return          
        if self.nodes_observed in self.nlimitlist and experiments.globals.cqi[self.current_iteration]<len(self.nlimitlist) and self.nodes_observed > self.nlimitlist[experiments.globals.cqi[self.current_iteration]]:
            experiments.globals.cqi[self.current_iteration] = experiments.globals.cqi[self.current_iteration] +1    # we increase the index of position of quota to check upon
            total_Zlist_dict_copy = copy.deepcopy(self.Zlist_dict)
            smplr.handle_quota_Furer(self.D,  self.P, total_Zlist_dict_copy,  [0,None], self.iteration_counter,self.current_iteration)
            ##print "Call to Furer quota handling (main routine) at quota %d" % nlimitlist[cqi-1]
        self.iteration_counter = self.iteration_counter +1
        
        n = self.root_nodes[random.randrange(len(self.root_nodes))]
        self.nodes_observed = self.nodes_observed + 1
        list_for_spent = []
        list_for_spent.append(self.nodes_observed)
        
        #s = sched.scheduler(time.time, time.sleep)
        #e1=s.enter(0, 4,smplr.rec_fit_False_Furer_global,([n], self.D,  self.P,  self.OBdecomp,  0,  [],  self.nlimitlist,  list_for_spent,  self.Zlist_dict,  self.iteration_counter,  0,self.current_iteration))
        #t = threading.Thread(target=s.run)
        #t.daemon=True
        #t.start()
        #t.join()
        #result=smplr.temp_result
        result = smplr.rec_fit_False_Furer([n], self.D,  self.P,  self.OBdecomp,  0,  [],  self.nlimitlist,  list_for_spent,  self.Zlist_dict,  self.iteration_counter,  0,self.current_iteration)
        self.nodes_observed = list_for_spent[0]
        if result[1] != None:
            actualX = result[0] * len(self.root_nodes)
            mapping = result[1]     # this is mapping for OBdecomp FLAT.
            OBd_flat = [item for sublist in self.OBdecomp for item in sublist]
            target_values = []
            for i in range(len(OBd_flat)):
                if self.P.node[OBd_flat[i]]['target'] == True:
                    if self.P.node[OBd_flat[i]]['target'] == True:
                       value_tuple = (self.P.node[OBd_flat[i]]['label'] , self.D.node[mapping[i]]['value'])
                       target_values.append(value_tuple)
            # now target_values contains all combinations of target nodes' label-value as tuples
            target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.
            
            with self.lock:
                if target_tuple in self.Zlist_dict:   # this checks for KEYS in Zlist_dict
                    self.Zlist_dict[target_tuple] = self.Zlist_dict[target_tuple] + actualX
                else:
                    self.Zlist_dict[target_tuple] = 0
                    self.Zlist_dict[target_tuple] = self.Zlist_dict[target_tuple] + actualX
                    
        nr_emb=get_nr_embeddings(self.Zlist_dict,self.iteration_counter)
        nr_extra_embeddings=(nr_emb-experiments.globals.sum_number_of_embeddings)
        experiments.globals.sum_number_of_embeddings+=nr_emb
        experiments.globals.sum_of_the_square_embeddings+=math.pow((nr_emb),2)
        experiments.globals.nr_iterations=self.iteration_counter

    if (experiments.globals.cqi[self.current_iteration] < len(self.nlimitlist)) and (self.nodes_observed >= self.nlimitlist[experiments.globals.cqi[self.current_iteration]]):
        experiments.globals.cqi[self.current_iteration] = experiments.globals.cqi[self.current_iteration] +1    # we increase the index of position of quota to check upon
        total_Zlist_dict_copy = copy.deepcopy(self.Zlist_dict)
        smplr.handle_quota_Furer(self.D,  self.P, total_Zlist_dict_copy,  [0,None], self.iteration_counter,self.current_iteration)
        ##print "Call to Furer quota handling (main routine down) at quota %d" % nlimitlist[cqi-1]

    for k in self.Zlist_dict.keys():
        freq_dict[k] = (self.Zlist_dict[k])/float(self.iteration_counter)   # simply an average of a list
    # now with quota handler we just return global lists of freqdicts
    return [experiments.globals.globalist_furer[self.current_iteration],  experiments.globals.globaltimes_furer[self.current_iteration]]

def get_nr_embeddings(Zlist,current_iteration):
    nr_emb=0
    for k in Zlist.keys():
        nr_emb+=Zlist[k]/float(current_iteration)
    return nr_emb