
from sampler_general_ex import *
import time
import pickle
import numpy
import networkx as nx
import sampling_utils as su
import matplotlib.pyplot as plt

start = time.time()

graph_file_name = "../../summerCode2013/S1.gml.gz"
short_graph_file_name = "S1"
pattern_file_name = "new_salsat_pattern.gml" # BEWARE: change below ALSO the Plist, OBdecomp and root-target AND fdict_ex pickle file !!!
repetitions = 10

latex_file_name = "experiments_ICDM__" + short_graph_file_name + pattern_file_name+".x"+str(repetitions)+".latex"
latexfile = open(latex_file_name,  'a')
latexfile.write("\n\\begin{table}\n")
latexfile.write("\\centering\n")
latexfile.write("\\begin{tabular}{|l|l|r|c|c|c|r} \\hline \n")
latexfile.write("graph		& algorithm     & observed	& KLD   				& BHD   				& HLD 				& s/run  \\\\ \\hline \n")
latexfile.close()

plot_result_dict = {}

# Total number of observations: 421,664
NLIMIT_values = [50000, 100000, 150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000]

exhaustive_times = []
all_randnode_times = []
all_furer_times = []    

rndicts = []
fudicts = []
for i in range(repetitions):
    print "starting iteration %d" % i
    D = nx.read_gml(graph_file_name)
    P = nx.read_gml(pattern_file_name)
    # --------------------------------------------############### ---------- HERE CHANGE ALL THOSE ALWAYS
    Plist = [2, 4, 1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    OBdecomp = [ [2], [4],  [1,  3,  5],  [6],  [7,  8],  [9],  [10,  11],  [12],  [13,  14] ]
    root_nodes = [x for x in D.nodes() if D.node[x]['predicate']=='satisfaction'] 


    startEX = time.time()
##        fdict_exhaustive = sampling_exhaustive_general2(D,  P,  Plist,  root_nodes)
    pickin = open('fdict_exhaustive_S1.pickle', 'rb')
    fdict_exhaustive = pickle.load(pickin)
    pickin.close()
    stopEX = time.time()
    # --------------------------------------------############### ----------------------------------------------------------------------
    limited_result = sampling_randomnode_general(D,  P,  Plist,  root_nodes,  NLIMIT_values)
    fdictionaries_limited = limited_result[0]
    times_limited = limited_result[1][1:]       # all without first element, which is absolute time of start
    #fdict_limited = fdictionaries_limited[-1:][0]      # samo najvecjega ne rabimo vec - rabimo listo vseh
    all_randnode_times.append(times_limited)
    rndicts.append(fdictionaries_limited)

    furer_result = Furer_run_general(D, P , OBdecomp, root_nodes, NLIMIT_values)
    fdictionaries_Furer = furer_result[0]
    times_Furer = furer_result[1][1:]       # all without first element, which is absolute time of start
    #fdict_Furer = fdictionaries_Furer[-1:][0]      # samo najvecjega ne rabimo vec - rabimo listo vseh
    all_furer_times.append(times_Furer)
    fudicts.append(fdictionaries_Furer)

# zdej vse rezultate imamo - samo se obdelat je treba...
# najprej pa SPICKLAT!
pickout = open('rndicts.pickle', 'wb')
pickle.dump(rndicts, pickout)
pickout.close()
pickout = open('fudicts.pickle', 'wb')
pickle.dump(fudicts, pickout)
pickout.close()
pickout = open('all_randnode_times.pickle', 'wb')
pickle.dump(all_randnode_times, pickout)
pickout.close()
pickout = open('all_furer_times.pickle', 'wb')
pickle.dump(all_furer_times, pickout)
pickout.close()
# poberi kar je za sprintat - ostalo spicklaj in je
# kar posimuliram kot je bilo nastavljeno prej:
#---pred tem se priprava fdict_exhaustive:
complete_combinations(fdict_exhaustive, D,  P,  Plist)      # add zeros to all not present combinations
smooth(fdict_exhaustive,  fdict_exhaustive)     # Laplace smoothing also for the exhaustive


for nli in range(len(NLIMIT_values)):
    plot_result_dict[NLIMIT_values[nli]] = {}
    randnode_results_KLD = []
    randnode_results_bhatta = []
    randnode_results_hellinger = []
    furer_results_KLD = []
    furer_results_bhatta = []
    furer_results_hellinger = []
    randnode_times = []
    furer_times = []
    for i in range(repetitions):
        randnode_times.append(all_randnode_times[i][nli])
        furer_times.append(all_furer_times[i][nli])
        
        fdict_limited = rndicts[i][nli]
        smooth(fdict_limited,  fdict_exhaustive)    # smoothing to avoid zeros
        fdict_Furer = fudicts[i][nli]
        smooth(fdict_Furer,  fdict_exhaustive)      # smoothing to avoid zeros



        ##pde = make_pd_general(fdict_exhaustive)
        [pde,  trash_list,  default_key] = make_pd_general_kickout_default(fdict_exhaustive,  trash_factor=0.01)     # we remove rows where frequencies do not reach 1%

        if len(pde) < 1:
            print "WARNING: bad (not enough present) pattern or too high trash threshold! STOPPING."
            break
        [pdl,  tl,  dk] = make_pd_general_kickout_default_limited(fdict_limited,  trash_list,  default_key)
        [pdf ,  tl,  dk]= make_pd_general_kickout_default_limited(fdict_Furer,  trash_list,  default_key)
        # new function also for limited ones : make_pd_general_kickout_default_limited(fdict,  trash,  default_key)



        randnode_results_KLD.append(su.avg_kld(transform_to_ptable(pde), transform_to_ptable(pdl)))
        randnode_results_bhatta.append(su.avg_bhatta(transform_to_ptable(pde), transform_to_ptable(pdl)))
        randnode_results_hellinger.append(su.avg_hellinger(transform_to_ptable(pde), transform_to_ptable(pdl)))
        
        furer_results_KLD.append(su.avg_kld(transform_to_ptable(pde), transform_to_ptable(pdf)))
        furer_results_bhatta.append(su.avg_bhatta(transform_to_ptable(pde), transform_to_ptable(pdf)))
        furer_results_hellinger.append(su.avg_hellinger(transform_to_ptable(pde), transform_to_ptable(pdf)))

    plot_result_dict[NLIMIT_values[nli]]["randomnode_KLD"] = (numpy.mean(randnode_results_KLD),  numpy.std(randnode_results_KLD,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["randomnode_BHT"] = (numpy.mean(randnode_results_bhatta),  numpy.std(randnode_results_bhatta,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["randomnode_HEL"] = (numpy.mean(randnode_results_hellinger),  numpy.std(randnode_results_hellinger,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["furer_KLD"] = (numpy.mean(furer_results_KLD),  numpy.std(furer_results_KLD,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["furer_BHT"] = (numpy.mean(furer_results_bhatta),  numpy.std(furer_results_bhatta,  ddof=1))
    plot_result_dict[NLIMIT_values[nli]]["furer_HEL"] = (numpy.mean(furer_results_hellinger),  numpy.std(furer_results_hellinger,  ddof=1))

    result_file_name = "ultimex_ICDM_" + short_graph_file_name + pattern_file_name+"."+str(repetitions) +"x"+str(NLIMIT_values[nli])+".result"
    resultfile = open(result_file_name,  'w')
    resultfile.write('-----SUMMARY-----\n')
    resultfile.write("experiment on graph: " + str(short_graph_file_name) +" and pattern: "+pattern_file_name+"\n")
    resultfile.write("NLIMIT: " + str(NLIMIT_values[nli]) +"\n")
    resultfile.write("repetitions: " + str(repetitions) +"\n")
    resultfile.write(" " +"\n")
    resultfile.write("average average KLD on randomnode: " + str(numpy.mean(randnode_results_KLD))  + " with SSTD: " + str(numpy.std(randnode_results_KLD,  ddof=1)) +"\n")
    resultfile.write("average average bhatta on randomnode: " + str(numpy.mean(randnode_results_bhatta))  + " with SSTD: " + str(numpy.std(randnode_results_bhatta,  ddof=1)) +"\n")
    resultfile.write("average average hellinger on randomnode: " + str(numpy.mean(randnode_results_hellinger))  + " with SSTD: " + str(numpy.std(randnode_results_hellinger,  ddof=1)) +"\n")
    resultfile.write(" " +"\n")
    resultfile.write("average average KLD on Furer: " + str(numpy.mean(furer_results_KLD))  + " with SSTD: " + str(numpy.std(furer_results_KLD,  ddof=1)) +"\n")
    resultfile.write("average average bhatta on Furer: " + str(numpy.mean(furer_results_bhatta))  + " with SSTD: " + str(numpy.std(furer_results_bhatta,  ddof=1)) +"\n")
    resultfile.write("average average hellinger on Furer: " + str(numpy.mean(furer_results_hellinger))  + " with SSTD: " + str(numpy.std(furer_results_hellinger,  ddof=1)) +"\n")
    resultfile.write(" " +"\n")
    #resultfile.write("Experiment took: " +str(stop-start) + " seconds." +"\n")
    resultfile.write(' ' +"\n")
    #resultfile.write("Exhaustive took per run on average: " +str(numpy.mean(exhaustive_times)) + " seconds." +"\n")
    resultfile.write("Random node took per run on average: " +str(numpy.mean(randnode_times)) + " seconds." +"\n")
    resultfile.write("Furer took per run on average: " +str(numpy.mean(furer_times)) + " seconds." +"\n")
    resultfile.write('-----DETAILED RESULTS-----' +"\n")
    resultfile.write('randnode_results_KLD :' + str(randnode_results_KLD) +"\n")
    resultfile.write('randnode_results_bhatta :' + str(randnode_results_bhatta) +"\n")
    resultfile.write('randnode_results_hellinger :' + str(randnode_results_hellinger) +"\n")
    resultfile.write('furer_results_KLD :' + str(furer_results_KLD) +"\n")
    resultfile.write('furer_results_bhatta :' + str(furer_results_bhatta) +"\n")
    resultfile.write('furer_results_hellinger :' + str(furer_results_hellinger) +"\n")
    #resultfile.write('exhaustive_times :' + str(exhaustive_times) +"\n")
    resultfile.write('randnode_times :' + str(randnode_times) +"\n")
    resultfile.write('furer_times :' + str(furer_times) +"\n")
    resultfile.close()
    
    latexfile = open(latex_file_name,  'a')
    line1 = '$%s$ 	& random vertex & %s	& %.5f (%.5f) 	& %.5f (%.5f) 	& %.5f (%.5f) 	& %.0f \\\\ \n' % (short_graph_file_name,  str(NLIMIT_values[nli]), numpy.mean(randnode_results_KLD),  numpy.std(randnode_results_KLD,  ddof=1), numpy.mean(randnode_results_bhatta) ,  numpy.std(randnode_results_bhatta,  ddof=1),  numpy.mean(randnode_results_hellinger),  numpy.std(randnode_results_hellinger,  ddof=1),  numpy.mean(randnode_times))
    latexfile.write(line1)
    line2 = '$%s$ 	& Furer-Kasiv.  & %s	& %.5f (%.5f) 	& %.5f (%.5f) 	& %.5f (%.5f) 	& %.0f \\\\ \\hline \n' % (short_graph_file_name,   str(NLIMIT_values[nli]), numpy.mean(furer_results_KLD), numpy.std(furer_results_KLD,  ddof=1),  numpy.mean(furer_results_bhatta),  numpy.std(furer_results_bhatta,  ddof=1),  numpy.mean(furer_results_hellinger),  numpy.std(furer_results_hellinger,  ddof=1),  numpy.mean(furer_times))
    latexfile.write(line2)
    latexfile.close()


# za vse tu spodaj je treba samo, da je "plot_result_dict" tak kot mora biti


plotfile = open("latest_plot_info.txt",  'w')
plt.figure(1)
name = 'KLD_'+str(short_graph_file_name)+'_'+'x'+str(repetitions)+'.pdf'
plt.ylabel(name)
plt.xlabel('number of observations')
plotfile.write('name:' + str(name) +"\n")
# gathering random vertex points
rv_values = [plot_result_dict[k]["randomnode_KLD"][0] for k in NLIMIT_values]
rv_deviations = [plot_result_dict[k]["randomnode_KLD"][1] for k in NLIMIT_values]
rv_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in rv_deviations]
plt.plot(NLIMIT_values, rv_values, 'b-', label='random vertex')
plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
plotfile.write('NLIMIT_values:' + str(NLIMIT_values) +"\n")
plotfile.write('rv_values:' + str(rv_values) +"\n")
plotfile.write('rv_CI_points:' + str(rv_CI_points) +"\n")
# gathering Furer points
fu_values = [plot_result_dict[k]["furer_KLD"][0] for k in NLIMIT_values]
fu_deviations = [plot_result_dict[k]["furer_KLD"][1] for k in NLIMIT_values]
fu_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in fu_deviations]
plt.plot( NLIMIT_values, fu_values, 'r-', label='Fur-Kas')
plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
plotfile.write('fu_values:' + str(fu_values) +"\n")
plotfile.write('fu_CI_points:' + str(fu_CI_points) +"\n")
margin = max(NLIMIT_values)*0.1
minX = min(NLIMIT_values) - margin
maxX = max(NLIMIT_values) + margin
minY = 0
maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))
plt.axis([minX,  maxX,  minY,  maxY])
plt.legend()
plt.savefig(name, format="pdf")


plt.figure(2)
name = 'BHT_'+str(short_graph_file_name)+'_'+'x'+str(repetitions)+'.pdf'
plt.ylabel(name)
plt.xlabel('number of observations')
plotfile.write('name:' + str(name) +"\n")
# gathering random vertex points
rv_values = [plot_result_dict[k]["randomnode_BHT"][0] for k in NLIMIT_values]
rv_deviations = [plot_result_dict[k]["randomnode_BHT"][1] for k in NLIMIT_values]
rv_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in rv_deviations]
plt.plot(NLIMIT_values, rv_values, 'b-', label='random vertex')
plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
plotfile.write('rv_values:' + str(rv_values) +"\n")
plotfile.write('rv_CI_points:' + str(rv_CI_points) +"\n")
# gathering Furer points
fu_values = [plot_result_dict[k]["furer_BHT"][0] for k in NLIMIT_values]
fu_deviations = [plot_result_dict[k]["furer_BHT"][1] for k in NLIMIT_values]
fu_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in fu_deviations]
plt.plot( NLIMIT_values, fu_values, 'r-', label='Fur-Kas')
plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
plotfile.write('fu_values:' + str(fu_values) +"\n")
plotfile.write('fu_CI_points:' + str(fu_CI_points) +"\n")
margin = max(NLIMIT_values)*0.1
minX = min(NLIMIT_values) - margin
maxX = max(NLIMIT_values) + margin
minY = 0
maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))
plt.axis([minX,  maxX,  minY,  maxY])
plt.legend()
plt.savefig(name, format="pdf")


plt.figure(3)
name = 'HEL_'+str(short_graph_file_name)+'_'+'x'+str(repetitions)+'.pdf'
plt.ylabel(name)
plt.xlabel('number of observations')
plotfile.write('name:' + str(name) +"\n")
# gathering random vertex points
rv_values = [plot_result_dict[k]["randomnode_HEL"][0] for k in NLIMIT_values]
rv_deviations = [plot_result_dict[k]["randomnode_HEL"][1] for k in NLIMIT_values]
rv_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in rv_deviations]
plt.plot(NLIMIT_values, rv_values, 'b-', label='random vertex')
plt.errorbar(NLIMIT_values, rv_values, yerr=rv_CI_points, fmt='o')
plotfile.write('rv_values:' + str(rv_values) +"\n")
plotfile.write('rv_CI_points:' + str(rv_CI_points) +"\n")
# gathering Furer points
fu_values = [plot_result_dict[k]["furer_HEL"][0] for k in NLIMIT_values]
fu_deviations = [plot_result_dict[k]["furer_HEL"][1] for k in NLIMIT_values]
fu_CI_points = [(x/math.sqrt(repetitions))*1.96 for x in fu_deviations]
plt.plot( NLIMIT_values, fu_values, 'r-', label='Fur-Kas')
plt.errorbar(NLIMIT_values, fu_values, yerr=fu_CI_points, ecolor='r', fmt='or')
plotfile.write('fu_values:' + str(fu_values) +"\n")
plotfile.write('fu_CI_points:' + str(fu_CI_points) +"\n")
margin = max(NLIMIT_values)*0.1
minX = min(NLIMIT_values) - margin
maxX = max(NLIMIT_values) + margin
maxY = max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points) + 0.1* (max(rv_values + fu_values) + max(rv_CI_points + fu_CI_points))
minY = 0
plt.axis([minX,  maxX,  minY,  maxY])
plt.legend()
plt.savefig(name, format="pdf")

plotfile.close()
