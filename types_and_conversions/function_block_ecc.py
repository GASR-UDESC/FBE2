#!/usr/bin/python

import time
from st_execute import *

class ECC():
    def __init__(self, fb, *args, **kwargs):
        self.states = set()
        self.events = set()
        self.fb = fb
        self.current_state = None

    def add_state(self, name, state):
        setattr(self, name, state)
        self.states.add(state)

    def set_current_state(self, state):
        self.current_state = state

    def run_ecc(self, event):
        print("Ran ECC with " + self.fb.name)
        if 1 in self.current_state.connections.keys():
            self.current_state = self.current_state.connections[1][0][0] # this is the state it's going to

        elif event in self.current_state.connections.keys() and event.active:
            for con in self.current_state.connections[event]:    
                print(con)
                if con[1] == None:
                    print("1")
                    self.current_state = con[0]
                    for ec_action in self.current_state.ec_actions:
                        getattr(self.fb, ec_action[2]).active = True
                        if ec_action[0] is not None:
                            run_st(self.fb, ec_action[0])
                            # ~ print(ec_action[1])


                elif con[2] == "=":
                    print("2")
                    if con[1].value == float(con[3]):
                        self.current_state = con[0]
                        for ec_action in self.current_state.ec_actions:
                            if ec_action[0] is not None:
                                run_st(self.fb, ec_action[0])
                            getattr(self.fb, ec_action[2]).active = True
                            print("deu reação")
                    else:
                        for ec_action in con[0].ec_actions:
                            getattr(self.fb, ec_action[2]).active = False
                elif con[2] == "!=":
                    print("3")
                    if con[1].value != float(con[3]):
                        self.current_state = con[0]
                        for ec_action in self.current_state.ec_actions:
                            if ec_action[0] is not None:
                                run_st(self.fb, ec_action[0])
                            getattr(self.fb, ec_action[2]).active = True
                    else:
                        for ec_action in con[0].ec_actions:
                            getattr(self.fb, ec_action[2]).active = False
                elif con[2] == ">":
                    print("4")
                    if con[1].value > float(con[3]):
                        self.current_state = con[0]
                        for ec_action in self.current_state.ec_actions:
                            if ec_action[0] is not None:
                                run_st(self.fb, ec_action[0])
                            getattr(self.fb, ec_action[2]).active = True
                    else:
                        for ec_action in con[0].ec_actions:
                            getattr(self.fb, ec_action[2]).active = False
                elif con[2] == "<":
                    print("5")
                    if con[1].value < float(con[3]):
                        self.current_state = con[0]
                        for ec_action in self.current_state.ec_actions:
                            if ec_action[0] is not None:
                                run_st(self.fb, ec_action[0])
                            getattr(self.fb, ec_action[2]).active = True
                    else:
                        for ec_action in con[0].ec_actions:
                            getattr(self.fb, ec_action[2]).active = False
                elif con[2] == ">=":
                    print("6")
                    if con[1].value >= float(con[3]):
                        self.current_state = con[0]
                        for ec_action in self.current_state.ec_actions:
                            if ec_action[0] is not None:
                                run_st(self.fb, ec_action[0])
                            getattr(self.fb, ec_action[2]).active = True
                    else:
                        for ec_action in con[0].ec_actions:
                            getattr(self.fb, ec_action[2]).active = False
                elif con[2] == "<=":
                    print("7")
                    if con[1].value <= float(con[3]):
                        self.current_state = con[0]
                        for ec_action in self.current_state.ec_actions:
                            if ec_action[0] is not None:
                                run_st(self.fb, ec_action[0])
                            getattr(self.fb, ec_action[2]).active = True
                    else:
                        for ec_action in con[0].ec_actions:
                            getattr(self.fb, ec_action[2]).active = False
                else:
                    print("8")
                    if con[1].value:
                        self.current_state = con[0]
                        for ec_action in self.current_state.ec_actions:
                            if ec_action[0] is not None:
                                run_st(self.fb, ec_action[0])
                            getattr(self.fb, ec_action[2]).active = True
                    else:
                        for ec_action in con[0].ec_actions:
                            getattr(self.fb, ec_action[2]).active = False
                                            
						
        if hasattr(self.current_state, "is_initial") != True:
            print("Stopped at " + self.current_state.name)
            self.run_ecc(event)
        else:
            print("Stopped at " + self.current_state.name +" FB: "+ self.fb.name)

class State():
    def __init__(self, name, ec_actions=list(), *args, **kwargs): # ec_actions is a list, ec_action is (algorithm_name, algorithm, output)
        self.connections = dict() # connections are EVENT:(STATE, VARIABLE, CONDITION_STATEMENT, CONDITION) this is where "With" statement comes in  
        self.name = name
        self.ec_actions = ec_actions


    def add_connection(self, state, event, variable=None, condition_stmnt = None, condition=1): # condition_stmnt {"==": "eq", "!=": "ne", ">": "gt", "<": "lt", ">=": "ge", "<=": "le"}
        if event not in self.connections.keys():
            self.connections[event] = list()
        self.connections[event].append((state, variable, condition_stmnt, condition))	

    def set_initial_state(self):
        setattr(self, "is_initial", True)



