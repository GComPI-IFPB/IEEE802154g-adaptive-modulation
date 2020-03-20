import random
import sys

number_of_retries = int(sys.argv[1])
    
modulations = {1:"FSK", 2:"OQPSK", 3:"OFDM"}

packet_counter = 0
retry = 0

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
                if(cont_window > 75):
                    continue
                pdr_fsk = float(ent[2])
                pdr_oqpsk = float(ent[3])
                pdr_ofdm = float(ent[4])
                if(verbose):
                    print("PDR FSK: ",pdr_fsk)
                    print("PDR OQPSK: ",pdr_oqpsk)
                    print("PDR OFDM",pdr_ofdm)
            cont_window -= 1
            
            
        retry_counter += 1
        
        rand_mod  = random.randint(0,2)
        
        if(verbose):
            print(rand_mod)
            
        trial  = random.random()
        if(verbose):
            print("Transmitting packet {} retry {} modulation {}".format(packet_counter, retry, rand_mod))
            
        pdr_phy = float(ent[rand_mod + 2])
        
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
