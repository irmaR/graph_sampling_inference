import matplotlib.pyplot as plt
import argparse,sys
import os,csv,math
import numpy as np
import random as rand
import graph_manipulator.visualization as vis
import subprocess
import os
import tempfile
import shutil

def extract_info_furer(path_info_file_furer):
    KLD=None
    embeddings=None
    stdev=None
    with open(path_info_file_furer,'r') as f:
        for line in f.readlines():
            if "average average KLD on furer:" in line:
                KLD=float(line.split(" ")[5])
            if "average of embeddings :" in line:
                embeddings=float(line.split(" ")[4])
            if "stdeviation of # embeddings:" in line:
                stdev=float(line.split(" ")[4])
    return (KLD,embeddings,stdev)

def extract_info_exhaustive(path_info_file_exhaustive):
    embeddings=None
    nr_observations=None
    with open(path_info_file_exhaustive,'r') as f:
        for line in f.readlines():
            if "Number of embeddings:" in line:
                embeddings=int(line.split(" ")[3])
            if "Total number of observations:" in line:
                nr_observations=int(line.split(" ")[4])
    return (embeddings,nr_observations)
             

def furer_plots(path_to_results):
  path=os.path.join(path_to_results,"results_furer","monitoring")
  x_minutes=list(range(5,600,5))
  y=[]
  KLDs=[]
  average_embeddings=[]
  stdevs=[]
  
  for el in x_minutes:
      if os.path.exists(os.path.join(path,'res_time_'+str(el*60)+".info")):
          KLD,embeddings,stdeviation=extract_info_furer(os.path.join(path,'res_time_'+str(el*60)+".info"))
          KLDs.append(KLD)
          average_embeddings.append(embeddings)
          stdevs.append(stdeviation)
      else:
          KLDs.append(np.nan)
          average_embeddings.append(np.nan)
          stdevs.append(np.nan)        
  return (KLDs,average_embeddings,stdevs)

def main(path_to_results):
  x_minutes=list(range(5,600,5))
  #EXHAUSTIVE
  exhaustive_result=os.path.join(path_to_results,"exhaustive_approach")
  if os.path.exists(exhaustive_result):
      for file in os.listdir(exhaustive_result):
         if file.endswith(".res"):
            nr_embeddings_exhaustive=extract_info_exhaustive(os.path.join(exhaustive_result,file))[0]
  print "Nr embeddings exhaustive, ",nr_embeddings_exhaustive
  nr_emb_exhaustive=[nr_embeddings_exhaustive]*len(x_minutes)
  #FURER
  KLDs_furer,embeddings_furer,stdev_furer=furer_plots(path_to_results)
  plt.figure(1)
  plt.subplot(211)
  plt.ylabel('KLD')
  plt.xlabel('Sampling time (minutes)')
  plt.plot(x_minutes, KLDs_furer, 'b-')
  plt.subplot(212)
  plt.ylabel('Avg. #embeddings')
  plt.xlabel('Sampling time (minutes)')
  plt.errorbar(x_minutes, embeddings_furer, stdev_furer, fmt='o-',label='Furer-OBD')
  plt.plot(x_minutes, nr_emb_exhaustive,label='exhaustive')
  plt.ylim(0,max(embeddings_furer)+10*max(stdev_furer))
  plt.legend( loc='upper left' )
  plt.show()


def get_embeddings_exhaustive_csv(exhaustive_csv):
    report_embeddings=[]
    final_embeddings=[]
    pattern_names=[]
    patterns=[]
    with open(exhaustive_csv, 'rb') as csvfile:
       reader = csv.DictReader(csvfile, delimiter=',')
       for row in reader:
          one_row_exh_embeddings=[]
          for i in xrange(1,121):
              if row["emb_"+str(i)]!="":
                one_row_exh_embeddings.append(float(row["emb_"+str(i)]))
          if row["exh_emb"]!="":
              final_embeddings.append(float(row["exh_emb"]))    
          else:
              final_embeddings.append(np.nan) 
          report_embeddings.append(row)
          readable_format=row["edges"]
          patterns.append(vis.convert_readable_format_to_graph(readable_format))
          pattern_names.append(row["pattern_name"])                  
    return patterns,pattern_names,report_embeddings,final_embeddings

