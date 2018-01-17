'''
Created on Jul 13, 2015

@author: irma
'''
import argparse,os
import networkx as nx

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-path', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-predicate', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')

    args = parser.parse_args() 
    results=args.path
    level=results.split("/")[-2].split("_")[-1]
    
    nr_selected_so_far=0
    not_completed=0
    completed_furer=0
    completed_false_furer=0
    completed_rnd=0
    completed_exhaustive=0
    
    
    for dir in os.listdir(results):
        if os.path.isdir(os.path.join(results,dir)):
            #go through batches
            #for pattern_res in os.listdir(os.path.join(results,dir)):
            result_to_batch=os.path.join(results,dir)
            graph=nx.read_gml(os.path.join(result_to_batch,dir+'.gml'))
            count=0
            for node in graph.nodes():
                if graph.node[node]['predicate']==args.predicate and graph.node[node]['target']==1:
                    count+=1
            
            if count>1:
                print result_to_batch