from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.ofproto import ofproto_v1_3
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
import numpy as np
import csv
import time
import os

class SimpleMonitor13(simple_switch_13.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)
        self.counter = 0

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                #self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                #self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(30)

    def _request_stats(self, datapath):
        #self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    
    @set_ev_cls(ofp_event.EventOFPPacketIn, 
                MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser

        # Determine the in_port based on the OpenFlow version
        if ev.msg.version == ofproto_v1_3.OFP_VERSION:
            in_port = ev.msg.match['in_port']
        else:
            in_port = ev.msg.in_port

        actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]

        data = None
        if msg.buffer_id == ofp.OFP_NO_BUFFER:
            data = msg.data

        out = ofp_parser.OFPPacketOut(
            datapath=dp, buffer_id=msg.buffer_id, in_port=in_port,
            actions=actions, data=data
        )

        dp.send_msg(out)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        matrix = np.zeros((10, 10))
        body = ev.msg.body

        self.logger.info('-------FLOW STATS------')
        self.logger.info('datapath         '
                        'in-port  eth-dst           '
                        'out-port packets  bytes     ')
        self.logger.info('---------------- '
                        '-------- ----------------- '
                        '-------- -------- --------')

        # MAC to index mapping
        mac_to_index = {}
        base_mac = '00:00:00:00:00'
        for i in range(10):
            mac_to_index[base_mac + f':{i+1:02}'] = i

        for stat in sorted([flow for flow in body if flow.priority == 1],
                        key=lambda flow: (flow.match['in_port'])):
          
            self.logger.info('%016x %8x %17s %8x %8d %8d',
                            ev.msg.datapath.id,
                            stat.match['in_port'], stat.match['eth_dst'],
                            stat.instructions[0].actions[0].port,
                            stat.packet_count, stat.byte_count)
            
            src = stat.match.get('eth_src')
            dst = stat.match.get('eth_dst')
            if src in mac_to_index and dst in mac_to_index:
                matrix[mac_to_index[src], mac_to_index[dst]] = stat.byte_count
     
        if self.counter < 100:
            # Save the matrix to a CSV file with a timestamp
            if np.any(matrix):
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"output/traffic_matrix_{timestamp}_{self.counter}.csv"

                # Check that the output directory exist
                if not os.path.exists('output'):
                    os.makedirs('output')
                    
                self._save_matrix_to_csv(matrix, filename)
                self.counter += 1
        else:
            pass

    def _save_matrix_to_csv(self, matrix, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in matrix:
                writer.writerow(row)