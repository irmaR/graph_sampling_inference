'''
Created on Mar 16, 2016

@author: irma
'''
import argparse,csv,os


def extract_nr_constants(nodes):
    counter=0
    for l in nodes.split(","):
        if "constant" in l:
            counter+=1
    return counter


def create_csv(path_to_csvs,output_csv,levels):
    b = open(output_csv, 'w')
    field_names=['timeout','nr_const','nr_nodes','nr_targ_nodes','nr_randvars','density','max_degree','avg_degree','exh_emb','time']
    writer = csv.DictWriter(b, fieldnames=field_names)
    writer.writeheader()
    for l in levels:
        path_to_csv=os.path.join(path_to_csvs,'exhaustive_'+str(l)+".csv")
        with open(path_to_csv) as exh:
           reader1 = csv.DictReader(exh)
           for row in reader1:
               res={}
               res['timeout']=row['timeout']
               res['nr_const']=extract_nr_constants(row['nodes'])
               res['nr_nodes']=l
               res['nr_targ_nodes']=row['nr_targets']
               res['nr_randvars']=row['nr_randvar_values']
               res['density']=row['density']
               res['max_degree']=row['max_degree']
               res['avg_degree']=row['avg_deg']
               res['exh_emb']=row['exh_emb']
               res['time']=row['time']
               writer.writerow(res)
    


if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')
  parser.add_argument('-e',help='dblp or y')
  parser.add_argument('-l',help='patterns size level')
  
  args = parser.parse_args()
  create_csv(args.r,os.path.join(args.r,'output.csv'),[4,5,6,7,8,9,10,11,12,13,14,15])
  
  