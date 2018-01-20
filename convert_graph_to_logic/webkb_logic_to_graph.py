import networkx as nx


def get_all_pages_to_classes(path_to_classes):
    output={}
    with open(path_to_classes,'r') as f:
        for line in f:
            if not "PageClass" in line:
                continue
            s=line.split("(")
            page1=s[1].replace(")","").rstrip()
            page2=page1.split(",")
            output[page2[0]]=page2[1].rstrip().lower()
    return output


def hash_pages(pages_dict):
    id=1
    out={}
    for k in pages_dict:
       out[k]="page_id_"+str(id)
       id+=1
    return out

def get_links(links_file,page_ids):
    output = {}
    with open(links_file, 'r') as f:
       for line in f:
           if not "Linked" in line:
               continue
           s=line.split("(")
           s1=s[1].split('","')
           page1=s1[0].replace(")","").rstrip()
           page2=s1[1].replace(")","").rstrip()
           page1_id=None
           page2_id=None
           try:
               page1_id=page_ids[page1]
           except:
               continue
           try:
               page2_id=page_ids[page2]
           except:
               continue
               #print "PRoblem!",page1_id
           if not (page1_id==None and page2_id==None):
               output[page1_id]=page2_id
    return output

def parse_linked(line):
    s = line.split("(")
    s1 = s[1].split('","')
    page1 = s1[0].replace(")", "").rstrip().replace('"', '')
    page2 = s1[1].replace(")", "").rstrip().replace('"', '')
    return page1,page2

def parse_page_class(line):
    s = line.split("(")
    page1 = s[1].replace(")", "").rstrip()
    page2 = page1.split(',')
    return page2[0].replace('"', '').rstrip(),page2[1].rstrip().lower().replace('"', '')

def parse_word(line):
    s = line.split("(")
    page1 = s[1].replace(")", "").rstrip()
    page2 = page1.split('","')
    return page2[0].replace('"', '').rstrip(),page2[1].rstrip().lower().replace('"', '')


def get_graph(pages,words,pclasses,links,prolog_output_file):
    D = nx.Graph()
    page_class_nodes={}
    word_nodes={}
    page_to_node_id={}
    prolog_pages=""
    prolog_words=""
    prolog_links=""
    distinct_words=[]
    id=0
    for p in pages:
        v=str(pages[p])
        D.add_node(id,predicate='page',label='page: '+v,value=v,name=v,id=id)
        page_to_node_id[pages[p]] = id
        id = id + 1

    for key, value in words.iteritems():
        page=page_to_node_id[key]
        for v in value:
            D.add_node(id, predicate='word', label='word: ' + v, value=v,name=v,id=id)
            D.add_edge(id,page)
            D.add_edge(page,id)
            prolog_words += "has(" + "pg_" + str(page) + "," + str(v) + ").\n"
            if not v in distinct_words:
                distinct_words.append(v)
            if v in word_nodes:
                word_nodes[v].append(id)
            else:
                word_nodes[v] = [id]
            id=id+1
    print "Nr of words: ",len(distinct_words)
    for key, value in pclasses.iteritems():
        page=page_to_node_id[key]
        for v in value:
            D.add_node(id, predicate='page_class', label='page_class: ' + v, value=v,name=v,id=id)
            D.add_edge(id,page)
            D.add_edge(page,id)
            prolog_pages+="page_class("+"pg_"+str(page)+","+str(v)+").\n"
            if v in page_class_nodes:
                page_class_nodes[v].append(id)
            else:
                page_class_nodes[v]=[id]
            id=id+1

    for key, value in links.iteritems():
        neigh1=page_to_node_id[key]
        for ne in value:
            neigh2 = page_to_node_id[ne]
            D.add_node(id, predicate='linked', label='linked: ',name='linked',id=id,value=True)
            D.add_edge(id,neigh1)
            D.add_edge(id,neigh2)
            prolog_links += "linked(" + "pg_" + str(neigh1) + "," + "pg_"+str(neigh2) + ").\n"
            id=id+1
    # for v in page_class_nodes:
    #     print v,page_class_nodes[v]
    #     for node1 in page_class_nodes[v]:
    #         for node2 in page_class_nodes[v]:
    #             if node1!=node2:
    #                 D.add_edge(node1,node2)
    # for v in word_nodes:
    #     print v, word_nodes[v]
    #     for node1 in word_nodes[v]:
    #         for node2 in word_nodes[v]:
    #             if node1!=node2:
    #                 D.add_edge(node1,node2)

    with open(prolog_output_file, 'w+') as f:
        f.write(prolog_pages)
        f.write(prolog_words)
        f.write(prolog_links)
    return D


