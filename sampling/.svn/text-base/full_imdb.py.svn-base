'''
Created on Jan 24, 2017

@author: irma
'''
'''
Created on Dec 1, 2016

@author: irma
'''
import os
import subprocess,argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-s',default=4,type=int,help='initial level')
    parser.add_argument('-e',default=10,type=int,help='end level')
    
    args = parser.parse_args()
    start=args.s
    end=args.e

    for i in xrange(start,end+1):
            subprocess.call("python /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/generate_commands_for_selected.py -data_graph_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/DATA/IMDB/imdb.gml -pattern_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB/patterns_size_"+str(i)+"/ -output_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_IMDB/patterns_size_"+str(i)+"/ -output_script /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(i)+"/ -path_to_scripts /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/ -runs 1 -time_interval 5 -level "+str(i)+" -max_time 600 -pattern_level_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_IMDB//patterns_size_"+str(i)+"/ -fo /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_IMDB/patterns_size_"+str(i)+"/",shell=True)
            #subprocess.call("wsub -l walltime=01:00:00 -l nodes=5:ppn=20:ivybridge -N fb_fur_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_FACEBOOK/patterns_size_"+str(i)+"/selected_patterns/worker_script/fur_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_FACEBOOK/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1 > /dev/null 2>&1",shell=True)
            #subprocess.call("wsub -l walltime=01:00:00 -l nodes=5:ppn=20:ivybridge -N fb_ffur_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_FACEBOOK/patterns_size_"+str(i)+"/selected_patterns/worker_script/ffur_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_FACEBOOK/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1 > /dev/null 2>&1",shell=True)
           # subprocess.call("wsub -l walltime=01:00:00 -l nodes=5:ppn=20:ivybridge -N fb_rnd_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_FACEBOOK/patterns_size_"+str(i)+"/selected_patterns/worker_script/rnd_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_FACEBOOK/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1 > /dev/null 2>&1",shell=True)
           # subprocess.call("wsub -l walltime=04:00:00 -l nodes=5:ppn=20:ivybridge -N fb_ffur_ord_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_FACEBOOK/patterns_size_"+str(i)+"/selected_patterns/worker_script/ffur_order_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_FACEBOOK/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1 > /dev/null 2>&1",shell=True)
            subprocess.call("wsub -l walltime=04:00:00 -l nodes=5:ppn=20:ivybridge -N im_ffur_order_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(i)+"/selected_patterns/worker_script/ffur_order_random_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_IMDB/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)

            #subprocess.call("wsub -l walltime=01:00:00 -l nodes=5:ppn=20:ivybridge -N fb_exh_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_FACEBOOK/patterns_size_"+str(i)+"/selected_patterns/worker_script/exh_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_FACEBOOK/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1 > /dev/null 2>&1",shell=True)
            