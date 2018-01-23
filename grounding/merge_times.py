import pandas as pd
import os,argparse

def get_average(csvs_to_merge,out):
    target_added=False
    grounding_added=False
    pattern_time_dict={}
    sum_time=0
    for filename in csvs_to_merge:
        # read the csv, making sure the first two columns are str
        df = pd.read_csv(filename, header=None, converters={0: str, 1: str},skiprows=1)

        for index, row in df.iterrows():
            pattern=row[0]
            time=float(row[1])
            sum_time+=time
            if pattern in pattern_time_dict:
                pattern_time_dict[pattern]+=time
            else:
                pattern_time_dict[pattern]=time

    average_time=sum_time/len(csvs_to_merge)
    average_time_per_pattern={}
    for p in pattern_time_dict:
        average_time_per_pattern[p]=pattern_time_dict[p]/len(csvs_to_merge)

    print "Average time over folds: ",average_time

def merge_csvs_main(path_to_results,out,exp):
    if not os.path.isdir(out):
        os.makedirs(out)
    csvs_to_merge_train = []
    csvs_to_merge_test = []
    for dir in os.listdir(path_to_results):
        if "fold" in dir:
            csvs_to_merge_train.append(os.path.join(path_to_results, dir, exp, "time_dict_train.csv"))
            csvs_to_merge_test.append(os.path.join(path_to_results, dir, exp, "time_dict_test.csv"))
    get_average(csvs_to_merge_train, os.path.join(out, "average_train_time.csv"))
    get_average(csvs_to_merge_test, os.path.join(out, "average_test_time.csv"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-p', help='path to train gpickle')
    parser.add_argument('-e', help='path to train gpickle')
    parser.add_argument('-o', help='output')
    args = parser.parse_args()
    merge_csvs_main(args.p, args.o, args.e)
