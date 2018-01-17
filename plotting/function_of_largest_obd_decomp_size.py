'''
Created on Jun 27, 2017

@author: irma
'''
import csv
import ast
import math
import numpy as np
import matplotlib.pyplot as plt
import experiments.utils_reporting_results as utils
import pandas as pd
from matplotlib.scale import LogScale


def emb_function_of_decomp_length(path_to_exhaustive_csv,pattern_size,path_to_approach):
   output={}
   with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)   
       for row in reader:
         array_values_appx=[]
         if row["timeout"]=="True":
             continue
         name_of_patterns='/'.join(row["pattern_name"].split("/")[:-1])
         with open(path_to_approach) as appX:
              reader1 = csv.DictReader(appX)  
              for row1 in reader1:
                  if('/'.join(row1["pattern_name"].split("/")[:-1])==name_of_patterns):
                      obd_decomp=row1["OBD"]
                      obd = obd_decomp.split('],[')[0]
                      obd = eval('[' + obd + ']')[0]
                      #find max length
                      
                      length=len(obd)
                      #find exhaustive count
                      nr_emb_exhaustive=float(row["exh_emb"])
                      
                      #get approach account (we take the final count)
                      appr_count=float('nan')
                      if(not(row1["emb_"+str(120)])):
                        appr_count=float('nan')
                      else:
                          appr_count=float(row1["emb_"+str(120)])
                     
                      relErr=calculate_Relative_Errors_exhaustive([nr_emb_exhaustive], [appr_count])
                      print relErr
                      if not length in output.keys():
                          output[length]=[relErr[0]]
                      else:
                          output[length].append(relErr[0])
   return output


'''
For each pattern result calculate average nr embeddings for all time intervals.
Then calculate relative error of the average estimate.
Report: average relative error on number of embeddings for all the patterns
'''
def emb_function_of_max_decomp_size(path_to_exhaustive_csv,pattern_size,path_to_approach):
   output={}
   with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)   
       for row in reader:
         array_values_appx=[]
         if row["timeout"]=="True":
             continue
         name_of_patterns='/'.join(row["pattern_name"].split("/")[:-1])
         with open(path_to_approach) as appX:
              reader1 = csv.DictReader(appX)  
              for row1 in reader1:
                  if('/'.join(row1["pattern_name"].split("/")[:-1])==name_of_patterns):
                      obd_decomp=row1["OBD"]
                      obd = obd_decomp.split('],[')[0]
                      obd = eval('[' + obd + ']')[0]
                      #find max length
                      max_size=0
                      for el in obd:
                          if len(el)>=max_size:
                              max_size=len(el)
                      #find exhaustive count
                      nr_emb_exhaustive=float(row["exh_emb"])
                      
                      #get approach account (we take the final count)
                      appr_count=float('nan')
                      if(not(row1["emb_"+str(120)])):
                        appr_count=float('nan')
                      else:
                          appr_count=float(row1["emb_"+str(120)])
                     
                      relErr=calculate_Relative_Errors_exhaustive([nr_emb_exhaustive], [appr_count])
                      print relErr
                      if not max_size in output.keys():
                          output[max_size]=[relErr[0]]
                      else:
                          output[max_size].append(relErr[0])
   return output


def calculate_Relative_Errors_exhaustive(array_of_nr_emb_exhaustive,array_of_nr_emb_approachX):
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
        else:
          rel_errors.append(float('nan'))
        
    #print "MEAN: ",np.mean(rel_errors)
    return rel_errors

