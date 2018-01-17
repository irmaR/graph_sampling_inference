'''
Created on Mar 8, 2016

@author: irma
'''
import argparse
import os,csv
import matplotlib.pyplot as plt
import numpy as np

def get_percentage_of_timout(exhaustive_csv):
    counter=0
    counter_time_out=0
    with open(exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
        counter+=1
        if row["timeout"]=="True":
            counter_time_out+=1
    return counter_time_out/float(counter)

def main(path_to_csvs,exp,levels):
    percentages_per_level={}
    for l in levels:
        exhaustive_csv=os.path.join(path_to_csvs,'exhaustive_'+str(l)+".csv")
        percentages_per_level[l]=get_percentage_of_timout(exhaustive_csv)
    
    percentages=[]
    for k in percentages_per_level.keys():
        percentages.append(percentages_per_level[k]*100)
    #plot
    print percentages
    x=levels
    plt.bar(x,percentages,align='center')
    plt.xlabel('Pattern size',size=20)
    plt.ylabel('% of timeouts for exhaustive',size=20)
    if exp=="dblp":
       plt.title("DBLP",size=20)
    if exp=="y":
       plt.title("YEAST",size=20)
       plt.xticks()
    plt.xticks(np.arange(min(x), max(x)+1, 1.0),size=25)
    plt.yticks(size=25)
    plt.tight_layout()
    axes = plt.gca()
    #axes.set_xlim([min(x),max(x)])
    axes.set_ylim([min(percentages),max(percentages)+5])
    plt.show()
        


if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')
  parser.add_argument('-e',help='dblp or y')
  
  args = parser.parse_args()
  main(args.r,args.e,[4,5,6,7,8,9,10,11,12,13,14,15])