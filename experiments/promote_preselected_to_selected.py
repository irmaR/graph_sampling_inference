'''
Created on Feb 12, 2016

@author: irma
'''
import argparse,os

def main(result_path,N):
    for dir in os.listdir(result_path):
        if not dir.startswith("batch"):
            continue
        #list patterns in batch
        counter=0
        
        for p in os.listdir(os.path.join(result_path,dir)):
                
                    if os.path.exists(os.path.join(result_path,dir,p,'preselected.info')) and not os.path.exists(os.path.join(result_path,dir,p,'selected.info')):
                        with open(os.path.join(result_path,dir,p,'selected.info'),'w') as f:
                            counter+=1
                            if counter>=N:
                                break
                            f.write("selected \n")
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-r',help='path to results')
    parser.add_argument('-N',help='promote N files')
    args = parser.parse_args()  
    main(args.r,args.N)