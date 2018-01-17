'''
Created on Mar 24, 2016

@author: irma
'''
import argparse,os

if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Run exhaustive approach')
  parser.add_argument('-r',help='path to results') 
  args = parser.parse_args()
  res=args.r
  
  overall=0
  no_obd=0
  no_obd_paths=[]
  timeout=0
  overall=0
  for b in os.listdir(res):
      if b.startswith("patterns_size"):
          for batch in os.listdir(os.path.join(res,b)):
              if batch.startswith("batch"):
                  for patt in os.listdir(os.path.join(res,b,batch)):
                      if os.path.exists(os.path.join(res,b,batch,patt,'results_furer','complete.info')):
                          #print os.path.join(res,b,batch,patt,'results_furer','complete.info')
                          overall+=1
                          if os.path.exists(os.path.join(res,b,batch,patt,'results_furer','no_obdecomp.info')):
                              no_obd+=1
                              no_obd_paths.append(os.path.join(res,b,batch,patt))
                          if os.path.exists(os.path.join(res,b,batch,patt,'results_furer','no_obdecomp.info')):
                              no_obd+=1
                              no_obd_paths.append(os.path.join(res,b,batch,patt))
  print "overall: ",overall
  print "no obd: ",no_obd
  for p in no_obd_paths:
    print p
  print "Precentage no obd: ",no_obd/float(overall)
                  
