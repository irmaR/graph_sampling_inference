'''
Created on Jun 10, 2017

@author: irma
'''
'''
Created on Mar 15, 2016

@author: irma
'''
import argparse,csv,os,math
import matplotlib.pyplot as plt
import numpy as np


def get_embeddings_and_time_FACT(csv_file,dataset):
    embs=[]
    time=[]
    with open(csv_file,'r') as exh:
       print exh
       reader = csv.DictReader(exh)
       for row in reader:
          if row['pattern_name']==dataset:
              try:
                embs.append(float(row['emb']))
              except ValueError:
                embs.append(None)
              try:
                time.append(float(row['time']))
              except:
                time.append(None)
    return (embs,time)


def get_embeddings_and_time_exhaustive(csv_file,dataset):
    embs=[]
    with open(csv_file) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
          if row['pattern_name']==dataset:
              embs.append(float(row['exh_emb']))
    return embs


def get_desired_intervals(FACT_times,interval):
    intervals=[]
    
    for i in FACT_times:
        if i==None:
          intervals.append(None)
        else:
          print i,interval
          intervals.append(math.ceil(i/interval)+1)
    
    return intervals

def get_furer_emb_at_interval(csv_furer,desired_intervals,dataset):
    counter_row=0
    embs=[]
    with open(csv_furer,'r') as exh:
       reader = csv.DictReader(exh)
       for row in reader:
          if row['pattern_name']==dataset:
              if desired_intervals[counter_row]==None:
                  embs.append(None)
              else:
                  embs.append(float(row['emb_'+str(int(desired_intervals[counter_row]))]))
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
        nr=abs((float(v1)-float(v2)))/max([v1,v2])
        if not math.isnan(nr):
          rel_errors.append(nr)
        
    #print "MEAN: ",np.mean(rel_errors)
    return rel_errors
        

def plotRES(title,ResFurer,ResFact,datasets,xlabel,ylabel_string,title_string,legend_x,legend_y,logScaleFlag=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if logScaleFlag:
        plt.yscale('log', nonposy='clip')
    ind=np.array([x*3 for x in range(1,len(datasets)+1)])         # the x locations for the groups
    print ind
    width = 1

    max_value=0
    max_value=max(ResFurer)
    min_value=min(ResFurer)
    if(max(ResFurer)>max_value):
        max_value=max(ResFurer)
    if(max(ResFact)>max_value):
        max_value=max(ResFact)
   
    print ResFurer

    rects1 = ax.bar(ind - width, ResFurer, width,
                    zorder=1, color='blue',
                    error_kw=dict(elinewidth=2.3, ecolor='blue', zorder=2), ec='blue', fill=False, linewidth=2,fc='blue',hatch='\\\\\\')

    #rects1 = ax.bar(ind-width, ResFurer, width,color='blue',hatch='\\\\\\')

    rects2 = ax.bar(ind, ResFact, width,
                    zorder=1, color='black', ec='black', fill=False, fc='black',linewidth=2,
                    hatch='||||')
    
    #rects2 = ax.bar(ind, ResFact, width,color='black')
    
    
    if not logScaleFlag:
        #plt.ylim(1E1,1E4)
        ax.set_ylim(0,max_value+(max_value/100))
        
    ax.set_ylabel(ylabel_string,fontsize=30)
    ax.set_xlabel("Dataset ID",fontsize=30)
    ax.set_title(title_string,fontsize=30)
    xTickMarks =datasets
    ax.set_xticks(ind)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=25)
    plt.title(title)
    zed = [tick.label.set_fontsize(25) for tick in ax.yaxis.get_major_ticks()]
    ax.legend((rects1[0], rects2[0]),('FK-OBD', 'FACT'),loc = 'upper left',prop={'size':30})
    fig.tight_layout()
    
    
def plotRES_scatter_plot(title,ResFurer,ResFfurer,ResRandom,datasets,xlabel,ylabel_string,title_string,legend_x,legend_y,logScaleFlag=False):
   fig = plt.figure()
   af = fig.add_subplot(111)
   if logScaleFlag:
        af.set_yscale('log',nonposy='clip')
   x=np.array([x*2 for x in range(1,len(datasets)+1)])

   af.scatter(x, ResFurer, s=10, c='red', marker="o", label='first')
   af.scatter(x,ResFfurer, s=10, c='blue', marker="o", label='second')
   af.scatter(x,ResRandom, s=10, c='black', marker="o", label='second')
   plt.show()




def get_relative_error(N,M):
    return abs((float(N)-float(M)))/M

