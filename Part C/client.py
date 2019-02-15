import subprocess
import sys
import socket
#import all the necessary packages

import os
import inspect
import time
#import all the necessary packages

from collections import defaultdict
#also import default dictionary

Host = (subprocess.check_output( "hostname", shell = True ) ).strip( '\n' )
print ("\nHost: "+Host)

path = os.path.dirname( os.path.abspath( inspect.getfile( inspect.currentframe() ) ) )
dist_vector = path + '/rtable_{}.csv'.format(Host)

ip = {}
neigh = defaultdict( list )
hosts = [ 'h1','r1','r2','r3','r4','h2' ]

ip['h1'] = '172.0.1.1'
neigh['h1'] = ['r1']

ip['h2'] = '172.0.4.1'
neigh['h2'] = ['r4']

ip['r1'] = '172.0.1.2'
neigh['r1'] = ['r2','r3','h1']

ip['r2'] = '172.0.2.2'
neigh['r2'] = ['r4','r1']

ip['r3'] = '172.0.6.1'
neigh['r3'] = ['r1','r4']

ip['r4'] = '172.0.4.2'
neigh['r4'] = ['r3','r2','h2']

present_time = time.time()
print ("\n Neighbour of the host - " + Host + " are - ",neigh[Host])
cnt = 0
latests_weights = {}

for host in hosts:
    latests_weights[ host ] = 0

while True:
    present_weights = defaultdict( lambda : None )
    file = open( dist_vector, 'r' )
    f_data = file.readlines()
    file.close()
    for l in f_data:
        l = l.strip( '\n' ).split( ',' )
        present_weights[ l[ 1 ] ] = l[ 3 ]
    updated = False

    for h in hosts:
        if latests_weights[h] != present_weights[ h ]:
            latests_weights = present_weights
            updated = True
            break

if updated == True:
    finished = set( neigh[ str( Host ) ] )
    cnt += 1
    while len( finished ) > 0 :
        following_hop = finished.pop()
        srv_addr = ( ip[ following_hop ], 5555 )
        clt_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        print ("\n Trying to ping to the next hop which is "+following_hop)
        try:
            clt_socket.connect(srv_addr)
            file_data = f_data
            file_data = ';'.join(file_data)
            print (file_data)
            
            if data:
                print ("\n Transferring data to client ")
                clt_socket.sendall(data)
            else:
                print ("\n Finished Sending........ ")
            
            print (" ----------------------------------------- ")

        except Exception:
            finished.add(following_hop)
        
        finally:
            clt_socket.close()

    sys.stdout.flush()