class Base_Function_Block():
    def __init__(self, name="NEW_FB", **kwargs):
        self.events = dict()
        self.variables = dict() 
        self.algorithm = dict()
        self.name = name
        self.selected = False
        self.pos = [0,0]
        self.type = None

    def get_event_output(self, event):
        return self.event.active

    def get_variable_value(self, variable):
        return self.variable.value

    def add_event(self, name, event):
        self.events[name] = event
        setattr(self, name, event)
        # ~ print("Event Added")
		
    def add_variable(self, name, variable):
        self.variables[name] = variable
        setattr(self, name, variable)

    def remove_event(self, name):
        delattr(self, name)	

    def remove_variable(self, name):
        delattr(self, name)

    def get_event(self, name):
        return self.events[name]

    def get_variable(self, name):
        return self.variables[name]

    def change_pos(self, pos_x, pos_y):
        self.pos[0],self.pos[1] = pos_x, pos_y

    def run(self):
        for event in self.events.values():
            event.run()
        for var in self.variables.values():
            var.run()

class Service():
    def __init__(self, interfaces=(None, None), *args, **kwargs):
        self.interfaces = interfaces
        self.service_sequences = dict()

    def add_service_sequence(self, service_sequence):
        self.service_sequences[service_sequence[0]] = service_sequence[1]


class ServiceSequence():
    def __init__(self, *args, **kwargs):
        self.service_transactions = list()

    def add_service_transaction(self, *service_transactions):			
        for st in service_transactions:
            self.service_transactions.append(st)


class ServiceTransaction():
    def __init__(self, input_primitive=None, output_primitive=None, *args, **kwargs):
        self.input_primitive = input_primitive #(event, interface, parameters)
        self.output_primitive = output_primitive #(event, interface, parameters)



class Event(): 
    def __init__(self, block, active=False, in_event=False, with_vars = list()):
        self.block = block
        self.active = active
        self.connections = set()
        self.with_vars = with_vars
        self.in_event = in_event
        self.selected = False
        self.selected_cn = False
        self.pos = [0,0]
        self.exec_flag = False 

    def activate(self, active=False):
        self.active = active

    def run(self):
        for con in self.connections:
            con.activate(self.active)

    def add_connection(self, in_event):
        self.connections.add(in_event)



class Variable():
    def __init__(self, block, value=None, in_var=False, var_type = "BOOL"):
        self.value = value
        self.block = block
        self.connections = set()
        self.in_var = in_var
        self.selected = False
        self.selected_cn = False
        self.pos = [0,0]
        self.type = var_type

    def set_value(self, value=None):
        self.value = value

    def run(self):
        for con in self.connections:
            con.set_value(self.value)

    def add_connection(self, in_var):
        self.connections.add(in_var)


class world():
    def __init__(self):

        self.function_blocks = set()

    def add_function_block(self, function_block):
        self.function_blocks.add(function_block)

    def remove_function_block(self, function_block):
        for fb in self.function_blocks:
            for event in fb.events.values():
                for connection in event.connections.copy():
                    if connection in function_block.events.values():
                        event.connections.remove(connection)
            for var in fb.variables.values():
                for connection in var.connections.copy():
                    if connection in function_block.variables.values():
                        var.connections.remove(connection)
        self.function_blocks.discard(function_block)

    def read_through(self, block, path):
        empty_block_flag = True
        for event in block.events.values():
            for connection in event.connections:
                if connection != set():
                    empty_block_flag = False

        if empty_block_flag:
            self.paths.append(path)
            del path[-1]
        for event in block.events.values():
            for in_event in event.connections:
                path.append(in_event)
                self.read_through(in_event.block, path)

    def connect_events(self, in_event, out_event):
        if type(in_event) is not Event or type(out_event) is not Event:
            print("Not event type, dummy")
        else:
            if (in_event.in_event and out_event.in_event) or (in_event.in_event != True and out_event.in_event != True):
                print("in_event with in_event or out_event with out_event")
            else:
                if in_event.in_event:
                    _in_event = in_event
                    _out_event = out_event
                else:
                    _in_event = out_event
                    _out_event = in_event
                _out_event.add_connection(_in_event)

    def connect_variables(self, in_var, out_var):
        if type(in_var) is not Variable or type(out_var) is not Variable:
            print("Not variable type, dummy")
        else:
            if (in_var.in_var and out_var.in_var) or (in_var.in_var != True and out_var.in_var != True):
                print("in_var with in_var or out_var with out_var, dummy")
            else:		
                if in_var.in_var:
                    _in_var = in_var
                    _out_var = out_var
                else:
                    _in_var = out_var
                    _out_var = in_var
                _out_var.add_connection(_in_var)

    def function_block_states(self, cnt="_"):
        print("-_-_-_-_-"+str(cnt)+"-_-_-_-_-")
        for fb in self.function_blocks:
            print(fb.name)
            for event in fb.events.items():
                print(event[0], ':', event[1].active)
            for var in fb.variables.items():
                print(var[0], ':', var[1].value)

    def simple_run_through(self, i_fb):
        i_fb.run()
        for event in i_fb.events.items():
            if event[1].in_event:
                if hasattr(i_fb, 'ecc') and event[1].in_event:
                    if event[1].exec_flag != True:
                        event[1].run()
                        print(event[0])
                        event[1].exec_flag = True
                        i_fb.ecc.run_ecc(event[1])
                        #print(i_fb.name)
                    else:
                        event[1].exec_flag = False

            if event[1].in_event != True:
                event[1].run()
                for i_event in event[1].connections:
                    print(i_event.block.name + " SimpleRunThrough")
                    self.simple_run_through(i_event.block)

    def execute(self, frequency, i_fb, duration=0):
        timer = time.time()	
        cycler = time.time()
        i = 0
        while(1):
            if duration != 0:
                if time.time()-timer >= duration:
                    break		
            if time.time() - cycler >= 1/frequency:
                for fb in self.function_blocks:
                    for event in fb.events.values():
                        event.exec_flag = False
                self.simple_run_through(i_fb)
                i = i+1
                self.function_block_states(i)
                cycler = time.time()		







