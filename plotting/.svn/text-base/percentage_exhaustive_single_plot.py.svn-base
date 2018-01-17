'''
Created on Mar 8, 2016

@author: irma
'''
'''
Created on Mar 8, 2016

@author: irma
'''
import argparse,os,csv,math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd




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


def get_runtimes_embeddings_exhaustive(path_to_exhaustive_csv,exp):
    print "Getting exhaustive runtimes..."
    map_runtimes={}
    map_embs={}
    if exp=="dblp" or exp=="am":
        total_time_sec=36000
    if exp=="y":
        total_time_sec=3600
    counter_row=0
    timeout=0
    with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
         print row["timeout"],row["exh_emb"]
         if(not(row["timeout"]=="False")):
             continue
         if(not(row["exh_emb"])):
             continue
         print float(row["time"]),float((total_time_sec*1)/100)
         #if(float(row["time"])<=float((total_time_sec*1)/100)):
         #    continue
         nr_emb_exhaustive=float(row["exh_emb"])
         name_of_patterns=row["pattern_name"].split("/")[-2]
         map_runtimes[name_of_patterns]=float(row["time"])
         map_embs[name_of_patterns]=nr_emb_exhaustive
    print "Number of eligible patterns by exhaustive: ",len(map_embs.keys())
    return map_runtimes,map_embs


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
    #print "emb exh: ",emb_exh
    embeddings_furer=[]
    for t in intervals:
        if t==0:
            t=1
        if t>120:
            t=120
        
        avg_emb=0
        counter=0
        for i in xrange(1,t+1):
            
            column_name="emb_"+str(i)
            
            try:
              avg_emb+=float(row[column_name])
              counter+=1
            except:
                print "Warning no entry"
                continue
        if counter>0:
          avg_emb=avg_emb/float(counter)
        try:
           embeddings_furer.append(avg_emb)
        except:
           embeddings_furer.append(0)
    print "EMBS: ",embeddings_furer 
    print "EXH: ",emb_exh
    return calculate_relative_errors_exhaustive([emb_exh] * len(embeddings_furer),embeddings_furer)

def collect_all_observations_exhaustive(path_to_exhaustive_csv):
    observations=[]
    with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
           observations.append(int(row["nr_observations"]))
    return observations

def collect_all_max_degrees(path_to_exhaustive_csv):
    observations=[]
    with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
           observations.append(float(row["max_degree"]))
    return observations

def plot(furer_OBD_results,furer_AD_results):
   fig = plt.figure()
   x=xrange(0,110,1)
   print "OBD: ",furer_OBD_results
   print "AD: ",furer_AD_results
   plt.plot(x, furer_OBD_results)
   plt.plot(x, furer_AD_results)
    
   plt.xlabel('time (s)')
   plt.ylabel('voltage (mV)')
   plt.title('About as simple as it gets, folks')
   plt.grid(True)
   plt.savefig("test.png")
   plt.legend(['Furer-OBD', 'Furer-AD'], loc='upper left')
   plt.show()

def get_average_errors_per_percentage(map_relative_errors,step_percentage):
    average_rel_errors=[]
    for i in xrange(0,int((100+step_percentage)/step_percentage)):
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
    for i in xrange(0,int((100+step_percentage)/step_percentage)):
        values=[]
        for patt in map_relative_errors.keys():
            values.append(map_relative_errors[patt][i])
        #print "STD OF VALS: ",values,np.std(values)
        stds.append(np.std(values))
    return stds

def divide_patterns_based_on(path_to_exhaustive_csv,bins,column):
     res={}
     with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
            name_of_pattern=row["pattern_name"].split("/")[-2]
            try:
              nr_obs=int(row[column])
            except:
              nr_obs=float(row[column])  
            exhDiscretized= pd.cut(np.array([nr_obs]),bins,include_lowest=True,labels=["small","medium","large"])
            res[name_of_pattern]=exhDiscretized[0]
     return res  

