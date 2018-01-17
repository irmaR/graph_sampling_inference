'''
Created on Nov 9, 2016

@author: irma
'''
import pickle
import networkx as nx
data_file_name="/home/irma/workspace/DATA/Facebook/facebook.gpickle"
output="/home/irma/workspace/DATA/Facebook/facebook.db"
output_prolog="/home/irma/workspace/DATA/Facebook/facebook.pl"

data_graph=nx.read_gpickle(data_file_name)

properties=[]

gender_string=""
education_type_string=""
user_string=""
friendships=[]
education_degree_string=""
birthday_string=""
hometown_string=""
language_string=""

nr_users=0
for n in data_graph.nodes():
    if not data_graph.node[n]['predicate'] in properties:
        properties.append(data_graph.node[n]['predicate'])
    
    if data_graph.node[n]['predicate']=='user':
        nr_users+=1

print "Nr users: ",nr_users

counter=0
for n in data_graph.nodes():
    if not data_graph.node[n]['predicate'] in properties:
        properties.append(data_graph.node[n]['predicate'])
    
    if data_graph.node[n]['predicate']=='user':
      counter+=1
      print "Processing user",counter,"out of",nr_users
      user_string+="User(Us_"+str(data_graph.node[n]['id']).title()+")\n"
      #get neighbours of the protein
      neighbours= data_graph.neighbors(n)
      for ne in neighbours:
          #print data_graph.node[ne]
          if data_graph.node[ne]['predicate']=='gender':
              gender_string+="Gender(Us_"+str(data_graph.node[n]['id'])+","+data_graph.node[ne]['value'].title()+")\n"
          if data_graph.node[ne]['predicate']=='education_type':
              education_type_string+="Education_type(Us_"+str(data_graph.node[n]['id'])+","+data_graph.node[ne]['value'].title()+")\n"
          if data_graph.node[ne]['predicate']=='education_degree':
              education_degree_string+="Education_degree(Us_"+str(data_graph.node[n]['id'])+","+data_graph.node[ne]['value'].title()+")\n"
          if data_graph.node[ne]['predicate']=='birthday':
              birthday_string+="Birthday(Us_"+str(data_graph.node[n]['id'])+","+data_graph.node[ne]['value'].title()+")\n"
          if data_graph.node[ne]['predicate']=='hometown':
              hometown_string+="Hometown(Us_"+str(data_graph.node[n]['id'])+","+data_graph.node[ne]['value'].title()+")\n"
          if data_graph.node[ne]['predicate']=='language':
              hometown_string+="Language(Us_"+str(data_graph.node[n]['id'])+","+data_graph.node[ne]['value'].title()+")\n"
          if data_graph.node[ne]['predicate']=='user':
              string_inter="Friends(Us_"+str(data_graph.node[ne]['id'])+",Us_"+str(data_graph.node[n]['id'])+")"
              string_inter_reverse="Friends(Us_"+str(data_graph.node[n]['id'])+",Us_"+str(data_graph.node[ne]['id'])+")"
              if not string_inter in friendships:
                  friendships.append(string_inter)
              if not string_inter_reverse in friendships:
                  friendships.append(string_inter_reverse)
print "Nr friendships", len(friendships)


with open(output,'w+') as f:
    f.write(user_string)
    f.write(gender_string)
    f.write(education_type_string)
    f.write(education_degree_string)
    f.write(birthday_string)
    f.write(hometown_string)
    f.write(language_string)

    for s in friendships: 
       f.write(s+"\n")
    
with open(output_prolog,'w+') as f:
    for s in user_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in gender_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in education_type_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in education_degree_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in birthday_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in hometown_string.split("\n"):
      f.write(s.lower()+".\n")
    for s in language_string.split("\n"):
      f.write(s.lower()+".\n")
    for inter in friendships:
         f.write(inter.lower()+".\n")

    
     
                 
