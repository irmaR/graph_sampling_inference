'''
Created on Jun 1, 2017

@author: irma
'''

import argparse,os,csv,math






def get_embeddings_and_time_FACT(csv_file):
    embs=[]
    time=[]
    with open(csv_file,'r') as exh:
       print exh
       reader = csv.DictReader(exh)
       for row in reader:
          try:
            embs.append(float(row['emb']))
          except ValueError:
            embs.append(None)
          try:
            time.append(float(row['time']))
          except:
            time.append(None)
    return (embs,time)


def get_embeddings_and_time_exhaustive(csv_file):
    embs=[]
    with open(csv_file) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
          embs.append(float(row['exh_emb']))
    return embs


def get_desired_intervals(FACT_times,interval):
    intervals=[]
    
    for i in FACT_times:
        if i==None:
          intervals.append(None)
        else:
          intervals.append(math.ceil(i/interval)+1)
    
    return intervals

def get_furer_emb_at_interval(csv_furer,desired_intervals):
    counter_row=0
    embs=[]
    with open(csv_furer,'r') as exh:
       reader = csv.DictReader(exh)
       for row in reader:
          if desired_intervals[counter_row]==None:
              embs.append(None)
          else:
              embs.append(float(row['emb_'+str(int(desired_intervals[counter_row]))]))
          counter_row+=1
    return embs

def calculate_relative_errors(array_of_nr_emb_exhaustive,array_of_nr_emb_approachX):
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
        if v1==None or v2==None:
            continue
        nr=abs((float(v1)-float(v2)))/v1
        if not math.isnan(nr):
          rel_errors.append(nr)
        
    #print "MEAN: ",np.mean(rel_errors)
    return rel_errors
        


def fact_vs_furer(pattern_sizes,path_to_csvs,experiment_name,step_percentage):
    FACT_per_pattern_size_embs={}
    FACT_per_pattern_size_time={}
    FURER_per_pattern_size={}
    Exhaustive_per_pattern_size={}
    interval=None
    
    if experiment_name=="y" or experiment_name=="imdb" or experiment_name=="webkb":
        interval=5
    else:
        interval=300
    
    
    for p in pattern_sizes:
        FACT_per_pattern_size_embs[p],FACT_per_pattern_size_time[p]=get_embeddings_and_time_FACT(os.path.join(path_to_csvs,'fact_'+str(p)+".csv"))
        Exhaustive_per_pattern_size[p]=get_embeddings_and_time_exhaustive(os.path.join(path_to_csvs,'exhaustive_'+str(p)+".csv"))
        #get desired intervals for furer
        desired_intervals=get_desired_intervals(FACT_per_pattern_size_time[p],interval)
        FURER_per_pattern_size[p]=get_furer_emb_at_interval(os.path.join(path_to_csvs,'furer_'+str(p)+".csv"),desired_intervals)

    #calculate relative errors
    FURER_relative_errors_per_pattern_size={} 
    FACT_relative_errors_per_pattern_size={} 
    for p in pattern_sizes:
        furer_rel_error=calculate_relative_errors(Exhaustive_per_pattern_size[p],FURER_per_pattern_size[p])
        fact_rel_error=calculate_relative_errors(Exhaustive_per_pattern_size[p],FACT_per_pattern_size_embs[p])
        FURER_relative_errors_per_pattern_size[p]=furer_rel_error
        FACT_relative_errors_per_pattern_size[p]=fact_rel_error

    print FURER_relative_errors_per_pattern_size
    print FACT_relative_errors_per_pattern_size




if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')
  parser.add_argument('-e',help='dblp,y,am,enr')
  parser.add_argument('-l',help='patterns size level')
  
  args = parser.parse_args()
  #
  #main_multiple_pattern_size_plots(args.r,args.l,args.e)
  fact_vs_furer([4,5,6,7,8,9,10],args.r,args.e,10)