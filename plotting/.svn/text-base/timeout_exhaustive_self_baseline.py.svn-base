'''
Created on Mar 25, 2016

@author: irma
'''
'''
Created on Mar 25, 2016

@author: irma
'''
import argparse,csv,os,ast,math
import numpy as np
import matplotlib.pyplot as plt

def get_relative_error(N,M):
    return abs((float(N)-float(M)))/M     
      
def no_obdecomp(n,OBD):
    obd=ast.literal_eval(OBD)
    if len(obd)==n:
        return True
    else:
        return False

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

def get_eligible_patterns_approach(level,map_exhaustive_patterns,appr,exp):
    eligible_patterns=[]
    interval=10
    if exp=="dblp" or exp=="am" or exp=="enr":
        total_time=36000
    else:
        total_time=3600
    with open(appr) as approach:
       reader1 = csv.DictReader(approach)
       for row in reader1:
            name_of_pattern=row["pattern_name"].split("/")[-2]
            if row["timeout"]==str(True):
                if name_of_pattern in map_exhaustive_patterns.keys():
                   eligible_patterns.append(name_of_pattern)

    print "level: ",level,"nr eligible: ",len(eligible_patterns)
    return eligible_patterns



def get_intervals(N,time_unit,step_percentage):
    intervals_seconds=[]
    if time_unit=="min":
       N=N/60
    
    for x in xrange(0,(100+step_percentage),step_percentage):
        intervals_seconds.append(int(((N*x)/100)/5))
    return intervals_seconds

