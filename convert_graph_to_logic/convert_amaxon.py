'''
Created on Jun 2, 2017

@author: irma
'''
'''
Created on Nov 9, 2016

@author: irma
'''
import networkx as nx
data_file_name="/home/irma/workspace/DATA/AMAZON/amazon.gpickle"
output="/home/irma/workspace/DATA/AMAZON/amazon.db"
output_prolog="/home/irma/workspace/DATA/AMAZON/amazon.pl"

data_graph=nx.read_gpickle(data_file_name)

properties=[]



friends_string=""


for n in data_graph.nodes():
      #get neighbours of the protein
      neighbours= data_graph.neighbors(n)
      for friends in neighbours:
         friends_string+=str("Connected(U_"+str(data_graph.node[n]['id'])+","+"U_"+str(data_graph.node[friends]['id'])+")\n")

with open(output,'w+') as f:
    f.write(friends_string)

    
with open(output_prolog,'w+') as f:
    for s in friends_string.split("\n"):
      f.write(s.lower()+".\n")
