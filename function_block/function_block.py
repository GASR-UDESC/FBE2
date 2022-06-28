#!/usr/bin/python

import time

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
        print("Ran ECC with" + self.fb.name)
        if 1 in self.current_state.connections.keys():
            self.current_state = self.current_state.connections[1][0][0] # this is the state it's going to

        elif event in self.current_state.connections.keys() and event.active:
            for con in self.current_state.connections[event]:    

                if con[1] == None:
                    self.current_state = con[0]
                    for ec_action in self.current_state.ec_actions:
                        getattr(self.fb, ec_action[2]).active = True
                        if ec_action[1] is not None:
                            ec_action[1]()
                            # ~ print(ec_action[1])


                elif con[2] == "=":
                    if con[1].value == con[3]:
                        self.current_state = con[0]
                        for ec_action in self.current_state.ec_actions:
                            if ec_action[1] is not None:
                                ec_action[1]()
                            getattr(self.fb, ec_action[2]).active = True
                    else:
                        for ec_action in con[0].ec_actions:
                            getattr(self.fb, ec_action[2]).active = False
                elif con[2] == "!=":
                    if con[1].value != con[3]:
                        self.current_state = con[0]
                        for ec_action in self.current_state.ec_actions:
                            if ec_action[1] is not None:
                                ec_action[1]()
                            getattr(self.fb, ec_action[2]).active = True
                    else:
                        for ec_action in con[0].ec_actions:
                            getattr(self.fb, ec_action[2]).active = False
                elif con[2] == ">":
                    if con[1].value > con[3]:
                        self.current_state = con[0]
                        for ec_action in self.current_state.ec_actions:
                            if ec_action[1] is not None:
                                ec_action[1]()
                            getattr(self.fb, ec_action[2]).active = True
                    else:
                        for ec_action in con[0].ec_actions:
                            getattr(self.fb, ec_action[2]).active = False
                elif con[2] == "<":
                    if con[1].value < con[3]:
                        self.current_state = con[0]
                        for ec_action in self.current_state.ec_actions:
                            if ec_action[1] is not None:
                                ec_action[1]()
                            getattr(self.fb, ec_action[2]).active = True
                    else:
                        for ec_action in con[0].ec_actions:
                            getattr(self.fb, ec_action[2]).active = False
                elif con[2] == ">=":
                    if con[1].value >= con[3]:
                        self.current_state = con[0]
                        for ec_action in self.current_state.ec_actions:
                            if ec_action[1] is not None:
                                ec_action[1]()
                            getattr(self.fb, ec_action[2]).active = True
                    else:
                        for ec_action in con[0].ec_actions:
                            getattr(self.fb, ec_action[2]).active = False
                elif con[2] == "<=":
                    if con[1].value <= con[3]:
                        self.current_state = con[0]
                        for ec_action in self.current_state.ec_actions:
                            if ec_action[1] is not None:
                                ec_action[1]()
                            getattr(self.fb, ec_action[2]).active = True
                    else:
                        for ec_action in con[0].ec_actions:
                            getattr(self.fb, ec_action[2]).active = False
        if hasattr(self.current_state, "is_initial") != True:
            print("Stopped at " + self.current_state.name)
            try:
                print(self.fb.RO.active)
            except:
                pass

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
        self.pos = [100,100]
        self.type = None

    def get_event_output(self, event):
        return self.event.active

    def get_variable_value(self, variable):
        return self.variable.value

    def add_event(self, name, event):
        self.events[name] = event
        setattr(self, name, event)
        print("Event Added")
		
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

    def add_service_sequence(self, *service_sequences):
        for ss in service_sequences:
            self.service_sequences[ss[0]] = ss[1]


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


