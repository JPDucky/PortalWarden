# import ./InputCapture
# import ./ConnectionManagement
# import ./InputSending
# import ./InputAbstraction
# import ./InputSharing

import socket
####### this file currently contains the logical boilerplate for the program @@@@@@@@@@

#Class for managing information bewteen hosts
# could potentially need to use some sort of network discovery
class ConnectionManagement:
    def __init__(self):
        self.host_information = []
        self.connection_status = False

    def establish_connection(self, host, port):
    #specifics here will pertain to each platform, etc.
    #TODO add steps to establish Connection
        #- will need to use sockets to establish conn between hosts, need to include err handling in case conn cannot be established
        pass

    def maintain_connection(self):
    #code to keep connection alive
        # will likely need to add retries, exponential backoff, etc
        #   - keep-alive messages, handle reconnection scenarios 
        pass

    def terminate_connection(self):
    #code to safely terminate connection
        # - handle closure of conn safely, free up resources was using
        pass


#Class for capturing input from mouse and keyboard
class InputCapture:
    def __init__(self):
        self.key_input = None
        self.mouse_input = None

    def get_key_input(self):
    #code to capture keyboard input
        #use pynput to control and monitor input devices
        pass

    def get_mouse_input(self):
    # code to capture mouse input
        #use pynput to control and monitor input devices


#class for abstracting and un-abstracting InputSending
class InputAbstraction:
    def __init__(self, input_capture: InputCapture):
        self.abstracted_input = None
        self.input_capture = input_capture
        self.system_type_info = None #Get system type

    def abstract_input(self):
    #code to convert raw input into a shared format(abstract)
        # convert user input into a format that can be used across systems (maybe a matrix or array or smthn), (intermediate format)
        pass

    def de-abstract_input(self):
    #code to convert abstract input back into usable format
    # convert intermediate format back into input that end-host can use and process


#class for determining and sending inputs to other hosts
class InputSending:
    def __init__(self, input_abstraction: InputAbstraction):
        self.send_trigger = None
        self.threshold = None
        self.input_abstraction = input_abstraction

    def determine_input_send(self):
    #code to determine when to send inputs to other hosts
        # logic to decide when to send inputs
        # could be keybind or a window threshold
        pass

    def send_input(self):
    #code to send inputs to other hosts
    # will need to handle errors in case of disconnect, etc.


#class for arranging how inputs are shared between hosts
class InputSharing:
    def __init__(self):
        self.input_share_plan = None

    def arrange_input_share(self):
    #code to decide how inputs will be shared between hosts
        # this will arrange how hosts will be orientatated relative to each other
        #   somewhat analagous/dependent to/on determine_input_send()
        pass