def getKLDS_per_dataset_name(csv_file):
    res_avg={}
    res_std={}
    with open(csv_file) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
           pattern_name=row["pattern_name"].split("/")[-2]
           #res[pattern_name]=row["KLD_120"]
           klds=[]
           for i in xrange(1,121):
             klds.append(float(row["KLD_"+str(i)]))
           avg_kld=np.mean(klds)
           stdev_kld=np.std(klds)
           res_avg[pattern_name]=avg_kld
           res_std[pattern_name]=stdev_kld
           
    return res_avg,res_std

def getrelErrors_per_dataset_name(csv_file,exhaustive_csv):
    res_avg_rel={}
    res_std_rel={}
    with open(exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
           pattern_name=row["pattern_name"].split("/")[-2]
           print "Calculating rel for: ",pattern_name
           print row["exh_emb"]
           nr_emb_exh=float(row["exh_emb"])
           with open(csv_file) as smpl:
               reader1 = csv.DictReader(smpl)
               for row1 in reader1:
                   pattern_name1=row1["pattern_name"].split("/")[-2]
                   if pattern_name==pattern_name1:
                       #emb_smpl=float(row1["emb_average"])
                       rel_errors=[]
                       for i in xrange(1,121):
                           rel_errors.append(get_relative_error(float(row1["emb_"+str(i)]),nr_emb_exh))
                       avg_rel_error=np.mean(rel_errors)
                       stdev_rel_error=np.std(rel_errors)
                       #emb_smpl=float(row1["emb_120"])
                       #rel_error=get_relative_error(emb_smpl,nr_emb_exh)
                       res_avg_rel[pattern_name]=avg_rel_error
                       res_std_rel[pattern_name]=stdev_rel_error
                       #print "patt name: ",pattern_name,nr_emb_exh,emb_smpl,rel_error
                       break
                       
    return res_avg_rel,res_std_rel
    

def main(path_to_csvs):
    #datasets_names_order=["S1","S3","S5","S2","S4","S6","R1","R2","R3","R4","R5","R6"]
    datasets_names_order_original=["R5","S5","R4","S4","R3","S3","R2","S2","R6","S6","R1","S1"]
    datasets_names_order_mapping=["R1","S1","R2","S2","R3","S3","R4","S4","R5","S5","R6","S6"]
    #datasets_names_order=["S1","S2","S6","R1","S3","R2","R6","S4","R3","S5","R4","R5"]
    
    FACT_per_dataset_embs={}
    FACT_per_dataset_time={}
    FURER_per_dataset={}
    Exhaustive_per_dataset={}
    interval=5
    
    
    for p in datasets_names_order_original:
        FACT_per_dataset_embs[p],FACT_per_dataset_time[p]=get_embeddings_and_time_FACT(os.path.join(path_to_csvs,'fact.csv'),p)
        Exhaustive_per_dataset[p]=get_embeddings_and_time_exhaustive(os.path.join(path_to_csvs,'exhaustive'+".csv"),p)
        #get desired intervals for furer
        print FACT_per_dataset_time[p]
        desired_intervals=get_desired_intervals(FACT_per_dataset_time[p],interval)
        FURER_per_dataset[p]=get_furer_emb_at_interval(os.path.join(path_to_csvs,'furer'+".csv"),desired_intervals,p)

    #calculate relative errors
    FURER_relative_errors_per_pattern_size={} 
    FACT_relative_errors_per_pattern_size={} 
    for p in datasets_names_order_original:
        furer_rel_error=calculate_relative_errors(Exhaustive_per_dataset[p],FURER_per_dataset[p])
        fact_rel_error=calculate_relative_errors(Exhaustive_per_dataset[p],FACT_per_dataset_embs[p])
        FURER_relative_errors_per_pattern_size[p]=furer_rel_error
        FACT_relative_errors_per_pattern_size[p]=fact_rel_error

    print FURER_relative_errors_per_pattern_size
    print FACT_relative_errors_per_pattern_size
    Furer_res=[]
    FACT_res=[]
    for p in datasets_names_order_original:
        Furer_res.append(FURER_relative_errors_per_pattern_size[p][0])
        FACT_res.append(FACT_relative_errors_per_pattern_size[p][0])
    plotRES("",Furer_res,FACT_res,datasets_names_order_mapping,"Dataset","Avg RelErr","",0.95,1)
    plt.show()
        
   


if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')  
  args = parser.parse_args()
  main('/home/irma/work/RESULTS/graph_sampling/satisfaction_results/')