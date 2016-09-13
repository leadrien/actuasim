# -*- coding: utf-8 -*-

from knxnet import *

__author__ = "Adrien Lescourt"
__copyright__ = "HES-SO 2015, Project EMG4B"
__credits__ = ["Adrien Lescourt"]
__version__ = "1.0.1"
__email__ = "adrien.lescourt@gmail.com"
__status__ = "Prototype"


class CommandHandler:
    def __init__(self, actuasim):
        self.actuasim = actuasim
        self.command_functions = {
            0: self._valve_command,
            1: self._blind_command,
            # 2: self._ask_blind_bool,
            3: self._blind_command,
            4: self._ask_blind_short
        }

    def handle_tunnelling_request(self, tunnelling_request):
        return self.command_functions[tunnelling_request.dest_addr_group.main_group](tunnelling_request)

    def _valve_command(self, tunnelling_request):
        valve = self._get_valve_from_group_address(tunnelling_request.dest_addr_group)
        if valve is not None:
            valve.position = int(tunnelling_request.data / 0xFF * 100)
        else:
            self.actuasim.logger.error('Destination address group not found in the simulator: ' +
                                       str(tunnelling_request.dest_addr_group))

    def _blind_command(self, tunnelling_request):
        blind = self._get_blind_from_group_address(tunnelling_request.dest_addr_group)
        if blind is not None:
            if tunnelling_request.dest_addr_group.main_group == 3:
                value = tunnelling_request.data
                blind_value = int(value * (100 / 255))  # [0-255] to [0-100]
                blind.move_to(blind_value)
            elif tunnelling_request.data == 0:
                blind.move_up()
            elif tunnelling_request.data == 1:
                blind.move_down()
        else:
            self.actuasim.logger.error('Destination address group not found in the simulator: ' +
                                       str(tunnelling_request.dest_addr_group))

    def _ask_blind_short(self, tunnelling_request):
        blind = self._get_blind_from_group_address(tunnelling_request.dest_addr_group)
        if blind is not None:
            data, data_size, apci = blind.position, 2, 2
            tunnel_req_response = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_REQUEST,
                                                      tunnelling_request.dest_addr_group,
                                                      tunnelling_request.channel_id,
                                                      data,
                                                      data_size,
                                                      apci)
            return tunnel_req_response
        else:
            self.actuasim.logger.error('Destination address group not found in the simulator: ' +
                                       str(tunnelling_request.dest_addr_group))

    def _get_valve_from_group_address(self, group_address):
        for classroom in self.actuasim.classrooms:
            for valve in classroom.valve_list:
                if valve.group_address == group_address:
                    return valve

    def _get_blind_from_group_address(self, group_address):
        for classroom in self.actuasim.classrooms:
            for blind in classroom.blind_list:
                # we ignore the action. we do care only about the floor and the block.
                if blind.group_address.middle_group == group_address.middle_group \
                        and blind.group_address.sub_group == group_address.sub_group:
                    return blind