def collect_stat_relative_error_average_selected_degree(file_name,dataset_name,path_to_csvs,pattern_sizes):
    #all_degrees=utils.collect_all_degrees(path_to_csvs, min(pattern_sizes),max(pattern_sizes))
    #arrayDiscretized,bins=pd.qcut(np.array(all_degrees), 3,retbins=True, labels=["small","medium","large"])
    #print bins
    Furer={}
    FFurer={}
    Random={}
    
    Furer_patt_size={}
    Ffurer_patt_size={}
    Random_patt_size={}
    
    for n in pattern_sizes:
        print "Patt size: ",n
        path_to_exhaustive_csv=path_to_csvs+"/exhaustive_"+str(n)+".csv"
        path_to_Furer=path_to_csvs+"/furer_"+str(n)+".csv"
        path_to_FFurer=path_to_csvs+"/Ffurer_"+str(n)+".csv"
        path_to_Random=path_to_csvs+"/random_"+str(n)+".csv"
        print "Path to Furer: ",path_to_Furer
        furer_patt_size=emb_function_of_max_decomp_size(path_to_exhaustive_csv,n,path_to_Furer)
        ffurer_patt_size=emb_function_of_max_decomp_size(path_to_exhaustive_csv,n,path_to_FFurer)
        random_patt_size=emb_function_of_max_decomp_size(path_to_exhaustive_csv,n,path_to_Random)
        
        Furer_patt_size[n]=furer_patt_size
        Ffurer_patt_size[n]=ffurer_patt_size
        Random_patt_size[n]=random_patt_size
        
        for k in furer_patt_size.keys():
            if not k in Furer.keys():
                Furer[k]=[]
            else:
                Furer[k].extend(furer_patt_size[k])
        for k in ffurer_patt_size.keys():
            if not k in FFurer.keys():
                FFurer[k]=[]
            else:
                FFurer[k].extend(ffurer_patt_size[k])
        for k in random_patt_size.keys():
            if not k in Random.keys():
                Random[k]=[]
            else:
                Random[k].extend(random_patt_size[k])
    


    fig = plt.figure()
    plt.subplots_adjust(wspace=0.5,hspace=0.5)
    iplot = 230
    for i in range(len(pattern_sizes)):
        iplot += 1
        level=pattern_sizes[i]
        all_obd_decomp_sizes=Furer_patt_size[level].keys()
        
        averagesFurer=[]
        stdFurer=[]
        
        averagesFfurer=[]
        stdFfurer=[]
        
        averagesRandom=[]
        stdRandom=[]
        
        counter=0
        for k in all_obd_decomp_sizes:
            print Furer_patt_size[level][k]
            print np.nanmean(Furer_patt_size[level][k])
            averagesFurer.append(np.nanmean(Furer_patt_size[level][k]))
            stdFurer.append(np.nanstd(Furer_patt_size[level][k]))
            
            averagesFfurer.append(np.nanmean(Ffurer_patt_size[level][k]))
            stdFfurer.append(np.nanstd(Ffurer_patt_size[level][k]))
            averagesRandom.append(np.nanmean(Random_patt_size[level][k]))
            stdRandom.append(np.nanstd(Random_patt_size[level][k]))
                        
        ax = fig.add_subplot(iplot)
        print all_obd_decomp_sizes
        ax.errorbar(all_obd_decomp_sizes, averagesFurer, color='blue',yerr=stdFurer,linewidth=3.5,elinewidth=2)
        ax.errorbar(all_obd_decomp_sizes, averagesFfurer, color='red',yerr=stdFurer,linewidth=3.5,elinewidth=2)
        #ax.errorbar(all_obd_decomp_sizes, averagesRandom, color='green',yerr=stdRandom,linewidth=3.5,elinewidth=2)
        #ax.plot(all_obd_decomp_sizes, averagesFurer,color='blue',linewidth=2)
        #ax.plot(all_obd_decomp_sizes, averagesFfurer,color='red',linewidth=2.0)
        
    plt.show()
    
    
    
    
    
    
    
    
    
    
def collect_stat_relative_error_size_of_OBD(file_name,dataset_name,path_to_csvs,pattern_sizes):
    #all_degrees=utils.collect_all_degrees(path_to_csvs, min(pattern_sizes),max(pattern_sizes))
    #arrayDiscretized,bins=pd.qcut(np.array(all_degrees), 3,retbins=True, labels=["small","medium","large"])
    #print bins
    Furer={}
    FFurer={}
    Random={}
    
    Furer_patt_size={}
    Ffurer_patt_size={}
    Random_patt_size={}
    
    for n in pattern_sizes:
        print "Patt size: ",n
        path_to_exhaustive_csv=path_to_csvs+"/exhaustive_"+str(n)+".csv"
        path_to_Furer=path_to_csvs+"/furer_"+str(n)+".csv"
        path_to_FFurer=path_to_csvs+"/Ffurer_"+str(n)+".csv"
        path_to_Random=path_to_csvs+"/random_"+str(n)+".csv"
        print "Path to Furer: ",path_to_Furer
        furer_patt_size=emb_function_of_decomp_length(path_to_exhaustive_csv,n,path_to_Furer)
        ffurer_patt_size=emb_function_of_decomp_length(path_to_exhaustive_csv,n,path_to_FFurer)
        random_patt_size=emb_function_of_decomp_length(path_to_exhaustive_csv,n,path_to_Random)
        
        Furer_patt_size[n]=furer_patt_size
        Ffurer_patt_size[n]=ffurer_patt_size
        Random_patt_size[n]=random_patt_size
        
        for k in furer_patt_size.keys():
            if not k in Furer.keys():
                Furer[k]=[]
            else:
                Furer[k].extend(furer_patt_size[k])
        for k in ffurer_patt_size.keys():
            if not k in FFurer.keys():
                FFurer[k]=[]
            else:
                FFurer[k].extend(ffurer_patt_size[k])
        for k in random_patt_size.keys():
            if not k in Random.keys():
                Random[k]=[]
            else:
                Random[k].extend(random_patt_size[k])
    


    fig = plt.figure()
    plt.subplots_adjust(wspace=0.5,hspace=0.5)
    iplot = 230
    for i in range(len(pattern_sizes)):
        iplot += 1
        level=pattern_sizes[i]
        all_obd_decomp_sizes=Furer_patt_size[level].keys()
        
        averagesFurer=[]
        stdFurer=[]
        
        averagesFfurer=[]
        stdFfurer=[]
        
        averagesRandom=[]
        stdRandom=[]
        
        counter=0
        for k in all_obd_decomp_sizes:
            print Furer_patt_size[level][k]
            print np.nanmean(Furer_patt_size[level][k])
            averagesFurer.append(np.nanmean(Furer_patt_size[level][k]))
            stdFurer.append(np.nanstd(Furer_patt_size[level][k]))
            
            averagesFfurer.append(np.nanmean(Ffurer_patt_size[level][k]))
            stdFfurer.append(np.nanstd(Ffurer_patt_size[level][k]))
            averagesRandom.append(np.nanmean(Random_patt_size[level][k]))
            stdRandom.append(np.nanstd(Random_patt_size[level][k]))
                        
        ax = fig.add_subplot(iplot)
        print all_obd_decomp_sizes
        ax.errorbar(all_obd_decomp_sizes, averagesFurer, color='blue',yerr=stdFurer,linewidth=3.5,elinewidth=2)
        ax.errorbar(all_obd_decomp_sizes, averagesFfurer, color='red',yerr=stdFurer,linewidth=3.5,elinewidth=2)
        #ax.errorbar(all_obd_decomp_sizes, averagesRandom, color='green',yerr=stdRandom,linewidth=3.5,elinewidth=2)
        #ax.plot(all_obd_decomp_sizes, averagesFurer,color='blue',linewidth=2)
        #ax.plot(all_obd_decomp_sizes, averagesFfurer,color='red',linewidth=2.0)
        
    plt.show()    
    
    
    
    
    
    
    
    
    
    
    
    
    
