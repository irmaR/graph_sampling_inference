'''
Created on Sep 22, 2016

@author: irma
'''

import networkx as nx

def convert_citations_data_gml_to_clause(gml,objects,relations):
    output=""
    id_cont=len(gml.nodes())+1
    for n in gml.nodes():
       neighbours=gml.neighbors(n)
       print "NODE: ",gml.node[n]
       print "nr eighbours: ",len(neighbours)
       if gml.node[n]["predicate"] in objects:
           print "Object node"
       elif gml.node[n]["predicate"] in relations:
           paper_constants=[]
           paper_constants1=[]
           dir_constants=[]
           for neighb in neighbours:
               if gml.node[neighb]["predicate"]=="constant":
                   paper_constants.append(neighb)
               else:
                   dir_constants.append(neighb)
               
               for d in dir_constants:
                   neighbours_d=gml.neighbors(d)
                   for n_d in neighbours_d:
                       if gml.node[n_d]["predicate"]=="constant":
                          paper_constants1.append(n_d)
           print paper_constants
           print paper_constants1
           if len(paper_constants1)==0:
              for p1 in paper_constants:
                 output+="ref("+gml.node[p1]["predicate"]+str(gml.node[p1]["id"])+",_"+")^"

           else:    
               for p1 in paper_constants:
                   for p2 in paper_constants1:
                       output+="ref("+gml.node[p1]["predicate"]+str(gml.node[p1]["id"])+","+gml.node[p2]["predicate"]+str(gml.node[p2]["id"])+")^"
                       
           
           

       else:
           for neighb in neighbours:
               print "NEIGHB:",gml.node[neighb]["predicate"]
           for neighb in neighbours:
               if gml.node[n]["valueinpattern"]==0:
                  if gml.node[n]["predicate"]=="dir":
                      if gml.node[neighb]["predicate"]=="constant":
                         output+=gml.node[n]["predicate"]+"("+gml.node[neighb]["predicate"]+str(gml.node[neighb]["id"])+")^"
                  else:
                      output+=gml.node[n]["predicate"]+"("+gml.node[neighb]["predicate"]+str(gml.node[neighb]["id"])+",_)^"
               else:
                  if gml.node[n]["predicate"]=="dir":
                      if gml.node[neighb]["predicate"]=="constant":
                          output+=gml.node[n]["predicate"]+"("+gml.node[neighb]["predicate"]+str(gml.node[neighb]["id"])+")^"
                  else: 
                      output+=gml.node[n]["predicate"]+"("+gml.node[neighb]["predicate"]+str(gml.node[neighb]["id"])+",_)^"

    
    print output
    


if __name__ == '__main__':
    path_pattern='/home/irma/workspace/Martin_experiments/DBLP_experiments/test_no_obd_decomp/PATTERNS/dblppattern_4d018fde05fd4af7a9035ac785641505/dblppattern_4d018fde05fd4af7a9035ac785641505.gml'
#     path_pattern='/home/irma/workspace/Martin_experiments/DBLP/dblp.gpickle'
#     pattern_gml=nx.read_gpickle(path_pattern)
#     for n in pattern_gml.nodes():
#         if pattern_gml.node[n]["predicate"]=="constant":
#             print "NEIGHB"
#             for ne in pattern_gml.neighbors(n):
#                 print pattern_gml.node[ne]
#             print pattern_gml.node[n]
    
    pattern_gml=nx.read_gml(path_pattern)
    specs={}
    convert_citations_data_gml_to_clause(pattern_gml,["constant"],["references"])
#     