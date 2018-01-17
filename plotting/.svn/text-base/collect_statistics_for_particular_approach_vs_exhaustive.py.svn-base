'''
Created on Jan 17, 2016

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

def isMissing(v1):
    if isinstance(v1, float) and math.isnan(v1):
        return True
    if not v1:
        return True
    if float(v1)<0:
        return True
    return False

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
        
    #print "MEAN: ",np.mean(rel_errors)
    return rel_errors




def normalize(array):
    maxV=max(array)
    minV=min(array)
    norm=[]
    for x in array:
        norm.append((x-minV)/maxV-minV)
    return norm

def normalize1(array,minV,maxV):
    norm=[]
    for x in array:
        norm.append((x-minV)/maxV-minV)
    return norm

def collect_KLDs_for_pattern_size_final_selected(bins,discretizing_column,path_to_exhaustive_csv,pattern_size,path_to_approach):
   array_of_KLD_approachX=[]
   appr_small=[]
   appr_medium=[]
   appr_large=[]
   with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)   
       for row in reader:
         array_values_appx=[] 
         name_of_patterns='/'.join(row["pattern_name"].split("/")[:-1])
         with open(path_to_approach) as appX:
              reader1 = csv.DictReader(appX)  
              for row1 in reader1:
                  if('/'.join(row1["pattern_name"].split("/")[:-1])==name_of_patterns):
                      #print row1["pattern_name"]
                      #print "KLD:",row1["KLD_120"]
                      kld=row1["KLD_120"]
                      if kld:
                        KLD=float(row1["KLD_120"])
                      else:
                        continue
                      nr_emb_exhaustive=float(row["exh_emb"])
                      discretizing=float(row[discretizing_column])
                      exhDiscretized= pd.cut(np.array([discretizing]),bins,include_lowest=True,labels=["small","medium","large"])
                      if(exhDiscretized=="small"):
                        appr_small.append(KLD)
                      if(exhDiscretized=="medium"):
                        appr_medium.append(KLD)
                      if(exhDiscretized=="large"):
                        appr_large.append(KLD)
                      break      
                  
   print np.mean(appr_small),np.mean(appr_medium),np.mean(appr_large)
   return np.mean(appr_small),np.mean(appr_medium),np.mean(appr_large)

'''
COLLECTING AVERAGE NORMALIZED KLDS OVER ALL PATTERNS
'''                
def collect_KLDs_for_pattern_size_final(path_to_exhaustive_csv,pattern_size,path_to_approach):
   array_of_final_kld_approachX=[] 

   #print "APPROACH: ",path_to_approach
   with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)   
       for row in reader:
         if row["timeout"]==True:
             continue
         array_values_appx=[]
         name_of_patterns2=None
         for s in row["pattern_name"].split("/"):
                      if "pattern_" in s:
                          name_of_patterns2=s
         #print path_to_approach
         with open(path_to_approach) as appX:
                  reader1 = csv.DictReader(appX)  
                  for row1 in reader1:
                      
                      name_of_patterns1=None
                      for s in row1["pattern_name"].split("/"):
                          #print s
                          if "pattern_" in s:
                              name_of_patterns1=s
                      #print name_of_patterns1
                      if(name_of_patterns1==name_of_patterns2):
                          #print row1
                          if(not(row1["KLD_"+str(120)])):
                              continue
                          array_of_final_kld_approachX.append(float(row1["KLD_"+str(120)])) 
                          #print "hey hoy",float(row1["KLD_"+str(120)])

   return np.nanmean(array_of_final_kld_approachX),np.nanstd(array_of_final_kld_approachX)           
              
def collect_average_nr_5_minute_interval_for_less_than_5_percent_error(path_to_exhaustive_csv,pattern_size,path_to_approach):
   with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       iterations=[]   
       for row in reader:
         if(not(row["exh_emb"])):
             continue
         nr_emb_exhaustive=float(row["exh_emb"])
         name_of_patterns='/'.join(row["pattern_name"].split("/")[:-1])
         with open(path_to_approach) as appX:
              reader1 = csv.DictReader(appX)  
              for row1 in reader1:
                  if('/'.join(row1["pattern_name"].split("/")[:-1])==name_of_patterns):
                      for i in range(1,121):
                          value=row1["emb_"+str(i)]
                          #print i,value,nr_emb_exhaustive,math.fabs(float(value)-nr_emb_exhaustive),(nr_emb_exhaustive*5)/100
                          if value:
                              difference=math.fabs(float(value)-nr_emb_exhaustive)
                              if(difference<=((nr_emb_exhaustive*5)/100)):
                                 iterations.append(i)
                                 break      
   print "ITERATIONS:",iterations
   return np.mean(iterations)           

'''
For each pattern result calculate average nr embeddings for all time intervals.
Then calculate relative error of the average estimate.
Report: average relative error on number of embeddings for all the patterns
'''
def collect_EMB_for_pattern_size_average_bins(bins,discretizing_column,path_to_exhaustive_csv,pattern_size,path_to_approach):
   array_of_nr_emb_exhaustive=[]
   array_of_final_nr_emb_approachX=[]
   exh_small=[]
   exh_medium=[]
   exh_large=[]
   appr_small=[]
   appr_medium=[]
   appr_large=[]
   with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)   
       for row in reader:
         array_values_appx=[]
         
         name_of_patterns='/'.join(row["pattern_name"].split("/")[:-1])
        
         with open(path_to_approach) as appX:
              reader1 = csv.DictReader(appX)  
              for row1 in reader1:
                  if('/'.join(row1["pattern_name"].split("/")[:-1])==name_of_patterns):
                      array_of_nr_emb_exhaustive.append(row["exh_emb"])
                      nr_emb_exhaustive=float(row["exh_emb"])
                      sum=0
                      i=0
                      for i in range(1,121):
                          value=row1["emb_"+str(i)]
                          if value:
                              i+=1
                              sum+=float(value)
                      avg=sum/i
                      discretizing=float(row[discretizing_column])
                      exhDiscretized= pd.cut(np.array([discretizing]),bins,include_lowest=True,labels=["small","medium","large"])
                      if(exhDiscretized=="small"):
                        appr_small.append(avg)
                        exh_small.append(nr_emb_exhaustive)
                      if(exhDiscretized=="medium"):
                        appr_medium.append(avg)
                        exh_medium.append(nr_emb_exhaustive)
                      if(exhDiscretized=="large"):
                        appr_large.append(avg)
                        exh_large.append(nr_emb_exhaustive)
                      break      
                  

   relative_error_appr_small=calculate_Relative_Errors_exhaustive(exh_small, appr_small)
   relative_error_appr_medium=calculate_Relative_Errors_exhaustive(exh_medium, appr_medium)
   relative_error_appr_large=calculate_Relative_Errors_exhaustive(exh_large, appr_large)
   print np.mean(relative_error_appr_small),np.mean(relative_error_appr_medium),np.mean(relative_error_appr_large)
   return np.mean(relative_error_appr_small),np.mean(relative_error_appr_medium),np.mean(relative_error_appr_large)
      
def no_obdecomp(n,OBD):
    obd=ast.literal_eval(OBD)
    if len(obd)==n:
        return True
    else:
        return False
                
def collect_EMB_for_pattern_size_average(path_to_exhaustive_csv,pattern_size,path_to_approach):
   array_of_nr_emb_exhaustive=[]
   array_of_final_nr_emb_approachX=[]
   number_of_patterns=0
   row_number=0
   nr_timeout=0
   with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)   
       for row in reader:
         if row["timeout"]==str(True):
             nr_timeout+=1
             continue
         array_values_appx=[]
         #print row["pattern_name"]
         name_of_patterns=None
         for s in row["pattern_name"].split("/"):
             if "pattern_" in s:
                 name_of_patterns=s
         
         #print "NAME OF PATTERN",name_of_patterns
         with open(path_to_approach) as appX:
              reader1 = csv.DictReader(appX)  
              for row1 in reader1:                 
                  #print row1["emb_1"]
                  if not row_number>0:
                      row_number+=1
                  #print row1["pattern_name"].split("/")
                  #print "P",'/'.join(row1["pattern_name"].split("/")[:-2]),"A",name_of_patterns
                  name_of_patterns2=None
                  for s in row1["pattern_name"].split("/"):
                      if "pattern_" in s:
                          name_of_patterns2=s
                  if(name_of_patterns2==name_of_patterns):
                      #print row1
                      #print name_of_patterns,name_of_patterns2
                      #if not no_obdecomp(pattern_size,row1["OBD"]):
                      #       continue
                      number_of_patterns+=1  
                      #print row
                     # value=row1["emb_1"]
                      #print "Value: ",value
                     # if value:
                               #print value
                     #          array_values_appx.append(float(value))
                      array_of_nr_emb_exhaustive.append(float(row["exh_emb"]))
                      #array_values_appx.append(float(row1["emb_120"]))
                      for i in range(1,121):
                        value=row1["emb_"+str(i)]
                        if value:
                           array_values_appx.append(float(value))
                        #print "Appending: ",value
                        #if value:
                        #    array_values_appx.append(float(value))
                     
                      #print name_of_patterns,value
                      array_of_final_nr_emb_approachX.append(np.mean(array_values_appx)) 
                      break

   print "APPROACH:",path_to_approach
   print array_of_final_nr_emb_approachX
   print "NUMBER OF PATTERNS FOR RANDOM: ",number_of_patterns
   print "NUMBER OF ROWS FOR RANDOM: ",row_number
   print "NUMBER OF TIMEOUT PATTERNS: ",nr_timeout
   relative_error_appr_small=calculate_Relative_Errors_exhaustive(array_of_nr_emb_exhaustive, array_of_final_nr_emb_approachX)
   counter=1
   for a in relative_error_appr_small:
       #print counter, a
       counter+=1
   return (np.mean(relative_error_appr_small),np.std(relative_error_appr_small))
 

def plotRMSE_function_of_pattern_size(title,out_file,RMSEFurer,RMSEFFurer,RMSEFFurer_ord,RMSERandom,STDFurer,STDFFurer,STDFFurer_ord,STDRandom,init_patt_size,end_patt_size,ylabel_string,title_string,legend_x,legend_y,logScaleFlag=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if logScaleFlag:
        print "Log scale!"
        ax.set_yscale('symlog',nonposy='clip')
    ind = np.array([x for x in range(init_patt_size,end_patt_size+1)])             # the x locations for the groups
    print ind
    width = 0.2    
    rects1 = ax.bar(ind-width, RMSEFurer, width,
                color='blue',
                error_kw=dict(elinewidth=2.3,ecolor='green'),yerr=STDFurer)
    
    
    rects2 = ax.bar(ind, RMSEFFurer, width,
                    color='black',
                    error_kw=dict(elinewidth=2.3,ecolor='green'),yerr=STDFFurer)
    
    rects3 = ax.bar(ind+width, RMSEFFurer_ord, width,
                    color='green',
                    error_kw=dict(elinewidth=2.3,ecolor='green'),yerr=STDFFurer_ord)
     
    rects4 = ax.bar(ind+2*width, RMSERandom, width,
                    color='red',
                    error_kw=dict(elinewidth=2.3,ecolor='green'),yerr=STDRandom)
    
   

#     max_value=0
#     max_value=max(RMSEFurer)
#     if(max(RMSEFFurer)>max_value):
#         max_value=max(RMSEFFurer)
#     if(max(RMSERandom)>max_value):
#         max_value=max(RMSERandom)
#     
#     if(max(RMSEFFurer_ord)>max_value):
#         max_value=max(RMSEFFurer_ord)
# 
#     ax.set_xlim(init_patt_size-width,end_patt_size+2*width)
#     if logScaleFlag:
#         ax.set_ylim(0,math.log(max_value)+(math.log(max_value)/100))
#     if not logScaleFlag:
#         #plt.ylim(1E1,1E4)
#         ax.set_ylim(0,max_value+(max_value/100))
        
    ax.set_ylabel(ylabel_string,fontsize=25)
    ax.set_xlabel("Pattern size",fontsize=25)
    ax.set_title(title_string,fontsize=25)
    xTickMarks = [str(i) for i in range(init_patt_size,end_patt_size+1)]
    ax.set_xticks(ind)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=20)
    plt.title(title)
    zed = [tick.label.set_fontsize(20) for tick in ax.yaxis.get_major_ticks()]
    print "FK-OBD:",RMSEFurer,"std: ",STDFurer
    print "FK-AD:", RMSEFFurer,"std: ",STDFFurer
    print "FK-AD-ORD:", RMSEFFurer_ord,"std: ",STDFFurer_ord
    print "Random:",STDRandom,"std: ",STDRandom
    ax.legend((rects1[0], rects2[0],rects3[0],rects4[0]),('FK-OBD', 'FK-AD','FK-AD-ORD','Random'),bbox_to_anchor=(legend_x,legend_y),prop={'size':15})
    fig.tight_layout()
    
    
def plotRMSE_function_of_pattern_size_normal_line(title,out_file,RMSEFurer,RMSEFFurer,RMSERandom,STDFurer,STDFFurer,STDRandom,init_patt_size,end_patt_size,ylabel_string,title_string,legend_x,legend_y,logScaleFlag=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if logScaleFlag:
        ax.set_yscale('log',nonposy='clip')
    ind = np.array([x for x in range(init_patt_size,end_patt_size+1)])             # the x locations for the groups
    max_value=0
    max_value=max(RMSEFurer)
    if(max(RMSEFFurer)>max_value):
        max_value=max(RMSEFFurer)
    if(max(RMSERandom)>max_value):
        max_value=max(RMSERandom)

    for i in xrange(0,len(STDFurer)):    
        STDFurer[i]=0.434*STDFurer[i]/RMSEFurer[i]
        if logScaleFlag and math.log(STDFurer[i])<0:
            STDFurer[i]=1
    for i in xrange(0,len(STDFFurer)):
        STDFFurer[i]=0.434*STDFFurer[i]/RMSEFFurer[i]
        if logScaleFlag and math.log(STDFFurer[i])<0:
            STDFFurer[i]=1
    for i in xrange(0,len(STDRandom)):
        STDRandom[i]=0.434*STDRandom[i]/RMSERandom[i]
        if logScaleFlag and math.log(STDRandom[i])<0:
            STDRandom[i]=1

    print "FURER: ",RMSEFurer
    print "FFUERE: ",RMSEFFurer
    print "RANDOM: ",RMSERandom
    plt.plot(ind, RMSEFurer,color='blue',linewidth=3)
    plt.errorbar(ind,RMSEFurer,yerr=STDFurer, fmt='o',color='blue',linewidth=3)

    plt.plot(ind, RMSEFFurer,color='black',linewidth=3)
    plt.errorbar(ind,RMSEFFurer,yerr=STDFFurer, fmt='o',color='black',linewidth=3)
  
    plt.plot(ind, RMSERandom,color='red',linewidth=3)
    plt.errorbar(ind,RMSERandom,yerr=STDRandom, fmt='o',color='red',linewidth=3)
    
    ax.set_xlim([4,15])
    #if logScaleFlag:
    #    ax.set_ylim(0,math.log(max_value)+(math.log(max_value)/100))
    #if not logScaleFlag:
        #
    #    ax.set_ylim(0,max_value+(max_value/100))

        
    plt.ylabel(ylabel_string,fontsize=25)
    plt.xlabel("Pattern size",fontsize=20)
    plt.title(title_string,fontsize=20)
    xTickMarks = [str(i) for i in range(init_patt_size,end_patt_size+1)]
    ax.set_xticks(ind)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=20)
    zed = [tick.label.set_fontsize(20) for tick in ax.yaxis.get_major_ticks()]
    plt.legend(('Furer-OBD', 'Furer-AD','Random'),bbox_to_anchor=(legend_x,legend_y),prop={'size':15})
    plt.show()
    
def subplotRMSE_function_of_pattern_size(title,name,ylabel,Small_Furer,Small_FFurer,Small_Random,Medium_Furer,Medium_FFurer,Medium_Random,Large_Furer,Large_FFurer,Large_Random,init_patt_size,end_patt_size,ylabel_string,title_string,legend_x,legend_y,right_side_label,logScaleFlag=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ind = np.array([x for x in range(init_patt_size,end_patt_size+1)])             # the x locations for the groups
    width = 0.2    
    left, width = .25, .2
    bottom, height = .25, .5
    right = left + 0.77
    top = bottom + height

    max_value_small=np.nanmax(Small_Furer+Small_FFurer+Small_Random)
    max_value_medium=np.nanmax(Medium_Furer+Medium_FFurer+Medium_Random)
    max_value_large=np.nanmax(Large_Furer+Large_FFurer+Large_Random)
    
    
    print "Max value small: ",max_value_small
    ax1=plt.subplot(3,1,1)
    ax1.set_ylim(1e-4, 1e5)
    if logScaleFlag:
        ax1.set_yscale('log')
        
    print "SMALL FURER: ",Small_Furer    
    rects1small = ax1.bar(ind-width, Small_Furer, width,
                color='black',log=True)

    
    rects2small = ax1.bar(ind, Small_FFurer, width,
                    color='red',log=True)
    
    rects3small = ax1.bar(ind+width, Small_Random, width,
                     color='green',log=True)
 
    ax1.text(right, top+0.25, right_side_label+'=small',
         horizontalalignment='center',
         verticalalignment='top',
         rotation='vertical',
         transform=ax.transAxes,
         fontsize=20)

    ax1.set_xlim(init_patt_size-width,end_patt_size+2*width)
    if not logScaleFlag:
      ax1.set_ylim(0,max_value_small+(max_value_small/100))
    ax1.set_ylabel(ylabel,fontsize=25)
    ax1.set_xlabel("Pattern size",fontsize=20)
    ax1.set_title(title,fontsize=20)
    xTickMarks = [str(i) for i in range(init_patt_size,end_patt_size+1)]
    ax1.set_xticks(ind)
    xtickNames = ax1.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=15)
    zed = [tick.label.set_fontsize(20) for tick in ax1.yaxis.get_major_ticks()]
    ax1.legend((rects1small[0], rects2small[0],rects3small[0]),('Furer-OBD', 'Furer-AD','Random'),bbox_to_anchor=(legend_x,legend_y),prop={'size':15})
    
    ax2=plt.subplot(3,1,2)
    ax2.set_ylim(1e-4, 1e5)
    if logScaleFlag:
        ax2.set_yscale('log')
    rects1 = ax2.bar(ind-width, Medium_Furer, width,
                color='black',
                error_kw=dict(elinewidth=2,ecolor='red'))

    
    rects2 = ax2.bar(ind, Medium_FFurer, width,
                    color='red',
                    error_kw=dict(elinewidth=2,ecolor='black'))
    
    rects3 = ax2.bar(ind+width, Medium_Random, width,
                    color='green',
                    error_kw=dict(elinewidth=2,ecolor='green'))
    
    ax2.text(right, 0.5*(bottom+top), right_side_label+'=medium',
        horizontalalignment='center',
        verticalalignment='center',
        rotation='vertical',
        transform=ax.transAxes,
        fontsize=20)


    ax2.set_xlim(init_patt_size-width,end_patt_size+2*width)
    if not logScaleFlag:
      ax2.set_ylim(0,max_value_medium+(max_value_medium/100))
      
    ax2.set_ylabel(ylabel,fontsize=25)
    ax2.set_xlabel("Pattern size",fontsize=20)
    #ax2.set_title(title_string,fontsize=20)
    xTickMarks = [str(i) for i in range(init_patt_size,end_patt_size+1)]
    ax2.set_xticks(ind)
    xtickNames = ax2.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=15)
    
    zed = [tick.label.set_fontsize(20) for tick in ax2.yaxis.get_major_ticks()]
    ax2.legend((rects1[0], rects2[0],rects3[0]),('Furer-OBD', 'Furer-AD','Random'),bbox_to_anchor=(legend_x,legend_y),prop={'size':15})
    
    ax3=plt.subplot(3,1,3)
    ax3.set_ylim(1e-4, 1e5)
    if logScaleFlag:
        ax3.set_yscale('log')
    rects1 = ax3.bar(ind-width, Large_Furer, width,
                color='black',
                error_kw=dict(elinewidth=2,ecolor='red'))

    
    rects2 = ax3.bar(ind, Large_FFurer, width,
                    color='red',
                    error_kw=dict(elinewidth=2,ecolor='black'))
    
    rects3 = ax3.bar(ind+width, Large_Random, width,
                    color='green',
                    error_kw=dict(elinewidth=2,ecolor='green'))

    ax3.set_xlim(init_patt_size-width,end_patt_size+2*width)
    if not logScaleFlag:
      ax3.set_ylim(0,max_value_large+(max_value_large/100))
    ax3.set_ylabel(ylabel,fontsize=25)
    ax3.set_xlabel("Pattern size",fontsize=20)
    ax3.text(right, top-height-0.1, right_side_label+'=large',
        horizontalalignment='center',
        verticalalignment='center',
        rotation='vertical',
        transform=ax.transAxes,fontsize=20)
    #ax3.set_title(title_string,fontsize=20)
    xTickMarks = [str(i) for i in range(init_patt_size,end_patt_size+1)]
    ax3.set_xticks(ind)
    xtickNames = ax3.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=15)
    #print "Setting title to: ",title
    #plt.title(title)
    zed = [tick.label.set_fontsize(20) for tick in ax3.yaxis.get_major_ticks()]
    ax3.legend((rects1[0], rects2[0],rects3[0]),('Furer-OBD', 'Furer-AD','Random'),bbox_to_anchor=(legend_x,legend_y),prop={'size':15})
    plt.savefig(name,bbox_inches='tight')
    plt.yscale('log', nonposy='clip')
    plt.show()
    
    
def subplot_RMSE_furer_ffurer_ffurer_ord(title,name,ylabel,Small_Furer,Small_FFurer,Small_FFurer_ord,Medium_Furer,Medium_FFurer,Medium_FFurer_ord,Large_Furer,Large_FFurer,Large_FFurer_ord,init_patt_size,end_patt_size,ylabel_string,title_string,legend_x,legend_y,right_side_label,logScaleFlag=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ind = np.array([x for x in range(init_patt_size,end_patt_size+1)])             # the x locations for the groups
    width = 0.2    
    left, width = .25, .2
    bottom, height = .25, .5
    right = left + 0.77
    top = bottom + height

    max_value_small=np.nanmax(Small_Furer+Small_FFurer+Small_FFurer_ord)
    max_value_medium=np.nanmax(Medium_Furer+Medium_FFurer+Medium_FFurer_ord)
    max_value_large=np.nanmax(Large_Furer+Large_FFurer+Large_FFurer_ord)
    
    
    print "Max value small: ",max_value_small
    ax1=plt.subplot(3,1,1)
    ax1.set_ylim(1e-4, 1e5)
    if logScaleFlag:
        ax1.set_yscale('log')
        
    print "SMALL FURER: ",Small_Furer    
    rects1small = ax1.bar(ind-width, Small_Furer, width,
                color='black',log=True)

    
    rects2small = ax1.bar(ind, Small_FFurer, width,
                    color='red',log=True)
    
    rects3small = ax1.bar(ind+width, Small_FFurer_ord, width,
                     color='green',log=True)
 
    ax1.text(right, top+0.25, right_side_label+'=small',
         horizontalalignment='center',
         verticalalignment='top',
         rotation='vertical',
         transform=ax.transAxes,
         fontsize=20)

    ax1.set_xlim(init_patt_size-width,end_patt_size+2*width)
    if not logScaleFlag:
      ax1.set_ylim(0,max_value_small+(max_value_small/100))
    ax1.set_ylabel(ylabel,fontsize=25)
    ax1.set_xlabel("Pattern size",fontsize=20)
    ax1.set_title(title,fontsize=20)
    xTickMarks = [str(i) for i in range(init_patt_size,end_patt_size+1)]
    ax1.set_xticks(ind)
    xtickNames = ax1.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=15)
    zed = [tick.label.set_fontsize(20) for tick in ax1.yaxis.get_major_ticks()]
    ax1.legend((rects1small[0], rects2small[0],rects3small[0]),('Furer-OBD', 'Furer-AD','Random'),bbox_to_anchor=(legend_x,legend_y),prop={'size':15})
    
    ax2=plt.subplot(3,1,2)
    ax2.set_ylim(1e-4, 1e5)
    if logScaleFlag:
        ax2.set_yscale('log')
    rects1 = ax2.bar(ind-width, Medium_Furer, width,
                color='black',
                error_kw=dict(elinewidth=2,ecolor='red'))

    
    rects2 = ax2.bar(ind, Medium_FFurer, width,
                    color='red',
                    error_kw=dict(elinewidth=2,ecolor='black'))
    
    rects3 = ax2.bar(ind+width, Medium_FFurer_ord, width,
                    color='green',
                    error_kw=dict(elinewidth=2,ecolor='green'))
    
    ax2.text(right, 0.5*(bottom+top), right_side_label+'=medium',
        horizontalalignment='center',
        verticalalignment='center',
        rotation='vertical',
        transform=ax.transAxes,
        fontsize=20)


    ax2.set_xlim(init_patt_size-width,end_patt_size+2*width)
    if not logScaleFlag:
      ax2.set_ylim(0,max_value_medium+(max_value_medium/100))
      
    ax2.set_ylabel(ylabel,fontsize=25)
    ax2.set_xlabel("Pattern size",fontsize=20)
    #ax2.set_title(title_string,fontsize=20)
    xTickMarks = [str(i) for i in range(init_patt_size,end_patt_size+1)]
    ax2.set_xticks(ind)
    xtickNames = ax2.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=15)
    
    zed = [tick.label.set_fontsize(20) for tick in ax2.yaxis.get_major_ticks()]
    ax2.legend((rects1[0], rects2[0],rects3[0]),('Furer-OBD', 'Furer-AD','Random'),bbox_to_anchor=(legend_x,legend_y),prop={'size':15})
    
    ax3=plt.subplot(3,1,3)
    ax3.set_ylim(1e-4, 1e5)
    if logScaleFlag:
        ax3.set_yscale('log')
    rects1 = ax3.bar(ind-width, Large_Furer, width,
                color='black',
                error_kw=dict(elinewidth=2,ecolor='red'))

    
    rects2 = ax3.bar(ind, Large_FFurer, width,
                    color='red',
                    error_kw=dict(elinewidth=2,ecolor='black'))
    
    rects3 = ax3.bar(ind+width, Large_FFurer_ord, width,
                    color='green',
                    error_kw=dict(elinewidth=2,ecolor='green'))

    ax3.set_xlim(init_patt_size-width,end_patt_size+2*width)
    if not logScaleFlag:
      ax3.set_ylim(0,max_value_large+(max_value_large/100))
    ax3.set_ylabel(ylabel,fontsize=25)
    ax3.set_xlabel("Pattern size",fontsize=20)
    ax3.text(right, top-height-0.1, right_side_label+'=large',
        horizontalalignment='center',
        verticalalignment='center',
        rotation='vertical',
        transform=ax.transAxes,fontsize=20)
    #ax3.set_title(title_string,fontsize=20)
    xTickMarks = [str(i) for i in range(init_patt_size,end_patt_size+1)]
    ax3.set_xticks(ind)
    xtickNames = ax3.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=15)
    #print "Setting title to: ",title
    #plt.title(title)
    zed = [tick.label.set_fontsize(20) for tick in ax3.yaxis.get_major_ticks()]
    ax3.legend((rects1[0], rects2[0],rects3[0]),('Furer-OBD', 'Furer-AD','Furer-AD-10'),bbox_to_anchor=(legend_x,legend_y),prop={'size':15})
    plt.savefig(name,bbox_inches='tight')
    plt.yscale('log', nonposy='clip')
    plt.show()
 

def  collect_average_nr_5_minute_interval_for_less_than_5_percent_error_filter_patterns(bins,discretized_column_name,path_to_exhaustive_csv,pattern_size,path_to_approach):
     appr_small=[]
     appr_medium=[]
     appr_large=[]
     with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       iterations=[]   
       for row in reader:
         if(not(row["exh_emb"])):
             continue
         nr_emb_exhaustive=float(row["exh_emb"])
         discretizing_column=float(row[discretized_column_name])
         exhDiscretized= pd.cut(np.array([discretizing_column]),bins,include_lowest=True,labels=["small","medium","large"])
         #print " discretized as: ",exhDiscretized
         name_of_patterns='/'.join(row["pattern_name"].split("/")[:-1])
         with open(path_to_approach) as appX:
              reader1 = csv.DictReader(appX)  
              for row1 in reader1:
                  if('/'.join(row1["pattern_name"].split("/")[:-1])==name_of_patterns):
                      for i in range(1,121):
                          value=row1["emb_"+str(i)]
                          #print i,value,nr_emb_exhaustive,math.fabs(float(value)-nr_emb_exhaustive),(nr_emb_exhaustive*5)/100
                          if value:
                              difference=math.fabs(float(value)-nr_emb_exhaustive)
                              if(difference<=((nr_emb_exhaustive*5)/100)):
                                 if(exhDiscretized=="small"):
                                     appr_small.append(i)
                                 if(exhDiscretized=="medium"):
                                     appr_medium.append(i)
                                 if(exhDiscretized=="large"):
                                     appr_large.append(i)
                                 break      
     return np.mean(appr_small),np.mean(appr_medium),np.mean(appr_large)
     
def collect_stat_5_percent_error_iteration_number(file_name,dataset_name,path_to_csvs,pattern_sizes):
    RMSEFurerEMB_5_per=[]
    RMSEFFurerEMB_5_per=[]
    RMSERandomEMB_5_per=[]    
    init=pattern_sizes[0]
    end=pattern_sizes[-1]
    for n in xrange(init,end+1):
        print "Patt size: ",n
        path_to_exhaustive_csv=path_to_csvs+"/exhaustive_"+str(n)+".csv"
        path_to_Furer=path_to_csvs+"/furer_"+str(n)+".csv"
        path_to_FFurer=path_to_csvs+"/Ffurer_"+str(n)+".csv"
        path_to_Random=path_to_csvs+"/random_"+str(n)+".csv"
        patt_size=n 
        print "Furer .."
        #EMBEDDINGS
        RMSEFurerEMB_5_per.append(collect_average_nr_5_minute_interval_for_less_than_5_percent_error(path_to_exhaustive_csv,patt_size,path_to_Furer))
        RMSEFFurerEMB_5_per.append(collect_average_nr_5_minute_interval_for_less_than_5_percent_error(path_to_exhaustive_csv,patt_size,path_to_FFurer))
        RMSERandomEMB_5_per.append(collect_average_nr_5_minute_interval_for_less_than_5_percent_error(path_to_exhaustive_csv,patt_size,path_to_Random))
    plotRMSE_function_of_pattern_size(dataset_name,path_to_csvs+"/"+file_name,RMSEFurerEMB_5_per,RMSEFFurerEMB_5_per,RMSERandomEMB_5_per,init,end,"# T","",0.3,1,False)
    
def collect_stat_5_percent_error_iteration_number_satisfaction(file_name,dataset_name,path_to_csvs,pattern_names):
    RMSEFurerEMB_5_per=[]
    RMSEFFurerEMB_5_per=[]
    RMSERandomEMB_5_per=[]    

    for n in xrange(0,1):
        print "Patt size: ",n
        path_to_exhaustive_csv=path_to_csvs+"/exhaustive_"+str(n)+".csv"
        path_to_Furer=path_to_csvs+"/furer_"+str(n)+".csv"
        path_to_FFurer=path_to_csvs+"/Ffurer_"+str(n)+".csv"
        path_to_Random=path_to_csvs+"/random_"+str(n)+".csv"
        patt_size=n 
        print "Furer .."
        #EMBEDDINGS
        RMSEFurerEMB_5_per.append(collect_average_nr_5_minute_interval_for_less_than_5_percent_error(path_to_exhaustive_csv,patt_size,path_to_Furer))
        RMSEFFurerEMB_5_per.append(collect_average_nr_5_minute_interval_for_less_than_5_percent_error(path_to_exhaustive_csv,patt_size,path_to_FFurer))
        RMSERandomEMB_5_per.append(collect_average_nr_5_minute_interval_for_less_than_5_percent_error(path_to_exhaustive_csv,patt_size,path_to_Random))
    plotRMSE_function_of_pattern_size(dataset_name,path_to_csvs+"/"+file_name,RMSEFurerEMB_5_per,RMSEFFurerEMB_5_per,RMSERandomEMB_5_per,0,1,"# T","",0.3,1,False)
 
def plotRMSE_function_of_pattern_size_scatter_plot(title,out_file,RMSEFurer,RMSEFFurer,RMSERandom,STDFurer,STDFFurer,STDRandom,init_patt_size,end_patt_size,ylabel_string,title_string,legend_x,legend_y,logScaleFlag=False):
   fig = plt.figure()
   af = fig.add_subplot(111)
   #if logScaleFlag:
   #     af.set_yscale('log',nonposy='clip')
   x = np.array([x for x in range(init_patt_size,end_patt_size+1)])
   for i in xrange(0,len(STDFurer)):    
        STDFurer[i]=0.434*STDFurer[i]/RMSEFurer[i]
        if logScaleFlag and math.log(STDFurer[i])<0:
            STDFurer[i]=1
   for i in xrange(0,len(STDFFurer)):
        STDFFurer[i]=0.434*STDFFurer[i]/RMSEFFurer[i]
        if logScaleFlag and math.log(STDFFurer[i])<0:
            STDFFurer[i]=1
   for i in xrange(0,len(STDRandom)):
        STDRandom[i]=0.434*STDRandom[i]/RMSERandom[i]
        if logScaleFlag and math.log(STDRandom[i])<0:
            STDRandom[i]=1
   af.scatter(x, RMSEFurer, s=30, c='blue', marker="o", label='first')
   af.errorbar(x, RMSEFurer, yerr=STDFurer, fmt='o',c='blue')
   af.scatter(x,RMSEFFurer, s=30, c='red', marker="o", label='second')
   af.errorbar(x, RMSEFFurer, yerr=STDFFurer, fmt='o',c='red')
   af.scatter(x,RMSERandom, s=30, c='black', marker="o", label='second')
   af.errorbar(x, RMSERandom, yerr=STDRandom, fmt='o',c='black')
   plt.show()
   
def collect_stat_relative_error_average_results(file_name,dataset_name,path_to_csvs,pattern_sizes,metric):
    RMSEFurerEMB=[]
    RMSEFFurerEMB=[]
    RMSEFFurer_ordEMB=[]
    RMSERandomEMB=[] 
    StdFurerEMB=[]
    StdFFurerEMB=[]
    StdFFurer_ordEMB=[]
    StdRandomEMB=[]  
    init=pattern_sizes[0]
    end=pattern_sizes[-1]
    
    for n in pattern_sizes:
        print "Patt size: ",n
        path_to_exhaustive_csv=path_to_csvs+"/exhaustive_"+str(n)+".csv"
        path_to_Furer=path_to_csvs+"/furer_"+str(n)+".csv"
        path_to_FFurer=path_to_csvs+"/Ffurer_"+str(n)+".csv"
        path_to_FFurer_ord=path_to_csvs+"/Ffurer_order_random_"+str(n)+".csv"
        path_to_Random=path_to_csvs+"/random_"+str(n)+".csv"
        print path_to_Random
        patt_size=n 
        print "Furer .."
        #EMBEDDINGS
        print "furer ..."
        if metric=="emb":
           rmse,stde=collect_EMB_for_pattern_size_average(path_to_exhaustive_csv,patt_size,path_to_Furer)
           RMSEFurerEMB.append(rmse)
           StdFurerEMB.append(stde)
        elif metric=="kld":
           rmse,stde=collect_KLDs_for_pattern_size_final(path_to_exhaustive_csv,patt_size,path_to_Furer)
           RMSEFurerEMB.append(rmse)
           StdFurerEMB.append(stde)
          
        print "ffurer ..."
        if metric=="emb":
           rmse,stde=collect_EMB_for_pattern_size_average(path_to_exhaustive_csv,patt_size,path_to_FFurer)
           print "RMSE FFURER: ",rmse
           print "STD FFURER: ",stde
           RMSEFFurerEMB.append(rmse)
           StdFFurerEMB.append(stde)
        elif metric=="kld":
           rmse,stde=collect_KLDs_for_pattern_size_final(path_to_exhaustive_csv,patt_size,path_to_FFurer)
           RMSEFFurerEMB.append(rmse)
           StdFFurerEMB.append(stde)
          
        print "ffurer ordered..."
        if metric=="emb":
           rmse,stde=collect_EMB_for_pattern_size_average(path_to_exhaustive_csv,patt_size,path_to_FFurer_ord)
           print "RMSE FFURER ORDERED: ",rmse
           print "STD FFURER ORDERED: ",stde
           RMSEFFurer_ordEMB.append(rmse)
           StdFFurer_ordEMB.append(stde)
        elif metric=="kld":
           rmse,stde=collect_KLDs_for_pattern_size_final(path_to_exhaustive_csv,patt_size,path_to_FFurer_ord)
           print "RMSE FFURER ORDERED: ",rmse
           print "STD FFURER ORDERED: ",stde
           RMSEFFurer_ordEMB.append(rmse)
           StdFFurer_ordEMB.append(stde)

        print "random ..."
        if metric=="emb":
            rmse,stde=collect_EMB_for_pattern_size_average(path_to_exhaustive_csv,patt_size,path_to_Random)
            RMSERandomEMB.append(rmse)
            StdRandomEMB.append(stde)
        elif metric=="kld":
            rmse,stde=collect_KLDs_for_pattern_size_final(path_to_exhaustive_csv,patt_size,path_to_Random)
            RMSERandomEMB.append(rmse)
            StdRandomEMB.append(stde)
        y_axis=None
        if metric=="emb":
            y_axis="Avg_RelErr"
        elif metric=="kld":
            y_axis="log Avg_KLD"
    print RMSEFurerEMB
    print RMSEFFurerEMB
    print RMSERandomEMB
    print "STDs"
    print StdFurerEMB
    print StdFFurerEMB
    print StdRandomEMB
    plotRMSE_function_of_pattern_size(dataset_name,path_to_csvs+"/"+file_name,RMSEFurerEMB,RMSEFFurerEMB,RMSEFFurer_ordEMB,RMSERandomEMB,StdFurerEMB,StdFFurerEMB,StdFFurer_ordEMB,StdRandomEMB,init,end,y_axis,"",1.0,0.3,True)
 

def collect_stat_5_percent_error_iteration_number_selected_degree(dataset_name,path_to_csvs,pattern_sizes):
    all_degrees=utils.collect_all_degrees(path_to_csvs, min(pattern_sizes),max(pattern_sizes))
    arrayDiscretized,bins=pd.qcut(np.array(all_degrees), 3,retbins=True, labels=["small","medium","large"])
    print bins
    Furer_Small=[]
    Furer_Medium=[]
    Furer_Large=[]
    FFurer_Small=[]
    FFurer_Medium=[]
    FFurer_Large=[]
    Random_Small=[]
    Random_Medium=[]
    Random_Large=[]
    for n in pattern_sizes:
        print "Patt size: ",n
        path_to_exhaustive_csv=path_to_csvs+"/exhaustive_"+str(n)+".csv"
        path_to_Furer=path_to_csvs+"/furer_"+str(n)+".csv"
        path_to_FFurer=path_to_csvs+"/Ffurer_"+str(n)+".csv"
        path_to_Random=path_to_csvs+"/random_"+str(n)+".csv"
        print "Path to Furer: ",path_to_Furer
        furer_small,furer_medium,furer_large=collect_average_nr_5_minute_interval_for_less_than_5_percent_error_filter_patterns(bins,"max_degree",path_to_exhaustive_csv,n,path_to_Furer)
        ffurer_small,ffurer_medium,ffurer_large=collect_average_nr_5_minute_interval_for_less_than_5_percent_error_filter_patterns(bins,"max_degree",path_to_exhaustive_csv,n,path_to_FFurer)
        rnd_small,rnd_medium,rnd_large=collect_average_nr_5_minute_interval_for_less_than_5_percent_error_filter_patterns(bins,"max_degree",path_to_exhaustive_csv,n,path_to_Random)
        print furer_small,ffurer_small,rnd_small
        print furer_medium,ffurer_medium,rnd_medium
        print furer_large,ffurer_large,rnd_large
        Furer_Small.append(furer_small)
        Furer_Medium.append(furer_medium)
        Furer_Large.append(furer_large)
        FFurer_Small.append(ffurer_small)
        FFurer_Medium.append(ffurer_medium)
        FFurer_Large.append(ffurer_large)
        Random_Small.append(rnd_small)
        Random_Medium.append(rnd_medium)
        Random_Large.append(rnd_large)
    subplotRMSE_function_of_pattern_size(path_to_csvs+"/"+dataset_name+"_"+"Max_degree_filter_5PercentEmbErrorIterationNr.png","#T",Furer_Small, FFurer_Small, Random_Small, Furer_Medium, FFurer_Medium, Random_Medium, Furer_Large, FFurer_Large, Random_Large, min(pattern_sizes),max(pattern_sizes), "","",0.3,1,"md")
 
def collect_stat_relative_error_average_selected_degree(file_name,dataset_name,path_to_csvs,pattern_sizes):
    all_degrees=utils.collect_all_degrees(path_to_csvs, min(pattern_sizes),max(pattern_sizes))
    arrayDiscretized,bins=pd.qcut(np.array(all_degrees), 3,retbins=True, labels=["small","medium","large"])
    print bins
    Furer_Small=[]
    Furer_Medium=[]
    Furer_Large=[]
    FFurer_Small=[]
    FFurer_Medium=[]
    FFurer_Large=[]
    Random_Small=[]
    Random_Medium=[]
    Random_Large=[]
    for n in pattern_sizes:
        print "Patt size: ",n
        path_to_exhaustive_csv=path_to_csvs+"/exhaustive_"+str(n)+".csv"
        path_to_Furer=path_to_csvs+"/furer_"+str(n)+".csv"
        path_to_FFurer=path_to_csvs+"/Ffurer_"+str(n)+".csv"
        path_to_Random=path_to_csvs+"/random_"+str(n)+".csv"
        print "Path to Furer: ",path_to_Furer
        furer_small,furer_medium,furer_large=collect_EMB_for_pattern_size_average_bins(bins,"max_degree",path_to_exhaustive_csv,n,path_to_Furer)
        ffurer_small,ffurer_medium,ffurer_large=collect_EMB_for_pattern_size_average_bins(bins,"max_degree",path_to_exhaustive_csv,n,path_to_FFurer)
        rnd_small,rnd_medium,rnd_large=collect_EMB_for_pattern_size_average_bins(bins,"max_degree",path_to_exhaustive_csv,n,path_to_Random)
        print furer_small,ffurer_small,rnd_small
        print furer_medium,ffurer_medium,rnd_medium
        print furer_large,ffurer_large,rnd_large
        Furer_Small.append(furer_small)
        Furer_Medium.append(furer_medium)
        Furer_Large.append(furer_large)
        FFurer_Small.append(ffurer_small)
        FFurer_Medium.append(ffurer_medium)
        FFurer_Large.append(ffurer_large)
        Random_Small.append(rnd_small)
        Random_Medium.append(rnd_medium)
        Random_Large.append(rnd_large)
    subplotRMSE_function_of_pattern_size(dataset_name,path_to_csvs+"/"+file_name,'ARE(#Emb)',Furer_Small, FFurer_Small, Random_Small, Furer_Medium, FFurer_Medium, Random_Medium, Furer_Large, FFurer_Large, Random_Large, min(pattern_sizes),max(pattern_sizes), "","",0.3,1,"md",True)
 


def collect_stat_5_percent_error_iteration_number_selected(file_name,dataset_name,path_to_csvs,pattern_sizes,selection_crit):
    right_side_axis=None
    discretizing=None
    if selection_crit=="nr_emb":
        all_emb_exhaustive=utils.collect_all_embeddings_exhaustive(path_to_csvs, min(pattern_sizes),max(pattern_sizes))
        arrayDiscretized,bins=pd.qcut(np.array(all_emb_exhaustive), 3,retbins=True, labels=["small","medium","large"])
        right_side_axis="#emb"
        discretizing="exh_emb"
    if selection_crit=="md":
        all_degrees=utils.collect_all_degrees(path_to_csvs, min(pattern_sizes),max(pattern_sizes))
        arrayDiscretized,bins=pd.qcut(np.array(all_degrees), 3,retbins=True, labels=["small","medium","large"])
        right_side_axis="md"
        discretizing="max_degree"
    Furer_Small=[]
    Furer_Medium=[]
    Furer_Large=[]
    FFurer_Small=[]
    FFurer_Medium=[]
    FFurer_Large=[]
    Random_Small=[]
    Random_Medium=[]
    Random_Large=[]
    for n in pattern_sizes:
        print "Patt size: ",n
        path_to_exhaustive_csv=path_to_csvs+"/exhaustive_"+str(n)+".csv"
        path_to_Furer=path_to_csvs+"/furer_"+str(n)+".csv"
        path_to_FFurer=path_to_csvs+"/Ffurer_"+str(n)+".csv"
        path_to_Random=path_to_csvs+"/random_"+str(n)+".csv"
        print "Path to Furer: ",path_to_Furer
        furer_small,furer_medium,furer_large=collect_average_nr_5_minute_interval_for_less_than_5_percent_error_filter_patterns(bins,discretizing,path_to_exhaustive_csv,n,path_to_Furer)
        ffurer_small,ffurer_medium,ffurer_large=collect_average_nr_5_minute_interval_for_less_than_5_percent_error_filter_patterns(bins,discretizing,path_to_exhaustive_csv,n,path_to_FFurer)
        rnd_small,rnd_medium,rnd_large=collect_average_nr_5_minute_interval_for_less_than_5_percent_error_filter_patterns(bins,discretizing,path_to_exhaustive_csv,n,path_to_Random)
        print furer_small,ffurer_small,rnd_small
        print furer_medium,ffurer_medium,rnd_medium
        print furer_large,ffurer_large,rnd_large
        Furer_Small.append(furer_small)
        Furer_Medium.append(furer_medium)
        Furer_Large.append(furer_large)
        FFurer_Small.append(ffurer_small)
        FFurer_Medium.append(ffurer_medium)
        FFurer_Large.append(ffurer_large)
        Random_Small.append(rnd_small)
        Random_Medium.append(rnd_medium)
        Random_Large.append(rnd_large)
    subplotRMSE_function_of_pattern_size(dataset_name,path_to_csvs+"/"+file_name+"_"+"5PercentEmbErrorIterationNr.png","#T",Furer_Small, FFurer_Small, Random_Small, Furer_Medium, FFurer_Medium, Random_Medium, Furer_Large, FFurer_Large, Random_Large, min(pattern_sizes),max(pattern_sizes), "","",0.3,1,right_side_axis,False)
   
        
def collect_stat_relative_error_average_results_selected(file_name,dataset_name,path_to_csvs,pattern_sizes,metric,selection):
    selection_crit=None
    right_axis_label=None
    if selection=="nr_emb":
       all_emb_exhaustive=utils.collect_all_embeddings_exhaustive(path_to_csvs, min(pattern_sizes),max(pattern_sizes))
       arrayDiscretized,bins=pd.qcut(np.array(all_emb_exhaustive), 3,retbins=True, labels=["small","medium","large"])
       selection_crit="exh_emb"
       right_axis_label="#emb"
    elif selection=="md":
       all_degrees=utils.collect_all_degrees(path_to_csvs, min(pattern_sizes),max(pattern_sizes))
       arrayDiscretized,bins=pd.qcut(np.array(all_degrees), 3,retbins=True, labels=["small","medium","large"])
       selection_crit="max_degree"
       right_axis_label="md"
    print arrayDiscretized,bins
    print "DOING METRIC: ",metric
    print "DOING SELECTION: ",selection
    Furer_Small=[]
    Furer_Medium=[]
    Furer_Large=[]
    FFurer_Small=[]
    FFurer_Medium=[]
    FFurer_Large=[]
    FFurer_ord_Small=[]
    FFurer_ord_Medium=[]
    FFurer_ord_Large=[]
    Random_Small=[]
    Random_Medium=[]
    Random_Large=[]
    for n in pattern_sizes:
        print "Patt size: ",n
        path_to_exhaustive_csv=path_to_csvs+"/exhaustive_"+str(n)+".csv"
        path_to_Furer=path_to_csvs+"/furer_"+str(n)+".csv"
        path_to_FFurer=path_to_csvs+"/Ffurer_"+str(n)+".csv"
        path_to_FFurer_ord=path_to_csvs+"/Ffurer_order_random_"+str(n)+".csv"
        path_to_Random=path_to_csvs+"/random_"+str(n)+".csv"
        print "Path to Furer: ",path_to_Furer
        if metric=="emb":
            furer_small,furer_medium,furer_large=collect_EMB_for_pattern_size_average_bins(bins,selection_crit,path_to_exhaustive_csv,n,path_to_Furer)
            ffurer_small,ffurer_medium,ffurer_large=collect_EMB_for_pattern_size_average_bins(bins,selection_crit,path_to_exhaustive_csv,n,path_to_FFurer)
            ffurer_small_ord,ffurer_medium_ord,ffurer_large_ord=collect_EMB_for_pattern_size_average_bins(bins,selection_crit,path_to_exhaustive_csv,n,path_to_FFurer_ord)
            rnd_small,rnd_medium,rnd_large=collect_EMB_for_pattern_size_average_bins(bins,selection_crit,path_to_exhaustive_csv,n,path_to_Random)
        elif metric=="kld":
            furer_small,furer_medium,furer_large=collect_KLDs_for_pattern_size_final_selected(bins,selection_crit,path_to_exhaustive_csv,n,path_to_Furer)
            ffurer_small,ffurer_medium,ffurer_large=collect_KLDs_for_pattern_size_final_selected(bins,selection_crit,path_to_exhaustive_csv,n,path_to_FFurer)
            ffurer_small_ord,ffurer_medium_ord,ffurer_large_ord=collect_KLDs_for_pattern_size_final_selected(bins,selection_crit,path_to_exhaustive_csv,n,path_to_FFurer_ord)
            rnd_small,rnd_medium,rnd_large=collect_KLDs_for_pattern_size_final_selected(bins,selection_crit,path_to_exhaustive_csv,n,path_to_Random)
        
        print "-----------------------"
        print furer_small,ffurer_small,rnd_small
        print furer_medium,ffurer_medium,rnd_medium
        print furer_large,ffurer_large,rnd_large
        print "------------------"
        Furer_Small.append(furer_small)
        Furer_Medium.append(furer_medium)
        Furer_Large.append(furer_large)
        FFurer_Small.append(ffurer_small)
        FFurer_Medium.append(ffurer_medium)
        FFurer_Large.append(ffurer_large)
        FFurer_ord_Small.append(ffurer_small_ord)
        FFurer_ord_Medium.append(ffurer_medium_ord)
        FFurer_ord_Large.append(ffurer_large_ord)
        Random_Small.append(rnd_small)
        Random_Medium.append(rnd_medium)
        Random_Large.append(rnd_large)
        y_axis=None
        if metric=="emb":
            y_axis="log(Avg_RelErr)"
        elif metric=="kld":
            y_axis="Avg_KLD"
    subplotRMSE_function_of_pattern_size(dataset_name,path_to_csvs+"/"+file_name,y_axis,Furer_Small, FFurer_Small, Random_Small, Furer_Medium, FFurer_Medium, Random_Medium, Furer_Large, FFurer_Large, Random_Large, min(pattern_sizes),max(pattern_sizes), "","",0.3,1,right_axis_label,True)
    subplot_RMSE_furer_ffurer_ffurer_ord(dataset_name,path_to_csvs+"/"+file_name,y_axis,Furer_Small, FFurer_Small, FFurer_ord_Small, Furer_Medium, FFurer_Medium, FFurer_ord_Medium, Furer_Large, FFurer_Large,FFurer_ord_Large, min(pattern_sizes),max(pattern_sizes), "","",0.3,1,right_axis_label,True)

    
def collect_KLD_selected(dataset_name,path_to_csvs,pattern_sizes):
    all_emb_exhaustive=utils.collect_all_embeddings_exhaustive(path_to_csvs, min(pattern_sizes),max(pattern_sizes))
    arrayDiscretized,bins=pd.qcut(np.array(all_emb_exhaustive), 3,retbins=True, labels=["small","medium","large"])
    Furer_Small=[]
    Furer_Medium=[]
    Furer_Large=[]
    FFurer_Small=[]
    FFurer_Medium=[]
    FFurer_Large=[]
    Random_Small=[]
    Random_Medium=[]
    Random_Large=[]
    for n in pattern_sizes:
        print "Patt size: ",n
        path_to_exhaustive_csv=path_to_csvs+"/exhaustive_"+str(n)+".csv"
        path_to_Furer=path_to_csvs+"/furer_"+str(n)+".csv"
        path_to_FFurer=path_to_csvs+"/Ffurer_"+str(n)+".csv"
        path_to_Random=path_to_csvs+"/random_"+str(n)+".csv"
        print "Path to Furer: ",path_to_Furer
        furer_small,furer_medium,furer_large=collect_KLDs_for_pattern_size_final_selected(bins,"exh_emb",path_to_exhaustive_csv,n,path_to_Furer)
        ffurer_small,ffurer_medium,ffurer_large=collect_KLDs_for_pattern_size_final_selected(bins,"exh_emb",path_to_exhaustive_csv,n,path_to_FFurer)
        rnd_small,rnd_medium,rnd_large=collect_KLDs_for_pattern_size_final_selected(bins,"exh_emb",path_to_exhaustive_csv,n,path_to_Random)
        print furer_small,ffurer_small,rnd_small
        print furer_medium,ffurer_medium,rnd_medium
        print furer_large,ffurer_large,rnd_large
        Furer_Small.append(furer_small)
        Furer_Medium.append(furer_medium)
        Furer_Large.append(furer_large)
        FFurer_Small.append(ffurer_small)
        FFurer_Medium.append(ffurer_medium)
        FFurer_Large.append(ffurer_large)
        Random_Small.append(rnd_small)
        Random_Medium.append(rnd_medium)
        Random_Large.append(rnd_large)
    subplotRMSE_function_of_pattern_size(path_to_csvs+"/"+dataset_name+"_"+"RelErrorEmb.png",'Avg_KLD',Furer_Small, FFurer_Small, Random_Small, Furer_Medium, FFurer_Medium, Random_Medium, Furer_Large, FFurer_Large, Random_Large, min(pattern_sizes),max(pattern_sizes), "","",0.3,1,"#emb",True)
        
        
 

if __name__ == '__main__':
    #avg_RelError
    #DBLP
    #collect_stat_relative_error_average_results("imdb_avgRelError_All.png","IMDB","/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/RESULTS/IMDB_results/csv_results/",[4,5,6,7,8,9,10],"emb")
    #collect_stat_relative_error_average_results_selected("dblp_avgRelError_nr_emb.png","DBLP","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15],"emb","nr_emb")
    #collect_stat_relative_error_average_selected_degree("dblp_avgRelError_max_degree.png","DBLP","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15],"emb")
    #collect_stat_relative_error_average_results("fb_avgRelError_All.png","FACEBOOK","/home/irma/workspace/DMKD_Paper_Sampling/facebook_csvs/csv_results/",[4,5,6,7,8,9,10],"emb")

    #YEAST
    #collect_stat_relative_error_average_results("yeast_avgRelError_All.png","YEAST","/home/irma/workspace/DMKD_Paper_Sampling/yeast_csvs/csv_results/",[4,5,6,7,8,9],"emb")
    #collect_stat_relative_error_average_results_selected("yeast_avgRelError_nr_emb.png","YEAST","/home/irma/workspace/Martin_Experiment/csv_results_YEAST/",[4,5,6,7,8,9,10,11,12,13,14],"emb","nr_emb")
    #collect_stat_relative_error_average_selected_degree("yeast_avgRelError_max_degree.png","YEAST","/home/irma/workspace/Martin_Experiment/csv_results_YEAST/",[4,5,6,7,8,9,10,11,12,13,14],"emb")
    
    #FACEBOOK
    #collect_stat_relative_error_average_results("fb_avgRelError_All.png","FACEBOOK","/home/irma/workspace/DMKD_Paper_Sampling/facebook_csvs/",[7,8,9,10],"emb")
    #collect_stat_relative_error_average_results_selected("fb_avgRelError_nr_emb.png","FACEBOOK","/home/irma/workspace/DMKD_Paper_Sampling/facebook_csvs/",[4,5,6,7,8,9,10],"emb","nr_emb")
    #collect_stat_relative_error_average_selected_degree("fb_avgRelError_max_degree.png","FACEBOOK","/home/irma/workspace/DMKD_Paper_Sampling/facebook_csvs/",[4,5,6,7,8,9,10],"emb")

    #avg_KLD
    #collect_stat_relative_error_average_results("dblp_avgRelError_All.png","DBLP","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15],"kld")
    #collect_stat_relative_error_average_results_selected("dblp_avgRelError_nr_emb.png","DBLP","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15],"kld","nr_emb")
    #collect_stat_relative_error_average_results_selected("dblp_avgRelError_max_degree.png","DBLP","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15],"kld","md")
    #collect_stat_relative_error_average_results("fb_avgRelError_All.png","FACEBOOK","/home/irma/workspace/DMKD_Paper_Sampling/facebook_csvs/csv_results/",[4,5],"kld")

    #YEAST
    #collect_stat_relative_error_average_results("yeast_avg_KLD_All.png","YEAST","/home/irma/workspace/DMKD_Paper_Sampling/yeast_csvs/",[4,5,6,7,8,9],"kld")
    #collect_stat_relative_error_average_results_selected("yeast_avg_KLD_nr_emb.png","YEAST","/home/irma/workspace/Martin_Experiment/csv_results_YEAST/",[4,5,6,7,8,9,10,11,12,13,14],"kld","nr_emb")
    #collect_stat_relative_error_average_results_selected("yeast_avg_KLD_max_degree.png","YEAST","/home/irma/workspace/Martin_Experiment/csv_results_YEAST/",[4,5,6,7,8,9,10,11,12,13,14],"kld","md")
   
    #FACEBOOK
    collect_stat_relative_error_average_results("fb_avg_KLD_All.png","FACEBOOK","/home/irma/workspace/DMKD_Paper_Sampling/facebook_csvs/",[4,5,6,7,8,9,10],"kld")

    
    
    #T
    #DBLP
    #collect_stat_5_percent_error_iteration_number("sampl_iteration_All.png","DBLP","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15])
    #collect_stat_5_percent_error_iteration_number_selected("sampl_iteration_nr_emb.png","DBLP","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15],"nr_emb")
    #collect_stat_5_percent_error_iteration_number_selected("sampl_iteration_md.png","DBLP","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15],"md")
    
    #YEAST
    #collect_stat_5_percent_error_iteration_number("sampl_iteration_All.png","YEAST","/home/irma/workspace/Martin_Experiment/csv_results_YEAST",[4,5,6,7,8,9,10,11,12,13,14])
    #collect_stat_5_percent_error_iteration_number_selected("sampl_iteration_nr_emb.png","YEAST","/home/irma/workspace/Martin_Experiment/csv_results_YEAST/",[4,5,6,7,8,9,10,11,12,13,14],"nr_emb")
    #collect_stat_5_percent_error_iteration_number_selected("sampl_iteration_md.png","YEAST","/home/irma/workspace/Martin_Experiment/csv_results_YEAST/",[4,5,6,7,8,9,10,11,12,13,14],"md")

    
    #DBLP PLOTS
    #collect_stat_5_percent_error_iteration_number_selected("dblp","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15])
    #collect_stat_5_percent_error_iteration_number("dblp","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15])
    #collect_stat_relative_error_average_results_selected("dblp","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15])
    #collect_stat_relative_error_average_results("dblp","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15])

    #YEAST PLOTS
    #collect_stat_5_percent_error_iteration_number("yeast","/home/irma/workspace/Martin_Experiment/csv_results_YEAST/",[4,5,6,7,8,9,10,11,12,13,14])
    #collect_stat_relative_error_average_results('yeast',"/home/irma/workspace/Martin_Experiment/csv_results_YEAST/",[4,5,6,7,8,9,10,11,12,13,14])
    #collect_stat_5_percent_error_iteration_number_selected("yeast","/home/irma/workspace/Martin_Experiment/csv_results_YEAST/",[4,5,6,7,8,9,10,11,12,13,14])
    #collect_stat_relative_error_average_results_selected("yeast","/home/irma/workspace/Martin_Experiment/csv_results_YEAST/",[4,5,6,7,8,9,10,11,12,13,14])
    
    #avg_RelError
    #SATISACTION
    #collect_stat_5_percent_error_iteration_number_satisfaction("satisfaction_iteration_All.png","SATISFACTION","/home/irma/workspace/Martin_Experiment/RESULTS/RESULTS_UNIVERSITY/csv_results",["R1","R2","R3","R4","R5","R6"])

    #collect_stat_relative_error_average_results("satisf_avgRelError_All.png","SATISFACTION","/home/irma/workspace/Martin_Experiment/RESULTS/RESULTS_UNIVERSITY/csv_results",[0],"emb",["R1","R2","R3","R4","R5","R6"])
    #collect_stat_relative_error_average_results("satsf_avgRelError_All.png","SATISFACTION","/home/irma/workspace/Martin_Experiment/RESULTS/RESULTS_UNIVERSITY/csv_results",[0],"kld")

    #collect_stat_relative_error_average_results_selected("dblp_avgRelError_nr_emb.png","DBLP","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15],"emb","nr_emb")
    #collect_stat_relative_error_average_selected_degree("dblp_avgRelError_max_degree.png","DBLP","/home/irma/workspace/Martin_Experiment/csv_results_DBLP/",[4,5,6,7,8,9,10,11,12,13,14,15],"emb")
    plt.show()