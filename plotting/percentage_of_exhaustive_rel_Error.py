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
import matplotlib.gridspec as gridspec



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
         if(not(row["timeout"]=="False")):
             continue
         if(not(row["exh_emb"])):
             continue
         #if(float(row["time"])<=float((total_time_sec*1)/100)):
         #    continue
         nr_emb_exhaustive=float(row["exh_emb"])
         name_of_patterns=row["pattern_name"].split("/")[-2]
         map_runtimes[name_of_patterns]=float(row["time"])
         map_embs[name_of_patterns]=nr_emb_exhaustive
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
                continue
        if counter>0:
          avg_emb=avg_emb/float(counter)
        try:
           embeddings_furer.append(avg_emb)
        except:
           embeddings_furer.append(0)
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
            if row["emb_"+str(interval)]=="":
                continue
            if not name_of_pattern in map_exhaustive_patterns.keys():
                continue
            emb_1=float(row["emb_"+str(interval)])            
            rel_error_furer=get_relative_error(emb_1,map_exhaustive_patterns[name_of_pattern])
            if name_of_pattern in map_exhaustive_patterns.keys() and not rel_error_furer*100<=5:
               eligible_patterns.append(name_of_pattern)
    return eligible_patterns

def main_multiple_pattern_size_plots(pattern_sizes,path_to_csv,exps,paths,step_percentage,m,n,eligibility=True):
    axis_tuple=()
    limit=(100+step_percentage)
    x=xrange(0,limit,step_percentage)
    #f, axis = plt.subplots(nrows=m, ncols=n, sharex=True, sharey=False) 
    exp_counter=0
    axis_counter=0
    i=0
    j=0
    fig = plt.figure()
    plt.subplots_adjust(wspace=0.5,hspace=0.5)
    iplot = 320
    for i in range(5):
        iplot += 1
        if exp_counter>=len(exps):
          break 
        path_to_csv=paths[exp_counter]
        exp=exps[exp_counter]
        furer_file='Ffurer_order_random_'
        exp_counter+=1
        #ax = axis[i][j]
         #go over all pattern levels
        all_levels_average_relative_errors_furer_OBD={}
        all_average_relative_errors_furer_AD={}
        all_average_relative_errors_furer_AD_10={}
        all_average_relative_errors_random={}
        for level in pattern_sizes:
             #print i,j
             
             
             #if j==0:
             #   ax.set_ylabel('Avg_RelEr',size=20)
             #if i==(m-1) and j==(n-1):
             #   ax.set_xlabel('% exhaustive runtime',size=18)
             map_furer_OBD_to_percentages_rel_errors={}
             map_furer_AD_to_percentages_rel_errors={}
             map_furer_AD_10_to_percentages_rel_errors={}
             map_random_to_percentages_rel_errors={}
             map_runtimes_seconds,map_final_embs=get_runtimes_embeddings_exhaustive(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"),exp)
             if eligibility:
                eligble_patterns=get_eligible_patterns_approach(map_final_embs,os.path.join(path_to_csv,furer_file+str(level)+".csv"))
             else:
                 eligble_patterns=map_final_embs.keys()
             print "Number of eligible patterns:",len(eligble_patterns),"for",exp
             for pattern in map_runtimes_seconds.keys():
                if pattern in eligble_patterns:
                    #print "PATTERN: ",pattern
                    map_furer_OBD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'furer_'+str(level)+".csv"),exp,step_percentage)
                    #map_furer_AD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"),exp,step_percentage)
                    map_furer_AD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"),exp,step_percentage)
                    map_random_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'random_'+str(level)+".csv"),exp,step_percentage)
                    
    
             average_relative_errors_furer_OBD=get_average_errors_per_percentage(map_furer_OBD_to_percentages_rel_errors,step_percentage)   
             average_relative_errors_furer_AD=get_average_errors_per_percentage(map_furer_AD_to_percentages_rel_errors,step_percentage)   
             average_relative_errors_random=get_average_errors_per_percentage(map_random_to_percentages_rel_errors,step_percentage)   
            
             stdev_furer_OBD=get_stdev_per_percentage(map_furer_OBD_to_percentages_rel_errors,step_percentage)
             stdev_furer_AD=get_stdev_per_percentage(map_furer_AD_to_percentages_rel_errors,step_percentage)
             stdev_random=get_stdev_per_percentage(map_random_to_percentages_rel_errors,step_percentage)
             
             all_levels_average_relative_errors_furer_OBD[level]=average_relative_errors_furer_OBD
             all_average_relative_errors_furer_AD[level]=average_relative_errors_furer_AD
             all_average_relative_errors_random[level]=average_relative_errors_random
         

                 
             
         #leave stdevs after each 10 iterations, the rest is zero
        avg_ERR_OBD=get_average_errors_per_percentage(all_levels_average_relative_errors_furer_OBD,step_percentage)
        avg_ERR_AD=get_average_errors_per_percentage(all_average_relative_errors_furer_AD,step_percentage)
        avg_ERR_random=get_average_errors_per_percentage(all_average_relative_errors_random,step_percentage)
        
        stdev_furer_OBD=get_stdev_per_percentage(all_levels_average_relative_errors_furer_OBD,step_percentage)
        stdev_furer_AD=get_stdev_per_percentage(all_average_relative_errors_furer_AD,step_percentage)
        stdev_furer_random=get_stdev_per_percentage(all_average_relative_errors_random,step_percentage)
        #if not exp=="dblp":
        #  stdev_furer_AD_10=get_stdev_per_percentage(all_average_relative_errors_furer_AD_10,step_percentage)
        
        
        for t in xrange(0,(100+step_percentage),step_percentage):
         if not t % 10==0:
             stdev_furer_AD[t]=0
             #if not exp=="dblp":
             #  stdev_furer_AD_10[t]=0
             stdev_furer_OBD[t]=0
             stdev_furer_random[t]=0
        
        if i == 4:
           #print "ovdje",exp
           ax = plt.subplot2grid((3,7), (i/2, 2), colspan=3)
           ax.set_ylabel('Avg RelErr',size=30)
           #ax = fig.add_subplot(iplot)
           #ax.legend(['FK-OBD', 'FK-AD','Random'],loc = 'upper right', bbox_to_anchor = (0,0.5,1.0,0.5),prop={'size':16})    
        else:
        # You can be fancy and use subplot2grid for each plot, which dosen't
        # require keeping the iplot variable:
        # ax = subplot2grid((4,2), (i/2,i%2))

        # Or you can keep using add_subplot, which may be simpler:
          ax = fig.add_subplot(iplot)
          if i==0 or i==2 or i==4:
            ax.set_ylabel('Avg RelErr',size=30)
        if exp=="dblp":
          ax.set_title("DBLP", fontsize=30)
          print i
        elif exp=="y":
          ax.set_title("YEAST", fontsize=30)
        elif exp=="webkb":
          ax.set_title("WEBKB", fontsize=30)
        elif exp=="facebook":
          ax.set_title("FACEBOOK", fontsize=30)
        elif exp=="imdb":
          ax.set_title("IMDB", fontsize=30)
        elif exp=="am":
          ax.set_title("AMAZON", fontsize=30)

        #x=xrange(5,605,15)
        ax.plot(x,avg_ERR_OBD,'-o',color='blue',linewidth=3.0)
        ax.plot(x,avg_ERR_AD,':v',color='red',linewidth=3.0)
        ax.plot(x,avg_ERR_random,'--D',color='green',linewidth=3.0)
        print 'plotting: ',exp
        print avg_ERR_OBD
        print avg_ERR_AD
        print avg_ERR_random
        ax.errorbar(x, avg_ERR_OBD,yerr=stdev_furer_OBD, fmt='o',color='blue',linewidth=2)
        ax.errorbar(x, avg_ERR_AD,yerr=stdev_furer_AD, fmt='v',color='red',linewidth=2.0)
        ax.errorbar(x, avg_ERR_random,yerr=stdev_furer_random, fmt='D',color='green',linewidth=2.0)
        ax.set_ylim([0,1])
        zed = [tick.label.set_fontsize(25) for tick in ax.yaxis.get_major_ticks()]
        zed = [tick.label.set_fontsize(25) for tick in ax.xaxis.get_major_ticks()]
        #ax.set_xticklabels(x,fontsize=25)
        #ax.set_xticklabels(x,fontsize=20)
        axis_counter+=1
    #ax = fig.add_subplot(iplot)
    plt.legend(['FK-OBD', 'FK-AD','Random'],loc = 'upper right', bbox_to_anchor = (0,0.5,1.0,0.5),prop={'size':16})    
    fig.add_subplot(111, frameon=False)     
    plt.xlabel('% exhaustive runtime',size=30)
    plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off',labelsize=30)
    #plt.tight_layout()
    #plt.subplots_adjust(wspace=0.3)
    #plt.subplots_adjust(hspace=0.3)
    plt.show()
    
