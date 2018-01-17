'''
Created on Oct 19, 2016

@author: irma
'''
import pandas as pd
import sys, time,copy
import networkx as nx
import graph_manipulator.visualization as vis
import graph_manipulator.graph_analyzer as an

PATH_DB1="/home/irma/workspace/some_scripts_martin_sampling/DATA/webkb_simpler/dbs/fold1.db"
PATH_DB2="/home/irma/workspace/some_scripts_martin_sampling/DATA/webkb_simpler/dbs/fold2.db"
PATH_DB3="/home/irma/workspace/some_scripts_martin_sampling/DATA/webkb_simpler/dbs/fold3.db"
PATH_DB4="/home/irma/workspace/some_scripts_martin_sampling/DATA/webkb_simpler/dbs/fold4.db"
FILE_NAME="/home/irma/workspace/some_scripts_martin_sampling/DATA/webkb_simpler/webkb.gml"
links={}
student_urls=[]
staff_urls=[]
project_urls=[]
faculty_urls=[]
department_urls=[]
course_urls=[]

student_urls1=[]
staff_urls1=[]
project_urls1=[]
faculty_urls1=[]
department_urls1=[]
course_urls1=[]



files=[PATH_DB1,PATH_DB2,PATH_DB3,PATH_DB4]
counter=0
for f in files:
    counter+=1
    with open(f,'r') as f_s:
        for line in f_s.readlines():
            if "PageClassCourse" in line:
                course_urls.append(line.split("(")[1].replace(")","").rstrip()+"_c"+str(counter))
                course_urls1.append(line.split("(")[1].replace(")","").rstrip()+str(counter))
            if "PageClassDepartment" in line:
                department_urls.append(line.split("(")[1].replace(")","").rstrip()+"_d"+str(counter))
                department_urls1.append(line.split("(")[1].replace(")","").rstrip()+str(counter))
            if "PageClassFaculty" in line:
                faculty_urls.append(line.split("(")[1].replace(")","").rstrip()+"_f"+str(counter))
                faculty_urls1.append(line.split("(")[1].replace(")","").rstrip()+str(counter))
            if "PageClassResearchProject" in line:
                project_urls.append(line.split("(")[1].replace(")","").rstrip()+"_p"+str(counter))
                project_urls1.append(line.split("(")[1].replace(")","").rstrip()+str(counter))
            if "PageClassStaff" in line:
                staff_urls.append(line.split("(")[1].replace(")","").rstrip()+"_s"+str(counter))
                staff_urls1.append(line.split("(")[1].replace(")","").rstrip()+str(counter))
            if "PageClassStudent" in line:
                student_urls.append(line.split("(")[1].replace(")","").rstrip()+"_st"+str(counter))
                student_urls1.append(line.split("(")[1].replace(")","").rstrip()+str(counter))
            if "Linked" in line:
                sublink=line.split("(")[1].rstrip()
                
                link1=sublink.split(",")[0]
                
                if link1+str(counter) in course_urls1:
                    link1=link1+"_c"+str(counter)
                if link1+str(counter) in department_urls1:
                    link1=link1+"_d"+str(counter)
                if link1+str(counter) in faculty_urls1:
                    link1=link1+"_f"+str(counter)
                if link1+str(counter) in project_urls1:
                    link1=link1+"_p"+str(counter)
                if link1+str(counter) in staff_urls1:
                    link1=link1+"_s"+str(counter)
                if link1+str(counter) in student_urls1:
                    link1=link1+"_st"+str(counter)
                
                link2=sublink.split(",")[1].replace(")","")
                
                if link2+str(counter) in course_urls1:
                    link2=link2+"_c"+str(counter)
                if link2+str(counter) in department_urls1:
                    link2=link2+"_d"+str(counter)
                if link2+str(counter) in faculty_urls1:
                    link2=link2+"_f"+str(counter)
                if link2+str(counter) in project_urls1:
                    link2=link2+"_p"+str(counter)
                if link2+str(counter) in staff_urls1:
                    link2=link2+"_s"+str(counter)
                if link2+str(counter) in student_urls1:
                    link2=link2+"_st"+str(counter)
                
                if link1 in links:
                   links[link1].append(link2)
                else:
                    links[link1]=[link2]

print links
print "Number of pages: ",len(student_urls)+len(staff_urls)+len(project_urls)+len(faculty_urls)+len(department_urls)+len(course_urls)
f = open(FILE_NAME, "w")
s1 = " "
ss = s1+s1
sss = s1+s1+s1
ssss = s1+s1+s1+s1
nl = "\n"

#loop helpers
added = []
ind = 0

#Root node
f.write("graph"+nl)
f.write("["+nl)

