import pandas as pd
import os

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
    path_to_results="/home/irma/work/DATA/INFERENCE_DATA/WEBKB/experiments_inference/page_class/RESULTS/"
    csvs_to_merge=[]
    for dir in os.listdir(path_to_results):
        if "pattern" in dir:
            csvs_to_merge.append(os.path.join(path_to_results,dir,"exact","train.csv"))
    merge_csvs(csvs_to_merge,"/home/irma/work/DATA/INFERENCE_DATA/WEBKB/experiments_inference/page_class/RESULTS/merged_test.csv")