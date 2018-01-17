'''
Created on Mar 16, 2016

@author: irma
'''
import argparse,csv,os
import matplotlib.pyplot as plt

def extract_nr_constants(nodes):
    counter=0
    for l in nodes.split(","):
        if "constant" in l:
            counter+=1
    return counter


def get_min_max_nr_constants(path_to_csvs):
    min=float('inf')
    max=0
    with open(path_to_csvs) as exh:
           reader1 = csv.DictReader(exh)
           for row in reader1:
              nr_const=extract_nr_constants(row["nodes"])
              print row["pattern_name"].split("/")[-2],nr_const
              if nr_const<min:
                  min=nr_const
              if nr_const>max:
                  max=nr_const  
    return min,max    


def get_percentage_failed_number_of_cyclic_patterns(path_to_csvs,levels):
     counter=0
     fail=0
     for l in levels:
        with open(os.path.join(path_to_csvs,'exhaustive_'+str(l)+".csv")) as exh:
           reader1 = csv.DictReader(exh)
           for row in reader1:
              if row["has_cycles"]==str(True) and row["nr_randvar_values"]!=str(0):
                  counter+=1
              else:
                  break
              if row["timeout"]==str(True):
                  fail+=1
            
     print "percentage: ",float(fail)/float(counter)*100
     print "count: ",counter
     print "fails: ",fail
     return float(fail)/float(counter)*100




def plot_exhaustive_versus_no_randvars_nr_constants(path_to_csvs,levels,exp):
    min_constants=float('inf')
    max_constants=0
    res={}
    for l in levels:
        #min,max=get_min_max_nr_constants(os.path.join(path_to_csvs,'exhaustive_'+str(l)+".csv"))
        

        with open(os.path.join(path_to_csvs,'exhaustive_'+str(l)+".csv")) as exh:
           reader1 = csv.DictReader(exh)
           for row in reader1:
               if exp=="dblp":
                   time=36000
               if exp=="y":
                   time=600
               #print row["time"],(time*90/100),float(row["time"])>=(time*90/100)
               if float(row["time"])>=(time*90/100):
                      nr_constants=extract_nr_constants(row["nodes"])
                      print l,nr_constants
                      if nr_constants<min_constants:
                         min_constants=nr_constants
                      if nr_constants>max_constants:
                         max_constants=nr_constants
                      if nr_constants in res.keys():
                          res[nr_constants]+=1
                      else:
                          res[nr_constants]=1
    x=xrange(min_constants,max_constants+1,1)
    print x
    y=[]
    for el in x:
        
        if el in res.keys():
           y.append(res[el])
        else:
            y.append(0)
    print x,y
    plt.plot(x,y)
    plt.show()
    
    
    print min_constants,max_constants


if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')
  parser.add_argument('-e',help='dblp or y')
  
  args = parser.parse_args()
  plot_exhaustive_versus_no_randvars_nr_constants(args.r, [4,5,6,7,8,9,10,11,12,13,14,15], "dblp")
  get_percentage_failed_number_of_cyclic_patterns(args.r, [4,5,6,7,8,9,10,11,12,13,14,15])