'''
Given a network format of a pattern, turn it into a basic tikz format"
'''
def get_tikz_format_pattern(pattern):
    str_res="\\begin{tikzpicture}\n"
    #str_res+="\\GraphInit[vstyle=Normal]\n"
    str_res+="\\tikzset{VertexStyle/.style = {\n"
    str_res+="shape = rectangle,\n"
    str_res+="fill = white,\n"
    str_res+="inner sep = 0pt,\n"
    str_res+="outer sep = 0pt,\n"
    str_res+="minimum size = 8pt,\n"
    str_res+="}}\n"
    str_res+="\\SetGraphUnit{2}\n"
    str_res+="\\begin{scope}[rotate=-135]\n"
    str_res+="\\Vertices{circle}{"
    counter=0
    for nd in pattern.nodes():
        if counter==(len(pattern.nodes())-1):
           str_res+=nd.split(":")[1].replace(":","\\_")+nd.split(":")[0].replace("u","")+"}\n"
        else:
           str_res+=nd.split(":")[1].replace(":","\\_")+nd.split(":")[0].replace("u","")+","
        counter+=1
    str_res+="\\end{scope}\n"
    #print str_res
    for n in pattern.nodes():
        edges=pattern.neighbors(n)
        for edge in edges:
            #print "EDGE: ",edge.split(":")[1].replace(":","\\_")+n.split(":")[0].replace("u","")
            str_res+="\Edge"+"("+n.split(":")[1].replace(":","\\_")+n.split(":")[0].replace("u","")+")("+edge.split(":")[1].replace(":","\\_")+edge.split(":")[0].replace("u","")+")\n"
    str_res+="\end{tikzpicture}\n"
    #print str_res
    return str_res
    

def get_tikz_format_KLD(pattern_graph,pattern_name_res,x_coord,KLD_furer,KLD_false_furer,KLD_random):
    #str_res="\\begin{figure}\n"
    #str_res+=get_tikz_format_pattern(pattern_graph)+"\n"
    #str_res+="\\end{figure}\n"
    str_res=""
    str_res+="\\begin{figure}\n"
    str_res+="\\centering\n"
    str_res+="\\begin{tikzpicture} \n"
    str_res+="\\begin{semilogyaxis}[\n"
    str_res+="xlabel=Sampling time (seconds),\n"
    str_res+="ylabel=KLD,\n"
    str_res+="height=11cm,\n"
    str_res+="width=13cm,\n"
    str_res+="legend pos=outer north east]\n"

    counter=0
    if KLD_furer!=None:
        str_res+="\\addplot coordinates {\n"
        for x in x_coord:
            str_res+="("+str(x)+","+str(KLD_furer[counter])+")\n"
            counter+=1
        str_res+="};\n" 
        str_res+="\\addlegendentry{Furer-OBD}\n" 
    
    if KLD_false_furer!=None:
        counter=0 
        str_res+="\\addplot coordinates {\n"
        for x in x_coord:
            str_res+="("+str(x)+","+str(KLD_false_furer[counter])+")\n"
            counter+=1
        str_res+="};\n" 
        str_res+="\\addlegendentry{Furer-AD}\n" 
    
    #random
    if KLD_random!=None:
        counter=0
        str_res+="\\addplot coordinates {\n"
        for x in x_coord:
            str_res+="("+str(x)+","+str(KLD_random[counter])+")\n"
            counter+=1
        str_res+="};\n" 
        str_res+="\\addlegendentry{Random}\n" 
    str_res+="\\end{semilogyaxis}\n"
    str_res+="\\end{tikzpicture}\n"
    str_res+="\\caption{Pattern: "+'/'.join(pattern_name_res.split("/")[-2:]).replace("_","\\_")+". Y axis is given in logarithmic scale.}\n"
    str_res+="\\end{figure}\n"
    return str_res

def get_error_bar_option():
    return "[error bars/.cd,\n"+"y dir=both, y explicit,\n"+"error bar style={line width=2pt}]\n"