def main_multiple_pattern_size_plots_one_plot(pattern_sizes,path_to_csv,exp,step_percentage,eligibility=True):
    axis_tuple=()
    limit=(100+step_percentage)
    x=xrange(0,limit,step_percentage)
    plt.title("SATISFACTION")
    axis_counter=0
    pattern_counter=0
    level=0
    plt.ylabel('Avg RelErr',size=30)
    plt.xlabel('% exhaustive runtime',size=30)
    map_furer_OBD_to_percentages_rel_errors={}
    map_furer_AD_to_percentages_rel_errors={}
    map_runtimes_seconds,map_final_embs=get_runtimes_embeddings_exhaustive(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"),exp)
    if eligibility:
        eligble_patterns=get_eligible_patterns_approach(map_final_embs,os.path.join(path_to_csv,'Ffurer_order_random_'+str(level)+".csv"))
    else:
        eligble_patterns=map_final_embs.keys()
    for pattern in map_runtimes_seconds.keys():
            if pattern in eligble_patterns:
                print "PATTERN: ",pattern
                print "furer"
                map_furer_OBD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'furer_'+str(level)+".csv"),exp,step_percentage)
                print "Ffurer"
                map_furer_AD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"),exp,step_percentage)
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

    plt.plot(x,average_relative_errors_furer_OBD,color='blue',linewidth=3.0,line='-')
    plt.plot(x,average_relative_errors_furer_AD,color='black',linewidth=3.0,line=':')
    plt.errorbar(x, average_relative_errors_furer_OBD,yerr=stdev_furer_OBD, fmt='o',color='blue')
    plt.errorbar(x, average_relative_errors_furer_AD,yerr=stdev_furer_AD, fmt='o',color='black')

    plt.legend(['Furer-OBD', 'Furer-AD'],loc = 'upper right',prop={'size':20})
    
    plt.tight_layout()
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
  #main_multiple_pattern_size_plots([4,5,6,7,8,9,10],args.r,['y','imdb','facebook','webkb','dblp'],['/home/irma/work/RESULTS/graph_sampling/yeast_csvs/','/home/irma/work/RESULTS/graph_sampling/imdb_csvs/','/home/irma/work/RESULTS/graph_sampling/facebook_csvs/','//home/irma/work/RESULTS/graph_sampling/webkb_csvs/','/home/irma/work/RESULTS/graph_sampling/dblp_csvs/'],10,3,2,eligibility=False)
  main_multiple_pattern_size_plots([5,6,7,8,9,10],args.r,['facebook'],['/home/irma/work/RESULTS/graph_sampling/facebook_csvs/'],10,3,2,eligibility=False)

  #main_multiple_pattern_size_plots([4,5,6,7,8,9,10],args.r,['dblp'],['/home/irma/workspace/DMKD_Paper_Sampling/dblp_csvs/'],10,3,2,eligibility=False)

  #main_multiple_pattern_size_plots([4,5,6,7,8,9,10],args.r,['dblp'],['/home/irma/workspace/DMKD_Paper_Sampling/dblp_csvs/'],10,1,1,eligibility=False)

  #main_multiple_pattern_size_plots([5,6,8,9,10],args.r,args.e,10,eligibility=False)

