'''
Created on Nov 9, 2016

@author: irma
'''
import networkx as nx
data_file_name="/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/DATA/Yeast/YEAST.gpickle"
output="/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/DATA/Logic/Yeast/yeast.db"
output_prolog="/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/DATA/Logic/Yeast/yeast.pl"

data_graph=nx.read_gpickle(data_file_name)

properties=[]

function_string=""
location_string=""
protein_string=""
interactions=[]
interactions_string=""
enzyme_string=""
protein_class_string=""
phenotype_string=""




for n in data_graph.nodes():
    if not data_graph.node[n]['predicate'] in properties:
        properties.append(data_graph.node[n]['predicate'])
    
    if data_graph.node[n]['predicate']=='constant':
      protein_string+="Protein("+data_graph.node[n]['name']+")\n"
      #get neighbours of the protein
      neighbours= data_graph.neighbors(n)
      for ne in neighbours:
          if data_graph.node[ne]['predicate']=='function':
              function_string+="Function("+data_graph.node[n]['name']+","+data_graph.node[ne]['name']+")\n"
          if data_graph.node[ne]['predicate']=='location':
              location_string+="Location("+data_graph.node[n]['name']+","+data_graph.node[ne]['name']+")\n"
          if data_graph.node[ne]['predicate']=='enzyme':
              enzyme_string+="Enzyme("+data_graph.node[n]['name']+","+data_graph.node[ne]['name']+")\n"
          if data_graph.node[ne]['predicate']=='protein_class':
              protein_class_string+="ProteinClass("+data_graph.node[n]['name']+","+data_graph.node[ne]['name']+")\n"
          if data_graph.node[ne]['predicate']=='phenotype':
              phenotype_string+="Phenotype("+data_graph.node[n]['name']+","+data_graph.node[ne]['name']+")\n"
          if data_graph.node[ne]['predicate']=='interaction':
              neighbouring_protein1= data_graph.neighbors(ne)[0]
              neighbouring_protein2= data_graph.neighbors(ne)[1]
              string_inter="Interaction("+data_graph.node[neighbouring_protein1]['name']+","+data_graph.node[neighbouring_protein2]['name']+")"
              string_inter_reverse="Interaction("+data_graph.node[neighbouring_protein2]['name']+","+data_graph.node[neighbouring_protein1]['name']+")"
              if not string_inter in interactions:
                  interactions.append(string_inter)
              if not string_inter_reverse in interactions:
                  interactions.append(string_inter_reverse)

for inter in interactions:
    interactions_string+=inter+"\n"

with open(output,'w+') as f:
    f.write(protein_string)
    f.write(function_string)
    f.write(location_string)
    f.write(enzyme_string)
    f.write(protein_class_string)
    f.write(phenotype_string)
    f.write(interactions_string)
    
with open(output_prolog,'w+') as f:
    for s in protein_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in function_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in location_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in enzyme_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in protein_class_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in phenotype_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in interactions_string.split("\n"):
      f.write(s.lower()+".\n")
                 

