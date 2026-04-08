from pox.core import core

import pox.openflow.libopenflow_01 as of



log = core.getLogger()



class DynamicBlocker(object):

    def __init__(self, connection):

        self.connection = connection

        connection.addListeners(self)

        self.packet_counts = {}

        # Threshold for suspicious activity

        self.BLOCK_THRESHOLD = 15 

        self.blocked_hosts = set()

        self.mac_to_port = {}



    def _handle_PacketIn(self, event):

        packet = event.parsed

        if not packet.parsed: return



        src_mac = packet.src

        dst_mac = packet.dst

        in_port = event.port



        # Ignore already blocked hosts

        if src_mac in self.blocked_hosts:

            return



        # 1. Detect Suspicious Activity (Count packets)

        self.packet_counts[src_mac] = self.packet_counts.get(src_mac, 0) + 1



        # 2. Check against Threshold

        if self.packet_counts[src_mac] > self.BLOCK_THRESHOLD:

            log.info(" SUSPICIOUS ACTIVITY! Host %s exceeded threshold.", src_mac)

            log.info(" Installing DROP rule for Host %s...", src_mac)

            

            # Create a drop rule (empty actions = DROP)

            msg = of.ofp_flow_mod()

            msg.match.dl_src = src_mac

            msg.priority = 100

            self.connection.send(msg)

            self.blocked_hosts.add(src_mac)

            return



        # Normal Learning Switch Logic

        self.mac_to_port[src_mac] = in_port



        if dst_mac in self.mac_to_port:

            out_port = self.mac_to_port[dst_mac]

            msg = of.ofp_packet_out()

            msg.actions.append(of.ofp_action_output(port=out_port))
            msg.data=event.ofp
            msg.in_port=in_port


            self.connection.send(msg)

        else:

            msg = of.ofp_packet_out()

            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))

            msg.data = event.ofp

            msg.in_port = in_port

            self.connection.send(msg)



def launch():

    def start_switch(event):

        DynamicBlocker(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
