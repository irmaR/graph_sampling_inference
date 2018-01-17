'''
Created on Jun 14, 2017

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

        if np.isnan(v1) or np.isnan(v2):
            rel_errors.append(float('nan'))
        else:
            nr=abs((float(v1)-float(v2)))/max([v1,v2])
            if not math.isnan(nr):
              rel_errors.append(abs((float(v1)-float(v2)))/max([v1,v2]))
    return rel_errors

def get_intervals(N,time_unit,step_percentage):
    intervals_seconds=[]
    if time_unit=="min":
       N=N/60
    
    for x in xrange(0,(100+step_percentage),step_percentage):
        intervals_seconds.append(int(((N*x)/100)/5))
    return intervals_seconds

def get_average_errors_per_percentage(map_relative_errors,step_percentage):
    avgs=[]
    for i in xrange(0,int((100+step_percentage)/step_percentage)):
        values=[]
        for patt in map_relative_errors.keys():
            values.append(map_relative_errors[patt][i])
        #print "STD OF VALS: ",values,np.std(values)
        avgs.append(np.nanmean(values))
    return avgs

def get_stdev_per_percentage(map_relative_errors,step_percentage):
    stds=[]
    for i in xrange(0,int((100+step_percentage)/step_percentage)):
        values=[]
        for patt in map_relative_errors.keys():
            values.append(map_relative_errors[patt][i])
        #print "STD OF VALS: ",values,np.std(values)
        stds.append(np.nanstd(values))
    return stds

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

def get_relative_error(N,M):
    return abs((float(N)-float(M)))/M

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
                avg_emb+=float('nan')
        if counter>0:
          avg_emb=avg_emb/float(counter)
        try:
           embeddings_furer.append(avg_emb)
        except:
           embeddings_furer.append(float('nan'))
    print "One:",embeddings_furer
    print "Two:",calculate_relative_errors_exhaustive([emb_exh] * len(embeddings_furer),embeddings_furer)
    return calculate_relative_errors_exhaustive([emb_exh] * len(embeddings_furer),embeddings_furer)


def main_multiple_pattern_size_plots(pattern_sizes,path_to_csv,exp,step_percentage,m,n,eligibility=True):
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
    iplot = 220
    for i in range(4):
        iplot += 1
        level=pattern_sizes[i+1]
        all_levels_average_relative_errors_furer_OBD={}
        all_average_relative_errors_furer_AD={}
        all_average_relative_errors_furer_AD_10={}
        all_average_relative_errors_random={}
        
        map_furer_OBD_to_percentages_rel_errors={}
        map_furer_AD_to_percentages_rel_errors={}
        map_runtimes_seconds,map_final_embs=get_runtimes_embeddings_exhaustive(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"),exp)
        if eligibility:
            eligble_patterns=get_eligible_patterns_approach(map_final_embs,os.path.join(path_to_csv,'furer_'+str(level)+".csv"))
        else:
             eligble_patterns=map_final_embs.keys()
        print "Number of eligible patterns:",len(eligble_patterns),"for",exp
        for pattern in map_runtimes_seconds.keys():
            if pattern in eligble_patterns:
                #print "PATTERN: ",pattern
                map_furer_OBD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'furer_'+str(level)+".csv"),exp,step_percentage)
                map_furer_AD_to_percentages_rel_errors[pattern]=get_results_percentages(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"),exp,step_percentage)
                            

        avg_ERR_OBD=get_average_errors_per_percentage(map_furer_OBD_to_percentages_rel_errors,step_percentage)   
        avg_ERR_AD=get_average_errors_per_percentage(map_furer_AD_to_percentages_rel_errors,step_percentage) 
        
        stdev_furer_OBD=get_stdev_per_percentage(map_furer_OBD_to_percentages_rel_errors,step_percentage)
        stdev_furer_AD=get_stdev_per_percentage(map_furer_AD_to_percentages_rel_errors,step_percentage)
         
        #all_levels_average_relative_errors_furer_OBD[level]=average_relative_errors_furer_OBD
        #all_average_relative_errors_furer_AD[level]=average_relative_errors_furer_AD
        #all_average_relative_errors_furer_AD_10[level]=average_relative_errors_furer_AD_10
        #all_average_relative_errors_random[level]=average_relative_errors_random
        print "Stdev obd: ",stdev_furer_OBD
        print "Stdev ad:",stdev_furer_AD
 
                 
         #leave stdevs after each 10 iterations, the rest is zero
        #avg_ERR_OBD=get_average_errors_per_percentage(all_levels_average_relative_errors_furer_OBD,step_percentage)
        #avg_ERR_AD=get_average_errors_per_percentage(all_average_relative_errors_furer_AD,step_percentage)
        #avg_ERR_random=get_average_errors_per_percentage(all_average_relative_errors_random,step_percentage)
        
        #stdev_furer_OBD=get_stdev_per_percentage(all_levels_average_relative_errors_furer_OBD,step_percentage)
        #stdev_furer_AD=get_stdev_per_percentage(all_average_relative_errors_furer_AD,step_percentage)
        #stdev_furer_random=get_stdev_per_percentage(all_average_relative_errors_random,step_percentage)
        #if not exp=="dblp":
        #  stdev_furer_AD_10=get_stdev_per_percentage(all_average_relative_errors_furer_AD_10,step_percentage)
        
        
        for t in xrange(0,(100+step_percentage),step_percentage):
         if not t % 10==0:
             stdev_furer_AD[t]=0
             #if not exp=="dblp":
             #  stdev_furer_AD_10[t]=0
             stdev_furer_OBD[t]=0
        
        if i == 4:
           #print "ovdje",exp
           #ax = plt.subplot2grid((3,7), (i/2, 2), colspan=3)
           ax = fig.add_subplot(iplot)
           ax.set_ylabel('Avg_RelEr',size=25)
           #ax = fig.add_subplot(iplot)
           #ax.legend(['FK-OBD', 'FK-AD','Random'],loc = 'upper right', bbox_to_anchor = (0,0.5,1.0,0.5),prop={'size':16})    
        else:
        # You can be fancy and use subplot2grid for each plot, which dosen't
        # require keeping the iplot variable:
        # ax = subplot2grid((4,2), (i/2,i%2))

        # Or you can keep using add_subplot, which may be simpler:
          ax = fig.add_subplot(iplot)
        
          if i==0 or i==2 or i==4:
            ax.set_ylabel('Avg_RelEr',size=25)
          

        #ax.set_yscale('log')
        ax.set_title("Pattern size: "+str(level), fontsize=25)
        ax.plot(x,avg_ERR_OBD,color='blue',linewidth=3.0)
        ax.plot(x,avg_ERR_AD,color='red',linewidth=3.0)
        print 'plotting: ',exp
        print avg_ERR_OBD
        print avg_ERR_AD
        ax.errorbar(x, avg_ERR_OBD,yerr=stdev_furer_OBD, fmt='o',color='blue',linewidth=2)
        ax.errorbar(x, avg_ERR_AD,yerr=stdev_furer_AD, fmt='o',color='red',linewidth=2.0)
        ax.set_ylim([0,1])
        zed = [tick.label.set_fontsize(25) for tick in ax.yaxis.get_major_ticks()]
        zed = [tick.label.set_fontsize(25) for tick in ax.xaxis.get_major_ticks()]
        #ax.set_xticklabels(x,fontsize=25)
        #ax.set_xticklabels(x,fontsize=20)
        if i==0:
               ax.legend(['FK-OBD', 'FK-AD'],loc = 'upper right', bbox_to_anchor = (0,0.5,1.02,0.5),prop={'size':16}, ncol=2)
            #ax.legend(['FK-OBD', 'FK-AD','FK-AD-10','Random'],prop={'size':15})    
        axis_counter+=1
    #ax = fig.add_subplot(iplot)
    fig.add_subplot(111, frameon=False)     


    plt.xlabel('% exhaustive runtime',size=25)
    plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off',labelsize=30)
#     if exp=="dblp":
#         plt.title("DBLP", fontsize=20)
#     elif exp=="y":
#         plt.title("YEAST", fontsize=20)
#     elif exp=="webkb":
#         plt.title("WEBKB", fontsize=20)
#     elif exp=="facebook":
#         plt.title("FACEBOOK", fontsize=20)
#     elif exp=="imdb":
#         plt.title("IMDB", fontsize=20)
#     elif exp=="am":
#         plt.title("AMAZON", fontsize=20)
    plt.show()


if __name__=='__main__':
  #parser = argparse.ArgumentParser(description='Run exhaustive approach')
  #parser.add_argument('-r',help='path to csv files')
  #parser.add_argument('-e',help='dblp for DBLP, y for YEAST, am for AMAZON')
  #parser.add_argument('-l',help='patterns size level')
  
  #args = parser.parse_args()
  #main_multiple_pattern_size_plots([4,5,6,7,8,9,10],args.r,args.e,10,2,2,eligibility=False)
  #main_multiple_pattern_size_plots([11,12,13,14,15],args.r,args.e,10,2,2,eligibility=False)
  main_multiple_pattern_size_plots([11, 12, 13, 14, 15], '/home/irma/work/RESULTS/graph_sampling/dblp_csvs/', 'dblp',10, 2, 2, eligibility=False)