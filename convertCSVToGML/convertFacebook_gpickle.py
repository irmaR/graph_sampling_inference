'''
Created on Nov 30, 2016

@author: irma
'''
import graph_manipulator.visualization as vis
import networkx as nx
import pickle
import graph_manipulator.graph_analyzer as an

FILE_NAME = "/home/irma/workspace/DATA/Facebook/facebook.gpickle"
users_and_edges="/home/irma/workspace/DATA/Facebook/facebook_combined.txt"

users_list=[]
edges_map={}
nr_edges=0



with open(users_and_edges,'r') as f:
    for line in f.readlines():
        users=line.rstrip().lstrip().split(" ") 
        if not users[0] in users_list:
            users_list.append(users[0])
        if not users[1] in users_list:
            users_list.append(users[1])
        if users[0] in edges_map:
            edges_map[users[0]].append(users[1])
        else:
            edges_map[users[0]]=[users[1]]
        
        nr_edges+=1

links=0

for user in edges_map.keys():
       for user2 in edges_map[user]:
          links+=1

print "Collected users..."        
print "Nr users:",len(users_list)
print "Nr edges:",nr_edges
print "links: ",links


ego_users=[0, 107,348,414,686,1684,1912,3437,3980]
birthday_indices={}
education_type_indices={}
education_degree_indices={}
gender_indices={}
hometown_indices={}
language_indices={}
features={}

bitrthday_ids={}
education_type_ids={}
education_degree_ids={}
gender_ids={}
hometown_ids={}
language_ids={}
features_ids={}

birthdays={}
education_types={}
education_degrees={}
gender={}
hometown={}
language={}


for e in ego_users:
    with open("/home/irma/workspace/DATA/Facebook/facebook/"+str(e)+".featnames",'r') as f:
        for line in f.readlines():
            fts=line.rstrip().split(" ")
            ft_name=fts[1]
            if "birthday" in ft_name:
                if str(e) in birthday_indices:
                    birthday_indices[str(e)].append(int(fts[0]))
                    bitrthday_ids[str(e)].append(int(fts[-1]))
                else:
                    birthday_indices[str(e)]=[int(fts[0])]
                    bitrthday_ids[str(e)]=[int(fts[-1])]
            
            if "education;type" in ft_name:
                if str(e) in education_type_indices:
                    education_type_indices[str(e)].append(int(fts[0]))
                    education_type_ids[str(e)].append(int(fts[-1]))
                else:
                    education_type_indices[str(e)]=[int(fts[0])]
                    education_type_ids[str(e)]=[int(fts[-1])]
                    
            if "gender" in ft_name:
                if str(e) in gender_indices:
                    gender_indices[str(e)].append(int(fts[0]))
                    gender_ids[str(e)].append(int(fts[-1]))
                else:
                    gender_indices[str(e)]=[int(fts[0])]
                    gender_ids[str(e)]=[int(fts[-1])]
                    
            if "education;degree" in ft_name:
                if str(e) in education_degree_indices:
                    education_degree_indices[str(e)].append(int(fts[0]))
                    education_degree_ids[str(e)].append(int(fts[-1]))
                else:
                    education_degree_indices[str(e)]=[int(fts[0])]  
                    education_degree_ids[str(e)]=[int(fts[-1])]  
            
            if "hometown" in ft_name:
                if str(e) in hometown_indices:
                    hometown_indices[str(e)].append(int(fts[0]))
                    hometown_ids[str(e)].append(int(fts[-1]))
                else:
                    hometown_indices[str(e)]=[int(fts[0])] 
                    hometown_ids[str(e)]=[int(fts[0])]    
                    
            if "language" in ft_name:
                if str(e) in language_indices:
                    language_indices[str(e)].append(int(fts[0]))
                    language_ids[str(e)].append(int(fts[-1]))
                else:
                    language_indices[str(e)]=[int(fts[0])]   
                    language_ids[str(e)]=[int(fts[-1])]    

alter_to_ego={}
edges={}

nr_links=0

for e in ego_users:
    with open("/home/irma/workspace/DATA/Facebook/facebook/"+str(e)+".feat",'r') as f:
        for line in f.readlines():
            fts=line.rstrip().split(" ")
            features[fts[0]]=fts[1:] 
            alter_to_ego[str(fts[0])]=str(e)
           
                
            
    with open("/home/irma/workspace/DATA/Facebook/facebook/"+str(e)+".egofeat",'r') as f:
        for line in f.readlines():
            fts=line.rstrip().split(" ")
            features[str(e)]=fts
            alter_to_ego[str(e)]=str(e)


user_birthday={}
user_hometown={}
user_education_type={}
user_education_degree={}
user_gender={}
user_language={}

gender_unknown=0
hometown_unknown=0
education_type_unknown=0
education_degree_unknown=0
birthday_unknown=0
language_unknown=0

