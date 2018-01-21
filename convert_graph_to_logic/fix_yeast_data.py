'''
Created on Nov 9, 2016

@author: irma
'''
import networkx as nx
input_data = "//home/irma/work/DATA/DATA/yeast/Folds/fold1/train.gpickle"
data_file_name = "/home/irma/work/DATA/DATA/yeast/Folds/fold1/train.gpickle"
data_graph = nx.read_gpickle(input_data)

for n1 in data_graph.nodes():
    for n2 in data_graph.nodes():
      if data_graph.node[n1]['predicate'] == data_graph.node[n2]['predicate']:
          if data_graph.node[n1]['predicate']=='interaction':
            continue
          try:
              if data_graph.node[n1]['value'] == data_graph.node[n2]['value']:
                 data_graph.add_edge(n1,n2)
          except KeyError:
              continue

nx.write_gpickle(data_graph,data_file_name)



