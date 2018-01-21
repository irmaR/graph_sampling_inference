
# a collection of functions for creation of synthetic graphs

import networkx as nx
import random,os
import copy,math,argparse
import numpy as np

def random_friends_graph(number_people, percentage_men, number_friends, number_married,  cdists):
    """
    creates a synthetic graph for the 'salary satisfaction' problem
    no string labels, only IDs. And all predicates are integers.
    """
    # before starting - some checks
    if number_married > number_people:
        print "ERROR, more married than all existing! Aborting."
        return None
    if (number_married % 2) != 0:
        print "WARNING: number of married not even. The algorithm will assume number of married + 1."
    #start
    G=nx.MultiGraph()       # MultiGraph - to allow for multiple edges among two nodes - no really needed currently (2013)
    # first we create all persons:
    idcounter = 1
    men_to_add = int(percentage_men * number_people)        # we discard everything after decimal dot
    women_to_add = number_people - men_to_add
    Men = []
    Women = []
    for i in range(number_people):
        person_id = idcounter
        G.add_node(person_id,  id=idcounter,  label="person")
        idcounter = idcounter + 1
        # to each person a gender node is attached
        if men_to_add >0:
            Men.append(person_id)
            man_id = idcounter
            G.add_node(man_id,  id=idcounter,  label="man")
            G.add_edge(person_id,  man_id)
            idcounter = idcounter + 1
            men_to_add = men_to_add -1
        elif women_to_add >0:
            Women.append(person_id)
            woman_id = idcounter
            G.add_node(woman_id,  id=idcounter,  label="woman")
            G.add_edge(person_id,  woman_id)
            idcounter = idcounter + 1
            women_to_add = women_to_add -1
        else:
            print "WARNING: men and women do not add up to the number of persons."
        # and to each person salary and satisfaction is attached
        salary_id = idcounter
        G.add_node(salary_id,  id=idcounter,  label="salary")
        idcounter = idcounter + 1
        ###G.node[salary_id]['value']=random_from_distribution({'low':0.40,  'mid':0.20,  'high':0.40})
        G.add_edge(person_id,  salary_id)
        satisfaction_id = idcounter
        ###satisfaction_value = random_from_distribution({'low':0.40,  'mid':0.20,  'high':0.40})
        G.add_node(satisfaction_id,  id=idcounter,  label="satisfaction")
        idcounter = idcounter + 1
        G.add_edge(person_id,  satisfaction_id)
    # now we add [married] nodes at random pairs
    married_to_add = number_married
    Married = []
    while married_to_add > 0:
        h = random.choice(Men)
        w = random.choice(Women)
        if (h not in Married) and (w not in Married):
            Married.append(h)
            Married.append(w)
            married_id = idcounter
            G.add_node(married_id,  id=idcounter,  label="married")
            G.add_edge(married_id,  h)
            G.add_edge(married_id,  w)
            idcounter = idcounter + 1
            married_to_add = married_to_add - 2
    # now we add friends at random (no self-friends, no marriage-friends)
    friends_to_add = number_friends
    Friends = []
    while friends_to_add > 0:
        f1 = random.choice(Men+Women)
        f2 = random.choice(Men+Women)
        if (f1 != f2) and ( (f1,  f2) not in Married ) and ( (f2,  f1) not in Married ) and ( (f1,  f2) not in Friends ) and ( (f2,  f1) not in Friends ):
            Friends.append( (f1, f2) )
            friends_id = idcounter
            G.add_node(friends_id,  id = idcounter,  label="friends")
            idcounter = idcounter + 1
            G.add_edge(friends_id,  f1)
            G.add_edge(friends_id,  f2)
            friends_to_add = friends_to_add - 1
    # everything added
    # here a CALL to procedure to populate salary and satisfaction values would be in order
    return G



