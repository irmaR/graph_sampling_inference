import os,shutil,argparse


def move_selected_patterns(selected_pattern_list,output_directory):
    if not os.path.exists(output_directory):
     os.makedirs(output_directory)
    with open(selected_pattern_list,'r') as f:
        for line in f:
             line=line.rstrip()
             pattern_file=os.path.join(line,'input_pattern.gml')
             pattern_name=line.split("/")[-1].replace("/","")
             print "pattern file: ",pattern_file
             print "pattern name", pattern_name
             print "output: ",os.path.join(output_directory,pattern_name+'.gml')
             shutil.copy(pattern_file,os.path.join(output_directory,pattern_name+'.gml'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-pl', help='path to data file')
    parser.add_argument('-o', help='output path')
    args = parser.parse_args()
    move_selected_patterns(args.pl, args.o)
