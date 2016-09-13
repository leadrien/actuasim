#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
from knxnet import *

__author__ = "Adrien Lescourt"
__copyright__ = "HES-SO 2015, Project EMG4B"
__credits__ = ["Adrien Lescourt"]
__version__ = "1.0.1"
__email__ = "adrien.lescourt@gmail.com"
__status__ = "Prototype"

###################################
# Set your KNXnet gateway address #
###################################
udp_ip = "127.0.0.1"
udp_port = 3671


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 3672))


def write_data_to_group_addr(dest_group_addr, data, data_size):
    data_endpoint = ('0.0.0.0', 0)  # for NAT
    control_enpoint = ('0.0.0.0', 0)

    # Connection request
    conn_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_REQUEST,
                                   control_enpoint,
                                   data_endpoint)
    print('==> Send connection request to {0}:{1}'.format(udp_ip, udp_port))
    print(repr(conn_req))
    print(conn_req)
    sock.sendto(conn_req.frame, (udp_ip, udp_port))

    # Connection response
    data_recv, addr = sock.recvfrom(1024)
    conn_resp = knxnet.decode_frame(data_recv)
    print('<== Received connection response:')
    print(repr(conn_resp))
    print(conn_resp)

    # Connection state request
    conn_state_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_STATE_REQUEST,
                                         conn_resp.channel_id,
                                         control_enpoint)
    print('==> Send connection state request to channel {0}'.format(conn_resp.channel_id))
    print(repr(conn_state_req))
    print(conn_state_req)
    sock.sendto(conn_state_req.frame, (udp_ip, udp_port))

    # Connection state response
    data_recv, addr = sock.recvfrom(1024)
    conn_state_resp = knxnet.decode_frame(data_recv)
    print('<== Received connection state response:')
    print(repr(conn_state_resp))
    print(conn_state_resp)

    # Tunnel request, apci to 0x2 = GroupValueWrite
    tunnel_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_REQUEST,
                                     dest_group_addr,
                                     conn_resp.channel_id,
                                     data,
                                     data_size,
                                     0x2)
    print('==> Send tunnelling request to {0}:{1}'.format(udp_ip, udp_port))
    print(repr(tunnel_req))
    print(tunnel_req)
    sock.sendto(tunnel_req.frame, (udp_ip, udp_port))

    # Tunnel ack
    data_recv, addr = sock.recvfrom(1024)
    ack = knxnet.decode_frame(data_recv)
    print('<== Received tunnelling ack:')
    print(repr(ack))
    print(ack)

    # Disconnect request
    disconnect_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.DISCONNECT_REQUEST,
                                         conn_resp.channel_id,
                                         control_enpoint)
    print('==> Send disconnect request to channel {0}'.format(conn_resp.channel_id))
    print(repr(disconnect_req))
    print(disconnect_req)
    sock.sendto(disconnect_req.frame, (udp_ip, udp_port))

    # Disconnect response
    data_recv, addr = sock.recvfrom(1024)
    disconnect_resp = knxnet.decode_frame(data_recv)
    print('<== Received connection state response:')
    print(repr(disconnect_resp))
    print(disconnect_resp)


def read_data_from_group_addr(dest_group_addr, data, data_size):
    data_endpoint = ('0.0.0.0', 0)  # for NAT
    control_enpoint = ('0.0.0.0', 0)

    # Connection request
    conn_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_REQUEST,
                                   control_enpoint,
                                   data_endpoint)
    print('==> Send connection request to {0}:{1}'.format(udp_ip, udp_port))
    print(repr(conn_req))
    print(conn_req)
    sock.sendto(conn_req.frame, (udp_ip, udp_port))

    # Connection response
    data_recv, addr = sock.recvfrom(1024)
    conn_resp = knxnet.decode_frame(data_recv)
    print('<== Received connection response:')
    print(repr(conn_resp))
    print(conn_resp)

    # Connection state request
    conn_state_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_STATE_REQUEST,
                                         conn_resp.channel_id,
                                         control_enpoint)
    print('==> Send connection state request to channel {0}'.format(conn_resp.channel_id))
    print(repr(conn_state_req))
    print(conn_state_req)
    sock.sendto(conn_state_req.frame, (udp_ip, udp_port))

    # Connection state response
    data_recv, addr = sock.recvfrom(1024)
    conn_state_resp = knxnet.decode_frame(data_recv)
    print('<== Received connection state response:')
    print(repr(conn_state_resp))
    print(conn_state_resp)

    # Tunnel request, apci to 0 = GroupValueRead
    tunnel_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_REQUEST,
                                     dest_group_addr,
                                     conn_resp.channel_id,
                                     data,
                                     data_size,
                                     0)
    print('==> Send tunnelling request to {0}:{1}'.format(udp_ip, udp_port))
    print(repr(tunnel_req))
    print(tunnel_req)
    sock.sendto(tunnel_req.frame, (udp_ip, udp_port))

    # receive tunnel ack
    data_recv, addr = sock.recvfrom(1024)
    ack = knxnet.decode_frame(data_recv)
    print('<== Received tunnelling ack:')
    print(repr(ack))
    print(ack)

    # Receive tunnelling request
    data_recv, addr = sock.recvfrom(1024)
    received_tunnelling_req = knxnet.decode_frame(data_recv)
    print('<== Received tunnelling req:')
    print(repr(received_tunnelling_req))
    print(received_tunnelling_req)
    print('===> DATA: ', received_tunnelling_req.data)

    # send disconnect request
    disconnect_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.DISCONNECT_REQUEST,
                                         conn_resp.channel_id,
                                         control_enpoint)
    print('==> Send disconnect request to channel {0}'.format(conn_resp.channel_id))
    print(repr(disconnect_req))
    print(disconnect_req)
    sock.sendto(disconnect_req.frame, (udp_ip, udp_port))

    # Disconnect response
    data_recv, addr = sock.recvfrom(1024)
    disconnect_resp = knxnet.decode_frame(data_recv)
    print('<== Received connection state response:')
    print(repr(disconnect_resp))
    print(disconnect_resp)


def print_usage():
    print('Usage: python3 test_client.py COMMAND [GROUP_ADDR] DATA')
    print('COMMAND LIST:')
    print('              -a GROUP_ADDR DATA    one blind/valve')
    print('              -b      no longer supported')
    print('              -v      no longer supported')
    print('DATA (INTEGER):')
    print('              0 for blind up')
    print('              1 for blind down')
    print('              [0-255] for blind position')
    print('              [0-255] for valve position')
    print('Main Group address: 0 = valve')
    print('                    1 = blind up down')
    print('                    3 = blind position')
    print('Example: python3 test_client.py -a 1/4/1 1')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)
    elif sys.argv[1] == '-a':
        if len(sys.argv) != 4:
            print_usage()
            sys.exit(0)
        dest = knxnet.GroupAddress.from_str(sys.argv[2])
        if dest.main_group == 0:
            write_data_to_group_addr(dest, int(sys.argv[3]), 2)
        elif dest.main_group == 1:
            write_data_to_group_addr(dest, int(sys.argv[3]), 1)
        elif dest.main_group == 3:
            write_data_to_group_addr(dest, int(sys.argv[3]), 2)
        elif dest.main_group == 4:
            read_data_from_group_addr(dest, int(sys.argv[3]), 2)
        else:
            print('Unsupported destination group address: main group has to be [0,1,3,4]')
    else:
        print_usage()
