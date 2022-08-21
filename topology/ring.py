from webbrowser import Elinks
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class RingTopo(app_manager.RyuApp):
    avoid_dst =['ff:ff:ff:ff:ff:ff','33:33:ff:00:00:08', '33:33:00:00:00:02','33:33:00:00:00:16']
    save_dst =['00:00:00:00:00:01','00:00:00:00:00:02','00:00:00:00:00:03','00:00:00:00:00:04','00:00:00:00:00:05','00:00:00:00:00:06','00:00:00:00:00:07','00:00:00:00:00:08','00:00:00:00:00:09','00:00:00:00:00:10']
    cutted=[4,7]
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    old_dst =''

    def __init__(self, *args, **kwargs):
        super(RingTopo, self).__init__(*args, **kwargs)
        # initialize mac address table.
        self.mac_to_port = {
                1: {'00:00:00:00:00:01':1,
                    '00:00:00:00:00:00':2},
                2: {'00:00:00:00:00:01':1,
                    '00:00:00:00:00:00':4},
                3: {'00:00:00:00:00:01':1,
                    '00:00:00:00:00:00':2},
                5: {'00:00:00:00:00:04':1,
                    '00:00:00:00:00:05':2,
                    '00:00:00:00:00:00':5},
                6: {'00:00:00:00:00:06':1,
                    '00:00:00:00:00:07':2,
                    '00:00:00:00:00:00':3},
                8: {'00:00:00:00:00:08':1,
                    '00:00:00:00:00:00':4},
                9: {'00:00:00:00:00:09':1,
                    '00:00:00:00:00:00':2},
                10: {'00:00:00:00:00:10':1,
                    '00:00:00:00:00:00':3}
                }

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        global old_dst
        
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # SWITCH ID.
        switch_id = datapath.id


        # analyse the received packets using the packet library.
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        # get the received port number from packet_in message.
        #print(vars(msg))
        in_port = msg.match['in_port']

        for x in datapath.ports:
            conf=datapath.ports[x].config
            break

        destinazione = dst.split(':')[5][1]
        if(dst not in self.avoid_dst and switch_id not in self.cutted):
            if(self.old_dst != dst and self.old_dst != '' and dst not in self.avoid_dst):
                self.logger.info("ARRIVED AT H%s",self.old_dst.split(':')[5][1])
            self.logger.info("input port: P%s IN SWITCH S%s looking for %s",in_port,switch_id,dst)

        # if the destination mac address is already learned,
        # decide which port to output the packet, otherwise FLOOD.

    
        if(switch_id in self.cutted):
            return
        elif dst in self.mac_to_port[switch_id]:
            out_port = self.mac_to_port[switch_id][dst]
        else:
            out_port = self.mac_to_port[switch_id]["00:00:00:00:00:00"]
        
        # construct action list.
        actions = [parser.OFPActionOutput(out_port)]

        if(dst not in self.avoid_dst):
            self.old_dst = dst
        # install a flow to avoid packet_in next time.
        if out_port != ofproto.OFPP_FLOOD and dst in self.save_dst:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)
        # construct packet_out message and send it.
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port, actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)
