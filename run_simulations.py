import os
import sys
from statistics import stdev,mean 

nodes = ["5653", "55ad", "55e4", "5599", "55dd", "5565", "560b", "5632", "55b3", "5563", "630a"]
#nodes = ["5563", "55ad"]
mod_names = {1: "FSK", 2: "OQPSK", 3: "OFDM", 4: "1M", 5: "2M", 6 : "3M", 7: "Round-Robin", 8: "Random", 9: "Best"}
mod_names = {1: "Random"}

results = {}
for n in nodes:
    results[n] = {}
    for i in range(1,len(mod_names)+1):
        results[n][mod_names[i]] = [[],[]]

number_retries = 3
replications = 10
output_file = "output_"+str(replications)+"rep_"+str(number_retries)+"rt_new_random.txt"

hasFile = False
pdr_or_rnp = 0# 0 => pdr 1 => rnp

if(not hasFile):
    for node in nodes:
        input_file = "traces/pdr_phy_"+node+".txt"
        of = open(output_file, "a+")
        of.write(node+"\n")
        of.close()
        if(False): 
            for i in range(1,4):
                of = open(output_file, "a+")
                of.write(mod_names[i]+"\n")
                of.close()
                for k in range(replications):
                    command = "python3 simulator_sun_single_1M_2M.py 1 "+str(number_retries)+" -10 "+str(i)+" < "+input_file+" >> "+output_file
                  #  print(command)
                    os.system(command)
                of = open(output_file, "a+")  
                of.write("1M\n")
                of.close()
            for k in range(replications):   
                command = "simulator_sun_single_1M_2M.py 1 "+str(number_retries)+" 10 1 < "+input_file+" >> "+output_file
               # print(command)
                os.system(command)
    
            of = open(output_file, "a+")
            of.write("2M\n")
            of.close()

            for k in range(replications):
                command = "python3 simulator_sun_single_1M_2M.py 2 "+str(number_retries)+" 10 < "+input_file+" >> "+output_file
                #print(command)
                os.system(command)
        if(False):

            of = open(output_file, "a+")    
            of.write("3M\n")
            of.close()
    
            for k in range(replications):   
                command = "python3 simulator_sun_3M.py "+str(number_retries)+" 10 < "+input_file+" >> "+output_file
                #print(command)
                os.system(command)
    
        if(False):
            
            of = open(output_file, "a+")    
            of.write("Round-Robin\n")
            of.close()

            for k in range(replications):
                command = "python3 simulator_sun_roundrobin.py "+str(number_retries)+" < "+input_file+" >> "+output_file
                #print(command)
                os.system(command)
            
        of = open(output_file, "a+")    
        of.write("Random\n")
        of.close()

        for k in range(replications):
            command = "python3 simulator_sun_random.py "+str(number_retries)+" < "+input_file+" >> "+output_file
            #print(command)
            os.system(command)
        
        if(False):
            of = open(output_file, "a+")    
            of.write("Best\n")
            of.close()

            for k in range(replications):
                command = "python3 simulator_sun_best.py "+str(number_retries)+" < "+input_file+" >> "+output_file
                #print(command)
                os.system(command)
        
of = open(output_file, "r")
for i in range(len(nodes)):
    n = of.readline()[:4]
    for j in range(len(mod_names)):
        m = of.readline()
        m = m[:(len(m))-1]
        for k in range(replications):
            res = of.readline()
            res = res[:(len(res))]
            res = res.split(",")
            results[n][m][0].append(float(res[0]))
            results[n][m][1].append(float(res[1]))
        #print(mean(results[n][m][0]))
        #print(mean(results[n][m][1]))   
        
#general results
out_mod = "Config"+"\t"
out_v = "PDR\t"
out_max = "MAX\t"
out_min = "MIN\t"
for i in range (1,(len(mod_names)+1)):
    m = mod_names[i]
    pdr = 0
    out_mod += m+"\t"
    maxv = 0
    minv = 1000
    for n in nodes:
        pdr += mean(results[n][m][pdr_or_rnp])
        if(mean(results[n][m][pdr_or_rnp]) > maxv):
            maxv = mean(results[n][m][pdr_or_rnp])
        if(mean(results[n][m][pdr_or_rnp]) < minv):
            minv = mean(results[n][m][pdr_or_rnp])
    pdr = pdr/len(nodes)
    out_v += str(pdr)+"\t"
    out_max += str(maxv) + "\t"
    out_min += str(minv) + "\t"
print(out_mod)
print(out_v)
print(out_max)
print(out_min)
print()
print()

#results per node
out_node = "Config" + "\t"
out_v = ""
out_max = ""
out_min = ""
out_mod = ""
for n in nodes:
    out_node += n+"\t"
print(out_node)

pdr = 0
maxv = 0
minv = 1000
for i in range (1,(len(mod_names)+1)):
    out_v += mod_names[i] + "\t"
    m = mod_names[i]
    for n in nodes:
        avg = mean(results[n][m][pdr_or_rnp])
        out_v += str(avg) + "\t"
    out_v += "\n"
print(out_v)
       
of.close()
    
    
    