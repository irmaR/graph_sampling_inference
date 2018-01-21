
# experiment script for the new salsat synth problem

import graphcreator as gc

from sampler_general_ex import *
import time
import pickle
import numpy
import random
import networkx as nx
import sampling_utils as su
import matplotlib.pyplot as plt


def freqd_from_emb(D, P,  Plist,  embeddings):
    """Procedure that takes the already discovered embeddings and just populates freq_dict according to them.
    """
    freq_dict={}    # dictionary with tuples of values as keys and frequency as value: (my_salary_value, his_salary_value, my_satisfaction)
    for mapping in embeddings:
        # we'll get the target indices accoding to Plist and collect the values
        target_values = []
        for i in range(len(Plist)):
            if P.node[Plist[i]]['target'] == True:
                value_tuple = (P.node[Plist[i]]['label'] , D.node[mapping[i]]['value'])
                target_values.append(value_tuple)
        # now target_values contains all combinations of target nodes' label-value as tuples
        target_tuple = tuple(target_values)     # this makes a tuple (needed, since lists cannot be dict keys) from a list.
        if target_tuple in freq_dict:
            freq_dict[target_tuple] += 1
        else:
            freq_dict[target_tuple] = 1
    return freq_dict



start = time.time()
graph_file_name = "randomFriends_1000_04_4985_1000x07.gml.gz"
pattern_file_name = "new_salsat_pattern.gml"  # BEWARE: change below ALSO the Plist, OBdecomp and root-target AND fdict_ex pickle file !!!

#exhaustive makes: 24 388 685
##NLIMIT_values = [1000000, 2000000,  4000000, 6000000, 8000000, 10000000, 12000000, 14000000, 16000000, 18000000, 20000000, 22000000, 24388685]

D = nx.read_gml(graph_file_name)
# zdaj rabimo predobdelavo, da dodamo "predicate" v graf:
gc.impose_distribution(D,  None) # does not really impose distribution yet - just gives random values and "predicate" keys

