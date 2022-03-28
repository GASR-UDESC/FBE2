#!/usr/bin/python

class ECC():
    def __init__(self, **kwargs):
        self.states = set()
        self.events = set() # list [event, BOOL(0 = not controllable, 1 = controllable)]
        self.connections = dict() # a single connection will be a tuple [state1, state2] == state1 -> state2

    def connect_states(self, state1, state2, event):
        self.connections[event] = (state1, state2)

    def run_ecc(self, initial_state):
        for event in self.connections.keys():
            if start in self.connections[event] and event == True:
                start = self.connections[event][1]
                self.run_ecc(start)


def NZRO_create_ecc(xml, name):
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
                    name.states.add(word[6:-1])	

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

def generate_ECC_fb(ECC):
	fb = Base_Function_Block()
	
	fb.add_event('INIT', Event(self, INIT))
	fb.add_event('INITO', Event(self))
	fb.add_event('OUT', Event(self))
	
	for event in ECC.events:
		fb.add_event(event[0], Event(self, event[0]))
	
	





