#!/usr/bin/python

from function_block import *

class ECC():
    def __init__(self, **kwargs):
        self.states = set()
        self.events = set() # list [event, BOOL(0 = not controllable, 1 = controllable)]
        self.connections = dict() # a single connection will be a tuple [state1, state2] == state1 -> state2
        self.initial_state = None

    def connect_states(self, state1, state2, event):
        self.connections[event] = (state1, state2)


def NZRO_create_ecc(xml):
    name = ECC()
    parse_lines = open(xml).readlines()
    read_mode = None

    for line in parse_lines:
        for word in line.split():
            if word == '<states>':
                read_mode = 'state'
            if word == '<events>':
                read_mode = 'event'
            if word == '<transitions>':
                read_mode = 'transition'
    # erro se name = '<events>', '<states>' ou 'transitions'
            if read_mode == 'state':
                if word[0:4] == "name":
                    state_iq = word[6:-1]
                    name.states.add(state_iq)	
                if word[0:13] == "initial_state":
                    name.initial_state = state_iq

            elif read_mode == 'event':
                if word[0:4] == 'name':
                    evt = list()
                    evt.append(word[6:-1])		
                if word[0:12] == 'controllable':
                    if	word[14:-1] == 'true':
                        evt.append(True)
                        name.events.add(tuple(evt))
                    elif word[14:-1] == 'false':
                        evt.append(False)
                        name.events.add(tuple(evt))

            elif read_mode == 'transition':
                if word[0:4] == 'from':
                    conn = list()
                    conn.append(word[6:-1])
                elif word[0:2] == 'to':
                    conn.append(word[4:-1])
                elif word[0:5] == 'event':
                    try:
                        name.connections[word[7:-1]].append(conn)
                    except KeyError:
                        name.connections[word[7:-1]] = list()
                        name.connections[word[7:-1]].append(conn)  

    return name

def generate_ECC_fb(ECC, INIT=False, REQ = False):
    fb = Base_Function_Block()

    setattr(fb, 'ECC', ECC)

    fb.add_event('INIT', Event(fb, INIT))
    fb.add_event('REQ', Event(fb, REQ))
    fb.add_event('INITO', Event(fb))
    fb.add_event('OUT', Event(fb))

    for event in ECC.events:
        fb.add_event(event[0], Event(fb)) # every event starts as False

    for state in ECC.states:
        fb.add_event(state, Event(fb)) # output event

    def algorithm(self):
        if self.INIT:
            self.INITO.active = True	
            if self.REQ:
                for event in ECC.connections.keys():
                    for states in ECC.connections[event]:
                        if state[0] == fb.ECC.initial_state and getattr(fb, event).active == True:
                            states[0].active = False
                            states[1].active = True
                            fb.ECC.initial_state = states[1]
        else:
            self.INITO.active = False

    setattr(fb, 'algorithm', algorithm)

    return fb

def automata_to_fb(automata):
    canvas = world()

    ECC_fb = generate_ECC_fb(NZRO_create_ecc(automata))
    canvas.add_function_block(ECC_fb)
    OR = E_MERGE(EI1=False, EI2=False)
    canvas.add_function_block(OR)

    for event in ECC_fb.ECC.events:

        setattr(canvas, "IN_" + event[0], IO_READER(INIT=False, REQ=False, QI=True, PARAMS=None, SD_1=None))
        reader = getattr(canvas, "IN_" + event[0])
        canvas.add_function_block(reader)
        reader.add_variable('IVAL', Variable(reader, False)) # creates IVAL variable in IO_READER fb, sets it to False
        print("reader created")
        setattr(canvas, "P_" + event[0], PERMIT(EI=False, PERMIT = False))
        permit = getattr(canvas, "P_" + event[0])
        canvas.add_function_block(permit)
        print("permit created")

        canvas.connect_events(reader.CNF, permit.EI)
        canvas.connect_variables(reader.RD_1, permit.PERMIT)

        canvas.connect_events(permit.EO, getattr(ECC_fb, event[0]))
        OR.add_event("REQ_" + event[0], Event(OR, False))
        canvas.connect_events(permit.EO, getattr(OR, 'REQ_' + event[0]))
        canvas.connect_events(OR.EO, ECC_fb.REQ)
		

	
    return canvas, ECC_fb