def main_2(path_to_csv,level,exp):
    all_observations_exhaustive=collect_all_observations_exhaustive(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"))
    arrayDiscretized,bins=pd.qcut(np.array(all_observations_exhaustive), 3,retbins=True, labels=["small","medium","large"])
    #print bins
    pattern_map=divide_patterns_based_on(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"),bins,"nr_observations")
    map_runtimes_seconds,map_final_embs=get_runtimes_embeddings_exhaustive(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"))
    results_OBD={}
    results_AD={}
    results_OBD["small"]={}
    results_OBD["medium"]={}
    results_OBD["large"]={}
    results_AD["small"]={}
    results_AD["medium"]={}
    results_AD["large"]={}
    for pattern in map_runtimes_seconds.keys():
        tmp=results_OBD[pattern_map[pattern]]
        tmp[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'furer_'+str(level)+".csv"),exp)
        tmp1=results_AD[pattern_map[pattern]]
        tmp1[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"),exp)
    
    # Three subplots sharing both x/y axes
    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)
    x=xrange(0,110,10)
    ax1.plot(x, get_average_errors_per_percentage(results_OBD["small"]),color='r')
    #ax1.errorbar(x, get_average_errors_per_percentage(results_OBD["small"]),yerr=get_stdev_per_percentage(results_OBD["small"]), fmt='o',color='r')
    ax1.plot(x, get_average_errors_per_percentage(results_AD["small"]),color='b')
    #ax1.errorbar(x, get_average_errors_per_percentage(results_AD["small"]),yerr=get_stdev_per_percentage(results_AD["small"]), fmt='o',color='b')
    #print "hm: small ",get_average_errors_per_percentage(results_OBD["small"])
    #print "hm:small ",get_average_errors_per_percentage(results_AD["small"])
    plt.legend(loc="upper left", bbox_to_anchor=[0, 1],
           ncol=2, shadow=True, title="Legend", fancybox=True)
    ax1.legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)
    
    #print "hm:medium ",get_average_errors_per_percentage(results_OBD["medium"])
    #print "hm:medium ",get_average_errors_per_percentage(results_AD["medium"])
    ax2.plot(x, get_average_errors_per_percentage(results_OBD["medium"]),color='r')
    #ax2.errorbar(x, get_average_errors_per_percentage(results_OBD["medium"]),yerr=get_stdev_per_percentage(results_OBD["medium"]), fmt='o',color='r')
    ax2.plot(x, get_average_errors_per_percentage(results_AD["medium"]),color='b')
    #ax2.errorbar(x, get_average_errors_per_percentage(results_AD["medium"]),yerr=get_stdev_per_percentage(results_AD["medium"]), fmt='o',color='b')
    
    ax3.plot(x, get_average_errors_per_percentage(results_OBD["large"]),color='r')
    #print "hm:large ",get_average_errors_per_percentage(results_OBD["large"])
    #print "hm:large ",get_average_errors_per_percentage(results_AD["large"])
    
    #ax3.errorbar(x, get_average_errors_per_percentage(results_OBD["large"]),yerr=get_stdev_per_percentage(results_OBD["large"]), fmt='o',color='r')
    ax3.plot(x,  get_average_errors_per_percentage(results_AD["large"]),color='b')
    #ax3.errorbar(x, get_average_errors_per_percentage(results_AD["large"]),yerr=get_stdev_per_percentage(results_AD["large"]), fmt='o',color='b')
    # Fine-tune figure; make subplots close to each other and hide x ticks for
    # all but bottom plot.
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)   
    plt.show()

def get_relative_error(N,M):
    return abs((float(N)-float(M)))/M
    
def get_eligible_patterns(map_exhaustive_patterns,ffurer_csv,furer_csv):
    eligible_patterns=[]
    with open(furer_csv) as furer, open(ffurer_csv) as ffurer:
       reader1 = csv.DictReader(furer)
       reader2 = csv.DictReader(ffurer)
       for row in reader1:
            name_of_pattern=row["pattern_name"].split("/")[-2]
            if not name_of_pattern in map_exhaustive_patterns.keys():
                continue
            if row["emb_1"]=="":
                continue
            emb_1=float(row["emb_1"])            
            rel_error_furer=get_relative_error(emb_1,map_exhaustive_patterns[name_of_pattern])
            #print "REL ERROR FURER: ",name_of_pattern,rel_error_furer
            if name_of_pattern in map_exhaustive_patterns.keys() and not rel_error_furer*100<=10:
                for row1 in reader2:
                    name_of_pattern1=row1["pattern_name"].split("/")[-2]
                    if name_of_pattern1!=name_of_pattern:
                        continue
                    if row1["emb_1"]=="":
                       continue
                    emb_2=float(row1["emb_1"])
                rel_error_ffurer=get_relative_error(emb_2,map_exhaustive_patterns[name_of_pattern])
                if not rel_error_ffurer*100<=10:
                      eligible_patterns.append(name_of_pattern)
    print "Nr eligible patterns: ",len(eligible_patterns)
    return eligible_patterns

