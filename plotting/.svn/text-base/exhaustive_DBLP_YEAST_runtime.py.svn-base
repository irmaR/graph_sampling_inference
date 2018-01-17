'''
Created on Mar 16, 2016

@author: irma
'''
import csv,os
import numpy as np
import matplotlib.pyplot as plt

def get_average_runtime_dblp(path_to_exhaustive_csv):
    runtimes=[]
    with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
           runtime=float(row["time"])/60
           if runtime>600:
               runtime=600              
           runtimes.append(runtime)
    return np.nanstd(runtimes),np.nanmean(runtimes)

def get_average_runtime_yeast(path_to_exhaustive_csv):
    runtimes=[]
    with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
           runtime=float(row["time"])/60
           if runtime>10:
               runtime=10              
           runtimes.append(runtime)
    return np.nanstd(runtimes),np.nanmean(runtimes)

def get_max_runtime_dblp(path_to_exhaustive_csv):
    runtimes=[]
    with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
           runtime=float(row["time"])/60
           if runtime>600:
               runtime=600              
           runtimes.append(runtime)
    return np.nanmax(runtimes)

def get_max_runtime_yeast(path_to_exhaustive_csv):
    runtimes=[]
    with open(path_to_exhaustive_csv) as exh:
       reader = csv.DictReader(exh)
       for row in reader:
           runtime=float(row["time"])/60
           if runtime>10:
               runtime=10              
           runtimes.append(runtime)
    return np.nanmax(runtimes)




path_to_DBLP="/home/irma/workspace/DMKD_Paper_Sampling/dblp_csvs/"
path_to_YEAST="/home/irma/workspace/DMKD_Paper_Sampling/yeast_csvs/"
runtimes={}
levels=[4,5,6,7,8,9,10,11,12,13,14,15]

#runtimes for DBLP
runtimes_DBLP=[]
std_DBLP=[]
for l in levels:
    path_to_exhaustive_csv=os.path.join(path_to_DBLP,"exhaustive_"+str(l)+".csv")
    std,mean=get_average_runtime_dblp(path_to_exhaustive_csv)
    std_DBLP.append(std)
    runtimes_DBLP.append(mean)
    
    
runtimes_YEAST=[]
std_YEAST=[]
for l in levels:
    path_to_exhaustive_csv=os.path.join(path_to_YEAST,"exhaustive_"+str(l)+".csv")
    std,mean=get_average_runtime_yeast(path_to_exhaustive_csv)
    runtimes_YEAST.append(mean)
    std_YEAST.append(std)

x=levels
print "DBLP:",runtimes_DBLP,len(runtimes_DBLP)
print "STD DBLP: ",std_DBLP

print "YEAST:",runtimes_YEAST
print "STD DBLP: ",std_YEAST
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

line1 = ax1.plot(x, runtimes_DBLP,color='blue',linewidth=3,label="DBLP")
#ax1.set_yscale('log')
ax1.errorbar(x, runtimes_DBLP, yerr=std_DBLP, color='blue',linewidth=2)
#ax1.set_ylabel("Average runtime (minutes)",size=15)



line2 = ax2.plot(x, runtimes_YEAST,color='black',linewidth=3,label="YEAST")
ax2.errorbar(x, runtimes_YEAST, yerr=std_YEAST, color='black',linewidth=2)
#plt.xlabel('Pattern size',size=15)
#plt.ylabel('Average runtime (minutes)')

fig.text(0.5, 0.04, 'Pattern size', ha='center', va='center',size=20)
fig.text(0.06, 0.5, 'Average runtime (minutes)', ha='center', va='center', rotation='vertical',size=20)


ax1.set_xlim(4, 16)
ax2.set_xlim(4, 16)
ax1.tick_params(labelsize=20)
ax2.tick_params(labelsize=20)

plt.show()



# fig1 = plt.figure()
# # and the first axes using subplot populated with data 
# ax1 = fig1.add_subplot(111)
# line1 = ax1.plot(x, runtimes_DBLP,color='blue',linewidth=3,label="DBLP")
# #ax1.set_yscale('log')
# ax1.errorbar(x, runtimes_DBLP, yerr=std_DBLP, color='blue',linewidth=2)
# plt.ylabel("Average runtime (seconds)",size=25)
#  
# # now, the second axes that shares the x-axis with the ax1
# ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
# line2 = ax2.plot(x, runtimes_YEAST,color='black',linewidth=3,label="YEAST")
# ax2.errorbar(x, runtimes_YEAST, yerr=std_YEAST, color='black',linewidth=2)
# ax2.yaxis.tick_right()
# ax2.yaxis.set_label_position("right")
# #ax2.set_yscale('log')
# plt.ylabel("Average runtime (seconds)",size=25)
# ax1.tick_params(labelsize=20)
# ax2.tick_params(labelsize=20)
# ax1.set_xlim(4, 15)
# ax2.set_xlim(4, 15)
# ax1.legend(loc=2,prop={'size':20})
# ax2.legend(loc=4,prop={'size':20})
# plt.tight_layout()
# plt.show()
