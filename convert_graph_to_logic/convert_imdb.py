'''
Created on Jun 2, 2017

@author: irma
'''
'''
Created on Nov 9, 2016

@author: irma
'''
import networkx as nx
data_file_name="/home/irma/workspace/DATA/IMDB/imdb.gml"
output="/home/irma/workspace/DATA/IMDB/imdb.db"
output_prolog="/home/irma/workspace/DATA/IMDB/imdb.pl"

data_graph=nx.read_gml(data_file_name)

properties=[]



movie_string=""
director_string=""
actor_string=""

genre_string=""
gender_string=""
worksWith_string=""
actsIn_string=""
directs_string=""







for n in data_graph.nodes():
    if not data_graph.node[n]['predicate'] in properties:
        properties.append(data_graph.node[n]['predicate'])
    
    if data_graph.node[n]['predicate']=='movie':
      movie_string+="Movie("+data_graph.node[n]['value']+")\n"
      
    if data_graph.node[n]['predicate']=='actor':
      actor_string+="Actor("+data_graph.node[n]['value']+")\n"
      
    if data_graph.node[n]['predicate']=='director':
      print data_graph.node[n]
      director_string+="Director("+data_graph.node[n]['value']+")\n"  
      
      #get neighbours of the protein
      neighbours= data_graph.neighbors(n)
      for ne in neighbours:
          if data_graph.node[ne]['predicate']=='gender':
              print data_graph.node[ne]
              gender_string+="Gender("+data_graph.node[n]['value']+","+data_graph.node[ne]['value']+")\n"
          if data_graph.node[ne]['predicate']=='genre':
              genre_string+="Genre("+data_graph.node[n]['value']+","+data_graph.node[ne]['value']+")\n"
          if data_graph.node[n]['predicate']=='actor' and data_graph.node[ne]['predicate']=='movie':
              actsIn_string+="ActsIn("+data_graph.node[n]['value']+","+data_graph.node[ne]['value']+")\n"
          if data_graph.node[n]['predicate']=='actor' and data_graph.node[ne]['predicate']=='director':
              worksWith_string+="WorksWith("+data_graph.node[n]['value']+","+data_graph.node[ne]['value']+")\n"
          if data_graph.node[n]['predicate']=='director' and data_graph.node[ne]['predicate']=='actor':
              worksWith_string+="WorksWith("+data_graph.node[ne]['value']+","+data_graph.node[n]['value']+")\n"
          if data_graph.node[n]['predicate']=='director' and data_graph.node[ne]['predicate']=='movie':
              directs_string+="Directs("+data_graph.node[n]['value']+","+data_graph.node[ne]['value']+")\n"


with open(output,'w+') as f:
    f.write(movie_string)
    f.write(director_string)
    f.write(actor_string)
    f.write(gender_string)
    f.write(genre_string)
    f.write(actsIn_string)
    f.write(worksWith_string)
    f.write(directs_string)

    
with open(output_prolog,'w+') as f:
    for s in movie_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in director_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in actor_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in gender_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in genre_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in actsIn_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in worksWith_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in directs_string.split("\n"):
      f.write(s.lower()+".\n")