def powerlaw_friends_graph(number_people, percentage_men, number_friends_initiated, number_married,  cdists):
    """
    creates a synthetic graph for the 'salary satisfaction' problem
    no string labels, only IDs. And all predicates are integers.
    """
    # before starting - some checks
    if number_married > number_people:
        print "ERROR, more married than all existing! Aborting."
        return None
    if (number_married % 2) != 0:
        print "WARNING: number of married not even. The algorithm will assume number of married + 1."
    #start
    G=nx.MultiGraph()       # MultiGraph - to allow for multiple edges among two nodes - no really needed currently (2013)
    # first we create all persons:
    idcounter = 1
    men_to_add = int(percentage_men * number_people)        # we discard everything after decimal dot
    women_to_add = number_people - men_to_add
    Men = []
    Women = []
    for i in range(number_people):
        person_id = idcounter
        G.add_node(person_id,  id=idcounter,  label="person")
        idcounter = idcounter + 1
        # to each person a gender node is attached
        if men_to_add >0:
            Men.append(person_id)
            man_id = idcounter
            G.add_node(man_id,  id=idcounter,  label="man")
            G.add_edge(person_id,  man_id)
            idcounter = idcounter + 1
            men_to_add = men_to_add -1
        elif women_to_add >0:
            Women.append(person_id)
            woman_id = idcounter
            G.add_node(woman_id,  id=idcounter,  label="woman")
            G.add_edge(person_id,  woman_id)
            idcounter = idcounter + 1
            women_to_add = women_to_add -1
        else:
            print "WARNING: men and women do not add up to the number of persons."
        # and to each person salary and satisfaction is attached
        salary_id = idcounter
        G.add_node(salary_id,  id=idcounter,  label="salary")
        idcounter = idcounter + 1
        ###G.node[salary_id]['value']=random_from_distribution({'low':0.40,  'mid':0.20,  'high':0.40})
        G.add_edge(person_id,  salary_id)
        satisfaction_id = idcounter
        ###satisfaction_value = random_from_distribution({'low':0.40,  'mid':0.20,  'high':0.40})
        G.add_node(satisfaction_id,  id=idcounter,  label="satisfaction")
        idcounter = idcounter + 1
        G.add_edge(person_id,  satisfaction_id)
    # now we add [married] nodes at random pairs
    married_to_add = number_married
    Married = []
    while married_to_add > 0:
        h = random.choice(Men)
        w = random.choice(Women)
        if (h not in Married) and (w not in Married):
            Married.append(h)
            Married.append(w)
            married_id = idcounter
            G.add_node(married_id,  id=idcounter,  label="married")
            G.add_edge(married_id,  h)
            G.add_edge(married_id,  w)
            idcounter = idcounter + 1
            married_to_add = married_to_add - 2
    print "Married set ..."
    # now we add friends according to power-law (no self-friends, no marriage-friends)
    Friends = []
    # first 'number_friends_initiated' amount of persons gets into core to be fully connected as friends
    Core = []
    while len(Core) != number_friends_initiated:
        c = random.choice(Men+Women)
        good_core_cand = True
        if c in Core:
            good_core_cand = False
        for el in Core:
            if ( (c, el) in Married ) or ( (el, c) in Married ):
                good_core_cand = False
        if good_core_cand == True:
            Core.append(c)
    # now fully connect the core elements
    allFriends = 0
    print "Core friends set ..."
    for i in range(len(Core)):
        for j in range(i+1, len(Core)):
            f1 = Core[i]
            f2 = Core[j]
            Friends.append( (f1, f2) )
            friends_id = idcounter
            G.add_node(friends_id,  id = idcounter,  label="friends")
            allFriends = allFriends + 1
            idcounter = idcounter + 1
            G.add_edge(friends_id,  f1)
            G.add_edge(friends_id,  f2)
    # finally add the rest
    Friendlyfied = {}
    for corel in Core:
        Friendlyfied[corel] = number_friends_initiated - 1    # core ones all have so much friends
    for const in Men+Women:
        if const not in Core:
            Friendlyfied[const] = 0
            friends_to_add = number_friends_initiated
            thisconstfriends = []
            while friends_to_add > 0:
                friend = random.choice(Friendlyfied.keys())
                if (friend != const) and (friend not in thisconstfriends):
                    p = float(Friendlyfied[friend]) / allFriends
                    chance = random.uniform(0,1)
                    if p > chance:
                        Friends.append( (friend, const) )
                        friends_id = idcounter
                        G.add_node(friends_id,  id = idcounter,  label="friends")
                        allFriends = allFriends + 1
                        idcounter = idcounter + 1
                        G.add_edge(friends_id,  friend)
                        G.add_edge(friends_id,  const)
                        Friendlyfied[const] = Friendlyfied[const] + 1
                        Friendlyfied[friend] = Friendlyfied[friend] + 1
                        thisconstfriends.append(friend)
                        friends_to_add = friends_to_add - 1
    # everything added
    # here a CALL to procedure to populate salary and satisfaction values would be in order
    return G





def impose_distribution(G,  dist):
    """procedure for imposing values to prob. variables in salsat problem so that the values in embeddings follow the given distribution"""
    # first, the values are set uniformly random
    for n in G.nodes():
        if (G.node[n]['label'] == 'salary') or (G.node[n]['label'] == 'satisfaction'):
            choice = random.choice(['high',  'mid',  'low'])
            G.node[n]['value'] = choice
    # now all the target values are set uniformly at random - we proceed with refinement towards --dist--
    # ZDAJ dodamo PREDICATE, da lahko uporabimo staro kodo:
    for n in G.nodes():
        G.node[n]['predicate'] = G.node[n]['label']
    # IN smo res pripravljeni na iskanje embedding-distribucije
    
    

