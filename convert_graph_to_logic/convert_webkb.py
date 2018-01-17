'''
Created on Jun 2, 2017

@author: irma
'''
'''
Created on Nov 9, 2016

@author: irma
'''
import networkx as nx
data_file_name="/home/irma/workspace/DATA/WEBKB/webkb.gml"
output="/home/irma/workspace/DATA/WEBKB/webkb.db"
output_prolog="/home/irma/workspace/DATA/WEBKB/webkb.pl"

data_graph=nx.read_gml(data_file_name)

properties=[]



page_string=""
references=""


for n in data_graph.nodes():
    if not data_graph.node[n]['predicate'] in properties:
        properties.append(data_graph.node[n]['predicate'])
    
    if data_graph.node[n]['predicate']=='page':
      #print data_graph.node[n]
      page_string+="Page("+"Pg_"+data_graph.node[n]['id']+","+data_graph.node[n]['value'].title()+")\n"
      
    
      #get neighbours of the protein
      neighbours= data_graph.neighbors(n)
      for ne in neighbours:
        if data_graph.node[ne]['predicate']=='ref':
            for refs in data_graph.neighbors(ne):
                  if data_graph.node[refs]['predicate']=='dir':
                             for dirs in data_graph.neighbors(refs):
                                  if data_graph.node[dirs]['predicate']=='page':
                                      ref="References("+"Pg_"+data_graph.node[n]['id']+","+"Pg_"+data_graph.node[dirs]['id'].title()+")\n"
                                      if not ref in references:
                                          references+=ref
                                      
            #get neighbours of the protein
      neighbours= data_graph.neighbors(n)
      for ne in neighbours:
        if data_graph.node[ne]['predicate']=='dir':
            for refs in data_graph.neighbors(ne):
                  if data_graph.node[refs]['predicate']=='ref':
                             for dirs in data_graph.neighbors(refs):
                                  if data_graph.node[dirs]['predicate']=='page':
                                      ref="References("+"Pg_"+data_graph.node[dirs]['id']+","+"Pg_"+data_graph.node[n]['id'].title()+")\n"
                                      if not ref in references:
                                          references+=ref
    

with open(output,'w+') as f:
    f.write(page_string)
    f.write(references)

    
with open(output_prolog,'w+') as f:
    for s in page_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in references.split("\n"):
      f.write(s.lower()+".\n")