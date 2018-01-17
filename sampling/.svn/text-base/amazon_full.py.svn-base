'''
Created on Dec 14, 2016

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
    parser.add_argument('-N',type=int,help='patterns size')
    parser.add_argument('-s',default=4,type=int,help='initial level')
    parser.add_argument('-e',default=10,type=int,help='end level')
    parser.add_argument('-exh',default=False,help='exhaustive only')
    
    args = parser.parse_args()
    start=args.s
    end=args.e
    patterns_size=args.N

    for i in xrange(start,end+1):
            #subprocess.call("python /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/generate_commands_for_selected.py -data_graph_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/DATA/AMAZON/amazon.gpickle -pattern_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_AMAZON/patterns_size_"+str(i)+"/ -output_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_AMAZON/patterns_size_"+str(i)+"/ -output_script /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_AMAZON/patterns_size_"+str(i)+"/ -path_to_scripts /user/leuven/311/vsc31168/Martin_experiments/graph_sampling/experiments/ -runs 1 -time_interval 300 -level "+str(i)+" -max_time 36000 -pattern_level_path /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/PATTERNS/PATTERNS_AMAZON//patterns_size_"+str(i)+"/ -fo /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/RESULTS/RESULTS_AMAZON/patterns_size_"+str(i)+"/"+" -write False" ,shell=True)
            if args.exh==False:
              subprocess.call("wsub -l walltime=20:00:00 -l nodes=5:ppn=20:ivybridge -N a_fur_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_AMAZON/patterns_size_"+str(i)+"/selected_patterns/worker_script/fur_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_AMAZON/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)
              subprocess.call("wsub -l walltime=20:00:00 -l nodes=5:ppn=20:ivybridge -N a_ffur_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_AMAZON/patterns_size_"+str(i)+"/selected_patterns/worker_script/ffur_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_AMAZON/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)
              subprocess.call("wsub -l walltime=20:00:00 -l nodes=5:ppn=20:ivybridge -N a_rnd_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_AMAZON/patterns_size_"+str(i)+"/selected_patterns/worker_script/rnd_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_AMAZON/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)
            else:
              subprocess.call("wsub -l walltime=20:00:00 -l nodes=5:ppn=20:ivybridge -N a_exh_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_AMAZON/patterns_size_"+str(i)+"/selected_patterns/worker_script/exh_"+str(i)+"_ws.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_AMAZON/patterns_size_"+str(i)+"/selected_patterns/worker_script/param.data -A lp_dtai1",shell=True)
            