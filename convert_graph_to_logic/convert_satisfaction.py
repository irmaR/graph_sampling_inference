'''
Created on Nov 9, 2016

@author: irma
'''
import networkx as nx
data_names=["R1","R2","R3","R4","R5","R6","S1","S2","S3","S4","S5","S6"]

for d in data_names:
    data_file_name="/home/irma/workspace/DATA/University/"+d+".gml"
    output="/home/irma/workspace/DATA/University/"+d+".db"
    output_prolog="/home/irma/workspace/DATA/University/"+d+".pl"
    
    data_graph=nx.read_gml(data_file_name)
    
    properties=[]
    
    man_string=""
    woman_string=""
    married_string=""
    salary_string=""
    satisfaction_string=""
    friends_string=""
    
    friends=[]
    married=[]
    
    for n in data_graph.nodes():
        if data_graph.node[n]['predicate']=='person':
          neighbours= data_graph.neighbors(n)
          for ne in neighbours:
              if data_graph.node[ne]['predicate']=='salary':
                  salary_string+="Salary(P"+str(data_graph.node[n]['id'])+","+data_graph.node[ne]['value'].rstrip().lstrip().title()+")\n"
              if data_graph.node[ne]['predicate']=='satisfaction':
                  satisfaction_string+="Satisfaction(P"+str(data_graph.node[n]['id'])+","+data_graph.node[ne]['value'].rstrip().lstrip().title()+")\n"
              if data_graph.node[ne]['predicate']=='woman':
                  woman_string+="Woman(P"+str(data_graph.node[n]['id'])+")\n"
              if data_graph.node[ne]['predicate']=='man':
                  man_string+="Man(P"+str(data_graph.node[n]['id'])+")\n"
              
              if data_graph.node[ne]['predicate']=='friends':
                  for ne1 in data_graph.neighbors(ne):
                    string_inter="Friends(P"+str(data_graph.node[n]['id'])+",P"+str(data_graph.node[ne1]['id'])+")"
                    string_inter_reverse="Friends(P"+str(data_graph.node[ne1]['id'])+",P"+str(data_graph.node[ne]['id'])+")"
                  if not string_inter in friends:
                      friends.append(string_inter)
                  if not string_inter_reverse in friends:
                      friends.append(string_inter_reverse)
                      
              if data_graph.node[ne]['predicate']=='married':
                  for ne1 in data_graph.neighbors(ne):
                    string_inter="Married(P"+str(data_graph.node[n]['id'])+",P"+str(data_graph.node[ne1]['id'])+")"
                    string_inter_reverse="Married(P"+str(data_graph.node[ne1]['id'])+",P"+str(data_graph.node[ne]['id'])+")"
                  if not string_inter in married:
                      married.append(string_inter)
                  if not string_inter_reverse in married:
                      married.append(string_inter_reverse)
    
        
    
    for inter in friends:
        friends_string+=inter+"\n"
        
    for inter in married:
        married_string+=inter+"\n"
    
    with open(output,'w+') as f:
        f.write(man_string)
        f.write(woman_string)
        f.write(married_string)
        f.write(salary_string)
        f.write(satisfaction_string)
        f.write(friends_string)
    
    with open(output_prolog,'w+') as f:
        for s in man_string.split("\n"):
          f.write(s.lower()+".\n")
        for s in woman_string.split("\n"):
          f.write(s.lower()+".\n")
        for s in married_string.split("\n"):
          f.write(s.lower()+".\n")
        for s in salary_string.split("\n"):
          f.write(s.lower()+".\n")
        for s in satisfaction_string.split("\n"):
          f.write(s.lower()+".\n")
        for s in friends_string.split("\n"):
          f.write(s.lower()+".\n")
    
                     
    