def main_powerlaw(output_path,V,c2,d):
    name_of_folder="PL_"+str(V)+"_"+str(c2)+"_"+str(d)
    path_to_folder=os.path.join(output_path,name_of_folder)
    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder)
    nr_persons=V
    percentage_men=40
    percentage_women=60
    percentage_married=40
    men_number=(nr_persons*percentage_men/100)
    nr_married=(men_number*percentage_married/100)
    nr_nodes=int((nr_persons*percentage_men/100)+(nr_persons*percentage_women/100)+2*nr_persons+nr_persons+nr_married)
    nr_friends=V*c2+V*V*d
   
    print "Nr nodes: ",nr_nodes
    print "Nr friends: ",nr_friends
    print "Nr married: ",nr_married
    print "Percentage men: ",percentage_men/float(100)
    H = powerlaw_friends_graph(nr_persons, percentage_men/float(100), nr_friends, nr_married, None)
    print "NR NODES: ",nx.number_of_nodes(H)
    print "NR EDGES: ",nx.number_of_edges(H)
    degree_sequence=sorted(nx.degree(H).values(),reverse=True) # degree sequence
    dmax=max(degree_sequence)
    davg=np.mean(degree_sequence)
    density=(2*nx.number_of_edges(H))/float((nx.number_of_nodes(H)*(nx.number_of_nodes(H)-1)))
    print "MAX DEGREE: ",dmax
    nr_satisf=0
    nr_women=0
    nr_men=0
    nr_salary=0
    nr_person=0
    for n in H.nodes():
        if H.node[n]['label']=='satisfaction':
            nr_satisf+=1
        if H.node[n]['label']=='woman':
            nr_women+=1    
        if H.node[n]['label']=='man':
            nr_men+=1  
        if H.node[n]['label']=='salary':
            nr_salary+=1      
        if H.node[n]['label']=='person':
            nr_person+=1 
    print "Nr persons: ",nr_person
    print "Nr women: ",nr_women
    print "Nr men: ",nr_men
    print "Nr salaries: ",nr_salary
    print "Nr satisfactions: ",nr_satisf  
    with open(os.path.join(path_to_folder,"nodes.info"),'w') as f:
        f.write("#nodes,"+"#edges,"+"#friends,"+"#max_degree,"+"avg_degree,"+"density,"+"\n")  
        f.write(str(nx.number_of_nodes(H))+","+str(nx.number_of_edges(H))+","+str(nr_friends)+","+str(dmax)+","+str(davg)+str(density)+"\n")
    nx.write_gml(H, os.path.join(path_to_folder,"pattern.gml"))
    
def main_random(output_path,V,c2,d):
    nr_persons=V
    name_of_folder="R_"+str(V)+"_"+str(c2)+"_"+str(d)
    path_to_folder=os.path.join(output_path,name_of_folder)
    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder)
    percentage_men=40
    percentage_women=60
    percentage_married=40
    men_number=(nr_persons*percentage_men/100)
    nr_married=(men_number*percentage_married/100)
    nr_nodes=int((nr_persons*percentage_men/100)+(nr_persons*percentage_women/100)+2*nr_persons+nr_persons+nr_married)
    print "Nr nodes: ",nr_nodes
    nr_friends=V*c2+V*V*d
    print "Nr friends: ",nr_friends
    print "Nr married: ",nr_married
    print "Percentage men: ",percentage_men/float(100)
    #H = powerlaw_friends_graph(nr_persons, percentage_men/float(100), nr_friends, nr_married, None)
    H = random_friends_graph(nr_persons, percentage_men/float(100), nr_friends, nr_married, None)
    print "NR NODES: ",nx.number_of_nodes(H)
    print "NR EDGES: ",nx.number_of_edges(H)
    degree_sequence=sorted(nx.degree(H).values(),reverse=True) # degree sequence
    #print "Degree sequence", degree_sequence
    dmax=max(degree_sequence)
    davg=np.mean(degree_sequence)
    density=(2*nx.number_of_edges(H))/float((nx.number_of_nodes(H)*(nx.number_of_nodes(H)-1)))
    print "MAX DEGREE: ",dmax
    nr_satisf=0
    nr_women=0
    nr_men=0
    nr_salary=0
    nr_person=0
    for n in H.nodes():
        if H.node[n]['label']=='satisfaction':
            nr_satisf+=1
        if H.node[n]['label']=='woman':
            nr_women+=1    
        if H.node[n]['label']=='man':
            nr_men+=1  
        if H.node[n]['label']=='salary':
            nr_salary+=1      
        if H.node[n]['label']=='person':
            nr_person+=1 
    print "Nr persons: ",nr_person
    print "Nr women: ",nr_women
    print "Nr men: ",nr_men
    print "Nr salaries: ",nr_salary
    print "Nr satisfactions: ",nr_satisf    
    with open(os.path.join(path_to_folder,"nodes.csv"),'w') as f:
        f.write("#nodes,"+"#edges,"+"#friends,"+"#max_degree,"+"avg_degree,"+"density,"+"\n")  
        f.write(str(nx.number_of_nodes(H))+","+str(nx.number_of_edges(H))+","+str(nr_friends)+","+str(dmax)+","+str(davg)+str(density)+"\n")
    nx.write_gml(H, os.path.join(path_to_folder,"pattern.gml"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate graphs')
    parser.add_argument('-o',help='output path')
    parser.add_argument('-V',help='nr persons')
    parser.add_argument('-c2', metavar='N',help='path to data file')
    parser.add_argument('-d', metavar='N',help='path to data file')
    parser.add_argument('-r', default=False,action='store_true',help='generate random graph. By default is False')
    args = parser.parse_args()
    if(args.r):
        main_random(args.o,int(args.V),int(args.c2),float(args.d))
    else:
        main_powerlaw(args.o,int(args.V),int(args.c2),float(args.d))
    
    