def get_tikz_format_embs(pattern_graph,pattern_name_res,x_coord,final_emb_exhaustive,embs_furer,embs_false_furer,embs_random,stdev_furer,stdevs_false_furer,stdevs_random,plotting_error_bars_flag):
    print "Plotting error bars? ",plotting_error_bars_flag
    embs_exh_fin_embeddings=[final_emb_exhaustive] * 120
    str_res=""
    #str_res="\\begin{figure}\n"
    #str_res+=get_tikz_format_pattern(pattern_graph)+"\n"
    #str_res+="\\end{figure}\n"
    str_res+="\\begin{figure}\n"
    str_res+="\\centering\n"
    str_res+="\\begin{tikzpicture} \n"
    str_res+="\\begin{axis}[\n"
    str_res+="xlabel=Sampling time (seconds),\n"
    str_res+="ylabel=\\# embeddings,\n"
    str_res+="height=11cm,\n"
    str_res+="width=13cm,\n"
    str_res+="legend pos=outer north east]\n"
    counter=0
    if embs_furer!=None:
        if not plotting_error_bars_flag: 
         str_res+="\\addplot "+""+" coordinates {\n"
        else:
         str_res+="\\addplot[error bars/.cd,y dir=both,y explicit] coordinates {\n"
        for x in x_coord:
            if stdev_furer!=None:
               str_res+="("+str(x)+","+str(embs_furer[counter])+") +- (0,"+str(stdev_furer[counter])+")\n"
            else:
               str_res+="("+str(x)+","+str(embs_furer[counter])+")\n" 
            counter+=1
        str_res+="};\n" 
        str_res+="\\addlegendentry{Furer-OBD}\n" 
  
    if embs_false_furer!=None:
        counter=0
        if not plotting_error_bars_flag: 
         str_res+="\\addplot "+""+" coordinates {\n"
        else:
         str_res+="\\addplot[error bars/.cd,y dir=both,y explicit] coordinates {\n"
        for x in x_coord:
            if stdevs_false_furer!=None:
               str_res+="("+str(x)+","+str(embs_false_furer[counter])+") +- (0,"+str(stdevs_false_furer[counter])+")\n"
            else:
               str_res+="("+str(x)+","+str(embs_false_furer[counter])+")\n" 
            counter+=1
        str_res+="};\n" 
        str_res+="\\addlegendentry{Furer-AD}\n" 
    #random
    if embs_random!=None:
        counter=0
        if not plotting_error_bars_flag: 
         str_res+="\\addplot "+""+" coordinates {\n"
        else:
         str_res+="\\addplot[error bars/.cd,y dir=both,y explicit] coordinates {\n"
        for x in x_coord:
            if stdevs_random!=None:
              str_res+="("+str(x)+","+str(embs_random[counter])+") +- (0,"+str(stdevs_random[counter])+")\n"
            else:
              str_res+="("+str(x)+","+str(embs_random[counter])+")\n"
            counter+=1
        str_res+="};\n" 
        str_res+="\\addlegendentry{Random}\n" 
        
    if embs_exh_fin_embeddings!=None:
        counter=0
        if not plotting_error_bars_flag: 
         str_res+="\\addplot "+""+" coordinates {\n"
        else:
         str_res+="\\addplot[error bars/.cd,y dir=both,y explicit] coordinates {\n"
        for x in x_coord:
            str_res+="("+str(x)+","+str(embs_exh_fin_embeddings[counter])+")\n"
            counter+=1
        str_res+="};\n" 
        str_res+="\\addlegendentry{Exhaustive}\n" 
    str_res+="\\end{axis}\n"
    str_res+="\\end{tikzpicture}\n"
    str_res+="\\caption{Pattern: "+'/'.join(pattern_name_res.split("/")[-2:]).replace("_","\\_")+".}\n"
    str_res+="\\end{figure}\n"
    return str_res

def get_info_furer_csv(furer_csv):
    tikz_string=""
    report_embeddings=[]
    report_KLDs=[]
    stdevs_furer=[]
    
    with open(furer_csv, 'rb') as csvfile:
       
       reader = csv.DictReader(csvfile, delimiter=',')
       for row in reader:
          KLD_nonNANentry=False
          STD_nonNANentry=False
          EMB_nonNANentry=False
          one_row_KLDs=[]
          one_row_embeddings=[]
          one_row_stdevs=[]
          for i in xrange(1,121):
              if row["emb_"+str(i)]!="":
                one_row_embeddings.append(float(row["emb_"+str(i)]))
                EMB_nonNANentry=True
              else:
                one_row_embeddings.append(np.nan)
              if row["std_"+str(i)]!="":
                one_row_stdevs.append(float(row["std_"+str(i)]))
                STD_nonNANentry=True
              else:
                one_row_stdevs.append(np.nan)
              if row["KLD_"+str(i)]!="":
                one_row_KLDs.append(float(row["KLD_"+str(i)]))
                KLD_nonNANentry=True
              else:
                one_row_KLDs.append(np.nan)
          if(KLD_nonNANentry):
             report_KLDs.append(one_row_KLDs)    
          else:
             report_KLDs.append([]) 
          if(EMB_nonNANentry):
             report_embeddings.append(one_row_embeddings)    
          else:
             report_embeddings.append([])     
          if(STD_nonNANentry):  
             stdevs_furer.append(one_row_stdevs)  
          else:
             stdevs_furer.append([])  
    return report_KLDs,report_embeddings,stdevs_furer

