from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch, Controller, RemoteController

class RoutingTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)


        # Create template host, switch, and link
        host_config = dict(inNamespace=True)
        host_link_config = dict()

        # Create switch nodes
        for i in range(10):
            #sconfig = {"switch_id": "%016x" % (i + 1)}
            sconfig = {"switch_id": "00:00:00:00:00:"+str(i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig)

        # Create host 
        for i in range(10):
            host_config = {"switch_id": "00:00:00:00:00:0"+str(i+1)}
            self.addHost("h%d" % (1+i), **host_config)

        # Add host links
        self.addLink("h1", "s1", **host_link_config)
        self.addLink("h2", "s2", **host_link_config)
        self.addLink("h3", "s3", **host_link_config)
        self.addLink("h4", "s5", **host_link_config)
        self.addLink("h5", "s5", **host_link_config)
        self.addLink("h6", "s6", **host_link_config)
        self.addLink("h7", "s6", **host_link_config)
        self.addLink("h8", "s8", **host_link_config)
        self.addLink("h9", "s9", **host_link_config)
        self.addLink("h10", "s10", **host_link_config)
        

        # Add switch links        
        self.addLink("s1", "s2", **host_link_config)
        self.addLink("s1", "s3", **host_link_config)
        self.addLink("s1", "s4", **host_link_config)
        self.addLink("s2", "s4", **host_link_config)
        self.addLink("s2", "s5", **host_link_config)
        self.addLink("s3", "s4", **host_link_config)
        self.addLink("s3", "s6", **host_link_config)
        self.addLink("s4", "s5", **host_link_config)
        self.addLink("s4", "s6", **host_link_config)
        self.addLink("s4", "s7", **host_link_config)
        self.addLink("s5", "s8", **host_link_config)
        self.addLink("s6", "s9", **host_link_config)
        self.addLink("s7", "s8", **host_link_config)
        self.addLink("s7", "s9", **host_link_config)
        self.addLink("s8", "s10", **host_link_config)
        self.addLink("s9", "s10", **host_link_config)
        self.addLink("s7", "s10", **host_link_config)        


topos = {'RoutingTopo': (lambda: RoutingTopo() )}     
        
if __name__ == "__main__":
    topo = RoutingTopo()
    net = Mininet(topo=topo,switch=OVSKernelSwitch, controller=RemoteController, build=False,autoSetMacs=True)
    controller = RemoteController("c1", ip="127.0.0.1")
    net.start()

    CLI(net)
    net.stop()

