import os

if __name__ == '__main__':
    patterns_path="/home/irma/work/DATA/DATA/WEBKB/experiments_inference/page_class/PATTERNS/"
    results_path="/home/irma/work/DATA/DATA/WEBKB/experiments_inference/page_class/RESULTS/"
    train="/home/irma/work/DATA/DATA/WEBKB/folds/fold1-train.db"
    test="/home/irma/work/DATA/DATA/WEBKB/folds/fold1-train.db"
    output_script="/home/irma/work/DATA/DATA/WEBKB/train_1.data"
    e="exact"
    const="page"
    attr="page_class"
    rT="page_class"
    sT=2
    max_time=600

    with open(output_script,'w') as f:
        f.write("train,test,o,e,p,const,attr,rT,sT,max_time\n")
        for dir in os.listdir(patterns_path):
            if not "pattern" in dir:
                continue
            p=os.path.join(patterns_path,dir)
            o=os.path.join(patterns_path,dir).replace("PATTERNS","RESULTS")
            f.write(train+","+test+","+o+","+e+","+p+","+const+","+attr+","+rT+","+str(sT)+","+str(max_time)+"\n")