def get_info_random_csv(random_csv):
    tikz_string=""
    report_embeddings=[]
    report_KLDs=[]
    stdevs_random=[]
    with open(random_csv, 'rb') as csvfile:
       reader = csv.DictReader(csvfile, delimiter=',')
       for row in reader:
          one_row_KLDs=[]
          one_row_embeddings=[]
          one_row_stdevs=[]
          for i in xrange(1,121):
              if row["emb_"+str(i)]!="":
                one_row_embeddings.append(float(row["emb_"+str(i)]))
              else:
                one_row_embeddings.append(np.nan)
              if row["std_"+str(i)]!="":
                one_row_stdevs.append(float(row["std_"+str(i)]))
              else:
                one_row_stdevs.append(np.nan)
              if row["KLD_"+str(i)]!="":
                one_row_KLDs.append(float(row["KLD_"+str(i)]))
              else:
                one_row_KLDs.append(np.nan)
          report_KLDs.append(one_row_KLDs)    
          report_embeddings.append(one_row_embeddings)
          stdevs_random.append(one_row_stdevs)         
    return report_KLDs,report_embeddings,stdevs_random

def plot(exhaustive_csv,furer_csv,false_furer_csv,random_csv,output_folder,level,plot_error_bars_flag,row):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    pattern_graphs,pattern_names,report_embeddings,final_embedding=get_embeddings_exhaustive_csv(exhaustive_csv)
    KLDs_furer,embeddings_furer,stdevs_furer=get_info_furer_csv(furer_csv)
    KLDs_false_furer,embeddings_false_furer,stdevs_false_furer=get_info_furer_csv(false_furer_csv)
    KLDs_random=[]
    embeddings_random=[]
    if os.path.exists(random_csv):
       KLDs_random,embeddings_random,stdevs_random=get_info_random_csv(random_csv)
    x_minutes=list(range(5,605,5))
    dim=math.sqrt(len(KLDs_false_furer))
    KLDs_latex_format=""
    embs_latex_format=""
    counter=0
    while counter<len(pattern_names):
         if row!=-1 and (counter+1)!=row:
             counter+=1
             continue
         pattern=pattern_graphs[counter]
         pattern_name=pattern_names[counter]
         KLDs_furer_inst=None
         embs_furer_inst=None
         KLDs_false_furer_inst=None
         embs_false_furer_inst=None
         KLDs_random_inst=None
         embs_random_inst=None
         stdevs_furer_inst=None
         stdevs_false_furer_inst=None
         stdevs_random_inst=None
         try:
           KLDs_furer_inst=KLDs_furer[counter]
         except IndexError:
           KLDs_furer_inst=None
         try:
           KLDs_false_furer_inst=KLDs_false_furer[counter]
         except IndexError:
           KLDs_false_furer_inst=None
         try:  
           KLDs_random_inst=KLDs_random[counter]
         except IndexError:
           KLDs_random_inst=None
         try:
           embs_furer_inst=embeddings_furer[counter]
         except IndexError:
           embs_furer_inst=None
         try:
           embs_false_furer_inst=embeddings_false_furer[counter]
         except IndexError:
           embs_false_furer_inst=None
         try:  
           embs_random_inst=embeddings_random[counter]
         except IndexError:
           embs_random_inst=None
         try:  
           stdevs_furer_inst=stdevs_furer[counter]
         except IndexError:
           stdevs_furer_inst=None
         try:  
           stdevs_false_furer_inst=stdevs_false_furer[counter]
         except IndexError:
           stdevs_false_furer_inst=None
         try:  
           stdevs_random_inst=stdevs_random[counter]
         except IndexError:
           stdevs_random_inst=None  
         if KLDs_furer_inst==[]:
             KLDs_furer_inst=None
         if KLDs_false_furer_inst==[]:
             KLDs_false_furer_inst=None
         if KLDs_random_inst==[]:
             KLDs_random_inst=None
         if embs_furer_inst==[]:
             embs_furer_inst=None
         if embs_false_furer_inst==[]:
            embs_false_furer_inst=None
         if embs_random_inst==[]:
             embs_random_inst=None
         if stdevs_furer_inst==[]:
            stdevs_furer_inst=None
         if stdevs_false_furer_inst==[]:
            stdevs_false_furer_inst=None
         if stdevs_random_inst==[]:
             stdevs_random_inst=None
         print KLDs_furer_inst
         KLDs_latex_format+=get_tikz_format_KLD(pattern,pattern_name,x_minutes,KLDs_furer_inst,KLDs_false_furer_inst,KLDs_random_inst)
         KLDs_latex_format+="\\clearpage\n"
         embs_latex_format+=get_tikz_format_embs(pattern,pattern_name,x_minutes,final_embedding[counter],embs_furer_inst,embs_false_furer_inst,embs_random_inst,stdevs_furer_inst,stdevs_false_furer_inst,stdevs_random_inst,plot_error_bars_flag)
         embs_latex_format+="\\clearpage\n"
         print pattern_names[counter]
         counter+=1
    
    file_KLD=os.path.join(output_folder+"/"+"KLD_results_"+str(level)+"_.tex")
    with open(os.path.join(output_folder+"/"+"KLD_results_"+str(level)+"_.tex"),'w') as f:
        str_res=""
        str_res+="\\documentclass[a4paper,10pt]{article}\n"
        str_res+="\\usepackage{a4wide}\n"
        str_res+="\\usepackage{hyperref}\n"
        str_res+="\\usepackage{graphicx}\n"
        str_res+="\\usepackage{pgfplots}\n"
        str_res+="\\usepackage{tkz-graph}\n"
        str_res+="\\GraphInit[vstyle = Normal]\n"
        str_res+="\\pgfplotsset{every tick label/.append style={font=\large}}\n"
        str_res+="\\pgfplotsset{every axis label/.append style={font=\LARGE}}\n"
        str_res+="\\begin{document} \n"
        f.write(str_res)
        f.write(KLDs_latex_format)
        f.write("\\end{document}")
    
    filEMB=os.path.join(output_folder+"/"+"EMB_results_"+str(level)+"_.tex")
    with open(os.path.join(output_folder+"/"+"EMB_results_"+str(level)+"_.tex"),'w') as f:
        str_res=""
        str_res+="\\documentclass[a4paper,10pt]{article}\n"
        str_res+="\\usepackage{a4wide}\n"
        str_res+="\\usepackage{hyperref}\n"
        str_res+="\\usepackage{graphicx}\n"
        str_res+="\\usepackage{pgfplots}\n"
        str_res+="\\usepackage{tkz-graph}\n"
        str_res+="\\GraphInit[vstyle = Normal]\n"
        str_res+="\\pgfplotsset{every tick label/.append style={font=\large}}\n"
        str_res+="\\pgfplotsset{every axis label/.append style={font=\LARGE}}\n"
        str_res+="\\begin{document} \n"
        f.write(str_res)
        f.write(embs_latex_format)
        f.write("\\end{document}")
        
    generate_pdf("KLD_results_"+str(level)+"_.pdf", file_KLD,output_folder)
    generate_pdf("EMB_results_"+str(level)+"_.pdf", filEMB,output_folder)
    
