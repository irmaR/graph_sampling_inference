'''
Created on Sep 26, 2016

@author: irma
'''
'''
Created on Sep 6, 2016

@author: irma
'''
import pandas as pd
import sys, time
import networkx as nx
import graph_manipulator.visualization as vis
import graph_manipulator.graph_analyzer as an

def f(x):
     return pd.Series(dict(A = x['page'], 
                        C = [].append(x['cite'])))

#Utility functions
def progress(v):
    v = str(v)
    sys.stdout.flush()
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(v)

FILE_NAME = "/home/irma/workspace/some_scripts_martin_sampling/DATA/imdb/output.gml"
imdb_input = '/home/irma/workspace/some_scripts_martin_sampling/DATA/imdb/imdb.db'

movies={}
actors={}
directors={}
worked_under={}
genre={}
associated_person={}
gender={}
id=0
same_gender={}

with open(imdb_input,'r') as f:
    for line in f.readlines():
        if "actor" in line:
            actors[line[line.find("(")+1:line.find(")")].rstrip().lstrip()]=id
        if "movie" in line:
            movie=line[line.find("(")+1:line.find(",")].rstrip().lstrip()
            movies[movie]=id
            if movie in associated_person:
              associated_person[movie].append(line[line.find(",")+1:line.find(")")].rstrip().lstrip())
            else:
              associated_person[movie]=[line[line.find(",")+1:line.find(")")].rstrip().lstrip()]  
        if "director" in line:
            directors[line[line.find("(")+1:line.find(")")].rstrip().lstrip()]=id
        if "workedUnder" in line:
            obj1=line[line.find("(")+1:line.find(",")].rstrip().lstrip()
            obj2=line[line.find(",")+1:line.find(")")].rstrip().lstrip()
            worked_under[obj1]=obj2
        if "gender" in line:
            obj1=line[line.find("(")+1:line.find(",")].rstrip().lstrip()
            gender_1=line[line.find(",")+1:line.find(")")].rstrip().lstrip()
            gender[obj1]=(gender_1,id)
            if gender_1 in same_gender:
                same_gender[gender_1].append(id)
            else:
                same_gender[gender_1]=[]
                same_gender[gender_1].append(id)
        if "genre" in line:
            obj1=line[line.find("(")+1:line.find(",")] #person
            genre_1=line[line.find(",")+1:line.find(")")].rstrip().lstrip()
            #print obj1,genre
            genre[obj1]=(genre_1,id)
        id+=1

f = open(FILE_NAME, "w")
#helpers
s = " "
ss = s+s
sss = s+s+s
ssss = s+s+s+s
nl = "\n"
 
#loop helpers
added = []
ind = 0
 
#Root node
f.write("graph"+nl)
f.write("["+nl)
 
#Write an edge
def write_edge(source,target):
    f.write( ss + "edge" + nl)
    f.write( ss + "[" + nl)
    f.write( ssss + "source" + s + str(source) + nl)
    f.write( ssss + "target" + s + str(target) + nl)
    f.write( ss + "]"+ nl)
 
#Write a node
def write_node(predicate,label,id):
    f.write( ss + "node" + nl)
    f.write( ss + "[" + nl)
    f.write( ssss + "id" + s + str(id)  + nl)
    f.write( ssss + "value" + s + '"' + label + '"' + nl)
    f.write( ssss + "predicate" + s + '"' + predicate + '"' + nl)
    f.write( ssss + "label" + s + '"' + label + '"' + nl)
    f.write( ss + "]"+ nl)
     
id+=1
#generate actor nodes
for a in actors:
    write_node("actor",a,actors[a])
    if a in gender:
       write_node("gender",gender[a][0],gender[a][1])
    if a in genre:
       write_node("genre",genre[a][0],genre[a][1])

#generate director nodes
for a in directors:
    write_node("director",a,directors[a])
    if a in gender:
       write_node("gender",gender[a][0],gender[a][1])
    if a in genre:
       write_node("genre",genre[a][0],genre[a][1])
    
#generate movies nodes
for a in movies:
    write_node("movie",a,movies[a])
   
       
    
print(nl+"Printing nodes over")

for a in worked_under:
    id+=1
    if a in actors:
        id1=actors[a]
    if a in directors:
        id1=directors[a]
    other=worked_under[a]
    if other in actors:
        id2=actors[other]
    if other in directors:
        id2=directors[other]
    #write_node("workedUnder","true",id)
    write_edge(id1,id2)
    #write_edge(id,id2)
    
for a in gender:
     if a in actors:
       write_edge(actors[a],gender[a][1])
     if a in directors:
       write_edge(directors[a],gender[a][1])

for a in genre:
     if a in actors:
       write_edge(actors[a],genre[a][1])
     if a in directors:
       write_edge(directors[a],genre[a][1])
           
print "ACTORS:"
for a in actors:
    print a           

#get associated persons with each movie
i=0
d=0
for a in movies:
     assoc_persons=associated_person[a]
     print assoc_persons
     for pers in assoc_persons:
         print pers, pers in actors
         print pers, pers in directors
         if pers in actors:
             id1=actors[pers]
             i+=1
         if pers in directors:
             id1=directors[pers]
             d+=1
         write_edge(id1,movies[a])

#same gender

# for g in same_gender:
#     print g,len(same_gender[g])
#      ind=1
#      for id in same_gender[g]:
#          ind1=ind+1
#          for id1 in same_gender[g]:
#              if id==id1:
#                  continue
#              if ind1>ind:
#                 write_edge(id,id1) 
#          ind+=1
    
f.write("]"+nl)
f.close()
print genre
graph=nx.read_gml(FILE_NAME)
# for n in graph.nodes():
#     print graph.node[n] 
vis.visualize_graph_standard(graph)


#data=nx.read_gpickle('/home/irma/workspace/Martin_experiments/DBLP/dblp.gpickle')
#for n in data.nodes():
#    if 'value' in data.node[n]:
#       print data.node[n]
#       break
