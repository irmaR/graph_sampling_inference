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

def get_eligible_patterns_approach(level,map_exhaustive_patterns,appr):
    eligible_patterns=[]
    interval=10
    with open(appr) as approach:
       reader1 = csv.DictReader(approach)
       for row in reader1:
            name_of_pattern=row["pattern_name"].split("/")[-2]
            if no_obdecomp(level,row["OBD"]):
                #print row["pattern_name"]
                eligible_patterns.append(name_of_pattern)
    #print "level: ",level,"nr eligible: ",len(eligible_patterns)
    return eligible_patterns

def get_eligible_patterns_approach_with_obd(level,map_exhaustive_patterns,appr):
    eligible_patterns=[]
    interval=10
    with open(appr) as approach:
       reader1 = csv.DictReader(approach)
       for row in reader1:
            name_of_pattern=row["pattern_name"].split("/")[-2]
            if not no_obdecomp(level,row["OBD"]):
                eligible_patterns.append(name_of_pattern)
    #print "level: ",level,"nr eligible: ",len(eligible_patterns)
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
    
    if exp=="dblp":
        intervals=get_intervals(runtime_exh,"min",step_percentage)
    else:
        intervals=get_intervals(runtime_exh,"sec",step_percentage)
    #print "INTERVALS: ",intervals
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
    #print "EMBS: ",embeddings_furer 
    #print "EXH: ",emb_exh
    #print "REL ERROR: ",calculate_relative_errors_exhaustive([emb_exh] * len(embeddings_furer),embeddings_furer)
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
        rel_error=get_relative_error(emb,emb_exh)
        embeddings_furer.append(rel_error)
       
    #print "EMBS: ",embeddings_furer,len(embeddings_furer)

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
         nr_emb_exhaustive=float(row["exh_emb"])
         if nr_emb_exhaustive==0:
             continue
         name_of_patterns=row["pattern_name"].split("/")[-2]
         map_runtimes[name_of_patterns]=float(row["time"])
         map_embs[name_of_patterns]=nr_emb_exhaustive
    return map_runtimes,map_embs



def get_runtimes_embeddings_last_furer(path_to_furer_csv,exp):
    map_runtimes={}
    map_embs={}
    if exp=="dblp" or exp=="am" or exp=="enr":
        total_time_sec=36000
    else:
        total_time_sec=3600
    
    with open(path_to_furer_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
         #if(not(row["timeout"]=="False")):
         #    continue
         try:
           nr_embfinal=float(row["emb_120"])
         except ValueError:
             continue
         
         if nr_embfinal==0:
             continue
         name_of_patterns=row["pattern_name"].split("/")[-2]
         map_runtimes[name_of_patterns]=total_time_sec;
         map_embs[name_of_patterns]=nr_embfinal
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

def main_multiple_pattern_size_plots(pattern_sizes,path_to_csv,exp,step_percentage,version):
       map_furer_percentages_no_obd={}
       map_ffurer_percentages_no_obd={}
       map_random_percentages_no_obd={}
       
       map_furer_percentages_obd={}
       map_ffurer_percentages_obd={}
       map_random_percentages_obd={}
       
       eligible_patterns=[]
       map_final_embs={}
       map_runtimes_seconds={}
       
       for level in pattern_sizes: 
          #
          if version==2:
             map_runtimes_seconds1,map_final_embs1=get_runtimes_embeddings_last_furer(os.path.join(path_to_csv,'furer_'+str(level)+".csv"),exp)
          else:
             map_runtimes_seconds1,map_final_embs1=get_runtimes_embeddings_exhaustive(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"),exp)
          els_flat_obd=get_eligible_patterns_approach(int(level),map_final_embs,os.path.join(path_to_csv,'furer_'+str(level)+".csv"))
          els_obd=get_eligible_patterns_approach_with_obd(int(level),map_final_embs,os.path.join(path_to_csv,'furer_'+str(level)+".csv"))
          print "OBD eligible: ",len(els_obd)
          print "AD eligible: ",len(els_flat_obd)
          print map_final_embs1
          for e in els_flat_obd:
              if e in map_final_embs1:
                map_final_embs[e]=map_final_embs1[e]
                map_runtimes_seconds[e]=map_runtimes_seconds1[e]
                map_furer_percentages_no_obd[e]=get_results_rel_errors(e,map_runtimes_seconds[e],map_final_embs[e],os.path.join(path_to_csv,'furer_'+str(level)+".csv"),exp,step_percentage)
              #map_ffurer_percentages_no_obd[e]=get_results_rel_errors(e,map_runtimes_seconds[e],map_final_embs[e],os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"),exp,step_percentage)
              #map_random_percentages_no_obd[e]=get_results_rel_errors(e,map_runtimes_seconds[e],map_final_embs[e],os.path.join(path_to_csv,'random_'+str(level)+".csv"),exp,step_percentage)


          for e in els_obd:
              if e not in map_final_embs1:
                  continue
              map_final_embs[e]=map_final_embs1[e]
              map_runtimes_seconds[e]=map_runtimes_seconds1[e]
              map_furer_percentages_obd[e]=get_results_rel_errors(e,map_runtimes_seconds[e],map_final_embs[e],os.path.join(path_to_csv,'furer_'+str(level)+".csv"),exp,step_percentage)
              #map_ffurer_percentages_obd[e]=get_results_rel_errors(e,map_runtimes_seconds[e],map_final_embs[e],os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"),exp,step_percentage)
              #map_random_percentages_obd[e]=get_results_rel_errors(e,map_runtimes_seconds[e],map_final_embs[e],os.path.join(path_to_csv,'random_'+str(level)+".csv"),exp,step_percentage)

          #eligible_patterns.extend(get_eligible_patterns_approach(int(level),map_final_embs,os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv")))
      
       average_relative_errors_furer_OBD=get_average_errors_per_percentage(map_furer_percentages_obd,step_percentage)   
       average_relative_errors_furer_AD=get_average_errors_per_percentage(map_furer_percentages_no_obd,step_percentage)   
       #average_relative_errors_random=get_average_errors_per_percentage(map_random_percentages,step_percentage)   
       stdev_furer_OBD=get_stdev_per_percentage(map_furer_percentages_no_obd,step_percentage)
       stdev_furer_AD=get_stdev_per_percentage(map_furer_percentages_obd,step_percentage)
       #stdev_random=get_stdev_per_percentage(map_random_percentages,step_percentage)
       
       x=xrange(5,605,15)
       plt.figure()
       #plt.yscale('log')
       for t in xrange(0,41):
         if not t % 5==0:
             stdev_furer_AD[t]=0
             stdev_furer_OBD[t-1]=0   
       (_, caps, _)=plt.errorbar(x, average_relative_errors_furer_OBD, color='green',yerr=stdev_furer_OBD,linewidth=3.5,elinewidth=2.5)
       (_, caps, _)=plt.errorbar(x, average_relative_errors_furer_AD, color='black',yerr=stdev_furer_AD,linewidth=3.5,elinewidth=2.5)
       plt.legend(['FK-OBD', 'FK-No-OBD'],loc = 'upper right',prop={'size':35})
       plt.ylabel('Avg_RelErr',size=25)
       plt.xlabel('Runtime (minutes)',size=25)
       plt.tick_params(axis='both', which='major', labelsize=25)
       plt.ylim([0,1])
       #plt.title("DBLP")   
       plt.tight_layout()
       plt.show()







if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')
  parser.add_argument('-e',help='dblp or y')
  parser.add_argument('-l',help='patterns size level')
  
  args = parser.parse_args()
  #
  main_multiple_pattern_size_plots([8],args.r,args.e,10,2)
