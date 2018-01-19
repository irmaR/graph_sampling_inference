import pandas as pd
import os,argparse

def merge_csvs(csvs_to_merge,out):
    dfs = []
    target_added=False
    grounding_added=False
    for filename in csvs_to_merge:
        # read the csv, making sure the first two columns are str
        df = pd.read_csv(filename, header=None, converters={0: str, 1: str})
        # throw away all but the first two columns
        if not target_added:
          df = df.ix[:,:2]
          target_added=True
        else:
          df = df.ix[:, 2]
        # change the column names so they won't collide during concatenation
        #df.columns = [filename + str(cname) for cname in df.columns]
        dfs.append(df)

    # concatenate them horizontally
    merged = pd.concat(dfs,axis=1)
    # write it out
    merged.to_csv(out, header=None, index=None)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-p', help='path to train gpickle')
    parser.add_argument('-e', help='path to train gpickle')
    parser.add_argument('-o', help='output')
    args = parser.parse_args()
    path_to_results=args.p
    if not os.path.isdir(path_to_results):
        os.makedirs(path_to_results)
    csvs_to_merge_train=[]
    csvs_to_merge_test = []
    for dir in os.listdir(path_to_results):
        if "pattern" in dir:
            csvs_to_merge_train.append(os.path.join(path_to_results,dir,args.e,"train.csv"))
            csvs_to_merge_test.append(os.path.join(path_to_results, dir, args.e,"test.csv"))
    merge_csvs(csvs_to_merge_train, os.path.join(args.o, "merged_train.csv"))
    merge_csvs(csvs_to_merge_test,os.path.join(args.o,"merged_test.csv"))
