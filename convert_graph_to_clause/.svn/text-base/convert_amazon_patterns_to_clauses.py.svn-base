'''
Created on Dec 5, 2016

@author: irma
'''
'''
Created on Nov 9, 2016

@author: irma
'''

import argparse,os
import networkx as nx
import graph_manipulator.graph_analyzer as an

def convert(nodes,edges,output):
    clause=""
    literals={}
    literal_ids={}
    edges_dict={}
    constants={}
    value_list=""
    
    for n in nodes:
        lit_split=n.split(":")
        literal_ids[str(lit_split[0]).rstrip().lstrip()]=str(lit_split[1].rstrip().lstrip())
    for e in edges:
        if e[0] not in edges_dict:
           edges_dict[e[0]]=[e[1]]
        else:
           edges_dict[e[0]].append(e[1])
        
        #if e[1] not in edges_dict:
        #   edges_dict[e[1]]=[e[0]]
        #else:
        #   edges_dict[e[1]].append(e[0])
    
    counter=1
    print literal_ids
    print edges_dict
    for n in literal_ids:
        if n in edges_dict:
           for friends in edges_dict[n]:
                literals[counter]=str("Connected(u_"+str(n)+","+"u_"+friends+")")
                counter+=1
            
    clause=""    
    for n in literals:
        clause+=literals[n]+"^"
    clause = clause[:-1]
    with open(os.path.join(output,'clause.info'),'w') as f:
        f.write(clause+"\n")
        f.write(value_list.lstrip().rstrip()[:-1])
    print clause,value_list
    return [clause,value_list]
    
    
    
if __name__ == '__main__':
     parser = argparse.ArgumentParser(description='turn yeast patterns into ')
     parser.add_argument('-p',help='selected patterns file')
     parser.add_argument('-c',help='path to commands')
     parser.add_argument('-r',help='one specific patterns')
    
     args = parser.parse_args()
     path_to_selected_patterns=args.p
      
     results_clause_dict={}
           
     if args.p!=None: 
         with open(path_to_selected_patterns,'r') as f:
             for line in f.readlines():
                 line=line.replace("RESULTS","PATTERNS")
                 for file in os.listdir(line.rstrip()):
                    if file.endswith(".gml"): 
                       print "HERE",os.path.join(line.rstrip(),file)                      
                       pattern=nx.read_gml(os.path.join(line.rstrip(),file))
                       print os.path.join(line.rstrip(),file)
                       readable_format=an.get_readable_text_format(pattern)
                       convert(readable_format[0],readable_format[1],line.rstrip())
                       clause=os.path.join(line.rstrip(),'clause.info')
                       res=os.path.join(line.replace("PATTERNS","RESULTS").rstrip(),'sdm')
                       results_clause_dict[res]=clause
                        
                        
     if args.r!=None:
         pattern=nx.read_gml(os.path.join(args.r.rstrip()))
         readable_format=an.get_readable_text_format(pattern)
         convert(readable_format[0],readable_format[1],"/".join(args.r.split("/")[:-1]))
     try:
       os.makedirs(os.path.join(args.c,'sdm'))
     except:
         print ""
    #make commands for running on supercomputer
     with open(os.path.join(args.c,'sdm/','param.data'),'w') as f:
       f.write("result,clause\n")
       for res in results_clause_dict.keys():
           f.write(res+","+results_clause_dict[res]+"\n")
     
    
        
         
    
 
    
    #convert([u'0:user', '1:user', '2:user', '3:user'], [['0', '2'], ['0', '3'], ['1', '3']],"")
    
