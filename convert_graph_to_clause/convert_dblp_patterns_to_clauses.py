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
        if "constant" in literal_ids[n]:
            if not "=" in literal_ids[n]:
                #literals[n]="Paper(pap"+n+")"
                constants[n]="pap"+n
            else:
                split_prot=literal_ids[n].split("=")
                #literals[n]="Paper("+split_prot+")"
                constants[n]=split_prot
                value_list+=split_prot[1]+","
    
    for n in literal_ids:
        if "citations" in literal_ids[n]:
            for e in edges_dict[n]:
                if not "=" in literal_ids[n]:
                    literals[n]="Citations("+constants[e]+",cit"+str(n)+")"
                else:
                    split_prot=literal_ids[n].split("=")
                    literals[n]="Citations("+constants[e]+","+split_prot[1].rstrip().lstrip()+")"
                    value_list+=split_prot[1].rstrip().lstrip()+","
    for n in literal_ids:
        if "references" in literal_ids[n]:
            for e in edges_dict[n]:
                if not "=" in literal_ids[n]:
                    literals[n]="Ref("+",ref"+str(n)+")"
                    constants[n]="ref"+n
    for n in literal_ids:
        if "dir" in literal_ids[n]:
            for e in edges_dict[n]:
                if not "=" in literal_ids[n]:
                    literals[n]="Dir("+",dir"+str(n)+")"
                    constants[n]="dir"+n
    print edges_dict
    print literal_ids
    print literals
    print "Constants: ",constants
    for n in literal_ids:
        print n,literal_ids[n],edges_dict[n]
        if "dir" in literal_ids[n]:
            if len(edges_dict[n])==2:
                literals[n]=str("Dir("+constants[edges_dict[n][0]]+","+constants[edges_dict[n][1]]+")"+"^Dir("+constants[edges_dict[n][1]]+","+constants[edges_dict[n][0]]+")")
            
            if len(edges_dict[n])==1:
                print "Halo",edges_dict[n][0],constants[edges_dict[n][0]]
                literals[n]=str("Dir("+constants[edges_dict[n][0]]+",_)"+"^Dir("+"_,"+constants[edges_dict[n][0]]+")")
        
        elif "references" in literal_ids[n]:
            if len(edges_dict[n])==2:
                print "Edges for ",n,"are: ",edges_dict[n],constants
                print constants[edges_dict[n][0]]
                print constants[edges_dict[n][1]]
                literals[n]=str("Ref("+constants[edges_dict[n][0]]+","+constants[edges_dict[n][1]]+")"+"^Ref("+constants[edges_dict[n][1]]+","+constants[edges_dict[n][0]]+")")
            
            if len(edges_dict[n])==1:
                print "Halo",edges_dict[n][0],constants[edges_dict[n][0]]
                literals[n]=str("Ref("+constants[edges_dict[n][0]]+",_)"+"^Ref("+"_,"+constants[edges_dict[n][0]]+")")
        
    clause=""    
    print literals
    for n in literals:
        clause+=literals[n]+"^"
    clause = clause[:-1]
    with open(os.path.join(output,'clause.info'),'w') as f:
        f.write(clause+"\n")
        f.write(value_list.lstrip().rstrip()[:-1])
    print clause
    return [clause,value_list]
 
 

    
if __name__ == '__main__':
     parser = argparse.ArgumentParser(description='turn yeast patterns into ')
     parser.add_argument('-p',help='selected patterns file')
     parser.add_argument('-r',help='one specific patterns')
     parser.add_argument('-c',help='path to commands')
    
     args = parser.parse_args()
     path_to_selected_patterns=args.p
     results_clause_dict={}
     
     if args.p!=None: 
         with open(path_to_selected_patterns,'r') as f:
             for line in f.readlines():
                 line=line.replace("RESULTS","PATTERNS")
                 line=line.replace("PATTERNS_400_BATCH_10_MAX_SAME_SEED","PATTERNS_400_BATCH")
                 line=line.replace("/cw/dtaijupiter/NoCsBack/dtai/irma/MARTIN_EXPERIMENTS_BACKUP/","/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/")
                 for file in os.listdir(line.rstrip()):
                    if file.endswith(".gml"):
                       pattern=nx.read_gml(os.path.join(line.rstrip(),file))
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
     print results_clause_dict
    #make commands for running on supercomputer
     with open(os.path.join(args.c,'sdm/','param.data'),'w') as f:
       f.write("result,clause\n")
       for res in results_clause_dict.keys():
           f.write(res+","+results_clause_dict[res]+"\n")


# gml="""graph [
#   name "invalid"
#   node [
#     id 0
#     label "citations"
#     predicate "citations"
#     target 1
#     valueinpattern 0
#     type None
#   ]
#   node [
#     id 1
#     label "constant:paper"
#     predicate "constant"
#     target 0
#     valueinpattern 0
#     type None
#   ]
#   node [
#     id 2
#     label "dir"
#     predicate "dir"
#     target 0
#     valueinpattern 0
#     type None
#   ]
#   node [
#     id 3
#     label "coauthored"
#     predicate "coauthored"
#     target 0
#     valueinpattern 0
#     type None
#   ]
#   node [
#     id 4
#     label "constant:paper"
#     predicate "constant"
#     target 0
#     valueinpattern 0
#     type None
#   ]
#   node [
#     id 5
#     label "references"
#     predicate "references"
#     target 0
#     valueinpattern 0
#     type None
#   ]
#   node [
#     id 6
#     label "dir"
#     predicate "dir"
#     target 0
#     valueinpattern 0
#     type None
#   ]
#   node [
#     id 7
#     label "coauthored"
#     predicate "coauthored"
#     target 0
#     valueinpattern 0
#     type None
#   ]
#   node [
#     id 8
#     label "references"
#     predicate "references"
#     type None
#     target 0
#     valueinpattern 0
#   ]
#   edge [
#     source 0
#     target 1
#   ]
#   edge [
#     source 1
#     target 2
#   ]
#   edge [
#     source 1
#     target 3
#   ]
#   edge [
#     source 1
#     target 5
#   ]
#   edge [
#     source 1
#     target 7
#   ]
#   edge [
#     source 1
#     target 8
#   ]
#   edge [
#     source 3
#     target 4
#   ]
#   edge [
#     source 4
#     target 6
#   ]
#   edge [
#     source 5
#     target 6
#   ]
# ]"""
# pattern=string_to_pattern(gml)
# readable_format=an.get_readable_text_format(pattern)
# convert(readable_format[0],readable_format[1],"")