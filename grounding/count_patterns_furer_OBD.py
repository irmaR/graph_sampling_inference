import networkx as nx
from algorithms import exhaustive_approach_inf
from experiments import furer_sampling_approach
from experiments import OBDsearch
from grounding import ground_target_predicate as gtp
import csv,math,sys,os,pickle
from graph_manipulator import visualization
import count_exact_patterns



def furer_OBD(pattern,data_graph,OBdecomp,root_node,time):
    NLIMIT_values=[9000]
    print "Running Furer for: "+str(time)+" seconds ..."
    monitoring_marks=generate_monitoring_marks(time,time)
    emb=furer_sampling_approach.get_nr_embedding(data_graph, pattern, OBdecomp,root_node,NLIMIT_values,monitoring_marks)
    return emb

def generate_monitoring_marks(time_interval_in_seconds,max_time_in_seconds):
    counter=0
    marks=[]
    while counter+time_interval_in_seconds<=max_time_in_seconds:
        marks.append(counter+time_interval_in_seconds)
        counter=counter+time_interval_in_seconds
    return marks

def count_combinations_arity_2(grounding_dictionary,ind1,ind2,pattern_equivalences,pattern_non_equivalences):
   output_dict={}
   for k in grounding_dictionary.keys():
       if not satisfied_equivalences(k,pattern_equivalences) and not satisfied_non_equivalence(k,pattern_non_equivalences):
           continue
       key=(k[ind1][1],k[ind2][1])
       if not key in output_dict:
           output_dict[key]=grounding_dictionary[k]
       else:
           output_dict[key]+=grounding_dictionary[k]
   print "Size dict: ",len(output_dict)
   for k in output_dict:
       print k,output_dict[k]
   return output_dict

def ground_the_pattern(data_graph,pattern,OBD,root_node,binding_indices,time,pattern_equivalences,pattern_non_equivalences):
    Plist = [item for sublist in OBD for item in sublist]
    indices=[]
    for b in binding_indices:
        indices.append(Plist.index(b))

    if pattern_equivalences==None:
        patt_equiv_indices=None
    else:
        patt_equiv_indices = []
        for eq in pattern_equivalences:
            ar=[]
            for eq1 in eq:
                ar.append(Plist.index(eq1))
            patt_equiv_indices.append(ar)

    if pattern_non_equivalences==None:
        patt_non_equiv_indices=None
    else:
        patt_non_equiv_indices = []
        for eq in pattern_non_equivalences:
            ar=[]
            for eq1 in eq:
                ar.append(Plist.index(eq1))
                patt_non_equiv_indices.append(ar)
    dictionary = furer_OBD(pattern, data_graph, OBD, root_node,time)
    return count_combinations_arity_2(dictionary, indices[0], indices[1],patt_equiv_indices,patt_non_equiv_indices)


def ground_the_target(data_graph,target,OBD,root_node,binding_indices):
    Plist = [item for sublist in OBD for item in sublist]
    indices=[]
    for b in binding_indices:
        indices.append(Plist.index(b))
    dictionary = count_exact_patterns.exact_counting_no_time_limit(target, data_graph, OBD, root_node)
    return count_combinations_arity_2(dictionary, indices[0], indices[1],None,None)


def get_time_for_exact(patterns,time_dict):
    out={}
    time_dict_exact={}
    with open(time_dict) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            time_dict_exact[str(row['pattern'])]=float(row['time'])
    for p in patterns:
        if p.name.lstrip().rstrip() in time_dict_exact:
            out[p.name.lstrip().rstrip()]=time_dict_exact[p.name.lstrip().rstrip()]
        else:
            raise KeyError('No pattern '+p.name+' in exact dictionary. Check the patterns specified!')
    return out

def satisfied_equivalences(grounding,equivalences):
    if equivalences==None:
        return True
    for eq in equivalences:
        if grounding[eq[0]][1]!=grounding[eq[1]][1]:
            return False
    return True

def satisfied_non_equivalence(grounding,non_equivalences):
    if non_equivalences==None:
        return True
    for eq in non_equivalences:
        if grounding[eq[0]][1]==grounding[eq[1]][1]:
            return False
    return True

