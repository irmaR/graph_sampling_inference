'''
Created on Oct 26, 2016

@author: irma
'''
import graph_manipulator.visualization as vis
import networkx as nx
import os,pickle
import graph_manipulator.graph_analyzer as an

FILE_NAME = "/home/irma/workspace/some_scripts_martin_sampling/DATA/twitter/twitter.gpickle"
users_and_edges="/home/irma/workspace/some_scripts_martin_sampling/DATA/twitter/twitter_combined.txt"

users_list=[]
edges_map={}
nr_edges=0
nr_lines=0
nodes={}


id_user=0
with open(users_and_edges,'r') as f:
    for line in f.readlines():
        nr_lines+=1
        print "Line: ",nr_lines
        users=line.rstrip().lstrip().split(" ") 
        
        if not users[0] in nodes:
            nodes[users[0]]=id_user
            id_user+=1
        
        if not users[1] in nodes:
            nodes[users[1]]=id_user
            id_user+=1
        
        if users[0] in edges_map:
            edges_map[users[0]].append(users[1])
        else:
            edges_map[users[0]]=[users[1]]
        
        nr_edges+=1

print nr_edges
print len(edges_map.keys())

G=nx.Graph() 
for n in nodes.keys():
    G.add_node(nodes[n],id=nodes[n],predicate='user')
     
for e in edges_map.keys():
    for e1 in edges_map[e]:
      G.add_edge(nodes[e],nodes[e1])
 
pickle.dump(G, open(FILE_NAME,'wb'))

data=nx.read_gpickle(FILE_NAME)
print "Nr nodes TWITTER: ",len(data.nodes())
print "Nr edges TWITTER: ",len(data.edges())
print "Max degree TWITTER: ",an.get_maximum_node_degree(data)
print "Density TWITTER: ",nx.density(data)
print "INFO TWITTER:",nx.info(data)


vis.visualize_graph_standard(data)