#         for t in xrange(0,(100+step_percentage),step_percentage):
#          if not t % 10==0:
#              stdev_furer_AD[t]=0
#              #if not exp=="dblp":
#              #  stdev_furer_AD_10[t]=0
#              stdev_furer_OBD[t]=0
#         
#         if i == 4:
#            #print "ovdje",exp
#            #ax = plt.subplot2grid((3,7), (i/2, 2), colspan=3)
#            ax = fig.add_subplot(iplot)
#            ax.set_ylabel('Avg_RelEr',size=25)
#            #ax = fig.add_subplot(iplot)
#            #ax.legend(['FK-OBD', 'FK-AD','Random'],loc = 'upper right', bbox_to_anchor = (0,0.5,1.0,0.5),prop={'size':16})    
#         else:
#         # You can be fancy and use subplot2grid for each plot, which dosen't
#         # require keeping the iplot variable:
#         # ax = subplot2grid((4,2), (i/2,i%2))
# 
#         # Or you can keep using add_subplot, which may be simpler:
#           ax = fig.add_subplot(iplot)
#         
#           if i==0 or i==2 or i==4:
#             ax.set_ylabel('Avg_RelEr',size=25)
#           
# 
#         #ax.set_yscale('log')
#         ax.set_title("Pattern size: "+str(level), fontsize=25)
#         ax.plot(x,avg_ERR_OBD,color='blue',linewidth=3.0)
#         ax.plot(x,avg_ERR_AD,color='red',linewidth=3.0)
#         print 'plotting: ',exp
#         print avg_ERR_OBD
#         print avg_ERR_AD
#         ax.errorbar(x, avg_ERR_OBD,yerr=stdev_furer_OBD, fmt='o',color='blue',linewidth=2)
#         ax.errorbar(x, avg_ERR_AD,yerr=stdev_furer_AD, fmt='o',color='red',linewidth=2.0)
#         ax.set_ylim([0,1])
#         zed = [tick.label.set_fontsize(25) for tick in ax.yaxis.get_major_ticks()]
#         zed = [tick.label.set_fontsize(25) for tick in ax.xaxis.get_major_ticks()]
#         #ax.set_xticklabels(x,fontsize=25)
#         #ax.set_xticklabels(x,fontsize=20)
#         if i==0:
#                ax.legend(['FK-OBD', 'FK-AD'],loc = 'upper right', bbox_to_anchor = (0,0.5,1.02,0.5),prop={'size':16}, ncol=2)
#             #ax.legend(['FK-OBD', 'FK-AD','FK-AD-10','Random'],prop={'size':15})    
#         axis_counter+=1
#     #ax = fig.add_subplot(iplot)
#     fig.add_subplot(111, frameon=False)     
# 
# 
#     plt.xlabel('% exhaustive runtime',size=25)
#     plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off',labelsize=30)
#        
       
 
 
if __name__ == '__main__':
     collect_stat_relative_error_size_of_OBD("sampl_iteration_All.png","YEAST","/home/irma/workspace/DMKD_Paper_Sampling/dblp_csvs/",[5,6,7,8,9,10])
