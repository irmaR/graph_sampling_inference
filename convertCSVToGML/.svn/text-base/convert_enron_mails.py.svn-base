'''
Created on Nov 10, 2016

@author: irma
'''
import graph_manipulator.visualization as vis
import networkx as nx
import graph_manipulator.graph_analyzer as an
import pickle

FILE_NAME = "/home/irma/workspace/some_scripts_martin_sampling/DATA/e_mail_enron/e_mail_enron.gpickle"
edges="/home/irma/workspace/some_scripts_martin_sampling/DATA/e_mail_enron/Email-Enron.txt"

edges_map={}
nodes={}
nr_edges=0
line_nr=0
 
node_id=0
with open(edges,'r') as f:
    for line in f.readlines():
        line_nr+=1
        print "Line: ",line_nr
        #if line_nr==2000:
        #    break
        edge1=int(line.split("\t")[0].rstrip())
        edge2=int(line.split("\t")[1].rstrip())
        if edge1 not in nodes:
            nodes[edge1]=node_id
            node_id+=1
        if edge2 not in nodes:
            nodes[edge2]=node_id
            node_id+=1
        if edge1 in edges_map.keys():
            edges_map[edge1].append(edge2)
            nr_edges+=1
        else:
            edges_map[edge1]=[edge2]
            nr_edges+=1
 
 
f = open(FILE_NAME, "w")
s1 = " "
ss = s1+s1
sss = s1+s1+s1
ssss = s1+s1+s1+s1
nl = "\n"
 
f.write("graph"+nl)
f.write("["+nl)
 
 
#Write an edge
def write_edge(source,target):
    f.write( ss + "edge" + nl)
    f.write( ss + "[" + nl)
    f.write( ssss + "source" + s1 + '"' + str(source) + '"' + nl)
    f.write( ssss + "target" + s1 + '"' + str(target) + '"' + nl)
    f.write( ss + "]"+ nl)
     
def edge_string(source,target):
    string=""
    string+= ss + "edge" + nl
    string+= ss + "[" + nl
    string+= ssss + "source" + s1 + '"' + str(source) + '"' + nl
    string+= ssss + "target" + s1 + '"' + str(target) + '"' + nl
    string+= ss + "]"+ nl
    return string
 
#Write a node
def write_node(predicate, id):
    f.write( ss + "node" + nl)
    f.write( ss + "[" + nl)
    #f.write( ssss + "value" + s1 + '"' + str(value) + '"' + nl)
    f.write( ssss + "predicate" + s1 + '"' + predicate + '"' + nl)
    #if value!=predicate:
    #   f.write( ssss + "label" + s1 + '"' + predicate + '='+str(value)+'"' + nl)
    #else:
    f.write( ssss + "label" + s1 + '"' + predicate +'"' + nl) 
    f.write( ssss + "id" + s1 + '"' + str(id) + '"' + nl)
    f.write( ss + "]"+ nl)
 
G=nx.Graph() 
for n in nodes.keys():
    G.add_node(nodes[n],id=nodes[n],predicate='user')
     
for e in edges_map.keys():
    for e1 in edges_map[e]:
      G.add_edge(nodes[e],nodes[e1])
 
# f.write("]"+nl)
# f.close()
pickle.dump(G, open(FILE_NAME,'wb'))

data=nx.read_gpickle(FILE_NAME)
print "Nr nodes ENRON: ",len(data.nodes())
print "Nr edges ENRON: ",len(data.edges())
print "Max degree ENRON: ",an.get_maximum_node_degree(data)
print "Density ENRON: ",nx.density(data)
print "INFO ENRON:",nx.info(data)
#print an.get_maximum_node_degree(graph)

number_of_pages=0
for node in data.nodes():
        if data.node[node]['predicate']=='page':
            number_of_pages+=1
print "NUMBER OF PAGES: ",number_of_pages

vis.visualize_graph_standard(data)
      