print "#USERS WITH FEATURES: ",len(features.keys())
print birthday_indices      
for user in features.keys():
    ego_index=alter_to_ego[user]
    user_feature=features[user]
    try:
      birthday_index = [user_feature[i] for i in birthday_indices[ego_index]].index('1')
      birthday_count = [user_feature[i] for i in birthday_indices[ego_index]].count('1')
      user_birthday[user]=bitrthday_ids[ego_index][birthday_index]
      if birthday_count>1:
         print "WARNING BIRTHDAY!!!"
    except:
        birthday_index=-1
        birthday_unknown+=1
        user_birthday[user]="unknown"
    try:
      gender_index = [user_feature[i] for i in gender_indices[ego_index]].index('1')
      gender_count = [user_feature[i] for i in gender_indices[ego_index]].count('1')
      user_gender[user]=gender_ids[ego_index][gender_index]
      if(gender_count>1):
          print "WARNING GENDER!"
    except:
      gender_index=-1
      gender_unknown+=1
      user_gender[user]="unknown"
    #print ego_index,user,hometown_indices[ego_index],[user_feature[i] for i in hometown_indices[ego_index]]
    try:
      hometown_index = [user_feature[i] for i in hometown_indices[ego_index]].index('1')
      hometown_count = [user_feature[i] for i in hometown_indices[ego_index]].count('1')
      user_hometown[user]=hometown_ids[ego_index][hometown_index]
      if hometown_count>1:
          print "WARNING HOMETOWN"
    except:
      hometown_index=-1
      hometown_unknown+=1
      user_hometown[user]="unknown"
    try:
      education_type_index = [user_feature[i] for i in education_type_indices[ego_index]].index('1')
      education_type_count = [user_feature[i] for i in education_type_indices[ego_index]].count('1')
      user_education_type[user]=education_type_ids[ego_index][education_type_index]
    except:
      education_type_index=-1
      education_type_unknown+=1
      user_education_type[user]="unknown"
    try:
       if ego_index!=686: #no education degree for this circle
          education_degree = [user_feature[i] for i in education_degree_indices[ego_index]].index('1')
          education_degree_count = [user_feature[i] for i in education_degree_indices[ego_index]].count('1')
          user_education_degree[user]=education_degree_ids[ego_index][education_degree]
    except:
          education_degree=-1
          education_degree_unknown+=1
          user_education_degree[user]="unknown"
    try: 
       language_index=[user_feature[i] for i in language_indices[ego_index]].index('1')
       language_count = [user_feature[i] for i in language_indices[ego_index]].count('1')
       user_language[user]=language_ids[ego_index][language_index]
    except:
        language_index=-1
        language_unknown+=1
        user_language[user]="unknown"

f = open(FILE_NAME, "w")

