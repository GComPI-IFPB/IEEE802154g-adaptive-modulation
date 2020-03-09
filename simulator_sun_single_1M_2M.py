#simulator considering the use of only one or two modulations at a given time and estimation at the end-node
import random
import sys

num_of_mod = int(sys.argv[1])
number_of_retries = int(sys.argv[2])
window_size = int(sys.argv[3])

current_mod = [1,2]

if(num_of_mod == 1):
    current_mod[0] = int(sys.argv[4])
    current_mod[1] = current_mod[0]
    
modulations = {1:"FSK", 2:"OQPSK", 3:"OFDM"}
    

packet_counter = 0
retry = 0

tx_counter = [0,0,0,0]
ack_counter = [0,0,0,0]
prr_th = 0.9

rx_counter = 0
retry_counter = 0
prev_packet = -1

cont_window = 0

cont_trial = 0
acc_trial = 0

verbose = False

try:
    random.seed()
    current_config = 0
   
    while (True):
        #the the PDR to transmit the next packet
        if(retry == 0):
            if(cont_window == 0):
                ent = input().split('\t')
                cont_window = int(ent[1])
                pdr_fsk = float(ent[2])
                pdr_oqpsk = float(ent[3])
                pdr_ofdm = float(ent[4])
                if(verbose):
                    print("PDR FSK: ",pdr_fsk)
                    print("PDR OQPSK: ",pdr_oqpsk)
                    print("PDR OFDM",pdr_ofdm)
            cont_window -= 1
            
        #calculating a new estimation for one of the modulations
        if(tx_counter[current_mod[retry%2]] == window_size):
            arr = ack_counter[current_mod[retry%2]]/tx_counter[current_mod[retry%2]]
            tx_counter[current_mod[retry%2]] = 0
            ack_counter[current_mod[retry%2]] = 0
            if(verbose):
                print("ARR of {} = {}: ".format(modulations[current_mod[retry%2]],arr))
            if(arr < prr_th):
                if(verbose):
                    print("Drop ",modulations[current_mod[retry%2]])
            
                if(num_of_mod == 1):
                    current_mod[retry%2] = 1 + current_mod[retry%2]%3
                    current_mod[(retry%2)-1] = current_mod[retry%2]
                    if(verbose):
                        print("Use ",modulations[current_mod[retry%2]])
                                
                elif(num_of_mod == 2):
                    mod1 = current_mod[(retry%2)-1]
                    mod2 = 1 + current_mod[retry%2]%3
                    if(mod2 == mod1):
                        mod2 = 1 + mod2%3
                    current_mod[0] = mod1
                    current_mod[1] = mod2
                    if(verbose):
                        print("Use ",modulations[current_mod[0]],"and",modulations[current_mod[1]])

            
        trial  = random.random()
        if(verbose):
            print("Transmitting packet {} retry {} modulation {}".format(packet_counter, retry, modulations[current_mod[retry%2]]))
        retry_counter += 1
        tx_counter[current_mod[retry%2]] += 1
        pdr_phy = float(ent[current_mod[retry%2]+1])
        
        #packet delivered
        if(trial <= pdr_phy):
            if(verbose):
                print("Receiving packet {} retry {}".format(packet_counter, retry))
            if(packet_counter != prev_packet):
                rx_counter += 1
                
            prev_packet = packet_counter
            
            #sending ACK
            trial = random.random()
            if(trial <= pdr_phy):
                if(verbose):
                    print("Receiving ACK {} retry {}".format(packet_counter, retry))
                ack_counter[current_mod[retry%2]] += 1
                packet_counter += 1
                retry = 0
            else:
                if(verbose):
                    print("ACK not received {} retry {}".format(packet_counter, retry))   
                #transmit again?
                if(retry < number_of_retries):
                    retry += 1
                else:
                    packet_counter += 1
                    retry = 0

        #transmission failed
        else:
            #transmit again?
            if(retry < number_of_retries):
                retry += 1
            else:
                packet_counter += 1
                retry = 0
        
except EOFError as e:
    print("{},{}".format(rx_counter/packet_counter,retry_counter/packet_counter))
