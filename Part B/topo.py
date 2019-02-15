"""
Example topology of Quagga routers
"""

import inspect
import os
from mininext.topo import Topo
from mininext.services.quagga import QuaggaService

from collections import namedtuple

QuaggaHost = namedtuple("QuaggaHost", "name ip loIP")
net = None


class QuaggaTopo(Topo):

    "Creates a topology of Quagga routers"

    def __init__(self):
        """Initialize a Quagga topology with 5 routers, configure their IP
           addresses, loop back interfaces, and paths to their private
           configuration directories."""
        Topo.__init__(self)

        # Directory where this file / script is located"
        selfPath = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))  # script directory

        # Initialize a service helper for Quagga with default options
        quaggaSvc = QuaggaService(autoStop=False)

        # Path configurations for mounts
        quaggaBaseConfigPath = selfPath + '/configs/'

        # List of Quagga host configs
        quaggaHosts = []
        #quaggaHosts.append(QuaggaHost(name='a1', ip='172.0.1.1/16', loIP = None))
        #quaggaHosts.append(QuaggaHost(name='b1', ip='172.0.2.1/16', loIP = None))
        #quaggaHosts.append(QuaggaHost(name='c1', ip='172.0.3.2/16', loIP = None))
        #quaggaHosts.append(QuaggaHost(name='c2', ip='172.0.3.1/16', loIP = None))
        #quaggaHosts.append(QuaggaHost(name='d1', ip='172.0.4.1/16', loIP = None))
        quaggaHosts.append( QuaggaHost( name='h1', ip ='172.0.1.1/24', loIP = None ) )
        #quaggaHosts.append(QuaggaHost(name = 'R1', ip = '172.0.1.2/24', loIP=None ) )
        quaggaHosts.append( QuaggaHost( name='h2', ip ='172.0.4.1/24', loIP = None ) )
        #quaggaHosts.append(QuaggaHost(name = 'R1', ip = '172.0.1.2/24', loIP=None ) )
        quaggaHosts.append( QuaggaHost( name='r1', ip ='172.0.1.2/24', loIP = None ) )
        #quaggaHosts.append(QuaggaHost(name = 'R1', ip = '173.0.1.1/16', loIP = None ) )
        #quaggaHosts.append(QuaggaHost(name = 'R1', ip = '174.0.1.1/16', loIP = None ) )
        quaggaHosts.append( QuaggaHost( name='r2', ip ='172.0.2.2/24', loIP = None ) )
        #quaggaHosts.append(QuaggaHost(name = 'R2',ip = '175.0.1.2/16', loIP = None ) )
        quaggaHosts.append( QuaggaHost( name='r3', ip ='172.0.6.1/24', loIP = None ) )
        #quaggaHosts.append(QuaggaHost(name = 'R3', ip='176.0.1.1/16', loIP = None ) )
        quaggaHosts.append( QuaggaHost( name='r4', ip ='172.0.4.2/24', loIP = None ) )
        #quaggaHosts.append(QuaggaHost(name='R4', ip='176.0.1.2/16', loIP='10.0.1.2/24'))
        #quaggaHosts.append(QuaggaHost(name='R4', ip='177.0.1.1/16', loIP = None ) )        
        #quaggaHosts.append(QuaggaHost(name='H2', ip='172.0.4.1/24', loIP=None ) )

        # Add switch for IXP fabric
        #ixpfabric = self.addSwitch('fabric-sw1')

        # Setup each Quagga router, add a link between it and the IXP fabric
        quagga_hosts = []
        for host in quaggaHosts:

            # Create an instance of a host, called a quaggaContainer
            quagga_hosts.append(self.addHost(name=host.name,
                                           ip=host.ip,
                                           hostname=host.name,
                                           privateLogDir=True,
                                           privateRunDir=True,
                                           inMountNamespace=True,
                                           inPIDNamespace=True,
                                           inUTSNamespace=True))
            #qh.append(quaggaContainer)
            # Add a loopback interface with an IP in router's announced range
            self.addNodeLoopbackIntf(node=host.name, ip=host.loIP)
		
            # Configure and setup the Quagga service for this node
            quaggaSvcConfig = \
                {'quaggaConfigPath': quaggaBaseConfigPath + host.name}
            self.addNodeService(node=host.name, service=quaggaSvc,
                                nodeConfig=quaggaSvcConfig)

            # Attach the quaggaContainer to the IXP Fabric Switch
            #self.addLink(quaggaContainer, ixpfabric)
	

        self.addLink( quagga_hosts[0], quagga_hosts[2] )
        #self.addLink( quagga_hosts[1], quagga_hosts[2] )
        self.addLink( quagga_hosts[2], quagga_hosts[3] )
        #self.addLink( quagga_hosts[1], quagga_hosts[2] )
        self.addLink( quagga_hosts[2], quagga_hosts[4] )
        self.addLink( quagga_hosts[5], quagga_hosts[1] )
        #self.addLink( quagga_hosts[3], quagga_hosts[4] )
        self.addLink( quagga_hosts[3], quagga_hosts[5] )
        self.addLink( quagga_hosts[4], quagga_hosts[5] )