def parse_file(file_path,prolog_out_file):
    page_dict = {}
    links_dict={}
    pClass_dict = {}
    word_dict = {}
    page_id=0

    with open(file_path, 'r') as f:
        for line in f:
            page1=None
            page2=None
            if "Linked" in line.split(")")[0]:
                page1,page2=parse_linked(line)
                if page1 in links_dict:
                    if not (page2 in links_dict and page1 in links_dict[page2]):
                       links_dict[page1].append(page2)
                else:
                    links_dict[page1] = [page2]
            if "PageClass" in line.split(")")[0]:
                    page1,pClass=parse_page_class(line)
                    if page1 in pClass_dict:
                        pClass_dict[page1].append(pClass)
                    else:
                        pClass_dict[page1]=[pClass]
            if "Has" in line.split(")")[0]:
                    page1,word=parse_word(line)
                    if page1 in word_dict:
                        word_dict[page1].append(word)
                    else:
                        word_dict[page1]=[word]


            if not page1 in page_dict:
                page_dict[page1] = page_id
                page_id += 1
            if page2!=None and not page2 in page_dict:
                page_dict[page2] = page_id
                page_id += 1
    links_hashed={}
    page_class_hashed={}
    words_hashed={}
    for l in links_dict:
        all_links=[]
        for l1 in links_dict[l]:
            all_links.append(page_dict[l1])
        links_hashed[page_dict[l]]=all_links
    for l in pClass_dict:
        page_class_hashed[page_dict[l]]=pClass_dict[l]
    for l in word_dict:
        words_hashed[page_dict[l]]=word_dict[l]

    output_graph=get_graph(page_dict,words_hashed,page_class_hashed,links_hashed,prolog_out_file)
    for n1 in output_graph.nodes():
        if output_graph.node[n1]['predicate']=="page":
            print output_graph.node[n1]
    #     for n2 in output_graph.nodes():
    #         if output_graph.node[n1]['predicate'] == output_graph.node[n2]['predicate']:
    #             if output_graph.node[n1]['predicate'] == 'linked':
    #                 continue
    #             try:
    #                 if output_graph.node[n1]['value'] == output_graph.node[n2]['value']:
    #                     output_graph.add_edge(n1, n2)
    #             except KeyError:
    #                 continue
    return output_graph






if __name__ == '__main__':
   path_to_data='/home/irma/work/DATA/INFERENCE_DATA/WEBKB/folds/fold1-train.db'
   output = '/home/irma/work/DATA/INFERENCE_DATA/WEBKB/folds/fold1-train.gpickle'
   prolog_out_file='/home/irma/work/DATA/INFERENCE_DATA/WEBKB/folds/fold1-train.pl'
   graph=parse_file(path_to_data,prolog_out_file)
   nx.write_gpickle(graph,output)
   #o=get_all_pages_to_classes(path_to_data)
   #pages_ids=hash_pages(o)
   #links=get_links(path_to_data,pages_ids)
   #for l in links:
   #    print l,links[l]

   #Course("http://cs.cornell.edu/Info/Courses/Current/CS415/CS414.html")
