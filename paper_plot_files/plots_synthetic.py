'''
Created on Mar 15, 2016

@author: irma
'''
import argparse,csv,os,math
import matplotlib.pyplot as plt
import numpy as np



def plotRES(title,ResFurer,ResFfurer,ResRandom,stdevFurer,stdevFfurer,stdevRandom,datasets,xlabel,ylabel_string,title_string,legend_x,legend_y,logScaleFlag=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if logScaleFlag:
        #plt.yscale('log', nonposy='clip')
        plt.yscale('log')
    ind=np.array([x*4 for x in range(1,len(datasets)+1)])         # the x locations for the groups
    print ind
    width = 1

    max_value=0
    max_value=max(ResFurer)
    min_value=min(ResFurer)
    if(max(ResFfurer)>max_value):
        max_value=max(ResFfurer)
    if(max(ResRandom)>max_value):
        max_value=max(ResRandom)
   
    if(min(ResFfurer)<min):
        min_value=min(ResFfurer)
    if(min(ResRandom)<min_value):
        min_value=max(ResRandom)
#     print "BEFORE: ",STDFurer
#     for i in xrange(0,len(STDFurer)):    
#         STDFurer[i]=0.434*STDFurer[i]/RMSEFurer[i]
#         if logScaleFlag and math.log(STDFurer[i])<0:
#             STDFurer[i]=1
#     for i in xrange(0,len(STDFFurer)):
#         STDFFurer[i]=0.434*STDFFurer[i]/RMSEFFurer[i]
#         if logScaleFlag and math.log(STDFFurer[i])<0:
#             STDFFurer[i]=1
#     for i in xrange(0,len(STDRandom)):
#         STDRandom[i]=0.434*STDRandom[i]/RMSERandom[i]
#         if logScaleFlag and math.log(STDRandom[i])<0:
#             STDRandom[i]=1
#     print "AFTER: ",STDFurer
#     for s in STDFurer:
#         print math.log(s)
    #print stdevFurer
    #rects1 = ax.bar(ind-width, ResFurer, width,color='red',
     #           error_kw=dict(elinewidth=2,ecolor='red'),yerr=stdevFurer)
    
    
    #rects2 = ax.bar(ind, ResFfurer, width,color='blue',
    #                error_kw=dict(elinewidth=2,ecolor='blue'),yerr=stdevFfurer)
    
    #rects3 = ax.bar(ind+width, ResRandom, width,color='green',
    #                error_kw=dict(elinewidth=2,ecolor='green'),yerr=stdevRandom)

    stdevFurer = [(0,) * len(stdevFurer), stdevFurer]
    rects1 = ax.bar(ind - width, ResFurer, width,
                    zorder=1, color='blue',
                    error_kw=dict(elinewidth=2.3, ecolor='blue', zorder=2), ec='blue', fill=False, fc='blue',
                    yerr=stdevFurer, hatch='\\\\\\')

    stdevFfurer = [(0,) * len(stdevFfurer), stdevFfurer]

    rects2 = ax.bar(ind, ResFfurer, width,
                    zorder=1, color='red',
                    error_kw=dict(elinewidth=2.3, ecolor='red', zorder=2), ec='red', fill=False, fc='red',
                    yerr=stdevFfurer, hatch='//////')

    stdevRandom = [(0,) * len(stdevRandom), stdevRandom]
    rects3 = ax.bar(ind + width, ResRandom, width, zorder=1, color='black',
                        error_kw=dict(elinewidth=2.3, ecolor='black', zorder=2), yerr=stdevRandom, fill=False,
                        ec='black', fc='black', hatch='---')


    #ax.set_xlim(init_patt_size-width,end_patt_size+2*width)
    #print "Min value",min_value,math.log(min_value)
    if logScaleFlag:
        ax.set_ylim([0.0001,1])

    if not logScaleFlag:
        #plt.ylim(1E1,1E4)
        ax.set_ylim(0,max_value+(max_value/100))
        
    ax.set_ylabel(ylabel_string,fontsize=30)
    ax.set_xlabel("Dataset ID",fontsize=30)
    ax.set_title(title_string,fontsize=30)
    xTickMarks =datasets
    ax.set_xticks(ind)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=30)
    plt.title(title)
    zed = [tick.label.set_fontsize(30) for tick in ax.yaxis.get_major_ticks()]
    plt.legend(['FK-OBD', 'FK-AD','Random'],loc = 'upper left',prop={'size':22})

    #ax.legend((rects1[0], rects2[0],rects3[0]),('FK-OBD', 'FK-AD','Random'),loc = 'lower right',bbox_to_anchor=(legend_x,legend_y),prop={'size':22})
    fig.tight_layout()
    
    
def plotRES_scatter_plot(title,ResFurer,ResFfurer,ResRandom,datasets,xlabel,ylabel_string,title_string,legend_x,legend_y,logScaleFlag=False):
   fig = plt.figure()
   af = fig.add_subplot(111)
   if logScaleFlag:
        af.set_yscale('log',nonposy='clip')
   x=np.array([x*2 for x in range(1,len(datasets)+1)])

   af.scatter(x, ResFurer, s=10, c='red', marker="o", label='first')
   af.scatter(x,ResFfurer, s=10, c='blue', marker="o", label='second')
   af.scatter(x,ResRandom, s=10, c='green', marker="o", label='second')
   plt.show()




