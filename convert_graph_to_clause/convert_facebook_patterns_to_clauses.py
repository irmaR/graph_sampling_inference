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
import tempfile

def string_to_pattern(gml_string):
    pattern=None
    with tempfile.NamedTemporaryFile() as f:
       f.write(gml_string)
       f.flush()
       pattern=nx.read_gml(f.name)
    return pattern

def convert(nodes,edges,output):
    clause=""
    literals={}
    literal_ids={}
    edges_dict={}
    constants={}
    value_list=""
    
    for n in nodes:
        print "Node",n
        lit_split=n.split(":")
        literal_ids[str(lit_split[0]).rstrip().lstrip()]=str(lit_split[1].rstrip().lstrip())
    
    print "Literal ids: ",literal_ids
    
    for e in edges:
        if e[0] not in edges_dict:
           edges_dict[e[0]]=[e[1]]
        else:
           edges_dict[e[0]].append(e[1])
        
        if e[1] not in edges_dict:
           edges_dict[e[1]]=[e[0]]
        else:
           edges_dict[e[1]].append(e[0])
    
    print "edges disct: ",edges_dict
    #first get all the constants
    for n in literal_ids:
        if "user" in literal_ids[n]:
            if not "=" in literal_ids[n]:
                literals[n]="User(us"+n+")"
                constants[n]="us"+n
            else:
                split_prot=literal_ids[n].split("=")
                literals[n]="User("+split_prot+")"
                constants[n]=split_prot
                value_list+=split_prot[1].title().lstrip().rstrip()+","
    
    for n in literal_ids:
        if "gender" in literal_ids[n]:
            for e in edges_dict[n]:
                if not "=" in literal_ids[n]:
                    literals[n]="Gender("+constants[e]+",gen"+str(n)+")"
                else:
                    split_prot=literal_ids[n].split("=")
                    literals[n]="Gender("+constants[e]+","+split_prot[1].rstrip().lstrip().title().lstrip().rstrip()+")"
                    value_list+=split_prot[1].rstrip().lstrip().title()+","
    print edges_dict
    print literal_ids
    print literals
    for n in literal_ids:
        print literal_ids[n]
        if "education_type" in literal_ids[n]:
            for e in edges_dict[n]:
                if not "=" in literal_ids[n]:
                    literals[n]="Education_type("+constants[e]+",et"+str(n)+")"
                    print "here: ",literals[n]
                else:
                    split_prot=literal_ids[n].split("=")
                    literals[n]="Education_type("+constants[e]+","+split_prot[1].title().lstrip().rstrip()+")"
                    value_list+=split_prot[1].title().lstrip().rstrip()+","
    
    for n in literal_ids:
        if "birthday" in literal_ids[n]:
            for e in edges_dict[n]:
                if not "=" in literal_ids[n]:
                    literals[n]="Birthday("+constants[e]+",bi"+str(n)+")"
                else:
                    split_prot=literal_ids[n].split("=")
                    print split_prot
                    literals[n]="Birthday("+constants[e]+","+split_prot[1].title().lstrip().rstrip()+")"
                    value_list+=split_prot[1].title().lstrip().rstrip()+","
    
    for n in literal_ids:
        if "hometown" in literal_ids[n]:
            for e in edges_dict[n]:
                if not "=" in literal_ids[n]:
                    literals[n]="Hometown("+constants[e]+",ht"+str(n)+")"
                else:
                    split_prot=literal_ids[n].split("=")
                    literals[n]="Hometown("+constants[e]+","+split_prot[1].title().lstrip().rstrip()+")"
                    value_list+=split_prot[1].title().lstrip().rstrip()+","
    for n in literal_ids:
        if "education_degree" in literal_ids[n]:
            for e in edges_dict[n]:
                if not "=" in literal_ids[n]:
                    literals[n]="Education_degree("+constants[e]+",ed"+str(n)+")"
                else:
                    split_prot=literal_ids[n].split("=")
                    literals[n]="Education_degree("+constants[e]+","+split_prot[1].title().lstrip().rstrip()+")"
                    value_list+=split_prot[1].title().lstrip().rstrip()+","
    
    for n in literal_ids:
        if "language" in literal_ids[n]:
            for e in edges_dict[n]:
                if not "=" in literal_ids[n]:
                    literals[n]="Language("+constants[e]+",l"+str(n)+")"
                else:
                    split_prot=literal_ids[n].split("=")
                    literals[n]="Language("+constants[e]+","+split_prot[1].title()+")"
                    value_list+=split_prot[1].title().lstrip().rstrip()+","                
    
    print "Constants: ",constants
    print edges_dict
    edges={}
    counter=0
    for n in literal_ids:            
                if n in constants:
                  for edge in edges_dict[n]:
                     if edge in constants:
                       edges[counter]=str("Friends("+constants[n]+","+constants[edge]+")")
                       counter+=1
                       edges[counter]=str("Friends("+constants[edge]+","+constants[n]+")")
                       counter+=1

    clause=""    
    print literals
    for n in literals:
        clause+=literals[n]+"^"
    edges_unique=set(edges.values())
    print edges_unique
    for n in edges_unique:
        clause+=n+"^"
    clause = clause[:-1]
    with open(os.path.join(output,'clause.info'),'w') as f:
        f.write(clause+"\n")
        f.write(value_list.lstrip().rstrip()[:-1])
    print clause
    return [clause,value_list]
    



if __name__ == '__main__':
     #convert(['0:education_type', '1:user', '2:hometown', '3:user', '4:education_degree = value_2'],[['0', '1'], ['1', '2'], ['1', '3'], ['3', '4']],"")
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
                 #line=line.replace("RESULTS_FACEBOOK","PATTERNS_FACEBOOK")
                 print "pattern path: ",line
                 for file in os.listdir(line.rstrip()):
                    if file.endswith(".gml"):
                       print os.path.join(line.rstrip(),file)       
                       pattern=nx.read_gml(os.path.join(line.rstrip(),file))
                       readable_format=an.get_readable_text_format(pattern)
                       print "readable format: ",readable_format
                       print "rf: ",readable_format[0]
                       print "rf: ",readable_format[1]
                       print "HaLo?"
                       convert(readable_format[0],readable_format[1],line.rstrip())
                       clause=os.path.join(line.rstrip(),'clause.info')
                       res=os.path.join(line.replace("PATTERNS","RESULTS").rstrip(),'sdm')
                       results_clause_dict[res]=clause
                          
                          
     if args.r!=None:
         pattern=nx.read_gml(os.path.join(args.r.rstrip()))
         readable_format=an.get_readable_text_format(pattern)
         print "readable format: ",readable_format
         print "rf: ",readable_format[0]
         print "rf: ",readable_format[1]
         print "HaLo?"
         convert(readable_format[0],readable_format[1],"/".join(args.r.split("/")[:-1]))
     try:
       os.makedirs(os.path.join(args.c,'sdm'))
     except:
         print ""
     print results_clause_dict
    #make commands for running on supercomputer
     with open(os.path.join(args.c,'sdm/','param.data'),'w') as f:
       f.write("result,clause\n")
       for res in results_clause_dict.keys():
           print res
           f.write(res+","+results_clause_dict[res]+"\n")