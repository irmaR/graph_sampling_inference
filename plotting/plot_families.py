'''
Created on Jun 13, 2017

@author: irma
'''
import csv,math,os
import numpy as np
import matplotlib.pyplot as plt

def get_families(patterns,path_csv):
    families={}
    counter=0
    reversed_patterns=patterns[::-1]
    base_level=reversed_patterns[0]
    end_level=reversed_patterns[-1]
    path_to_pattern_size=os.path.join(path_csv,'furer_'+str(base_level)+".csv")
    
    path_to_pattern_size=os.path.join(path_csv,'furer_'+str(base_level)+".csv")
    with open(path_to_pattern_size) as f:
               reader = csv.DictReader(f)
               for row in reader:
                    
                    name_of_pattern=row["pattern_name"].split("/")[-2]
                    if not counter in families.keys():
                        families[counter]=[]
                    if not name_of_pattern in families[counter]:
                        families[counter].append(name_of_pattern)
                    if len(row["parent_id"].split("/"))==1:
                           name_of_parent=row["parent_id"]
                    else:
                         name_of_parent=row["parent_id"].split("/")[-2]
                         families[counter].append(name_of_parent)
                    counter+=1

    for r in xrange(1,len(reversed_patterns)):
        path_to_pattern_size=os.path.join(path_csv,'furer_'+str(reversed_patterns[r])+".csv")
        for c in families.keys():
            with open(path_to_pattern_size) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name_of_pattern=row["pattern_name"].split("/")[-2]
                    if reversed_patterns[r]!=end_level:
                        if len(families[c])>r and name_of_pattern==families[c][r]:
                             if len(row["parent_id"].split("/"))==1:
                                   name_of_parent=row["parent_id"]
                             else:
                                 name_of_parent=row["parent_id"].split("/")[-2]
                             families[c].append(name_of_parent)
    return families

