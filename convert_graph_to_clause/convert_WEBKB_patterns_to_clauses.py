
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
        
        if e[1] not in edges_dict:
           edges_dict[e[1]]=[e[0]]
        else:
           edges_dict[e[1]].append(e[0])
    
    print "edges disct: ",edges_dict
    #first get all the constants
    for n in literal_ids:
        if "page" in literal_ids[n]:
            #if not "=" in literal_ids[n]:
                #literals[n]="Page(pg"+n+")"
                constants[n]="pg"+n
            #else:
            #    split_prot=literal_ids[n].split("=")[1].rstrip().lstrip()
                #literals[n]="Page("+split_prot+")"
            #    constants[n]=split_prot
            #    value_list+=split_prot[1].rstrip().lstrip()+","
    print constants   
    for n in literal_ids:
        if "page" in literal_ids[n]:
            if not "=" in literal_ids[n]:
                    literals[n]="Page("+constants[n]+",val"+str(n)+")"
            else:
                    split_prot=literal_ids[n].split("=")
                    literals[n]="Page("+constants[n]+","+split_prot[1].rstrip().lstrip().title()+")"
                    value_list+=split_prot[1].rstrip().lstrip().title()+","
    print constants
#     for n in literal_ids:
#         if "ref" in literal_ids[n]:
#             if not "=" in literal_ids[n]:
#                 literals[n]="Ref(ref"+n+")"
#                 constants[n]="ref"+n
#             else:
#                 split_prot=literal_ids[n].split("=")
#                 literals[n]="Ref("+split_prot+")"
#                 constants[n]=split_prot
#                 value_list+=split_prot[1].rstrip().lstrip()+","
#     for n in literal_ids:
#         if "dir" in literal_ids[n]:
#             if not "=" in literal_ids[n]:
#                 literals[n]="Dir(dir"+n+")"
#                 constants[n]="dir"+n
#             else:
#                 split_prot=literal_ids[n].split("=")
#                 literals[n]="Dir("+split_prot+")"
#                 constants[n]=split_prot
#                 value_list+=split_prot[1].rstrip().lstrip()+","
            
#see if there connection exists between following pairs, dir and page (reference), page and ref (direction)
    counter=1
    for n in literal_ids:
        if "page" in literal_ids[n]:
            print "lit",n
            print edges_dict[n]
            for e in edges_dict[n]:
                #get all directions neihbours
                if "dir" in literal_ids[e]:
                    for refs in edges_dict[e]:
                        print "refs: ",refs
                        if "ref" in literal_ids[refs]:
                            for pages in edges_dict[refs]:
                                   if "page" in literal_ids[pages]:
                                      literals['ref'+str(counter)]="References("+constants[n]+","+constants[pages]+")"
                                      counter+=1
                                      
                                   
    for n in literal_ids:
        if "page" in literal_ids[n]:
            print "lit",n
            for e in edges_dict[n]:
                #get all directions neihbours
                if "ref" in literal_ids[e]:
                    for refs in edges_dict[e]:
                        if "dir" in literal_ids[refs]:
                            for pages in edges_dict[refs]:
                                   if "page" in literal_ids[pages]:
                                      literals['ref'+str(counter)]="References("+constants[pages]+","+constants[n]+")"
                                      counter+=1
    

#     print "Constants: ",constants
#     for n in literal_ids:
#         print n,literal_ids[n],edges_dict[n]
#         if "interaction" in literal_ids[n]:
#             if len(edges_dict[n])==2:
#                 literals[n]=str("Interaction("+constants[edges_dict[n][0]]+","+constants[edges_dict[n][1]]+")"+"^Interaction("+constants[edges_dict[n][1]]+","+constants[edges_dict[n][0]]+")")
#             
#             if len(edges_dict[n])==1:
#                 literals[n]=str("Interaction("+constants[edges_dict[n][0]]+",_)"+"^Interaction("+"_,"+constants[edges_dict[n][0]]+")")
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
                 #line=line.replace("RESULTS_400_BATCH_10_MAX","PATTERNS_400_BATCH")
                 line=line.replace("RESULTS","PATTERNS")
                 for file in os.listdir(line.rstrip()):
                    if file.endswith(".gml"):                       
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
      
      
        
         
    
 
    
   #convert(['0:ref', '1:ref', '2:page', '3:ref', '4:dir', '5:page = faculty', '6:dir', '7:page = project'],[['0', '2'], ['0', '4'], ['1', '2'], ['1', '6'], ['2', '3'], ['4', '5'], ['6', '7']],"")
    
