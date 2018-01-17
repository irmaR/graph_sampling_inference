'''
Created on Jun 1, 2017

@author: irma
'''

import argparse,os,csv,math
import numpy as np





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
            embs.append(float('nan'))
          try:
            time.append(float(row['time']))
          except:
            time.append(float('nan'))
    return embs,time


def get_embeddings_and_time_exhaustive(csv_file):
    embs=[]
    time=[]
    with open(csv_file) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
          embs.append(float(row['exh_emb']))
          time.append(float(row['time']))
    return embs,time


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
              try:
                embs.append(float(row['emb_'+str(int(desired_intervals[counter_row]))]))
              except ValueError:
                embs.append(None)  
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
        #print float(v1),float(v2)
        nr=abs((float(v1)-float(v2)))/max([v1,v2])
        if not math.isnan(nr):
          rel_errors.append(nr)
       
    #print "MEAN: ",np.mean(rel_errors)
    return rel_errors
        


def fact_vs_furer(pattern_sizes,path_to_csvs,experiment_name,step_percentage):
    FACT_per_pattern_size_embs={}
    FACT_per_pattern_size_time={}
    
    FURER_per_pattern_size={}
    FFURER_per_pattern_size={}
    random_per_pattern_size={}
    
    Exhaustive_per_pattern_size={}
    time_exhaustive_per_pattern_size={}
    interval=None
    
    if experiment_name=="y" or experiment_name=="imdb" or experiment_name=="webkb":
        interval=5
    else:
        interval=300
    
    
    for p in pattern_sizes:
        FACT_per_pattern_size_embs[p],FACT_per_pattern_size_time[p]=get_embeddings_and_time_FACT(os.path.join(path_to_csvs,'fact_'+str(p)+".csv"))
        Exhaustive_per_pattern_size[p],time_exhaustive_per_pattern_size[p]=get_embeddings_and_time_exhaustive(os.path.join(path_to_csvs,'exhaustive_'+str(p)+".csv"))
        #get desired intervals for furer
        desired_intervals=get_desired_intervals(FACT_per_pattern_size_time[p],interval)
        FURER_per_pattern_size[p]=get_furer_emb_at_interval(os.path.join(path_to_csvs,'furer_'+str(p)+".csv"),desired_intervals)
        FFURER_per_pattern_size[p]=get_furer_emb_at_interval(os.path.join(path_to_csvs,'Ffurer_'+str(p)+".csv"),desired_intervals)
        random_per_pattern_size[p]=get_furer_emb_at_interval(os.path.join(path_to_csvs,'random_'+str(p)+".csv"),desired_intervals)

    #calculate relative errors
    FURER_relative_errors_per_pattern_size={} 
    FACT_relative_errors_per_pattern_size={} 
    FFURER_relative_errors_per_pattern_size={} 
    random_relative_errors_per_pattern_size={} 
    
    exhaustive_average_time={}
    FACT_average_time={}
    exhaustive_std_time={}
    FACT_std_time={}
    for p in pattern_sizes:
        furer_rel_error=calculate_relative_errors(Exhaustive_per_pattern_size[p],FURER_per_pattern_size[p])
        fact_rel_error=calculate_relative_errors(Exhaustive_per_pattern_size[p],FACT_per_pattern_size_embs[p])
        ffurer_rel_error=calculate_relative_errors(Exhaustive_per_pattern_size[p],FFURER_per_pattern_size[p])
        random_rel_error=calculate_relative_errors(Exhaustive_per_pattern_size[p],random_per_pattern_size[p])
        FURER_relative_errors_per_pattern_size[p]=furer_rel_error
        FACT_relative_errors_per_pattern_size[p]=fact_rel_error
        FFURER_relative_errors_per_pattern_size[p]=ffurer_rel_error
        random_relative_errors_per_pattern_size[p]=random_rel_error
        exhaustive_average_time[p]=np.nanmean(time_exhaustive_per_pattern_size[p])
        FACT_average_time[p]=np.nanmean(FACT_per_pattern_size_time[p])
        exhaustive_std_time[p]=np.nanstd(time_exhaustive_per_pattern_size[p])
        FACT_std_time[p]=np.nanstd(FACT_per_pattern_size_time[p])
    
    Furer_all_results=[]
    FACT_all_results=[]
    FFURER_all_results=[]
    random_all_results=[]
    for p in pattern_sizes:
        for a in FURER_relative_errors_per_pattern_size[p]:
            Furer_all_results.append(a)
        for a in FACT_relative_errors_per_pattern_size[p]:
            FACT_all_results.append(a)
        for a in FFURER_relative_errors_per_pattern_size[p]:
            FFURER_all_results.append(a)
        for a in random_relative_errors_per_pattern_size[p]:
            random_all_results.append(a)
    FURER_Average=np.mean(Furer_all_results)
    FURER_Stdev=np.std(Furer_all_results)
    FACT_average=np.mean(FACT_all_results)
    FACT_stdev=np.std(FACT_all_results)
    random_average=np.mean(random_all_results)
    random_stdev=np.std(random_all_results)
    FFURER_average=np.mean(FFURER_all_results)
    FFFURER_stdev=np.std(FFURER_all_results)
    
    print FURER_Average,FURER_Stdev
    print FACT_average,FACT_stdev
    
    print FFURER_average,FFFURER_stdev
    print random_average,random_stdev
    
    FK_OBD_avg=[]
    FK_AD_avg=[]
    FACT_avg=[]
    random_avg=[]
    
    FK_OBD_row=""
    FK_AD_row=""
    random_row=""
    FACT_row=""
    
    for i in pattern_sizes:
        klds_FK_OBD=FURER_relative_errors_per_pattern_size[i]
        #std_FK_OBD=FK_OBD_per_pattern_size_std[i]
        klds_FK_AD=FFURER_relative_errors_per_pattern_size[i]
        #std_FK_AD=FK_AD_per_pattern_size_std[i]
        klds_FK_random=random_relative_errors_per_pattern_size[i]
        klds_FACT=FACT_relative_errors_per_pattern_size[i]

        FK_OBD_avg.extend(klds_FK_OBD)
        FK_AD_avg.extend(klds_FK_AD)
        FACT_avg.extend(klds_FACT)
        random_avg.extend(klds_FK_random)
        FK_OBD_row+=str(round(np.nanmean(klds_FK_OBD),3))+"&"
        FK_AD_row+=str(round(np.nanmean(klds_FK_AD),3))+"&"
        random_row+=str(round(np.nanmean(klds_FK_random),3))+"&"
        FACT_row+=str(round(np.nanmean(klds_FACT),3))+"&"
        
    print FK_OBD_row+str(round(np.nanmean(FK_OBD_avg),3)) 
    print FK_AD_row+str(round(np.nanmean(FK_AD_avg),3)) 
    print FACT_row+str(round(np.nanmean(FACT_avg),3)) 
    print random_row+str(round(np.nanmean(random_avg),3)) 
    print "Averages:"
    print np.nanmean(FK_OBD_avg) 
    print np.nanmean(FK_AD_avg) 
    print np.nanmean(random_avg) 
    print "Average times"
    output_str1=""
    output_str2=""
    #for p in pattern_sizes:
    #    output_str1+=str(format(exhaustive_average_time[p],'.2f'))+"&"+str(format(exhaustive_std_time[p],'.2f'))+"&"
    #    output_str2+=str(format(FACT_average_time[p],'.2f'))+"&"+str(format(FACT_std_time[p],'.2f'))+"&"
    all_exh=[]
    all_fact=[]
    for p in pattern_sizes:
        output_str1+=str(format(exhaustive_average_time[p],'.2f'))+"&"
        output_str2+=str(format(FACT_average_time[p],'.2f'))+"&"
        all_exh.append(exhaustive_average_time[p])
        all_fact.append(FACT_average_time[p])
    
    
    print output_str1+str(format(np.nanmean(all_exh),'.2f'))
    print output_str2+str(format(np.nanmean(all_fact),'.2f'))
    
    
    
        
        




if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')
  parser.add_argument('-e',help='dblp,y,am,enr')
  parser.add_argument('-l',help='patterns size level')
  
  args = parser.parse_args()
  #
  #main_multiple_pattern_size_plots(args.r,args.l,args.e)
  fact_vs_furer([4,5,6,7,8,9,10],args.r,args.e,10)