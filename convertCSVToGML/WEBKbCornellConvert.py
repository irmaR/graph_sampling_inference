'''
Created on Sep 6, 2016

@author: irma
'''
import pandas as pd
import sys, time
import networkx as nx
import graph_manipulator.visualization as vis
import graph_manipulator.graph_analyzer as an

def f(x):
     return pd.Series(dict(A = x['page'], 
                        C = [].append(x['cite'])))

#Utility functions
def progress(v):
    v = str(v)
    sys.stdout.flush()
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(v)

FILE_NAME = "/home/irma/workspace/some_scripts_martin_sampling/DATA/webkb/output.gml"

int_id_counter=0
int_label_counter=0

dictionary_labels={}
dictionary_types={}
dictionary_edges={}

pages = pd.read_csv('/home/irma/workspace/some_scripts_martin_sampling/DATA/webkb/WebKB.csv', sep=',')
links= pd.read_csv('/home/irma/workspace/some_scripts_martin_sampling/DATA/webkb/WebKB_cocite.rn', sep=',')
cites= pd.read_csv('/home/irma/workspace/some_scripts_martin_sampling/DATA/webkb/WebKB.rn', sep=',')

for index, row in pages.iterrows():
   dictionary_labels[row['page']]=row['id']
   dictionary_types[row['page']]=row['type']

links_lists= links.groupby('page')['cocite'].apply(list)
cites_list= cites.groupby('page')['cite'].apply(list)

f = open(FILE_NAME, "w")
#helpers
s = " "
ss = s+s
sss = s+s+s
ssss = s+s+s+s
nl = "\n"

#loop helpers
added = []
ind = 0

#Root node
f.write("graph"+nl)
f.write("["+nl)

#Write an edge
def write_edge(r,source,target):
    f.write( ss + "edge" + nl)
    f.write( ss + "[" + nl)
    f.write( ssss + "source" + s + '"' + str(source) + '"' + nl)
    f.write( ssss + "target" + s + '"' + str(target) + '"' + nl)
    f.write( ss + "]"+ nl)

#Write a node
def write_node(r,i):
    f.write( ss + "node" + nl)
    f.write( ss + "[" + nl)
    f.write( ssss + "value" + s + '"' + str(r['type']) + '"' + nl)
    f.write( ssss + "predicate" + s + '"' + 'page' + '"' + nl)
    f.write( ssss + "label" + s + '"' + str(r['page']) + '"' + nl)
    f.write( ssss + "id" + s + '"' + str(r['id']) + '"' + nl)
    f.write( ss + "]"+ nl)
    

#Generate nodes
for i, r in pages.iterrows():
    #increment, as index not reliable
    ind += 1
    #Check for duplicates
    if (r['page'] not in added):
        #Add to list
        added.append(r['page'])
        write_node(r,int_label_counter)
        int_label_counter+=1
    #print the progress    
    #progress(ind)

print(nl+"Printing nodes over")

#flush index
ind = 0    
#Generate edges    
already_connected=[]

direct_combos=[]
inverse_combos=[]


for i, r in links_lists.iteritems():
    ind += 1
    source=dictionary_labels[i]
    targets=r
    target_ids=[]
    for t in targets:
        if str(source)+"_"+str(dictionary_labels[t]) in inverse_combos:
            continue
        else:
            direct_combos.append(str(source)+"_"+str(dictionary_labels[t]))
            inverse_combos.append(str(dictionary_labels[t])+"_"+str(source))


        

# double=0
# for i in inverse_combos:   
#     if i in direct_combos:
#         double+=1
#         print double
# print double  

for i, r in links_lists.iteritems():
    #increment, as index not reliable
    ind += 1
    source=dictionary_labels[i]
 
    targets=r
    target_ids=[]
    for t in targets:
        if str(source)+"_"+str(dictionary_labels[t]) in direct_combos:
           target_ids.append(dictionary_labels[t])
    for t in target_ids:
       write_edge(r,source,t)
    #print the progress            
    #progress(ind)
     
 
 
print(nl+"Printing nodes and edges over")
 
#closing node
f.write("]"+nl)
f.close()
 
graph=nx.read_gml(FILE_NAME)
print "Nr nodeS: ",len(graph.nodes())
print "Nr edges: ",len(graph.edges())
#print an.get_maximum_node_degree(graph)
#vis.visualize_graph_standard(graph)


#data=nx.read_gpickle('/home/irma/workspace/Martin_experiments/DBLP/dblp.gpickle')
#for n in data.nodes():
#    if 'value' in data.node[n]:
#       print data.node[n]
#       break