#Write an edge
def write_edge(r,source,target):
    f.write( ss + "edge" + nl)
    f.write( ss + "[" + nl)
    f.write( ssss + "source" + s1 + '"' + str(source) + '"' + nl)
    f.write( ssss + "target" + s1 + '"' + str(target) + '"' + nl)
    f.write( ss + "]"+ nl)
    
def edge_string(source,target):
    string=""
    string+= ss + "edge" + nl
    string+= ss + "[" + nl
    string+= ssss + "source" + s1 + '"' + str(source) + '"' + nl
    string+= ssss + "target" + s1 + '"' + str(target) + '"' + nl
    string+= ss + "]"+ nl
    return string

#Write a node
def write_node(value,predicate, id):
    f.write( ss + "node" + nl)
    f.write( ss + "[" + nl)
    f.write( ssss + "value" + s1 + '"' + str(value) + '"' + nl)
    f.write( ssss + "predicate" + s1 + '"' + predicate + '"' + nl)
    if value!=predicate:
       f.write( ssss + "label" + s1 + '"' + predicate + '='+str(value)+'"' + nl)
    else:
       f.write( ssss + "label" + s1 + '"' + predicate +'"' + nl) 
    f.write( ssss + "id" + s1 + '"' + str(id) + '"' + nl)
    f.write( ss + "]"+ nl)

page_ids={}
edge_strings=[]

student_staff=0
student_student=0
student_faculty=0
student_course=0
student_department=0
student_project=0

staff_project=0
staff_course=0
staff_faculty=0
staff_department=0
staff_student=0
staff_staff=0


course_student=0
course_staff=0
course_project=0
course_department=0
course_faculty=0
course_course=0

faculty_student=0
faculty_staff=0
faculty_project=0
faculty_department=0
faculty_faculty=0
faculty_course=0

faculty_faculty=0
project_course=0
id=0
for s in [student_urls,course_urls,department_urls,faculty_urls,project_urls,staff_urls]:
    for el in s:
       if el in page_ids:
           print "WARNING DUPLICATE PAGE: ",el
       page_ids[el]=id
       id+=1

print "SIZE DICT: ",len(page_ids)

number_of_links=0

for s in [student_urls,course_urls,department_urls,faculty_urls,project_urls,staff_urls]:
    for el in s:
      print page_ids[el]

for s in student_urls:
    write_node("student",'page',page_ids[s])
    id+=1
    if s in links:
        for links_of_s in links[s]:
            
            if s==links_of_s:
                continue
            if links_of_s in staff_urls:
                student_staff+=1
            if links_of_s in student_urls:
                student_student+=1
                print s,"->",links_of_s
                print page_ids[s],page_ids[links_of_s]
            if links_of_s in course_urls:
                student_course+=1
            if links_of_s in department_urls:
                student_department+=1
            if links_of_s in faculty_urls:
                student_faculty+=1
            if links_of_s in project_urls:
                student_project+=1
            ref_id=id
            write_node("ref",'ref',ref_id)
            edge_strings.append(edge_string(page_ids[s],ref_id))
            id+=1
            dir_id=id
            write_node("dir",'dir',dir_id)
            edge_strings.append(edge_string(ref_id,dir_id))
            edge_strings.append(edge_string(dir_id,page_ids[links_of_s]))
            number_of_links+=1
            id+=1
 
for s in staff_urls:
    write_node("staff",'page',page_ids[s])
    id+=1
    if s in links:
        for links_of_s in links[s]:
            if s==links_of_s:
                continue
            if links_of_s in student_urls:
                staff_student+=1
            if links_of_s in staff_urls:
                  staff_staff+=1
            if links_of_s in project_urls:
                  staff_project+=1
            if links_of_s in course_urls:
                  staff_course+=1
            if links_of_s in department_urls:
                  staff_department+=1
            if links_of_s in faculty_urls:
                  staff_faculty+=1
            #remove self links
            
            ref_id=id
            write_node("ref",'ref',ref_id)
            edge_strings.append(edge_string(page_ids[s],ref_id))
            id+=1
            dir_id=id
            write_node("dir",'dir',dir_id)
            edge_strings.append(edge_string(ref_id,dir_id))
            edge_strings.append(edge_string(dir_id,page_ids[links_of_s]))
            number_of_links+=1
            id+=1
id+=1
for s in project_urls:
    write_node("project",'page',page_ids[s])
    id+=1
    if s in links:
        for links_of_s in links[s]:
            if s==links_of_s:
                continue
            ref_id=id
            if links_of_s in course_urls:
                  project_course+=1
            write_node("ref",'ref',ref_id)
            edge_strings.append(edge_string(page_ids[s],ref_id))
            id+=1
            dir_id=id
            write_node("dir",'dir',dir_id)
            edge_strings.append(edge_string(ref_id,dir_id))
            edge_strings.append(edge_string(dir_id,page_ids[links_of_s]))
            number_of_links+=1
            id+=1
