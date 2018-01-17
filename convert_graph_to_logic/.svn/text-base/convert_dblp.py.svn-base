
import networkx as nx
data_file_name="/home/irma/workspace/DATA/Dblp/DBLP_2001-2_discretized.gpickle"
output="/home/irma/workspace/DATA/Dblp/dblp.db"
output_prolog="/home/irma/workspace/DATA/Dblp/dblp.pl"

data_graph=nx.read_gpickle(data_file_name)

properties=[]

citations_string=""
references_string=""
direction_string=""
references=[]
dirs=[]
paper_string=""

for n in data_graph.nodes():
    if not data_graph.node[n]['predicate'] in properties:
        properties.append(data_graph.node[n]['predicate'])
    
    if data_graph.node[n]['predicate']=='constant':
      const=data_graph.node[n]['predicate'][:3]+str(data_graph.node[n]['id'])
      #paper_string+="Paper("+const.title()+")\n"
      
      #get neighbours of the protein
      neighbours= data_graph.neighbors(n)
      for ne in neighbours:
          if data_graph.node[ne]['predicate']=='citations':
              print data_graph.node[ne]
              citations_string+="Citations("+const.title()+","+data_graph.node[ne]['value'].title()+")\n"

          if data_graph.node[ne]['predicate']=='references':
              neighbouring_protein1= data_graph.neighbors(ne)[0]
              neighbouring_protein2= data_graph.neighbors(ne)[1]
              neighb1=data_graph.node[neighbouring_protein1]['predicate'][:3]+str(data_graph.node[neighbouring_protein1]['id'])
              neighb2=data_graph.node[neighbouring_protein2]['predicate'][:3]+str(data_graph.node[neighbouring_protein2]['id'])
              string_inter="Ref("+neighb1.title()+","+neighb2.title()+")"
              string_inter_reverse="Ref("+neighb2.title()+","+neighb1.title()+")"
              if not string_inter in references:
                  references.append(string_inter)
              if not string_inter_reverse in references:
                  references.append(string_inter_reverse)
          
          if data_graph.node[ne]['predicate']=='dir':
              neighbouring_protein1= data_graph.neighbors(ne)[0]
              neighbouring_protein2= data_graph.neighbors(ne)[1]
              neighb1=data_graph.node[neighbouring_protein1]['predicate'][:3]+str(data_graph.node[neighbouring_protein1]['id'])
              neighb2=data_graph.node[neighbouring_protein2]['predicate'][:3]+str(data_graph.node[neighbouring_protein2]['id'])
              print data_graph.node[neighbouring_protein1]['predicate'],data_graph.node[neighbouring_protein2]['predicate']
              string_inter="Dir("+neighb1.title()+","+neighb2.title()+")"
              string_inter_reverse="Dir("+neighb2.title()+","+neighb1.title()+")"
              if not string_inter in dirs:
                  dirs.append(string_inter)
              if not string_inter_reverse in dirs:
                  dirs.append(string_inter_reverse)

for inter in references:
    references_string+=inter+"\n"
    
for inter in dirs:
    direction_string+=inter+"\n"

with open(output,'w+') as f:
    f.write(paper_string)
    f.write(references_string)
    f.write(direction_string)
    f.write(citations_string)

    
with open(output_prolog,'w+') as f:
    for s in paper_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in citations_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in references_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in direction_string.split("\n"):
      f.write(s.lower()+".\n")
   

