'''
Created on Nov 9, 2016

@author: irma
'''
def convert(nodes,edges):
    clause=""
    literals={}
    literal_ids={}
    edges_dict={}
    constants={}
    value_list=""
    
    for n in nodes:
        lit_split=n.split(":")
        literal_ids[lit_split[0]]=lit_split[1]
    for e in edges:
        if e[0] not in edges_dict:
           edges_dict[e[0]]=[e[1]]
        else:
           edges_dict[e[0]].append(e[1])
        
        if e[1] not in edges_dict:
           edges_dict[e[1]]=[e[0]]
        else:
           edges_dict[e[1]].append(e[0])
    
    #first get all the constants
    for n in literal_ids:
        if "constant" in literal_ids[n]:
            if not "=" in literal_ids[n]:
                literals[n]="Protein(prot"+n+")"
                constants[n]="prot"+n
            else:
                split_prot=literal_ids[n].split("=")
                literals[n]="Protein("+split_prot+")"
                constants[n]=split_prot
                value_list+=split_prot[1]+","
    
    for n in literal_ids:
        if "location" in literal_ids[n]:
            for e in edges_dict[n]:
                if not "=" in literal_ids[n]:
                    literals[n]="Location("+constants[e]+",loc"+str(n)+")"
                else:
                    split_prot=literal_ids[n].split("=")
                    literals[n]="Location("+constants[e]+","+split_prot[1].rstrip().lstrip()+")"
                    value_list+=split_prot[1].rstrip().lstrip()+","
    print edges_dict
    
    for n in literal_ids:
        if "function" in literal_ids[n]:
            for e in edges_dict[n]:
                if not "=" in literal_ids[n]:
                    literals[n]="Function("+constants[e]+",loc"+str(n)+")"
                else:
                    split_prot=literal_ids[n].split("=")
                    literals[n]="Function("+constants[e]+","+split_prot[1]+")"
                    value_list+=split_prot[1]+","
    
    for n in literal_ids:
        if "phenotype" in literal_ids[n]:
            for e in edges_dict[n]:
                if not "=" in literal_ids[n]:
                    literals[n]="Phenotype("+constants[e]+",phen"+str(n)+")"
                else:
                    split_prot=literal_ids[n].split("=")
                    literals[n]="Phenotype("+constants[e]+","+split_prot[1]+")"
                    value_list+=split_prot[1]+","
    
    for n in literal_ids:
        if "protein_class" in literal_ids[n]:
            for e in edges_dict[n]:
                if not "=" in literal_ids[n]:
                    literals[n]="ProteinClass("+constants[e]+",pc"+str(n)+")"
                else:
                    split_prot=literal_ids[n].split("=")
                    literals[n]="ProteinClass("+constants[e]+","+split_prot[1]+")"
                    value_list+=split_prot[1]+","
    
    for n in literal_ids:
        if "interaction" in literal_ids[n]:
            if len(edges_dict[n])==2:
                literals[n]=["Interaction("+constants[edges_dict[0]]+","+constants[edges_dict[1]]+")","Interaction("+constants[edges_dict[1]]+","+constants[edges_dict[0]]+")"]
            
            if len(edges_dict[n])==1:
                literals[n]=["Interaction("+constants[edges_dict[0]]+",_)","Interaction("+"_,"+constants[edges_dict[0]]+")"]
    clause=""    
               
    for n in literals:
        clause+=literals[n]+"^"

    print clause
    print value_list
    return [clause,value_list]
    
    
    
if __name__ == '__main__':
    convert(['0:phenotype= Phen_Blah', '1:constant:protein', '2:phenotype= Phen_random', '3:function = Func_id_11'],[['0', '1'], ['1', '2'], ['1', '3']])   
    
