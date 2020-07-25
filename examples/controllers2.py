#!/usr/bin/python

"""
This example creates a multi-controller network from semi-scratch by
using the net.add*() API and manually starting the switches and controllers.

This is the "mid-level" API, which is an alternative to the "high-level"
Topo() API which supports parametrized topology classes.

Note that one could also create a custom switch class and pass it into
the Mininet() constructor.
"""


from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def multiControllerNet():
    "Create a network from semi-scratch with multiple controllers."

   net = Mininet( controller=RemoteController, switch=OVSSwitch)

    info( "*** Creating remote controllers\n" )
    c1 = net.addController( 'c1', ip='172.17.0.2', port=6633, protocols=["OpenFlow13"] )
   

    info( "*** Creating switches\n" )
    s1 = net.addSwitch( 's1',  protocols=["OpenFlow13"]  )
    s2 = net.addSwitch( 's2',  protocols=["OpenFlow13"]  )
    s3 = net.addSwitch( 's3',  protocols=["OpenFlow13"]  )
    

    info( "*** Creating hosts\n" )
    hostsSwitch1 = [ net.addHost( 'h%d' % n ) for n in [1, 2] ] #add hosts named h1,h2
    hostsSwitch2 = [ net.addHost( 'h%d' % n ) for n in [3, 4] ] #add hosts named h3,h4
    hostsSwitch3 = [ net.addHost( 'h%d' % n ) for n in [5, 6] ] #add hosts named h5,h6

    info( "*** Creating links\n" )
    for h in hostsSwitch1:
        net.addLink( s1, h )
    for h in hostsSwitch2:
        net.addLink( s2, h )
    for h in hostsSwitch3:
        net.addLink( s3, h )
    net.addLink( s1, s2 )
    net.addLink( s2, s3 )
    net.addLink( s3, s1 )

    info( "*** Starting network\n" ) #Connect switches to remote controller
    net.build()
    s1.start( [ c1 ] )
    s2.start( [ c1 ] )
    s3.start( [ c1 ] )

    info( "*** Testing network\n" )
    net.pingAll()

    info( "*** Running CLI\n" )
    CLI( net )

if __name__ == '__main__':
    setLogLevel( 'info' )  # for CLI output
    remoteControllerNet()
