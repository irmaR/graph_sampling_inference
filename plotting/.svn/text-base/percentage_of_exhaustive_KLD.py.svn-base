'''
Created on Mar 8, 2016

@author: irma
'''
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
    print rel_errors
    return rel_errors


def get_runtimes_embeddings_exhaustive(path_to_exhaustive_csv):
    map_runtimes={}
    map_embs={}
    with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
         if(not(row["timeout"]=="True")):
             continue
         if(not(row["exh_emb"])):
             continue
         
         nr_emb_exhaustive=float(row["exh_emb"])
         name_of_patterns=row["pattern_name"].split("/")[-2]
         map_runtimes[name_of_patterns]=float(row["time"])
         map_embs[name_of_patterns]=nr_emb_exhaustive
    return map_runtimes,map_embs


def get_intervals(N,time_unit):
    intervals_seconds=[]
    if time_unit=="min":
       N=N/60
    
    for x in xrange(0,110,10):
        intervals_seconds.append(int(((N*x)/100)/5))
    return intervals_seconds


def get_results_percentages(pattern_name,runtime_exh,emb_exh,furer_csv,exp):
    klds=[]
    row_of_interest={}
    with open(furer_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
         name_of_pattern=row["pattern_name"].split("/")[-2]
         if name_of_pattern==pattern_name:
             row_of_interest=row
             break
    if exp=="dblp":
        intervals=get_intervals(runtime_exh,"min")
    else:
        intervals=get_intervals(runtime_exh,"sec")
    print intervals
    #print pattern_name,intervals
    embeddings_furer=[]
    for t in intervals:
        if t==0:
            t=1
        if t>120:
            t=120
        column_name="KLD_"+str(t)
        try:
           klds.append(float(row[column_name]))
        except:
           klds.append(0) 
    return klds

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
   x=xrange(0,110,10)
   print "OBD: ",furer_OBD_results
   print "AD: ",furer_AD_results
   plt.plot(x, furer_OBD_results)
   plt.plot(x, furer_AD_results)
    
   plt.xlabel('time (s)')
   plt.ylabel('voltage (mV)')
   plt.title('About as simple as it gets, folks')
   plt.grid(True)
   plt.savefig("test.png")
   plt.legend(['FK-OBD', 'FK-AD'], loc='upper left')
   plt.show()

def get_average_errors_per_percentage(map_relative_errors):
    average_rel_errors=[]
    for i in xrange(0,11):
        sum=0
        c=0
        for patt in map_relative_errors.keys():
            c+=1
            num=map_relative_errors[patt][i]
            if math.isnan(map_relative_errors[patt][i]):
                num=0
            sum+=num
        print sum,float(c)
        average_rel_errors.append(sum/float(c))
    return average_rel_errors

def get_stdev_per_percentage(map_relative_errors):
    stds=[]
    for i in xrange(0,11):
        values=[]
        for patt in map_relative_errors.keys():
            values.append(map_relative_errors[patt][i])
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
    print bins
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
    print "hm: small ",get_average_errors_per_percentage(results_OBD["small"])
    print "hm:small ",get_average_errors_per_percentage(results_AD["small"])
    plt.legend(loc="upper left", bbox_to_anchor=[0, 1],
           ncol=2, shadow=True, title="Legend", fancybox=True)
    ax1.legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)
    
    print "hm:medium ",get_average_errors_per_percentage(results_OBD["medium"])
    print "hm:medium ",get_average_errors_per_percentage(results_AD["medium"])
    ax2.plot(x, get_average_errors_per_percentage(results_OBD["medium"]),color='r')
    #ax2.errorbar(x, get_average_errors_per_percentage(results_OBD["medium"]),yerr=get_stdev_per_percentage(results_OBD["medium"]), fmt='o',color='r')
    ax2.plot(x, get_average_errors_per_percentage(results_AD["medium"]),color='b')
    #ax2.errorbar(x, get_average_errors_per_percentage(results_AD["medium"]),yerr=get_stdev_per_percentage(results_AD["medium"]), fmt='o',color='b')
    
    ax3.plot(x, get_average_errors_per_percentage(results_OBD["large"]),color='r')
    print "hm:large ",get_average_errors_per_percentage(results_OBD["large"])
    print "hm:large ",get_average_errors_per_percentage(results_AD["large"])
    
    #ax3.errorbar(x, get_average_errors_per_percentage(results_OBD["large"]),yerr=get_stdev_per_percentage(results_OBD["large"]), fmt='o',color='r')
    ax3.plot(x,  get_average_errors_per_percentage(results_AD["large"]),color='b')
    #ax3.errorbar(x, get_average_errors_per_percentage(results_AD["large"]),yerr=get_stdev_per_percentage(results_AD["large"]), fmt='o',color='b')
    # Fine-tune figure; make subplots close to each other and hide x ticks for
    # all but bottom plot.
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)   
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
    # Fine-tune figure; make subplots close to each other and hide x ticks for
    # all but bottom plot.
    f.subplots_adjust(hspace=0)
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
        map_furer_AD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"),exp)

    average_relative_errors_furer_OBD=get_average_errors_per_percentage(map_furer_OBD_to_percentages_rel_errors)   
    average_relative_errors_furer_AD=get_average_errors_per_percentage(map_furer_AD_to_percentages_rel_errors)   
    print "OBD: ",average_relative_errors_furer_OBD
    print "AD:",average_relative_errors_furer_AD
    plot(average_relative_errors_furer_OBD,average_relative_errors_furer_AD) 
   

if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')
  parser.add_argument('-e',help='dblp or y')
  parser.add_argument('-l',help='patterns size level')
  
  args = parser.parse_args()
  main(args.r,args.l,args.e)