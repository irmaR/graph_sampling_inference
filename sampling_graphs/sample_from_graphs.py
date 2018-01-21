'''
Created on Mar 11, 2015

@author: irma
'''
import random
import networkx as nx # @UndefinedVariable
import graph_manipulator.visualization as vis

def random_walk_sampling(complete_graph,upper_bound_nr_nodes_to_sample):
    nr_nodes=len(complete_graph.nodes())
    index_of_first_random_node=random.randint(0,nr_nodes)
    sampled_graph=nx.Graph()
    nodes_ids=[]
    added_nodes=[]
    sampled_graph.add_node(complete_graph.node[index_of_first_random_node]['id'],complete_graph.node[index_of_first_random_node])
    nodes_ids.append(complete_graph.node[index_of_first_random_node]['id'])
    added_nodes.append(complete_graph.node[index_of_first_random_node])
    
    for i in range(1,upper_bound_nr_nodes_to_sample):
        edges=complete_graph.neighbors(added_nodes[i-1]['id']) 
        index_of_edge=random.randint(0,len(edges)-1)
        chosen_node=edges[index_of_edge]
        counter=1
        
        while(not(exists_non_added_neighbour(chosen_node, complete_graph))):#means that the current chosen node has no other possible outgoing edges
            if(not('added' in complete_graph.node[chosen_node])):
                nodes_ids,added_nodes,sampled_graph,complete_graph=add_node_to_graph(complete_graph, sampled_graph, chosen_node, added_nodes[i-1]['id'], nodes_ids, added_nodes)
                
            counter+=1
            #then choose another node to start from (in existing added nodes)
            #backtrack to the previous nodes
            edges=complete_graph.neighbors(added_nodes[i-counter]['id']) 
            index_of_edge=random.randint(0,len(edges)-1)
            chosen_node=edges[index_of_edge]
         
        nodes_ids,added_nodes,sampled_graph,complete_graph=add_node_to_graph(complete_graph, sampled_graph, chosen_node, added_nodes[i-1]['id'], nodes_ids, added_nodes)   
    return sampled_graph
    
def add_node_to_graph(graph, sampled_graph,chosen_node,current_node,nodes_ids,added_nodes):
    graph.node[chosen_node]['added']=True
    nodes_ids.append(chosen_node)
    added_nodes.append(graph.node[chosen_node])
    sampled_graph.add_node(chosen_node,graph.node[chosen_node])
    sampled_graph.add_edge(current_node, chosen_node)
    return nodes_ids,added_nodes,sampled_graph,graph


def exists_non_added_neighbour(current_node,graph):
        edges=graph.neighbors(current_node)      
        for node in edges:
            if(not('added' in graph.node[node])):
                return True
        
        return False
           
    

if __name__ == '__main__':
     Yeast=nx.read_gpickle("/cw/dtailocal/irma/Martin_paper/graph_sampling/graph_sampling/patternSampler/YEAST.gpickle")    
    
     graph=random_walk_sampling(Yeast,300)
     nx.write_gml(graph, "/cw/dtailocal/irma/Martin_paper/graph_sampling/graph_sampling/patternSampler/YEAST_"+str(len(graph.nodes()))+".gpickle")
     vis.visualize_graph(graph)
    
     