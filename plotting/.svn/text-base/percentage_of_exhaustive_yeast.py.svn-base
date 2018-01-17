'''
Created on Mar 8, 2016

@author: irma
'''
import argparse,os,csv,math
import matplotlib.pyplot as plt

def calculate_relative_errors_exhaustive(array_of_nr_emb_exhaustive,array_of_nr_emb_approachX):
    sum=0
    max_value=0
    min_value=float('inf')
    missing_values_appX_indices=[]
    missing_values_exh_indices=[]
    rel_errors=[]
    n=0
    for i in xrange(0,len(array_of_nr_emb_exhaustive)):
        v1=array_of_nr_emb_exhaustive[i]
        v2=array_of_nr_emb_approachX[i]
        nr=abs((float(v1)-float(v2)))/v1
        if not math.isnan(nr):
          rel_errors.append(abs((float(v1)-float(v2)))/v1)
    return rel_errors


def get_runtimes_embeddings_exhaustive(path_to_exhaustive_csv):
    map_runtimes={}
    map_embs={}
    with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
         if(not(row["exh_emb"])):
             continue
         nr_emb_exhaustive=float(row["exh_emb"])
         name_of_patterns=row["pattern_name"].split("/")[-2]
         map_runtimes[name_of_patterns]=float(row["time"])
         map_embs[name_of_patterns]=nr_emb_exhaustive
    return map_runtimes,map_embs


def get_intervals(N):
    intervals_seconds=[]
    for x in xrange(0,110,10):
        intervals_seconds.append(int(((N*x)/100)/5))
    return intervals_seconds


def get_results_percentages(pattern_name,runtime_exh,emb_exh,furer_csv):
    relative_errors=[]
    row_of_interest={}
    with open(furer_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
         name_of_pattern=row["pattern_name"].split("/")[-2]
         if name_of_pattern==pattern_name:
             row_of_interest=row
             break
    intervals=get_intervals(runtime_exh)
    print intervals
    #print pattern_name,intervals
    embeddings_furer=[]
    for t in intervals:
        if t==0:
            t=1
        if t>120:
            t=120
        column_name="emb_"+str(t)
        embeddings_furer.append(float(row[column_name]))
    return calculate_relative_errors_exhaustive([emb_exh] * len(embeddings_furer),embeddings_furer)



def plot(furer_OBD_results,furer_AD_results):
   fig = plt.figure()
   x=xrange(0,110,10)
   print len(furer_OBD_results),len(x)
   plt.plot(x, furer_OBD_results)
   plt.plot(x, furer_AD_results)
    
   plt.xlabel('time (s)')
   plt.ylabel('voltage (mV)')
   plt.title('About as simple as it gets, folks')
   plt.grid(True)
   plt.savefig("test.png")
   plt.legend(['Furer-OBD', 'Furer-AD'], loc='upper left')
   plt.show()

def get_average_errors_per_percentage(map_relative_errors):
    average_rel_errors=[]
    for i in xrange(0,11):
        sum=0
        c=0
        for patt in map_relative_errors.keys():
            c+=1
            sum+=map_relative_errors[patt][i]
        average_rel_errors.append(sum/float(c))
    return average_rel_errors
    
def main(path_to_csv,level):
    map_furer_OBD_to_percentages_rel_errors={}
    map_furer_AD_to_percentages_rel_errors={}
    map_runtimes_seconds,map_final_embs=get_runtimes_embeddings_exhaustive(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"))
    
    for pattern in map_runtimes_seconds.keys():
        map_furer_OBD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'furer_'+str(level)+".csv"))
        map_furer_AD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"))

    average_relative_errors_furer_OBD=get_average_errors_per_percentage(map_furer_OBD_to_percentages_rel_errors)   
    average_relative_errors_furer_AD=get_average_errors_per_percentage(map_furer_AD_to_percentages_rel_errors)   
    plot(average_relative_errors_furer_OBD,average_relative_errors_furer_AD) 
    print average_relative_errors_furer_OBD
    print average_relative_errors_furer_AD

if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')
  parser.add_argument('-l',help='patterns size level')
  args = parser.parse_args()
  main(args.r,args.l)