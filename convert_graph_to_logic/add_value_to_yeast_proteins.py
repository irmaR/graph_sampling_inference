'''
Created on Nov 9, 2016

@author: irma
'''
import networkx as nx

data_file_name = "/home/irma/work/DATA/DATA/yeast/YEAST.gpickle"


data_graph = nx.read_gpickle(data_file_name)


for n in data_graph.nodes():
     if data_graph.node[n]['predicate']=='interaction':
       print data_graph.node[n]
#    if data_graph.node[n]['predicate']=='constant':
#        data_graph.node[n]['value']=data_graph.node[n]['name']


#nx.write_gpickle(data_graph,data_file_name)
