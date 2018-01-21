'''
Created on Oct 28, 2016

@author: irma
'''
import os
import subprocess,argparse

if __name__ == "__main__":
    for i in xrange(4,11):
            subprocess.call("wsub -l walltime=01:00:00 -l nodes=5:ppn=20:ivybridge -N imdb_r_fur_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/reporting/report_furer.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/reporting/param.data -A lp_dtai1",shell=True)
            subprocess.call("wsub -l walltime=01:00:00 -l nodes=5:ppn=20:ivybridge -N imdb_r_ffur_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/reporting/report_false_furer.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/reporting/param.data -A lp_dtai1",shell=True)
            subprocess.call("wsub -l walltime=01:00:00 -l nodes=5:ppn=20:ivybridge -N imdb_r_rnd_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/reporting/report_random.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/reporting/param.data -A lp_dtai1",shell=True)
            subprocess.call("wsub -l walltime=01:00:00 -l nodes=5:ppn=20:ivybridge -N imdb_r_exh_"+str(i)+" -batch /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/reporting/report_exhaustive.pbs -data /data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/COMMANDS/COMMANDS_WEBKB/patterns_size_"+str(i)+"/selected_patterns/reporting/param.data -A lp_dtai1",shell=True)