def generate_csv_furerOBD_count(data_graph,target_graph,target_constant,target_attr,OBDTarget,root_node_target,patterns,OBDPatterns,indices,root_nodes_patterns,pattern_equivalence,non_equivalences,csvfile,fieldnames,time_dict,runtime):
    tg = gtp.find_all_groundings_of_predicates(data_graph, target_attr, target_constant)
    # for each ground target, ground all patterns and perfom counting, output a csv row
    dictionary_target_counts = {}
    pattern_groundings = []

    if runtime==None:
      exact_time_dict=get_time_for_exact(patterns,time_dict)
    counter = 0
    # count the patterns
    for pattern, OBD, root_node, indices in zip(patterns, OBDPatterns, root_nodes_patterns, indices):
        #take 10 percent of time
        #furer_max_time=int((10 * furer_max_time) / 100.0)
        if runtime==None:
            furer_max_time = exact_time_dict[pattern.name]
            runtime=furer_max_time
        #if runtime!=None and not runtime<=furer_max_time:
        #    pattern_groundings.append({})
        #    print "Runtime not good: ",runtime,furer_max_time
        #    continue
        pattern_groundings.append(ground_the_pattern(data_graph, pattern, OBD, root_node, indices,runtime,pattern_equivalence[counter],non_equivalences[counter]))
        counter+=1
    target_counts = ground_the_target(data_graph, target_graph, OBDTarget, root_node_target, [1, 2])
    print "All patterns counted"
    for target in tg:
        key = (target.node[1]['value'], target.node[2]['value'])
        if key in target_counts:
            nr_target = target_counts[key]
        else:
            nr_target = 0
        dictionary_target_counts[key] = nr_target
    with open(csvfile, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for target in tg:
            res_dict = {}
            key = (target.node[1]['value'], target.node[2]['value'])
            res_dict['target'] = dictionary_target_counts[key]
            res_dict['dummy'] = key
            field_counter = 2
            pattern_counter=0
            for p in patterns:
                if key in pattern_groundings[pattern_counter]:
                    res_dict[fieldnames[field_counter]] = pattern_groundings[pattern_counter][key]
                else:
                    res_dict[fieldnames[field_counter]] = 0
                field_counter += 1
                pattern_counter+=1
            writer.writerow(res_dict)




if __name__ == '__main__':
   #dict_path='/home/irma/work/DATA/DATA/yeast/exhaustive_approach/fdict_exhaustive_pattern4.pickle'
   #pkl_file = open(dict_path, 'rb')
   #count_combinations_arity_2(pickle.load(pkl_file),0,2)

   #data_graph = '/home/irma/work/DATA/DATA/yeast/YEAST_equiv.gpickle'
   #data_graph = nx.read_gpickle(data_graph)
   data_graph = '/home/irma/work/DATA/DATA/yeast/dummy_yeast.gml'
   data_graph = nx.read_gml(data_graph)

   #Target
   target_attr = 'function'
   target_constant = 'constant'
   root_node_target = 'function'
   target=gtp.get_target_graph(target_constant, target_attr)
   OBD1 = OBDsearch.get_heuristic4_OBD(target, startNode=2)
   print OBD1
   OBDTarget = [[2], [1]]
   print OBDTarget

   # pattern=nx.read_gml('/home/irma/work/DATA/DATA/yeast/pattern4.gml')
   # #ground_pattern = gtp.ground_pattern(tg, pattern)
   # OBD1 = OBDsearch.get_heuristic4_OBD(pattern, startNode = 6)
   # patterns=[pattern]
   # OBDPatterns=[OBD1]
   # root_nodes_patterns=['function']
   # indices=[[1,6]]
   # csvfile = '/home/irma/work/DATA/DATA/yeast/testFurer.csv'
   # fieldnames = ['dummy','target', 'patt2']
   # generate_csv_furerOBD_count(data_graph, target, OBDTarget, root_node_target, patterns,OBDPatterns,indices, root_nodes_patterns, csvfile, fieldnames)