id+=1
for s in faculty_urls:
    write_node("faculty",'page',page_ids[s])
    id+=1
    if s in links:
        for links_of_s in links[s]:
            if s==links_of_s:
                continue
            if links_of_s in student_urls:
                faculty_student+=1
            if links_of_s in staff_urls:
                  faculty_staff+=1
            if links_of_s in project_urls:
                  faculty_project+=1
            if links_of_s in course_urls:
                  faculty_course+=1
            if links_of_s in department_urls:
                  faculty_department+=1
            if links_of_s in faculty_urls:
                  
                  faculty_faculty+=1  
            ref_id=id
            write_node("ref",'ref',ref_id)
            edge_strings.append(edge_string(page_ids[s],ref_id))
            id+=1
            dir_id=id
            write_node("dir",'dir',dir_id)
            edge_strings.append(edge_string(ref_id,dir_id))
            edge_strings.append(edge_string(dir_id,page_ids[links_of_s]))
            number_of_links+=1
            id+=1
id+=1
for s in department_urls:
    write_node("department",'page',page_ids[s])
    id+=1
    if s in links:
        for links_of_s in links[s]:
            if s==links_of_s:
                continue
            ref_id=id
            write_node("ref",'ref',ref_id)
            edge_strings.append(edge_string(page_ids[s],ref_id))
            id+=1
            dir_id=id
            write_node("dir",'dir',dir_id)
            edge_strings.append(edge_string(ref_id,dir_id))
            edge_strings.append(edge_string(dir_id,page_ids[links_of_s]))
            number_of_links+=1
            id+=1
id+=1
for s in course_urls:
    write_node("course",'page',page_ids[s])
    id+=1
    if s in links:
        for links_of_s in links[s]:
            if s==links_of_s:
                continue
            
            if links_of_s in student_urls:
                course_student+=1
            if links_of_s in staff_urls:
                  course_staff+=1
            if links_of_s in project_urls:
                  course_project+=1
            if links_of_s in course_urls:
                  course_course+=1
            if links_of_s in department_urls:
                  course_department+=1
            if links_of_s in faculty_urls:
                  course_faculty+=1               
            ref_id=id
            write_node("ref",'ref',ref_id)
            edge_strings.append(edge_string(page_ids[s],ref_id))
            id+=1
            dir_id=id
            write_node("dir",'dir',dir_id)
            edge_strings.append(edge_string(ref_id,dir_id))
            edge_strings.append(edge_string(dir_id,page_ids[links_of_s]))
            number_of_links+=1
            id+=1
     
     
for edges in edge_strings:
    f.write(edges)
 
f.write("]"+nl)
f.close()

print "student->staff: ",student_staff
print "student->student: ",student_student
print "student->course: ",student_course
print "student->faculty: ",student_faculty
print "student->department: ",student_department
print "student->project: ",student_project
print "---------------------------------------"
print "staff->student: ",staff_student
print "staff->staff: ",staff_staff
print "staff->project: ",staff_project
print "staff->department: ",staff_department
print "staff->faculty: ",staff_faculty
print "staff->course: ",staff_course
print "----------------------------------"
print "course->student: ",course_student
print "course->staff: ",course_staff
print "course->project: ",course_project
print "course->department: ",course_department
print "course->faculty: ",course_faculty
print "course->course: ",course_course
print "----------------------------------"
print "faculty->student: ",faculty_student
print "faculty->staff: ",faculty_staff
print "faculty->project: ",faculty_project
print "faculty->department: ",faculty_department
print "faculty->faculty: ",faculty_faculty
print "faculty->course: ",faculty_course
print "----------------------------------"

print "faculty-> faculty: ",faculty_faculty
print "project-> course: ",project_course

data=nx.read_gml(FILE_NAME)
print "Number of directed links: ",number_of_links
print "Nr nodes WEBKB: ",len(data.nodes())
print "Nr edges WEBKB: ",len(data.edges())
print "Max degree WEBKB: ",an.get_maximum_node_degree(data)
print "Density WEBKB: ",nx.density(data)
print "INFO WEBKB:",nx.info(data)
#print an.get_maximum_node_degree(graph)

number_of_pages=0
for node in data.nodes():
        if data.node[node]['predicate']=='page':
            number_of_pages+=1
print "NUMBER OF PAGES: ",number_of_pages

#vis.visualize_graph_standard(data)
     