def plotRMSE_function_of_pattern_size(title,RMSEFurer,RMSEFFurer,RMSEFFurer_ord,RMSERandom,STDFurer,STDFFurer,STDFFurer_ord,STDRandom,init_patt_size,end_patt_size,ylabel_string,title_string,legend_x,legend_y,logScaleFlag=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if logScaleFlag:
        print "Log scale!"
        ax.set_yscale('symlog',nonposy='clip')
    ind = np.array([x for x in range(init_patt_size,end_patt_size+1)])             # the x locations for the groups
    width = 0.2    
    rects1 = ax.bar(ind-width, RMSEFurer, width,
                color='blue',
                error_kw=dict(elinewidth=2.3,ecolor='blue'),yerr=STDFurer)
    
    
    rects2 = ax.bar(ind, RMSEFFurer, width,
                    color='red',
                    error_kw=dict(elinewidth=2.3,ecolor='red'),yerr=STDFFurer)
    
    rects3 = ax.bar(ind+width, RMSEFFurer_ord, width,
                    color='green',
                    error_kw=dict(elinewidth=2.3,ecolor='green'),yerr=STDFFurer_ord)
     
    rects4 = ax.bar(ind+2*width, RMSERandom, width,
                    color='black',
                    error_kw=dict(elinewidth=2.3,ecolor='black'),yerr=STDRandom)

    ax.set_ylabel(ylabel_string,fontsize=25)
    ax.set_xlabel("Pattern size",fontsize=25)
    ax.set_title(title_string,fontsize=25)
    ax.set_ylim([0,np.max([np.max(RMSEFurer),np.max(RMSEFFurer),np.max(RMSEFFurer_ord),np.max(RMSERandom)])+0.2])    
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
    ax.legend((rects1[0], rects2[0],rects3[0],rects4[0]),('FK-OBD', 'FK-AD','FK-AD-ORD','Random'),loc = 'upper left',bbox_to_anchor=(legend_x,legend_y),prop={'size':15})
    fig.tight_layout()
    plt.show()

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
        if v1==float('nan') or v2==float('nan'):
            rel_errors.append(float('nan'))
        else:
            nr=abs((float(v1)-float(v2)))/v1
            if not math.isnan(nr):
              rel_errors.append((abs((float(v1)-float(v2)))/max(v1,v2)))
        
    #print "MEAN: ",np.mean(rel_errors)
    return rel_errors

def collect_EMB_for_pattern_2(path_to_exhaustive_csv,path_to_approach):
   array_of_nr_emb_exhaustive=[]
   array_of_final_nr_emb_approachX=[]
   number_of_patterns=0
   row_number=0
   nr_timeout=0
   result_per_pattern=[]
   exh_result_per_pattern=[]
   with open(path_to_exhaustive_csv) as exh:
           reader = csv.DictReader(exh)   
           for row in reader:
             
             if row["timeout"]==str(True):
                 nr_timeout+=1
                 continue
             name_of_patterns=None
             for s in row["pattern_name"].split("/"):
                 if "pattern_" in s:
                     name_of_patterns=s
             array_values_appx=[]
             with open(path_to_approach) as appX:
                  reader1 = csv.DictReader(appX)  
                  for row1 in reader1:                 
                      #if not row_number>0:
                      #    row_number+=1
                      name_of_patterns2=None
                      for s in row1["pattern_name"].split("/"):
                          if "pattern_" in s:
                              name_of_patterns2=s
                      if(name_of_patterns2==name_of_patterns):
                          number_of_patterns+=1  
                          exh_result_per_pattern.append(float(row["exh_emb"]))
                          #value=row1["emb_120"]
                          for i in range(1,121):
                               value=row1["emb_"+str(i)]                               
                               #print row1["pattern_name"]
                               if not value:
                                   array_values_appx.append(float('nan'))
                               elif value==None:
                                  array_values_appx.append(float('nan'))
                               elif value=="None":
                                  array_values_appx.append(float('nan'))
                               else:
                                  array_values_appx.append(float(value))
                          value=np.nanmean(array_values_appx)
                          if value:
                               result_per_pattern.append(float(value))
                          else:
                               result_per_pattern.append(float('nan'))
                          break
   relative_error_appr_small=calculate_Relative_Errors_exhaustive(exh_result_per_pattern, result_per_pattern)
   counter=1
   for a in relative_error_appr_small:
       #print counter, a
       counter+=1
   return relative_error_appr_small


def collect_EMB_for_pattern(path_to_exhaustive_csv,patterns,path_to_approach):
   array_of_nr_emb_exhaustive=[]
   array_of_final_nr_emb_approachX=[]
   number_of_patterns=0
   row_number=0
   nr_timeout=0
   result_per_pattern=[]
   exh_result_per_pattern=[]
   for p in patterns:
       with open(path_to_exhaustive_csv) as exh:
           reader = csv.DictReader(exh)   
           for row in reader:
             array_values_appx=[]
             name_of_patterns=None
             for s in row["pattern_name"].split("/"):
                 if "pattern_" in s:
                     name_of_patterns=s
             if not name_of_patterns.rstrip().lstrip()==p:
                 continue 
             
             if row["timeout"]==str(True):
                 nr_timeout+=1
                 continue
             with open(path_to_approach) as appX:
                  reader1 = csv.DictReader(appX)  
                  for row1 in reader1:                 
                      #if not row_number>0:
                      #    row_number+=1
                      name_of_patterns2=None
                      for s in row1["pattern_name"].split("/"):
                          if "pattern_" in s:
                              name_of_patterns2=s
                      if(name_of_patterns2==name_of_patterns):
                          number_of_patterns+=1  
                          exh_result_per_pattern.append(float(row["exh_emb"]))
                          value=row1["emb_120"]
                          if value:
                               result_per_pattern.append(float(value))
                          else:
                               result_per_pattern.append(float('nan'))
                          break
   relative_error_appr_small=calculate_Relative_Errors_exhaustive(exh_result_per_pattern, result_per_pattern)
   counter=1
   for a in relative_error_appr_small:
       #print counter, a
       counter+=1
   return relative_error_appr_small
 



def collect_statistics_families(pattern_sizes,exps,path_to_csvs):
     
    init=pattern_sizes[0]
    end=pattern_sizes[-1]
    exp_counter=0
    axis_counter=0
    logScaleFlag=False
    fig = plt.figure()
    plt.subplots_adjust(wspace=0.5,hspace=0.5)
    iplot = 220
    for i in range(4):
        RMSEFurerEMB=[]
        RMSEFFurerEMB=[]
        RMSEFFurer_ordEMB=[]
        RMSERandomEMB=[]
        StdFurerEMB=[]
        StdFFurerEMB=[]
        StdFFurer_ordEMB=[]
        StdRandomEMB=[]
        iplot += 1
        if exp_counter>=len(exps):
          break 
        path_to_csv=path_to_csvs[exp_counter]
        exp=exps[exp_counter]
        families=get_families(pattern_sizes,path_to_csv)
        exp_counter+=1
        patterns_per_pattern_size={}
        patterns_reversed=pattern_sizes[::-1]
        for c in families.keys():
            if len(families[c])==len(patterns_reversed):
                for k in xrange(len(patterns_reversed)):
                    if not patterns_reversed[k] in patterns_per_pattern_size:
                        patterns_per_pattern_size[patterns_reversed[k]]=[]
                    patterns_per_pattern_size[patterns_reversed[k]].append(families[c][k])
                    
        for n in pattern_sizes:
                path_to_exhaustive_csv=path_to_csv+"/exhaustive_"+str(n)+".csv"
                path_to_Furer=path_to_csv+"/furer_"+str(n)+".csv"
                path_to_FFurer=path_to_csv+"/Ffurer_"+str(n)+".csv"
                path_to_FFurer_ord=path_to_csv+"/Ffurer_order_random_"+str(n)+".csv"
                path_to_Random=path_to_csv+"/random_"+str(n)+".csv"
                rmseFurer=collect_EMB_for_pattern(path_to_exhaustive_csv,patterns_per_pattern_size[n],path_to_Furer)
                print n,len(patterns_per_pattern_size[n])
                rmseFfurer=collect_EMB_for_pattern(path_to_exhaustive_csv,patterns_per_pattern_size[n],path_to_FFurer)
                if exp!="dblp":
                  rmseFurerOrd=collect_EMB_for_pattern(path_to_exhaustive_csv,patterns_per_pattern_size[n],path_to_FFurer_ord)
                rmseRandom=collect_EMB_for_pattern(path_to_exhaustive_csv,patterns_per_pattern_size[n],path_to_Random)
                RMSEFurerEMB.append(np.nanmean(rmseFurer))
                RMSEFFurerEMB.append(np.nanmean(rmseFfurer))
                if exp!="dblp":
                   RMSEFFurer_ordEMB.append(np.nanmean(rmseFurerOrd))
                RMSERandomEMB.append(np.nanmean(rmseRandom))
                 
                StdFurerEMB.append(np.nanstd(rmseFurer))
                StdFFurerEMB.append(np.nanstd(rmseFfurer))
                if exp!="dblp":
                   StdFFurer_ordEMB.append(np.nanstd(rmseFurerOrd))
                StdRandomEMB.append(np.nanstd(rmseRandom))
         
        print RMSEFurerEMB,StdFurerEMB
        print RMSEFFurerEMB,StdFFurerEMB
        print RMSEFFurer_ordEMB,StdFFurer_ordEMB
        print RMSERandomEMB,StdRandomEMB

    
        if i == 3:
           print "ovdje",exp
        #   ax = plt.subplot2grid((3,7), (i/2, 2), colspan=3)
           ax = fig.add_subplot(iplot)
           ax.set_xlabel('Pattern size',size=25)
           #ax.legend(['FK-OBD', 'FK-AD','Random'],loc = 'upper right', bbox_to_anchor = (0,0.5,1.0,0.5),prop={'size':16})    
        else:
        # You can be fancy and use subplot2grid for each plot, which dosen't
        # require keeping the iplot variable:
        # ax = subplot2grid((4,2), (i/2,i%2))

        # Or you can keep using add_subplot, which may be simpler:
          ax = fig.add_subplot(iplot)
          if i==0 or i==2:
            ax.set_ylabel('Avg_RelEr',size=25)
          if i==2 or i==3:
            ax.set_xlabel('Pattern size',size=25)
        if exp=="dblp":
          ax.set_title("DBLP", fontsize=20)
        elif exp=="y":
          ax.set_title("YEAST", fontsize=20)
        elif exp=="webkb":
          ax.set_title("WEBKB", fontsize=20)
        elif exp=="facebook":
          ax.set_title("FACEBOOK", fontsize=20)
        elif exp=="imdb":
          ax.set_title("IMDB", fontsize=20)
        elif exp=="am":
          ax.set_title("AMAZON", fontsize=20)


        if logScaleFlag:
            print "Log scale!"
            ax.set_yscale('symlog',nonposy='clip')
        #ylabel_string='Avg Rel_Er'
        title_string=exp
        ind = np.array([x for x in range(init,end+1)])             # the x locations for the groups
        width = 0.2    
        print RMSEFurerEMB
        rects1 = ax.bar(ind-width, RMSEFurerEMB, width,
                    color='blue',
                    error_kw=dict(elinewidth=2.3,ecolor='blue'),yerr=StdFurerEMB)
        
        
        rects2 = ax.bar(ind, RMSEFFurerEMB, width,
                        color='red',
                        error_kw=dict(elinewidth=2.3,ecolor='red'),yerr=StdFFurerEMB)
        
        if exp!="dblp":
            rects3 = ax.bar(ind+width, RMSEFFurer_ordEMB, width,
                            color='black',
                            error_kw=dict(elinewidth=2.3,ecolor='black'),yerr=StdFFurer_ordEMB)
         
        rects4 = ax.bar(ind+2*width, RMSERandomEMB, width,
                        color='green',
                        error_kw=dict(elinewidth=2.3,ecolor='green'),yerr=StdRandomEMB)
    
        #ax.set_ylabel(ylabel_string,fontsize=25)
        #ax.set_xlabel("Pattern size",fontsize=25)
        #ax.set_title(title_string,fontsize=25)
        #if exp=="webkb" or exp=="dblp":
        # ax.set_ylim([0,0.55])
        #elif exp=="facebook":
        #    ax.set_ylim([0,0.02])
        #else:  
         #ax.set_ylim([0,np.max([np.max(RMSEFurerEMB),np.max(RMSEFFurerEMB),np.max(RMSEFFurer_ordEMB),np.max(RMSERandomEMB)])+0.2])
        # ax.set_ylim([0,0.22])    
        xTickMarks = [str(i) for i in range(init,end+1)]
        ax.set_xticks(ind)
        xtickNames = ax.set_xticklabels(xTickMarks)
        #plt.setp(xtickNames, rotation=45, fontsize=20)
        #plt.title(title_string)
        zed = [tick.label.set_fontsize(25) for tick in ax.yaxis.get_major_ticks()]
        zed = [tick.label.set_fontsize(25) for tick in ax.xaxis.get_major_ticks()]
        axis_counter+=1
        #ax = fig.add_subplot(iplot)
    plt.legend(['FK-OBD', 'FK-AD','FK-AD-10','Random'],loc = 'upper right', bbox_to_anchor = (0,0.5,1.0,0.5),prop={'size':16})    
    #fig.add_subplot(111, frameon=False)     
    #plt.xlabel('% exhaustive runtime',size=18)
    #plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off',labelsize=30)
    #plt.tight_layout()
    #plt.subplots_adjust(wspace=0.3)
    #plt.subplots_adjust(hspace=0.3)
    plt.show()
    #plotRMSE_function_of_pattern_size("YEAST",RMSEFurerEMB,RMSEFFurerEMB,RMSEFFurer_ordEMB,RMSERandomEMB,StdFurerEMB,StdFFurerEMB,StdFFurer_ordEMB,StdRandomEMB,init,end,y_axis,"",1.0,0.3,False)


def get_per_pattern_size_results(pattern_sizes,exps,path_to_csvs):
    init=pattern_sizes[0]
    end=pattern_sizes[-1]
    exp_counter=0
    axis_counter=0
    logScaleFlag=False
    fig = plt.figure()
    plt.subplots_adjust(wspace=0.3,hspace=0.3)
    iplot = 220
    for i in range(4):
        print 'HALLLLLLLLLLOOOOO',i
        RMSEFurerEMB=[]
        RMSEFFurerEMB=[]
        RMSEFFurer_ordEMB=[]
        RMSERandomEMB=[]
        StdFurerEMB=[]
        StdFFurerEMB=[]
        StdFFurer_ordEMB=[]
        StdRandomEMB=[]
        iplot += 1
        if exp_counter>=len(exps):
          break 
        path_to_csv=path_to_csvs[exp_counter]
        exp=exps[exp_counter]
        exp_counter+=1
        patterns_per_pattern_size={}
        
        
                    
        
                    
        for n in pattern_sizes:
                path_to_exhaustive_csv=path_to_csv+"/exhaustive_"+str(n)+".csv"
                path_to_Furer=path_to_csv+"/furer_"+str(n)+".csv"
                path_to_FFurer=path_to_csv+"/Ffurer_"+str(n)+".csv"
                path_to_FFurer_ord=path_to_csv+"/Ffurer_order_random_"+str(n)+".csv"
                path_to_Random=path_to_csv+"/random_"+str(n)+".csv"
                rmseFurer=collect_EMB_for_pattern_2(path_to_exhaustive_csv,path_to_Furer)
                rmseFfurer=collect_EMB_for_pattern_2(path_to_exhaustive_csv,path_to_FFurer)
                if exp!="dblp":
                  rmseFurerOrd=collect_EMB_for_pattern_2(path_to_exhaustive_csv,path_to_FFurer_ord)
                rmseRandom=collect_EMB_for_pattern_2(path_to_exhaustive_csv,path_to_Random)
                RMSEFurerEMB.append(np.nanmean(rmseFurer))
                RMSEFFurerEMB.append(np.nanmean(rmseFfurer))
                if exp!="dblp":
                   RMSEFFurer_ordEMB.append(np.nanmean(rmseFurerOrd))
                RMSERandomEMB.append(np.nanmean(rmseRandom))
                 
                StdFurerEMB.append(np.nanstd(rmseFurer))
                StdFFurerEMB.append(np.nanstd(rmseFfurer))
                if exp!="dblp":
                   StdFFurer_ordEMB.append(np.nanstd(rmseFurerOrd))
                StdRandomEMB.append(np.nanstd(rmseRandom))
         
        #print RMSEFurerEMB,StdFurerEMB
        #print RMSEFFurerEMB,StdFFurerEMB
        #print RMSEFFurer_ordEMB,StdFFurer_ordEMB
        #print RMSERandomEMB,StdRandomEMB

    
        if i == 3:
           print "ovdje",exp
        #   ax = plt.subplot2grid((3,7), (i/2, 2), colspan=3)
           ax = fig.add_subplot(iplot)
           ax.set_xlabel('pattern size',size=30)
           #ax.legend(['FK-OBD', 'FK-AD','Random'],loc = 'upper right', bbox_to_anchor = (0,0.5,1.0,0.5),prop={'size':16})    
        else:
        # You can be fancy and use subplot2grid for each plot, which dosen't
        # require keeping the iplot variable:
        # ax = subplot2grid((4,2), (i/2,i%2))

        # Or you can keep using add_subplot, which may be simpler:
          ax = fig.add_subplot(iplot)
          if i==0 or i==2:
            ax.set_ylabel('Avg RelErr',size=30)
          if i==2 or i==3:
            ax.set_xlabel('pattern size',size=30)
        if exp=="dblp":
          ax.set_title("DBLP", fontsize=25)
        elif exp=="y":
          ax.set_title("YEAST", fontsize=25)
        elif exp=="webkb":
          ax.set_title("WEBKB", fontsize=25)
        elif exp=="facebook":
          ax.set_title("FACEBOOK", fontsize=25)
        elif exp=="imdb":
          ax.set_title("IMDB", fontsize=25)
        elif exp=="am":
          ax.set_title("AMAZON", fontsize=25)


        if logScaleFlag:
            print "Log scale!"
            ax.set_yscale('symlog',nonposy='clip')
        #ylabel_string='Avg Rel_Er'
        title_string=exp
        ind = np.array([5*x for x in range(init,end+1)])             # the x locations for the groups
        width = 1
        print RMSEFurerEMB
        StdFurerEMB = [(0,) * len(StdFurerEMB), StdFurerEMB]
        rects1 = ax.bar(ind-width, RMSEFurerEMB, width,
                    zorder=1,color='blue',
                    error_kw=dict(elinewidth=2.3,ecolor='blue',zorder=2),ec='blue',fill=False,fc='blue',yerr=StdFurerEMB,hatch='\\\\\\')

        StdFFurerEMB=[(0,)*len(StdFFurerEMB), StdFFurerEMB]

        rects2 = ax.bar(ind, RMSEFFurerEMB, width,
                        zorder=1,color='red',
                        error_kw=dict(elinewidth=2.3,ecolor='red',zorder=2),ec='red',fill=False,fc='red',yerr=StdFFurerEMB,hatch='//////')

        StdFFurer_ordEMB = [(0,) * len(StdFFurer_ordEMB), StdFFurer_ordEMB]
        if exp!="dblp":
            rects3 = ax.bar(ind+width, RMSEFFurer_ordEMB, width,zorder=1,color='black',
                            error_kw=dict(elinewidth=2.3, ecolor='black',zorder=2),yerr=StdFFurer_ordEMB,fill=False,ec='black',fc='black',hatch='|||')

            StdRandomEMB = [(0,) * len(StdRandomEMB), StdRandomEMB]
        rects4 = ax.bar(ind+2*width, RMSERandomEMB, width,
                        color='green',
                        error_kw=dict(elinewidth=2.3,ecolor='green'),fill=False,ec='green',fc='green',yerr=StdRandomEMB,hatch='x')




        #ax.set_ylabel(ylabel_string,fontsize=25)
        #ax.set_xlabel("Pattern size",fontsize=25)
        #ax.set_title(title_string,fontsize=25)
        if exp=="dblp":
         ax.set_ylim([0,0.55])
        if exp=="webkb":
         ax.set_ylim([0,1])
        elif exp=="facebook":
            ax.set_ylim([0,1])
        else:  
          ax.set_ylim([0,np.max([np.max(RMSEFurerEMB),np.max(RMSEFFurerEMB),np.max(RMSEFFurer_ordEMB),np.max(RMSERandomEMB)])+0.2])
        # ax.set_ylim([0,0.22])    
        xTickMarks = [str(v) for v in range(init,end+1)]
        ax.set_xticks(ind)
        xtickNames = ax.set_xticklabels(xTickMarks)
        #plt.setp(xtickNames, rotation=45, fontsize=20)
        #plt.title(title_string)
        zed = [tick.label.set_fontsize(25) for tick in ax.yaxis.get_major_ticks()]
        zed = [tick.label.set_fontsize(25) for tick in ax.xaxis.get_major_ticks()]
        print "Ovdje i",i
        if i==2:
          ax.legend(['FK-OBD', 'FK-AD','FK-AD-10','Random'],loc = 'upper left', bbox_to_anchor = (0,0.5,1.0,0.5),prop={'size':16})    

        rects = ax.patches
        labels = ["label%d" % i for i in xrange(len(rects))]

        #for rect, label in zip(rects, labels):
        #    height = rect.get_height()
        #    ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label, ha='center', va='bottom')

        axis_counter+=1
        #ax = fig.add_subplot(iplot)
    #fig.add_subplot(111, frameon=False)     
    #plt.xlabel('% exhaustive runtime',size=18)
    #plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off',labelsize=30)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.3)
    plt.subplots_adjust(hspace=0.3)

    # Now make some labels


    plt.show()

            
            
            
            
if __name__ == '__main__':
      #collect_statistics_families('/home/irma/workspace/DMKD_Paper_Sampling/yeast_csvs/',[4,5,6,7,8,9,10],'emb')     
      #collect_statistics_families('/home/irma/workspace/DMKD_Paper_Sampling/yeast_csvs/',[4,5,6,7,8,9,10],'emb')         
      #collect_statistics_families([4,5,6,7,8,9,10],['y','fb','webkb','imdb'],['/home/irma/workspace/DMKD_Paper_Sampling/yeast_csvs/','/home/irma/workspace/DMKD_Paper_Sampling/facebook_csvs/','/home/irma/workspace/DMKD_Paper_Sampling/webkb_csvs/','/home/irma/workspace/DMKD_Paper_Sampling/imdb_csvs/'])
      get_per_pattern_size_results([6,7,8,9,10],['y','facebook','webkb','imdb'],['/home/irma/work/RESULTS/graph_sampling/yeast_csvs/','/home/irma/work/RESULTS/graph_sampling/facebook_csvs/','//home/irma/work/RESULTS/graph_sampling/webkb_csvs/','/home/irma/work/RESULTS/graph_sampling/imdb_csvs/'])

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        