def get_relative_error(N,M):
    return abs((float(N)-float(M)))/max([N,M])

def getKLDS_per_dataset_name(csv_file):
    res_avg={}
    res_std={}
    with open(csv_file) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
           print row
           pattern_name=row["pattern_name"]
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
           pattern_name=row["pattern_name"]
           print "Calculating rel for: ",pattern_name
           print row["exh_emb"]
           nr_emb_exh=float(row["exh_emb"])
           with open(csv_file) as smpl:
               reader1 = csv.DictReader(smpl)
               for row1 in reader1:
                   pattern_name1=row1["pattern_name"]
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
    

def main(path_to_csv):
    #datasets_names_order=["S1","S3","S5","S2","S4","S6","R1","R2","R3","R4","R5","R6"]
    #datasets_names_order=["S1","S2","S6","R1","S3","R2","R6","S4","R3","S5","R4","R5"]
    #datasets_names_order=["S1","S2","S3","S4","S5","S6","R1","R2","R3","R4","R5","R6"]
    #datasets_names_order_original=["R1","S1","R2","S2","R3","S6","R5","S3","R4","S4","R5","S5"]
    datasets_names_order_original=["R5","S5","R4","S4","R3","S3","R2","S2","R6","S6","R1","S1"]
    datasets_names_order_mapping=["R1","S1","R2","S2","R3","S3","R4","S4","R5","S5","R6","S6"]
    datasets_names_order=datasets_names_order_original
    avgFurerKLD,stdevFurerKLD=getKLDS_per_dataset_name(os.path.join(path_to_csv,'furer.csv'))
    avgFFurerKLD,stdevFfurerKLD=getKLDS_per_dataset_name(os.path.join(path_to_csv,'Ffurer.csv'))
    avgRandomKLD,stdevRandomKLD=getKLDS_per_dataset_name(os.path.join(path_to_csv,'random.csv'))
    relErrorsFurer,stdevErrorsFurer=getrelErrors_per_dataset_name(os.path.join(path_to_csv,'furer.csv'),os.path.join(path_to_csv,'exhaustive.csv'))
    relErrorsFfurer,stdevErrorsFfurer=getrelErrors_per_dataset_name(os.path.join(path_to_csv,'Ffurer.csv'),os.path.join(path_to_csv,'exhaustive.csv'))
    relErrorsRandom,stdevErrorsRandom=getrelErrors_per_dataset_name(os.path.join(path_to_csv,'random.csv'),os.path.join(path_to_csv,'exhaustive.csv'))
    
    resultsKLDFurer_ordered=[]
    resultsKLDFfurer_ordered=[]
    resultsKLDRandom_ordered=[]
    
    stdev_resultsKLDFurer_ordered=[]
    stdev_resultsKLDFfurer_ordered=[]
    stdev_resultsKLDRandom_ordered=[]
    
    resultsRelErrFurer_ordered=[]
    resultsRelErrFfurer_ordered=[]
    resultsRelErrRandom_ordered=[]
    
    stdev_resultsRelErrFurer_ordered=[]
    stdev_resultsRelErrFfurer_ordered=[]
    stdev_resultsRelErrRandom_ordered=[]
    
    print avgFFurerKLD["R1"]
    for d in datasets_names_order:
        print "D: ",d
        print "adding"
        resultsKLDFurer_ordered.append(float(avgFurerKLD[d]))
        resultsKLDFfurer_ordered.append(float(avgFFurerKLD[d]))
        resultsKLDRandom_ordered.append(float(avgRandomKLD[d]))
        
        resultsRelErrFurer_ordered.append(float(relErrorsFurer[d]))
        resultsRelErrFfurer_ordered.append(float(relErrorsFfurer[d]))
        resultsRelErrRandom_ordered.append(float(relErrorsRandom[d]))
        
        stdev_resultsRelErrFurer_ordered.append(float(stdevErrorsFurer[d]))
        stdev_resultsRelErrFfurer_ordered.append(float(stdevErrorsFfurer[d]))
        stdev_resultsRelErrRandom_ordered.append(float(stdevErrorsRandom[d]))
        
        stdev_resultsKLDFurer_ordered.append(float(stdevFurerKLD[d]))
        stdev_resultsKLDFfurer_ordered.append(float(stdevFfurerKLD[d]))
        stdev_resultsKLDRandom_ordered.append(float(stdevRandomKLD[d]))
        
        
    print len(resultsKLDFfurer_ordered)
    plotRES("",resultsKLDFurer_ordered,resultsKLDFfurer_ordered,resultsKLDRandom_ordered,stdev_resultsKLDFurer_ordered,stdev_resultsKLDFfurer_ordered,stdev_resultsKLDRandom_ordered,datasets_names_order_mapping,"Dataset","Average KLD","",1,1,True)
    plotRES("",resultsRelErrFurer_ordered,resultsRelErrFfurer_ordered,resultsRelErrRandom_ordered,stdev_resultsRelErrFurer_ordered,stdev_resultsRelErrFfurer_ordered,stdev_resultsRelErrRandom_ordered,datasets_names_order_mapping,"Dataset","Avg RelErr","",0.95,1,True)
    plt.show()


if __name__=='__main__':
  #parser = argparse.ArgumentParser(description='Run exhaustive approach')
  #parser.add_argument('-r',help='path to csv files')
  #args = parser.parse_args()
  main('/home/irma/work/RESULTS/graph_sampling/satisfaction_results')