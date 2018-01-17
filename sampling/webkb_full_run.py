'''
Created on Oct 25, 2016

@author: irma
'''
'''
Created on Oct 19, 2016

@author: irma
'''
import os
import subprocess,argparse

if __name__ == "__main__":
    for i in xrange(7,8):
            #subprocess.call("python /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/generate_commands_for_selected.py -data_graph_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/DATA/WEBKB/webkb.gml -pattern_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_WEBKB//patterns_size_"+str(i)+"/ -output_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_WEBKB/patterns_size_"+str(i)+"/ -output_script /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/ -path_to_scripts /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/ -runs 1 -time_interval 5 -level "+str(i)+" -max_time 600 -pattern_level_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_WEBKB//patterns_size_"+str(i)+"/ -fo /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_WEBKB/patterns_size_"+str(i)+"/",shell=True)
            #subprocess.call("wsub -l walltime=01:00:00 -l nodes=5:ppn=20:ivybridge -N wb_fur_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/worker_script/fur_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)
            #subprocess.call("wsub -l walltime=01:00:00 -l nodes=5:ppn=20:ivybridge -N wb_ffur_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/worker_script/ffur_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)
            #subprocess.call("wsub -l walltime=01:00:00 -l nodes=5:ppn=20:ivybridge -N wb_rnd_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/worker_script/rnd_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)
            #subprocess.call("wsub -l walltime=01:00:00 -l nodes=5:ppn=20:ivybridge -N wb_exh_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/worker_script/exh_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)
            subprocess.call("wsub -l walltime=05:00:00 -l nodes=5:ppn=20:ivybridge -N wb_ffur_ord_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/worker_script/ffur_order_random_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)