def generate_pdf(pdfname,tex_file,dest):
    """
    Genertates the pdf from string
    """
    import subprocess
    import os
    import tempfile
    import shutil
    
    current = dest
    temp = tempfile.mkdtemp()
    os.chdir(temp)
    
    tex=""
    with open(tex_file,'r') as f:
        for line in f.readlines():
            tex+=line
    f = open('cover.tex','w')
    f.write(tex)
    f.close()
    
    proc=subprocess.check_call(['pdflatex','-interaction=batchmode','cover.tex','1>/dev/null'])
    #subprocess.Popen(['pdflatex',tex])
    #proc.communicate()
    
    os.rename('cover.pdf',pdfname)
    print "Copying ",pdfname,"to ",current
    shutil.copy(pdfname,current)
    shutil.rmtree(temp)   
    
if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to csv files')
  parser.add_argument('-l',help='patterns size level')
  parser.add_argument('-eb',default=False,action='store_true',help='flag for plotting error bars: true or false. FALSE by default')
  parser.add_argument('-row',default=-1,type=int,help='Specific row counting from 1. By default -1 which means, plot all rows')
  args = parser.parse_args()
  plot(os.path.join(args.r,"exhaustive_"+str(args.l)+".csv"),os.path.join(args.r,"furer_"+str(args.l)+".csv"),os.path.join(args.r,"Ffurer_"+str(args.l)+".csv"),os.path.join(args.r,"random_"+str(args.l)+".csv"),os.path.join(args.r,"plots"),args.l,args.eb,args.row)