def chunkIt(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0

  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg

  return out
  
#loop helpers
added = []
ind = 0


G=nx.Graph() 
      
nr_users=0
user_ids={}
id=0    
for user in users_list:
    nr_users+=1
    G.add_node(id,id=id,predicate='user')
    user_ids[user]=id
    id+=1



birthdays=0
hometowns=0
education_types=0
education_degrees=0
genders=0
languages=0

feature_edges=""

birthday_values=[]
hometown_values=[]
education_type_values=[]
education_degree_values=[]
language_values=[]
gender_values=[]

#write birthdays
for user in user_birthday.keys():
    if not str(user_birthday[user]) in birthday_values:
        birthday_values.append(str(user_birthday[user]))        
birthday_categories=chunkIt(birthday_values, 3)

for user in user_birthday.keys():
    if str(user_birthday[user])=='unknown':
       G.add_node(id,id=id,value="value_unknown",predicate='birthday') 
    elif str(user_birthday[user]) in birthday_categories[0]:
       G.add_node(id,id=id,value="value_1",predicate='birthday')
    elif str(user_birthday[user]) in birthday_categories[1]:
       G.add_node(id,id=id,value="value_2",predicate='birthday')
    elif str(user_birthday[user]) in birthday_categories[2]:
       G.add_node(id,id=id,value="value_3",predicate='birthday')
    G.add_edge(user_ids[user],id)
    birthdays+=1
    id+=1

#print "Birthday values: ",birthday_values
#for node in G.nodes():
#    print G.node[node]['predicate']

#write hometowns

for user in user_hometown.keys():
    if not str(user_hometown[user]) in hometown_values:
        hometown_values.append(str(user_hometown[user]))        
hometown_categories=chunkIt(hometown_values, 3) 
 
for user in user_hometown.keys():
     if str(user_hometown[user])=='unknown':
       G.add_node(id,id=id,value="value_unknown",predicate='hometown')
     elif str(user_hometown[user]) in hometown_categories[0]:
       G.add_node(id,id=id,value="value_1",predicate='hometown')
     elif str(user_hometown[user]) in hometown_categories[1]:
       G.add_node(id,id=id,value="value_2",predicate='hometown')
     elif str(user_hometown[user]) in hometown_categories[2]:
       G.add_node(id,id=id,value="value_3",predicate='hometown')
     
     if user in user_ids:
        G.add_edge(int(user_ids[user]),id)
     hometowns+=1
     id+=1
  
 #write education type
for user in user_education_type.keys():
    if not str(user_education_type[user]) in education_type_values:
        education_type_values.append(str(user_education_type[user]))        
education_type_categories=chunkIt(education_type_values, 3) 

for user in user_education_type.keys():
     if str(user_education_type[user])=='unknown':
       G.add_node(id,id=id,value="value_unknown",predicate='education_type')
     
     elif str(user_education_type[user]) in education_type_categories[0]:
       G.add_node(id,id=id,value="value_1",predicate='education_type')
    
     elif str(user_education_type[user]) in education_type_categories[1]:
       G.add_node(id,id=id,value="value_2",predicate='education_type')
       
     elif str(user_education_type[user]) in education_type_categories[2]:
       G.add_node(id,id=id,value="value_3",predicate='education_type')
     
     if user in user_ids:
       G.add_edge(int(user_ids[user]),id)
     education_types+=1
     id+=1
     
 
 #write education degree
for user in user_education_degree.keys():
    if not str(user_education_degree[user]) in education_degree_values:
        education_degree_values.append(str(user_education_degree[user]))        
education_degree_categories=chunkIt(education_degree_values, 3)

for user in user_education_degree.keys():
     if str(user_education_degree[user])=='unknown':
        G.add_node(id,id=id,value="value_unknown",predicate='education_degree')
     elif str(user_education_degree[user]) in education_degree_categories[0]:
        G.add_node(id,id=id,value="value_1",predicate='education_degree')
     elif str(user_education_degree[user]) in education_degree_categories[1]:
        G.add_node(id,id=id,value="value_2",predicate='education_degree')
     elif str(user_education_degree[user]) in education_degree_categories[2]:
        G.add_node(id,id=id,value="value_3",predicate='education_degree')
     
     if user in user_ids:
       G.add_edge(int(user_ids[user]),id)
     education_degrees+=1
     id+=1
     
print "Education degree values: ",education_degree_values
 
 #write gender
for user in user_gender.keys():
     G.add_node(id,id=id,value="value_"+str(user_gender[user]),predicate='gender')
     if not "value_"+str(user_gender[user]) in gender_values:
         gender_values.append("value_"+str(user_gender[user]))
     if user in user_ids:
        G.add_edge(int(user_ids[user]),id)
     genders+=1
     id+=1
 
print "Gender values: ",gender_values
 
 #write language
for user in user_language.keys():
    if not str(user_language[user]) in language_values:
        language_values.append(str(user_language[user]))        
language_values_categories=chunkIt(language_values, 3) 

for user in user_language.keys():
     if str(user_language[user])=='unknown':
        G.add_node(id,id=id,value="value_unkwnon",predicate='language')
     elif str(user_language[user]) in language_values_categories[0]:
        G.add_node(id,id=id,value="value_1",predicate='language')
     elif str(user_language[user]) in language_values_categories[1]:
        G.add_node(id,id=id,value="value_2",predicate='language')
     elif str(user_language[user]) in language_values_categories[2]:
        G.add_node(id,id=id,value="value_3",predicate='language')
     
     if user in user_ids:
        G.add_edge(int(user_ids[user]),id)
     languages+=1
     id+=1

links=0
edges_pairs=[]
for user in edges_map.keys():
       for user2 in edges_map[user]:
          #if not str(user_ids[user])+","+str(user_ids[user2]) in edges_pairs and not str(user_ids[user2])+","+str(user_ids[user]) in edges_pairs:
            print "edge: ",user_ids[user],user_ids[user2]
            G.add_edge(user_ids[user],user_ids[user2])
            edges_pairs.append(str(user_ids[user])+","+str(user_ids[user2]))
            links+=1

print "nr nodes before pickling: ",len(G.nodes())
number_of_users=0
print "NUMBER OF USERS: ",number_of_users

pickle.dump(G, open(FILE_NAME,'wb'))

data=nx.read_gpickle(FILE_NAME)
print "Nr nodes FACEBOOK: ",len(data.nodes())
print "Nr edges FACEBOOK: ",len(data.edges())
print "Max degree FACEBOOK: ",an.get_maximum_node_degree(data)
print "Density FACEBOOK: ",nx.density(data)
print "INFO FACEBOOK:",nx.info(data)
print "Nr user links: ",links
#print an.get_maximum_node_degree(graph)
print "Number of nodes after pickling",len(data.nodes())
#for n in data.nodes():
#        print data.node[n]
#        if data.node[n]['predicate']=='user':
#            number_of_users+=1

#vis.visualize_graph_standard(data)