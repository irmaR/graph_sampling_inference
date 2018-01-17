'''
Created on Mar 9, 2016

@author: irma
'''
import argparse,csv,os
import matplotlib.pyplot as plt
import numpy as np


def get_results_embeddings(pattern_name,runtime_exh,emb_exh,furer_csv,exp,step_percentage):
    relative_errors=[]
    row_of_interest={}
    with open(furer_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
         name_of_pattern=row["pattern_name"].split("/")[-2]
         if name_of_pattern==pattern_name:
             row_of_interest=row
             break
    embeddings_furer=[]
    for t in xrange(1,121):
        column_name="emb_"+str(t)
        value=None
        try:
           value=float(row[column_name])
        except:
           value=0
        relative_errors.append(get_relative_error(value, emb_exh))
    return relative_errors

def get_relative_error(N,M):
    return abs((float(N)-float(M)))/M

def get_eligible_patterns_approach(map_exhaustive_patterns,appr):
    eligible_patterns=[]
    interval=2
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
            #print "REL ERROR FURER: ",name_of_pattern,rel_error_furer
            if name_of_pattern in map_exhaustive_patterns.keys() and not rel_error_furer*100<=5:
                eligible_patterns.append(name_of_pattern)
    print "Nr eligible patterns: ",len(eligible_patterns)
    return eligible_patterns

def get_runtimes_embeddings_exhaustive(path_to_exhaustive_csv):
    map_runtimes={}
    map_embs={}
    with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
         if(not(row["timeout"]=="False")):
             continue
         if(not(row["exh_emb"])):
             continue
         nr_emb_exhaustive=float(row["exh_emb"])
         name_of_patterns=row["pattern_name"].split("/")[-2]
         map_runtimes[name_of_patterns]=float(row["time"])
         map_embs[name_of_patterns]=nr_emb_exhaustive
    return map_runtimes,map_embs

def get_stdev_per_interval(map_relative_errors,step_percentage):
    stds=[]
    for i in xrange(0,120):
        values=[]
        for patt in map_relative_errors.keys():
            values.append(map_relative_errors[patt][i])
        stds.append(np.std(values))
    return stds

def get_average_errors_per_interval(map_relative_errors,step_percentage):
    average_rel_errors=[]
    for i in xrange(0,120):
        sum=0
        c=0
        for patt in map_relative_errors.keys():
            c+=1
            sum+=map_relative_errors[patt][i]
        if float(c)==0.0:
            return []
        average_rel_errors.append(sum/float(c))
    return average_rel_errors

def main_multiple_pattern_size_plots(pattern_sizes,path_to_csv,exp,step_percentage,m,n,eligibility=True):
    axis_tuple=()
    limit=120
    x=xrange(0,limit,1)
    f, axis = plt.subplots(nrows=m, ncols=n, sharex=True, sharey=False)   
    if exp=="dblp":
         plt.title("DBLP")
    if exp=="am":
         plt.title("AMAZON")
    if exp=="y":
         plt.title("YEAST")
    if exp=="fb":
         plt.title("FACEBOOK")
    if exp=="enr":
         plt.title("ENRON")
    if exp=="imdb":
         plt.title("IMDB")
   
    axis_counter=0
    pattern_counter=0
    for i in xrange(0,m):
        for j in xrange(0,n):
         if pattern_counter>=len(pattern_sizes):
             break
         level=pattern_sizes[pattern_counter]
         pattern_counter+=1
         print "Processing level ",level
         ax = axis[i][j]
         if j==0:
            ax.set_ylabel('AvgRelError',size=15)
         if i==3:
            ax.set_xlabel('% exhaustive runtime',size=15)
         map_furer_OBD_to_percentages_rel_errors={}
         map_furer_AD_to_percentages_rel_errors={}
         map_runtimes_seconds,map_final_embs=get_runtimes_embeddings_exhaustive(os.path.join(path_to_csv,'exhaustive_'+str(level)+".csv"))
         if eligibility:
            eligble_patterns=get_eligible_patterns_approach(map_final_embs,os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"))
         else:
             eligble_patterns=map_final_embs.keys()
         for pattern in map_runtimes_seconds.keys():
            if pattern in eligble_patterns:
                print "PATTERN: ",pattern
                print "furer"
                map_furer_OBD_to_percentages_rel_errors[pattern]=get_results_embeddings(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'furer_'+str(level)+".csv"),exp,step_percentage)
                print "Ffurer"
                map_furer_AD_to_percentages_rel_errors[pattern]=get_results_embeddings(pattern,map_runtimes_seconds[pattern],map_final_embs[pattern],os.path.join(path_to_csv,'Ffurer_'+str(level)+".csv"),exp,step_percentage)
         print map_furer_OBD_to_percentages_rel_errors
         print map_furer_AD_to_percentages_rel_errors
         average_relative_errors_furer_OBD=get_average_errors_per_interval(map_furer_OBD_to_percentages_rel_errors,step_percentage)   
         average_relative_errors_furer_AD=get_average_errors_per_interval(map_furer_AD_to_percentages_rel_errors,step_percentage)   
         
         stdev_furer_OBD=get_stdev_per_interval(map_furer_OBD_to_percentages_rel_errors,step_percentage)
         stdev_furer_AD=get_stdev_per_interval(map_furer_AD_to_percentages_rel_errors,step_percentage)

         for t in xrange(0,120):
             if not t % 10==0:
                 stdev_furer_AD[t]=0
                 stdev_furer_OBD[t]=0
         print "OBD FURER: ",average_relative_errors_furer_OBD
         print "OBD FFURER: ",average_relative_errors_furer_AD

         print "STD OBD ",stdev_furer_OBD,len(stdev_furer_OBD)
         #print "AD:",average_relative_errors_furer_AD
         ax.set_title("Level: "+str(level))
         if average_relative_errors_furer_AD==[] or average_relative_errors_furer_AD==[]:
             continue
         print len(average_relative_errors_furer_OBD),len(stdev_furer_OBD)
         print len(x),len(average_relative_errors_furer_OBD)
         ax.plot(x,average_relative_errors_furer_OBD,color='blue',linewidth=3.0)
         ax.plot(x,average_relative_errors_furer_AD,color='black',linewidth=3.0)
         ax.errorbar(x, average_relative_errors_furer_OBD,yerr=stdev_furer_OBD, fmt='o',color='blue')
         ax.errorbar(x, average_relative_errors_furer_AD,yerr=stdev_furer_AD, fmt='o',color='black')
         
         ax.set_yscale('log')
         #ax.set_xscale('log')
         axis_counter+=1
    
    plt.legend(['Furer-OBD', 'Furer-AD'],loc = 'upper right', bbox_to_anchor = (0,0.5,1.1,0.5))
    f.tight_layout()
    
    f.subplots_adjust(wspace=0.3)
    f.subplots_adjust(hspace=0.3)
    plt.show()


if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')
  parser.add_argument('-e',help='dblp,y,fb,am,imdb,enr,wb')
  parser.add_argument('-l',help='patterns size level')
  
  args = parser.parse_args()
  #
  #main_multiple_pattern_size_plots(args.r,args.l,args.e)
  main_multiple_pattern_size_plots([4,5,6,7,8,9,10],args.r,args.e,10,4,3,True)