def get_eligible_patterns_approach(map_exhaustive_patterns,appr):
    eligible_patterns=[]
    interval=10
    with open(appr) as approach:
       reader1 = csv.DictReader(approach)
       for row in reader1:
            name_of_pattern=row["pattern_name"].split("/")[-2]
            print name_of_pattern
            if row["emb_"+str(interval)]=="":
                continue
            if not name_of_pattern in map_exhaustive_patterns.keys():
                continue
            emb_1=float(row["emb_"+str(interval)])            
            rel_error_furer=get_relative_error(emb_1,map_exhaustive_patterns[name_of_pattern])
            #print rel_error_furer,rel_error_furer*100,not rel_error_furer*100<=5,name_of_pattern in map_exhaustive_patterns.keys()
            #print "REL ERROR FURER: ",name_of_pattern,rel_error_furer
            print rel_error_furer
            if name_of_pattern in map_exhaustive_patterns.keys() and not rel_error_furer*100<=5:
               eligible_patterns.append(name_of_pattern)
    print "Nr eligible patterns: ",len(eligible_patterns)
    return eligible_patterns

def main_multiple_pattern_size_plots(pattern_sizes,path_to_csv,exp,step_percentage,m,n,eligibility=True):
    axis_tuple=()
    limit=(100+step_percentage)
    x=xrange(0,limit,step_percentage)
    f, axis = plt.subplots(nrows=m, ncols=n, sharex=True, sharey=False)  
    print axis 
    if exp=="dblp":
      plt.title("DBLP")
    elif exp=="y":
      plt.title("YEAST")
    if exp=="am":
      plt.title("AMAZON")
    axis_counter=0
    
    pattern_counter=0
    for i in xrange(0,m):
        for j in xrange(0,n):
         if pattern_counter>=len(pattern_sizes):
             break
         level=pattern_sizes[pattern_counter]
         pattern_counter+=1
         print "Processing level ",level
         #print i,j
         ax = axis[i][j]
         ax.tick_params(labelsize=15)
         if j==0:
            ax.set_ylabel('Avg_RelEr',size=20)
         if i==3:
            ax.set_xlabel('% exhaustive runtime',size=18)
         map_furer_OBD_to_percentages_rel_errors={}
         map_furer_AD_to_percentages_rel_errors={}
         map_runtimes_seconds,map_final_embs=get_runtimes_embeddings_exhaustive(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"),exp)
         
         if eligibility:
            eligble_patterns=get_eligible_patterns_approach(map_final_embs,os.path.join(path_to_csv,'Ffurer_order_random_'+str(level)+".csv"))
         else:
             eligble_patterns=map_final_embs.keys()
         print "Number of eligible patterns:",len(eligble_patterns)
         
         for pattern in map_runtimes_seconds.keys():
            if pattern in eligble_patterns:
                #print "PATTERN: ",pattern
                print "furer"
                map_furer_OBD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'furer_'+str(level)+".csv"),exp,step_percentage)
                print "Ffurer"
                map_furer_AD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'Ffurer_order_random_'+str(level)+".csv"),exp,step_percentage)

         print map_furer_OBD_to_percentages_rel_errors
         print map_furer_AD_to_percentages_rel_errors
         average_relative_errors_furer_OBD=get_average_errors_per_percentage(map_furer_OBD_to_percentages_rel_errors,step_percentage)   
         average_relative_errors_furer_AD=get_average_errors_per_percentage(map_furer_AD_to_percentages_rel_errors,step_percentage)   
         
         stdev_furer_OBD=get_stdev_per_percentage(map_furer_OBD_to_percentages_rel_errors,step_percentage)
         stdev_furer_AD=get_stdev_per_percentage(map_furer_AD_to_percentages_rel_errors,step_percentage)
         
         
         #leave stdevs after each 10 iterations, the rest is zero
         for t in xrange(0,(100+step_percentage),step_percentage):
             if not t % 10==0:
                 stdev_furer_AD[t]=0
                 stdev_furer_OBD[t]=0
         
         print "OBD FURER: ",average_relative_errors_furer_OBD
         print "OBD FFURER: ",average_relative_errors_furer_AD

         print "STD OBD ",stdev_furer_OBD,len(stdev_furer_OBD)
         print "STD AD ",stdev_furer_AD,len(stdev_furer_AD)
         #print "AD:",average_relative_errors_furer_AD
         ax.set_title("Level: "+str(level))
         if average_relative_errors_furer_AD==[] or average_relative_errors_furer_AD==[]:
             continue
         print len(average_relative_errors_furer_OBD),len(stdev_furer_OBD)
         print len(x),len(average_relative_errors_furer_OBD)
         ax.plot(x,average_relative_errors_furer_OBD,color='blue',linewidth=3.0)
         ax.plot(x,average_relative_errors_furer_AD,color='red',linewidth=3.0)
         ax.errorbar(x, average_relative_errors_furer_OBD,yerr=stdev_furer_OBD, fmt='o',color='blue',linewidth=2)
         ax.errorbar(x, average_relative_errors_furer_AD,yerr=stdev_furer_AD, fmt='o',color='red',linewidth=2.0)
         
         #ax.set_yscale('log')
         #ax.set_xscale('log')
         axis_counter+=1
    
    plt.legend(['FK-OBD', 'FK-AD'],loc = 'upper right', bbox_to_anchor = (0,0.5,1.0,0.5),prop={'size':16})
    f.tight_layout()
    
    f.subplots_adjust(wspace=0.3)
    f.subplots_adjust(hspace=0.3)
    plt.show()

    
    
