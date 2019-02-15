
import subprocess
import inspect
import sys
import socket
#import all the necessary packages

import os
import time
#import all the necessary packages

from collections import defaultdict
#also import default dictionary

Host = (subprocess.check_output( "hostname", shell = True ) ).strip( '\n' )
print ("\nHost: " + Host)

clt_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
srv_addr = ( '', 5555 )
clt_socket.bind(srv_addr)
clt_socket.listen(10)
print ("\nServer starts on port " + str(srv_addr[1]) + " with address - " + Host)

path = os.path.dirname( os.path.abspath( inspect.getfile( inspect.currentframe() ) ) )
dist_vector = path + '/rtable_{}.csv'.format(Host)
print ("\ndistance-vector file is " + dist_vector)

present_time = time.time()
ip = {}
hosts = [ 'h1','r1','r2','r3','r4','h2' ]
ip[ '172.0.1.1' ] = 'h1'
ip[ '172.0.1.2' ] = 'r1'
ip[ '172.0.2.1' ] = 'r1'
ip[ '172.0.6.2' ] = 'r1'
ip[ '172.0.2.2' ] = 'r2'
ip[ '172.0.3.1' ] = 'r2'
ip[ '172.0.6.1' ] = 'r3'
ip[ '172.0.5.2' ] = 'r3'
ip[ '172.0.4.2' ] = 'r4'
ip[ '172.0.3.2' ] = 'r4'
ip[ '172.0.5.1' ] = 'r4'
ip[ '172.0.4.1' ] = 'h2'

def bellmanFord(Graph, edges, Host, previous_weight, address) :
    parent = defaultdict( lambda : None )
    Graph[Host] = 0
    
    for i in range( 6 ):
        
        for e in edges:
            v=e[1]
            u=e[0]
            
            if(e[2]!='max'):
                wt = float(e[2])
            else:
                wt = float('inf')
            
            if( Graph[u] + wt < Graph[v] and Graph[u] != float('inf') ) :
                parent[v] = u
                Graph[v] = Graph[u] + wt

    following_hops = defaultdict( lambda : '_' )
    flag = False
    
    print ("\n Graph : ",Graph)
    print ("\n\nPrevious Weight : ",previous_weight)
    
    for h in hosts:
        if Graph[h] == float('inf'):
            Graph[h] = 'max'
            if( previous_weight[h][1] == 'max' ) :
                following_hops[ h ] = '_'
            else:
                flag=True
                following_hops[ h ] = previous_weight[h][0]

        else:
            if( previous_weight[h][1] != 'max'):
                
                if( float( previous_weight[h][1] ) <= float( Graph[h] )):
                    following_hops[ h ] = previous_weight[h][0]
                else:
                    following_hops[ h ] = ip[address]
                    flag=True

                if( float( previous_weight[h][1] ) != float( Graph[h] ) ):
                    flag=True

            else:
                flag = True
                following_hops[h] = ip[address]

    if flag==True:
        
        print ("\n Updating the weights after changes.....\n")
        final_output = [ ]
        file = open( dist_vector, 'w+' )
        
        for h in hosts:
            l = []
            l.append( Host )
            line.append( h )
            line.append( following_hops[ h ] )
            
            if Graph[h] == float( 'inf' ):
                Graph[h] = 'max'
            
            l.append( str( Graph[h] ) + '\n' )
            l = ','.join(l)

            file.write(l)
            final_output.append(l)
    
        file.close()
        
        for l in final_output:
            print (l)

        print ("\nCompleted updating the weights.....\n")
        print ("\nCurrent time taken: ", time.time() - present_time)

    sys.stdout.flush()

while True:
    
    #print (" waiting for the connection....... ")
    client_sckt,address = clt_socket.accept()
    
    try:
        #print (" connection is established from - ", address)
        cumulative_data = [ ]
        data = client_sckt.recv( 4096 )
        
        while data:
            cumulative_data.append( data )
            data = client_sckt.recv( 4096 )
        
        #print (" cumulative data is received.......")
        
        cumulative_data = ''.join( cumulative_data )
        
        if cumulative_data == '':
            continue

        cumulative_data = cumulative_data.split(';')
        print (cumulative_data)
        Graph = defaultdict( lambda : float( 'inf' ) )
        edges = [ ]
        
        for l in cumulative_data:
            l = l.strip( '\n' ).split( ',' )
            edges.append( ( l[0], l[1], l[3] ) )
            print (l)

        previous_weight = { }
        file = open( dist_vector, 'r' )
        file_data = file.readlines()

        for l in file_data:
            l = l.strip( '\n' ).split( ',' )
            previous_weight[ l[ 1 ] ] = ( l[ 2 ], l[ 3 ] )
            edges.append( ( l[0], l[1], l[3] ) )

        bellmanFord(Graph, edges, Host, previous_weight, address[0])
        print ("---------------------------------------------")

    finally:
        client_sckt.close()




