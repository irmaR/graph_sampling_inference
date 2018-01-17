'''
Created on Jun 13, 2017

@author: irma
'''
import argparse,csv,os

def get_families(patterns,path_csv):
    families={}
    counter=0
    reversed_patterns=patterns[::-1]
    base_level=reversed_patterns[0]
    end_level=reversed_patterns[-1]
    path_to_pattern_size=os.path.join(path_csv,'furer_'+str(base_level)+".csv")
    
    path_to_pattern_size=os.path.join(path_csv,'furer_'+str(base_level)+".csv")
    with open(path_to_pattern_size) as f:
               reader = csv.DictReader(f)
               for row in reader:
                    
                    name_of_pattern=row["pattern_name"].split("/")[-2]
                    if not counter in families.keys():
                        families[counter]=[]
                    if not name_of_pattern in families[counter]:
                        families[counter].append(name_of_pattern)
                    if len(row["parent_id"].split("/"))==1:
                           name_of_parent=row["parent_id"]
                    else:
                         name_of_parent=row["parent_id"].split("/")[-2]
                         families[counter].append(name_of_parent)
                    counter+=1
    for r in xrange(1,len(reversed_patterns)):
        path_to_pattern_size=os.path.join(path_csv,'furer_'+str(reversed_patterns[r])+".csv")
        for c in families.keys():
            with open(path_to_pattern_size) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name_of_pattern=row["pattern_name"].split("/")[-2]
                    if reversed_patterns[r]!=end_level:
                        if name_of_pattern==families[c][r]:
                             if len(row["parent_id"].split("/"))==1:
                                   name_of_parent=row["parent_id"]
                             else:
                                 name_of_parent=row["parent_id"].split("/")[-2]
                             families[c].append(name_of_parent)
    for c in families.keys():
        print families[c]              
    return families


if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')
  
  args = parser.parse_args()
  get_families([4,5,6,7,8,9,10],args.r)