class PERMIT(Base_Function_Block):
    def __init__(self, EI=False, PERMIT=False, name="PERMIT", **kwargs):
        super().__init__(name, **kwargs)

        # ~ self.EI = Event(EI)
        self.add_event('EI', Event(self, EI, in_event=True, with_vars=["PERMIT"]))
        self.add_event('EO', Event(self))	

        self.add_variable('PERMIT', Variable(self, PERMIT, in_var=True))

        self.type = "Basic"

        self.ecc = ECC(self)
        self.ecc.add_state("START", State("START"))
        self.ecc.add_state('EO', State('EO', ec_actions=[(None, None, "EO")]))
        self.ecc.START.add_connection(self.ecc.EO, self.EI, self.PERMIT, "=", 1)
        self.ecc.EO.add_connection(self.ecc.START, 1)
        self.ecc.set_current_state(self.ecc.START)
        self.ecc.START.set_initial_state()


#Contador
class E_CTU(Base_Function_Block):
    def __init__(self, PV=None, CU=False, R=False, CV=0, Q=False,  name="E_CTU", **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('CU', Event(self,CU, in_event=True, with_vars=["PV"]))	
        self.add_event('R', Event(self, R, in_event=True))
        self.add_event('CUO', Event(self, with_vars=["Q, CV"]))
        self.add_event('RO', Event(self, with_vars=["Q, CV"]))
        self.add_variable('PV', Variable(self, PV, in_var=True, var_type="INT"))
        self.add_variable('Q', Variable(self, Q, var_type="BOOL"))
        self.add_variable('CV', Variable(self, CV, var_type="INT"))
        self.type = "Basic"

        self.ecc = ECC(self)
        self.ecc.add_state("START", State("START"))
        self.ecc.add_state('CUO', State('CUO', ec_actions=[('Count', None, 'CUO')]))
        self.ecc.START.add_connection(self.ecc.CUO, self.CU, self.CV,"<",6499)
        self.ecc.add_state('RO', State('RO', ec_actions=[('Reset', None, 'RO')]))
        self.ecc.START.add_connection(self.ecc.RO, self.R)
        self.ecc.RO.add_connection(self.ecc.START, 1)
        self.ecc.CUO.add_connection(self.ecc.START, 1)
        self.ecc.set_current_state(self.ecc.START)
        self.ecc.START.set_initial_state()

        self.algorithm = {"R": "CV := 0;&#13;&#10;Q := FALSE;", "CU": "CV := CV + 1;&#13;&#10;Q  := (CV &gt;= PV);"}

class E_MERGE(Base_Function_Block):
    def __init__(self, name="E_MERGE", EI1=False, EI2=False, **kwargs):
        super().__init__(name, **kwargs)		

        self.add_event("EI1", Event(self, EI1, in_event=True))
        self.add_event("EI2", Event(self, EI2, in_event=True))
        self.add_event("EO", Event(self))
        self.type = "Basic"

        self.ecc = ECC(self)
        self.ecc.add_state("START", State("START"))
        self.ecc.add_state("EO", State("EO", ec_actions=[(None, None, 'EO')]))
        self.ecc.START.add_connection(self.ecc.EO, self.EI1)
        self.ecc.START.add_connection(self.ecc.EO, self.EI2)
        self.ecc.EO.add_connection(self.ecc.START, 1)
        self.ecc.set_current_state(self.ecc.START)
        self.ecc.START.set_initial_state()


#Demultiplexação		
class E_DEMUX(Base_Function_Block):
    def __init__(self, EI=False, K=None, name='E_DEMUX', **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('EI', Event(self, EI, in_event=True, with_vars=["K"]))
        self.add_event('EO0', Event(self))				
        self.add_event('EO1', Event(self))
        self.add_event('EO2', Event(self))
        self.add_event('EO3', Event(self))
        self.add_variable('K', Variable(self, K, in_var=True, var_type="INT"))
        self.type = "Basic"


        self.ecc = ECC(self)
        self.ecc.add_state("START", State("START"))
        self.ecc.add_state('EO0', State('EI', ec_actions=[(None, None, "EO0")]))
        self.ecc.add_state('EO1', State('EI', ec_actions=[(None, None, "EO1")]))
        self.ecc.add_state('EO2', State('EI', ec_actions=[(None, None, "EO2")]))
        self.ecc.add_state('EO3', State('EI', ec_actions=[(None, None, "EO3")]))
        self.ecc.add_state('State', State('State'))
        self.ecc.START.add_connection(self.ecc.state, self.EI)
        self.ecc.START.add_connection(self.ecc.state, self.EI)
        self.ecc.START.add_connection(self.ecc.state, self.EI)
        self.ecc.START.add_connection(self.ecc.state, self.EI)
        self.ecc.State.add_connection(self.ecc.EO0, 1, self.K, "=", 0)
        self.ecc.State.add_connection(self.ecc.EO1, 1, self.K, "=", 1)
        self.ecc.State.add_connection(self.ecc.EO2, 1, self.K, "=", 2)
        self.ecc.State.add_connection(self.ecc.EO3, 1, self.K, "=", 3)
        self.EO0.add_connection(self.ecc.START, 1)
        self.EO1.add_connection(self.ecc.START, 1)
        self.EO2.add_connection(self.ecc.START, 1)
        self.EO3.add_connection(self.ecc.START, 1)
        self.ecc.set_current_state(self.ecc.START)
        self.ecc.START.set_initial_state()


class E_DELAY(Base_Function_Block):
    def __init__(self, START=False, STOP=False, DT=1, name='E_DELAY', **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('START', Event(self, START, in_event=True))
        self.add_event('STOP', Event(self, STOP, in_event=True))
        self.add_variable('DT', Variable(self, DT, in_var=True, var_type="INT"))
        self.add_event('EO', Event(self))
        self.first_run = True
        self.start_time = None
        self.type = "Service Interface"

    def algorithm(self):
        if self.START.active and self.first_run:
            self.start_time = time.time()
            self.first_run = False
        if self.START.active:
            if time.time()-self.start_time >= self.DT.value:
                self.EO.active = True
                self.first_run = True
        if self.STOP.active:
            self.first_run = True
            self.EO.active = False
        else:
            self.EO.active = False
        self.run()

class E_RESTART(Base_Function_Block):
    def __init__(self, COLD=False, WARM=False, STOP=False, name='E_RESTART', **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('COLD', Event(self, COLD))
        self.add_event('WARM', Event(self, WARM))		
        self.add_event('STOP', Event(self, STOP))
        self.type = "Service Interface"

    def algorithm(self):
        self.run()

class E_CYCLE(Base_Function_Block):
    def __init__(self, DT=None, STOP=None, START=None, name='E_CYCLE', **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('START', Event(self, START, in_event=True))
        self.add_event('STOP', Event(self, STOP, in_event=True))
        self.add_event('EO', Event(self))
        self.add_variable('DT', Variable(self, DT, in_var=True, var_type="INT"))
        self.start_time = 0
        self.running = False
        self.type = "Service Interface"

    def algorithm(self):
        if self.START.active:
            self.running = True
        if self.STOP.active:
            self.running = False
        if self.running:
            if time.time() - self.start_time >= self.DT.value:
                self.EO.active = True
                self.start_time = time.time()
            else:
                self.EO.active = False	

        self.run()


class IO_WRITER(Base_Function_Block):
    def __init__(self, INIT=None, REQ=None, QI=None, PARAMS=None, SD_1=None, SD_2=None, name="IO_WRITER", **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('INIT', Event(self, INIT, in_event=True))
        self.add_event('REQ', Event(self, REQ, in_event=True))
        self.add_event('INITO', Event(self))
        self.add_event('CNF', Event(self))
        self.add_variable('QI', Variable(self, QI, in_var=True))
        self.add_variable('PARAMS', Variable(self, PARAMS, in_var=True))
        self.add_variable('SD_1', Variable(self, SD_1, in_var=True)) # output address
        self.add_variable('SD_2', Variable(self, SD_2, in_var=True)) # output value
        self.add_variable('QO', Variable(self))
        self.add_variable('STATUS', Variable(self))
        self.add_variable('RD_1', Variable(self))
        self.type = "Service Interface"

    def algorithm(self):
        if self.INIT.active:
            if self.QI and self.REQ:
                write()
                self.CNF.active = True
            else:
                self.CNF.active = False # needs to be researched, because both CNF and INITO depend on the proper
                                #functioning of the system. No parameters yet introduced can control this.
            self.INITO.active = True
        else:
            self.INITO.active = False
        self.run

    def write(self):
        pass

class IO_READER(Base_Function_Block):
    def __init__(self, INIT=None, REQ=None, QI=None, PARAMS=None, SD_1=None, name="IO_READER", **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('INIT', Event(self, INIT, in_event=True))
        self.add_event('REQ', Event(self, REQ, in_event=True))
        self.add_event('INITO', Event(self))
        self.add_event('CNF', Event(self))
        self.add_variable('QI', Variable(self, QI, in_var=True))
        self.add_variable('PARAMS', Variable(self, PARAMS, in_var=True))
        self.add_variable('SD_1', Variable(self, SD_1, in_var=True)) # input address
        self.add_variable('QO', Variable(self))
        self.add_variable('STATUS', Variable(self))
        self.add_variable('RD_1', Variable(self))
        self.type = "Service Interface"


    def algorithm(self):
        if self.INIT.active:
            if self.QI and self.REQ:
                read()
                self.CNF.active = True
            else:
                self.CNF.active = False # needs to be researched, because both CNF and INITO depend on the proper
                                #functioning of the system. No parameters yet introduced can control this.
            self.INITO.active = True
        else:
            self.INITO.active = False
        self.run()

    def read(self):
        try:
            self.RD_1.value = self.IVAL
        except:
            pass # in case we want to use IVAL for input value, instead of the address


class PID_SIMPLE(Base_Function_Block):
    def __init__(self, INIT=None, REQ=None, name="PID_SIMPLE", **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('INIT', Event(self, INIT, in_event=True))		
        self.add_event('REQ', Event(self, REQ, in_event=True))
        self.add_event('INITO', Event(self))		
        self.add_event('CNF', Event(self))
        self.type = "Service Interface"	

        # Variables go here

        def algorithm(self):
            if self.INIT.active:
                self.INITO.active = True
            else:
                self.INITO.active = False	
            if self.REQ.active:
                PID_Control()
                self.CNF.active = True


        def PID_Control(self):
            pass # control function

class world():
    def __init__(self):
        self.fb_instantiators = {
                "Base Function Block": Base_Function_Block, 
                "E_CTU": E_CTU,
                "PERMIT": PERMIT,
                "E_MERGE": E_MERGE,
                "E_DEMUX": E_DEMUX,
                "E_RESTART": E_RESTART,
                "E_CYCLE": E_CYCLE,
                "IO_WRITER": IO_WRITER,
                "IO_READER": IO_READER,
                "PID_SIMPLE": PID_SIMPLE,
                "E_DELAY": E_DELAY,
                }

        self.function_blocks = set()

    def add_function_block(self, function_block):
        self.function_blocks.add(function_block)

    def new_function_block(self, fb_id, fb_type):
        setattr(self, fb_id, self.fb_instantiators[fb_type]())
        print(self.fb_instantiators[fb_type]())
        self.add_function_block(getattr(self, fb_id))

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
        # ~ for fb in self.function_blocks:
            # ~ print(fb.name)
            # ~ for event in fb.events.items():
                # ~ print(event[0], ':', event[1].active)
            # ~ for var in fb.variables.items():
                # ~ print(var[0], ':', var[1].value)

    def simple_run_through(self, i_fb):
        i_fb.run()
        for event in i_fb.events.items():
            if event[1].in_event:
                if hasattr(i_fb, 'ecc') and event[1].in_event:
                    event[1].run()
                    print(event[0])
                    i_fb.ecc.run_ecc(event[1])
                    #print(i_fb.name)

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
                self.simple_run_through(i_fb)
                i = i+1
                self.function_block_states(i)
                cycler = time.time()		