P = nx.read_gml(pattern_file_name)
# --------------------------------------------############### ---------- HERE CHANGE ALL THOSE ALWAYS
Plist = [2, 4, 1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
##OBdecomp = [ [0], [1] , [2], [3, 4], [5] , [6,  7],  [8],  [9],  [10,  11] , [12],  [13] ]
root_nodes = [x for x in D.nodes() if D.node[x]['predicate']=='satisfaction']    

startEX = time.time()
(fdict_exhaustive,  embeddings) = sampling_exhaustive_general2(D,  P,  Plist,  root_nodes,  returnEmb = True)
stopEX = time.time()
print fdict_exhaustive

#---se priprava fdict_exhaustive:
complete_combinations(fdict_exhaustive, D,  P,  Plist)      # add zeros to all not present combinations
#-----------we should not smoot for this purpose    smooth(fdict_exhaustive,  fdict_exhaustive)     # Laplace smoothing also for the exhaustive
##pde = make_pd_general(fdict_exhaustive)
pde = make_pd_general_kickout(fdict_exhaustive,  trash_factor=0.01)     # we remove rows where frequencies do not reach 1% of embeddings
if len(pde) < 1:
    print "WARNING: bad (not enough present) pattern or too high trash threshold!"

targetpd = {
                ('high', 'high'): {'high': 0.30, 'mid': 0.50, 'low': 0.20}, 
                ('low', 'low'): {'high': 0.20, 'low': 0.30, 'mid': 0.50}, 
                ('mid', 'high'): {'high': 0.20, 'low': 0.30, 'mid': 0.50}, 
                ('low', 'mid'): {'high': 0.20, 'low': 0.30, 'mid': 0.50}, 
                ('high', 'low'): {'high': 0.80, 'mid': 0.15, 'low': 0.05}, 
                ('low', 'high'): {'high': 0.05, 'low': 0.80, 'mid': 0.15}, 
                ('high', 'mid'): {'high': 0.60, 'mid': 0.30, 'low': 0.10}, 
                ('mid', 'low'): {'high': 0.50, 'mid': 0.40, 'low': 0.10}, 
                ('mid', 'mid'): {'high': 0.15, 'mid': 0.70, 'low': 0.15}}
                
difference = su.avg_kld(transform_to_ptable(pde), targetpd)
print "the KLD compared to target dist: %.4f" % difference

start = time.time()


currentKLD = difference
random.shuffle(embeddings)          # random shuffling of the list of embeddings (in place - it changes the order in the original list)
for emb in embeddings:              # we take each embedding at random
    # 3, 1, 14    are node IDs of target nodes in the salsat pattern - totally DOMAIN DEPENDENT code here beware!
    # and since list indices start at 0 instead of 1, they are at positions 2, 0, 13  of embeddings (see Plist)
    # and we take one of its target nodes at random
    t_positions = [2, 0, 13]
    random.shuffle(t_positions)
    for tid in t_positions:
        nodeid = emb[tid]
        # now we try all three possible values - again, DOMAIN DEPENDENT
        madequick = freqd_from_emb(D, P,  Plist,  embeddings)
        complete_combinations(madequick, D,  P,  Plist)
        pdq = make_pd_general_kickout(madequick,  trash_factor=0.01)
        diff = su.avg_kld(transform_to_ptable(pdq), targetpd)
        best_diff = diff
        best_value = D.node[nodeid]['value']
        for value in ['low',  'mid',  'high']:      # DOMAIN DEPENDENT
            if value == best_value:
                pass
            else:
                D.node[nodeid]['value'] = value
                madequick = freqd_from_emb(D, P,  Plist,  embeddings)
                complete_combinations(madequick, D,  P,  Plist)
                pdq = make_pd_general_kickout(madequick,  trash_factor=0.01)
                diff = su.avg_kld(transform_to_ptable(pdq), targetpd)
                if diff < best_diff:
                    best_diff = diff
                    best_value = value
        D.node[nodeid]['value'] = best_value
        currentKLD = best_diff



##targetKLD = 0.01
##while currentKLD > targetKLD:
##    # we take a random embedding
##    emb = random.choice(embeddings)
##    # 3, 1, 14    are node IDs of target nodes in the salsat pattern - totally DOMAIN DEPENDENT code here beware!
##    # and since list indices start at 0 instead of 1, they are at positions 2, 0, 13  of embeddings (see Plist)
##    # and we take one of its target nodes at random
##    tid = random.choice([2, 0, 13])
##    nodeid = emb[tid]
##    # now we try all three possible values - again, DOMAIN DEPENDENT
##    madequick = freqd_from_emb(D, P,  Plist,  embeddings)
##    complete_combinations(madequick, D,  P,  Plist)
##    pdq = make_pd_general_kickout(madequick,  trash_factor=0.01)
##    diff = su.avg_kld(transform_to_ptable(pdq), targetpd)
##    best_diff = diff
##    best_value = D.node[nodeid]['value']
##    for value in ['low',  'mid',  'high']:      # DOMAIN DEPENDENT
##        if value == best_value:
##            pass
##        else:
##            D.node[nodeid]['value'] = value
##            madequick = freqd_from_emb(D, P,  Plist,  embeddings)
##            complete_combinations(madequick, D,  P,  Plist)
##            pdq = make_pd_general_kickout(madequick,  trash_factor=0.01)
##            diff = su.avg_kld(transform_to_ptable(pdq), targetpd)
##            if diff < best_diff:
##                best_diff = diff
##                best_value = value
##    D.node[nodeid]['value'] = best_value
##    currentKLD = best_diff


stop = time.time()

print "after some enforcing...through all embeddings..."
madequick = freqd_from_emb(D, P,  Plist,  embeddings)
complete_combinations(madequick, D,  P,  Plist)
pdq = make_pd_general_kickout(madequick,  trash_factor=0.01)
diff = su.avg_kld(transform_to_ptable(pdq), targetpd)
print "the KLD compared to target dist: %.8f" % diff
print " "
print "enforcing dist to this threshold took %.2f seconds." % float(stop-start)