def main_based_on_max_degree(path_to_csv,level,exp):
    all_observations_exhaustive=collect_all_max_degrees(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"))
    arrayDiscretized,bins=pd.qcut(np.array(all_observations_exhaustive), 3,retbins=True, labels=["small","medium","large"])
    pattern_map=divide_patterns_based_on(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"),bins,"max_degree")
    map_runtimes_seconds,map_final_embs=get_runtimes_embeddings_exhaustive(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"))
    results_OBD={}
    results_AD={}
    results_OBD["small"]={}
    results_OBD["medium"]={}
    results_OBD["large"]={}
    results_AD["small"]={}
    results_AD["medium"]={}
    results_AD["large"]={}
    for pattern in map_runtimes_seconds.keys():
        tmp=results_OBD[pattern_map[pattern]]
        tmp[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'furer_'+str(level)+".csv"),exp)
        tmp1=results_AD[pattern_map[pattern]]
        tmp1[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"),exp)
        

    # Three subplots sharing both x/y axes
    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)
    x=xrange(0,110,10)
    ax1.plot(x, get_average_errors_per_percentage(results_OBD["small"]),color='r')
    ax1.errorbar(x, get_average_errors_per_percentage(results_OBD["small"]),yerr=get_stdev_per_percentage(results_OBD["small"]), fmt='o',color='r')
    ax1.plot(x, get_average_errors_per_percentage(results_AD["small"]),color='b')
    ax1.errorbar(x, get_average_errors_per_percentage(results_AD["small"]),yerr=get_stdev_per_percentage(results_AD["small"]), fmt='o',color='b')

    plt.legend(loc="upper left", bbox_to_anchor=[0, 1],
           ncol=2, shadow=True, title="Legend", fancybox=True)
    ax1.legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)
    
    ax2.plot(x, get_average_errors_per_percentage(results_OBD["medium"]),color='r')
    ax2.errorbar(x, get_average_errors_per_percentage(results_OBD["medium"]),yerr=get_stdev_per_percentage(results_OBD["medium"]), fmt='o',color='r')
    ax2.plot(x, get_average_errors_per_percentage(results_AD["medium"]),color='b')
    ax2.errorbar(x, get_average_errors_per_percentage(results_AD["medium"]),yerr=get_stdev_per_percentage(results_AD["medium"]), fmt='o',color='b')
    
    ax3.plot(x, get_average_errors_per_percentage(results_OBD["large"]),color='r')
    ax3.errorbar(x, get_average_errors_per_percentage(results_OBD["large"]),yerr=get_stdev_per_percentage(results_OBD["large"]), fmt='o',color='r')
    ax3.plot(x,  get_average_errors_per_percentage(results_AD["large"]),color='b')
    ax3.errorbar(x, get_average_errors_per_percentage(results_AD["large"]),yerr=get_stdev_per_percentage(results_AD["large"]), fmt='o',color='b')
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)   
    plt.show()
    
def main(path_to_csv,level,exp):
    map_furer_OBD_to_percentages_rel_errors={}
    map_furer_AD_to_percentages_rel_errors={}
    map_runtimes_seconds,map_final_embs=get_runtimes_embeddings_exhaustive(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"))
    
    for pattern in map_runtimes_seconds.keys():
        print "furer"
        map_furer_OBD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'furer_'+str(level)+".csv"),exp)
        print "Ffurer"
        map_furer_AD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'Ffurer_order_'+str(level)+".csv"),exp)
    
    average_relative_errors_furer_OBD=get_average_errors_per_percentage(map_furer_OBD_to_percentages_rel_errors)   
    average_relative_errors_furer_AD=get_average_errors_per_percentage(map_furer_AD_to_percentages_rel_errors)   
    print "OBD: ",average_relative_errors_furer_OBD
    print "AD:",average_relative_errors_furer_AD
    plot(average_relative_errors_furer_OBD,average_relative_errors_furer_AD) 
   

if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')
  parser.add_argument('-e',help='dblp for DBLP, y for YEAST, am for AMAZON')
  parser.add_argument('-l',help='patterns size level')
  
  args = parser.parse_args()
  main_multiple_pattern_size_plots_one_plot([4,5,6,7,8,9,10],args.r,args.e,10,2,2,eligibility=False)

