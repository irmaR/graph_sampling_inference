'''
Created on Jun 5, 2017

@author: irma
'''
import argparse,os,shutil
if __name__ == '__main__':
     parser = argparse.ArgumentParser(description='turn yeast patterns into ')
     parser.add_argument('-p',help='selected patterns file')
     
     args = parser.parse_args()
     path_to_selected_patterns=args.p
        
     results_clause_dict={}
             
     if args.p!=None: 
         with open(path_to_selected_patterns,'r') as f:
             for line in f.readlines():
                 fact_result=os.path.join(line.rstrip(),'sdm')
                 for file in os.listdir(fact_result):
                     file1=os.path.join(fact_result,file)
                     if not file1.endswith('.res'):
                         os.remove(file1)
                 