def get_results_percentages(pattern_name,runtime_exh,emb_exh,furer_csv,exp,step_percentage):
    relative_errors=[]
    row_of_interest={}
    with open(furer_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
         name_of_pattern=row["pattern_name"].split("/")[-2]
         if name_of_pattern==pattern_name:
             row_of_interest=row
             break
    
    if exp=="dblp" or exp=="am" or exp=="enr":
        intervals=get_intervals(runtime_exh,"min",step_percentage)
    else:
        intervals=get_intervals(runtime_exh,"sec",step_percentage)
    embeddings_furer=[]
    for t in intervals:
        if t==0:
            t=1
        if t>120:
            t=120
        
        avg_emb=0
        counter=0
        for i in xrange(1,t+1):
            counter+=1
            column_name="emb_"+str(i)
            try:
              avg_emb+=float(row[column_name])
            except:
                avg_emb+=0
        avg_emb=avg_emb/float(counter)
        try:
           embeddings_furer.append(avg_emb)
        except:
           embeddings_furer.append(0)
    print "EMBS: ",embeddings_furer 
    print "EXH: ",emb_exh
    print "REL ERROR: ",calculate_relative_errors_exhaustive([emb_exh] * len(embeddings_furer),embeddings_furer)
    return calculate_relative_errors_exhaustive([emb_exh] * len(embeddings_furer),embeddings_furer)


def get_results_rel_errors(pattern_name,runtime_exh,emb_exh,furer_csv,exp,step_percentage):
    relative_errors=[]
    row_of_interest={}
    with open(furer_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader: 
         name_of_pattern=row["pattern_name"].split("/")[-2]
         if name_of_pattern==pattern_name:
             row_of_interest=row
             break
    avg_emb=0
    counter=0
    embeddings_furer=[]
    for i in xrange(0,121,3):
        if i==0:
            i=1
        counter+=1
        column_name="emb_"+str(i)
        try:
          emb=float(row[column_name])
        except:
            emb=0
        if emb_exh==0:
            emb_exh=1
        rel_error=get_relative_error(emb,emb_exh)
        embeddings_furer.append(rel_error)
    return embeddings_furer

def get_runtimes_embeddings_exhaustive(path_to_exhaustive_csv,exp):
    map_runtimes={}
    map_embs={}
    if exp=="dblp" or exp=="am" or exp=="enr":
        total_time_sec=36000
    else:
        total_time_sec=3600
    
    with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
         #if(not(row["timeout"]=="False")):
         #    continue
         if(not(row["exh_emb"])):
             continue
         nr_emb_exhaustive=float(row["exh_emb"])
         name_of_patterns=row["pattern_name"].split("/")[-2]
         map_runtimes[name_of_patterns]=float(row["time"])
         map_embs[name_of_patterns]=nr_emb_exhaustive
    return map_runtimes,map_embs

def get_runtimes_embeddings_furer(path_to_exhaustive_csv,exp):
    map_runtimes={}
    map_embs={}
    if exp=="dblp" or exp=="am" or exp=="enr":
        total_time_sec=36000
    else:
        total_time_sec=3600
    
    with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
         if not row["emb_120"]:
             continue
         nr_emb_exhaustive=float(row["emb_120"])
         name_of_patterns=row["pattern_name"].split("/")[-2]
         map_runtimes[name_of_patterns]=float(36000)
         map_embs[name_of_patterns]=nr_emb_exhaustive
    return map_runtimes,map_embs


def get_average_errors_per_percentage(map_relative_errors,step_percentage):
    average_rel_errors=[]
    for i in xrange(0,40):
        sum=0
        c=0
        for patt in map_relative_errors.keys():
            c+=1
            sum+=map_relative_errors[patt][i]
        if float(c)==0.0:
            return []
        average_rel_errors.append(sum/float(c))
    return average_rel_errors

def get_stdev_per_percentage(map_relative_errors,step_percentage):
    stds=[]
    for i in xrange(0,40):
        values=[]
        for patt in map_relative_errors.keys():
            values.append(map_relative_errors[patt][i])
        stds.append(np.std(values))
    return stds

def main_multiple_pattern_size_plots(pattern_sizes,path_to_csv,exp,step_percentage):
       map_furer_percentages={}
       map_ffurer_percentages={}
       map_random_percentages={}
       map_exh_percentages={}
       eligible_patterns=[]
       map_final_embs={}
       map_runtimes_seconds={}
       
       for level in pattern_sizes: 
          #map_runtimes_seconds1,map_final_embs1=get_runtimes_embeddings_exhaustive(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"),exp)
          map_runtimes_seconds_exh,map_final_embs_exh=get_runtimes_embeddings_furer(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"),exp)
          map_runtimes_seconds_furer,map_final_embs_furer=get_runtimes_embeddings_furer(os.path.join(path_to_csv,'furer_'+str(level)+".csv"),exp)
          map_runtimes_seconds_ffurer,map_final_embs_ffurer=get_runtimes_embeddings_furer(os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"),exp)
          map_runtimes_seconds_random,map_final_embs_random=get_runtimes_embeddings_furer(os.path.join(path_to_csv,'random_'+str(level)+".csv"),exp)
          els=get_eligible_patterns_approach(int(level),map_final_embs_exh,os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"),exp)
 
          for e in els:
              if e in map_final_embs_furer and e in map_final_embs_ffurer and e in map_final_embs_random:
                  map_furer_percentages[e]=get_results_rel_errors(e,map_runtimes_seconds_furer[e],map_final_embs_furer[e],os.path.join(path_to_csv,'furer_'+str(level)+".csv"),exp,step_percentage)
                  map_exh_percentages[e]=get_results_rel_errors(e,map_runtimes_seconds_exh[e],map_final_embs_exh[e],os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"),exp,step_percentage)
                  map_ffurer_percentages[e]=get_results_rel_errors(e,map_runtimes_seconds_ffurer[e],map_final_embs_ffurer[e],os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"),exp,step_percentage)
                  map_random_percentages[e]=get_results_rel_errors(e,map_runtimes_seconds_random[e],map_final_embs_random[e],os.path.join(path_to_csv,'random_'+str(level)+".csv"),exp,step_percentage)

          #eligible_patterns.extend(get_eligible_patterns_approach(int(level),map_final_embs,os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"),exp))
       
       average_relative_errors_furer_OBD=get_average_errors_per_percentage(map_furer_percentages,step_percentage)   
       average_relative_errors_furer_AD=get_average_errors_per_percentage(map_ffurer_percentages,step_percentage)   
       average_relative_errors_random=get_average_errors_per_percentage(map_random_percentages,step_percentage)  
       average_relative_errors_exh=get_average_errors_per_percentage(map_exh_percentages,step_percentage)   

       stdev_furer_OBD=get_stdev_per_percentage(map_furer_percentages,step_percentage)
       stdev_furer_AD=get_stdev_per_percentage(map_ffurer_percentages,step_percentage)
       stdev_random=get_stdev_per_percentage(map_random_percentages,step_percentage)
       stdev_exh=get_stdev_per_percentage(map_exh_percentages,step_percentage)
       
       
       
       x=xrange(5,605,15)
       plt.figure()
       plt.yscale('symlog')
       stdev_furer_OBD_log=[]
       stdev_furer_AD_log=[]
       stdev_random_log=[]
       stdev_exh_log=[]
       for t in xrange(0,40):
             #print t,len(stdev_furer_OBD),len(average_relative_errors_furer_OBD)
             #print stdev_furer_OBD[t],average_relative_errors_furer_OBD[t]
             stdev_furer_OBD_log.append(stdev_furer_OBD[t]/average_relative_errors_furer_OBD[t])
             stdev_furer_AD_log.append(stdev_furer_AD[t]/average_relative_errors_furer_AD[t])
             #stdev_random[t]=stdev_random[t]/average_relative_errors_random[t]
             stdev_exh_log.append(stdev_exh[t]/average_relative_errors_exh[t])
             if not t % 5==0:
                 stdev_furer_AD[t]=0
                 stdev_furer_OBD[t]=0
                 stdev_random[t]=0
                 stdev_exh[t]=0
      
       #print average_relative_errors_furer_AD
       plt.errorbar(x, average_relative_errors_furer_OBD, color='green',yerr=stdev_furer_OBD,linewidth=3.5,elinewidth=2)
       plt.errorbar(x, average_relative_errors_furer_AD, color='black',yerr=stdev_furer_AD,linewidth=3.5,elinewidth=2)
       plt.errorbar(x, average_relative_errors_random, color='red',linewidth=3.5,elinewidth=2)
       plt.errorbar(x, average_relative_errors_exh, color='m',yerr=stdev_furer_AD,linewidth=3.5,elinewidth=2)
       #for cap in caps:
       #    print cap
       #    cap.set_markeredgewidth(2)
       #plt.legend(['FK-OBD', 'FK-AD','Random','Exhaustive'],loc = 'lower right',prop={'size':30})
       #plt.legend(['Furer-AD','Random','Exhaustive'],loc = 'upper right',prop={'size':20})
       #plt.legend(['Furer-OBD','Random','Exhaustive'],loc = 'upper right',prop={'size':20})
       #plt.legend(['Furer-OBD','Furer-AD','Exhaustive'],loc = 'upper right',prop={'size':20})
       if exp=="y":
           experiment_label="YEAST"
       if exp=="fb":
           experiment_label="FACEBOOK"
       if exp=="am":
           experiment_label="AMAZON"
       if exp=="enr":
           experiment_label="ENRON"
       if exp=="fb":
           experiment_label="FACEBOOK"
       plt.ylabel('log Avg_RelErr',size=30)
       plt.xlabel('Runtime (seconds)',size=30)
       plt.tick_params(axis='both', which='major', labelsize=30)
       plt.title(experiment_label,size=30)   
       plt.tight_layout()
       plt.show()



if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')
  parser.add_argument('-e',help='dblp,y,am,enr')
  parser.add_argument('-l',help='patterns size level')
  
  args = parser.parse_args()
  #
  #main_multiple_pattern_size_plots(args.r,args.l,args.e)
  main_multiple_pattern_size_plots([4,5,6,7,8,9,10],args.r,args.e,10)
  #main_multiple_pattern_size_plots_one_plot([0],args.r,args.e,10,False)