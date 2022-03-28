#!/usr/bin/python

import time

class Base_Function_Block():
	def __init__(self, **kwargs):
		self.events = dict()
		self.variables = dict() 
	
	def get_event_output(self, event):
		return self.event.active
	
	def get_variable_value(self, variable):
		return self.variable.value
	
	def add_event(self, name, event):
		self.events[name] = event
		setattr(self, name, event)
	
	def add_variable(self, name, variable):
		self.variables['name'] = variable
		setattr(self, name, variable)
		
	def remove_event(self, name):
		delattr(self, name)	
	
	def remove_variable(self, name):
		delattr(self, name)
	
	def get_event(self, name):
		return self.events[name]
	
	def get_variable(self, name):
		return self.variables[name]
				
	def run(self):
		for event in self.events.values():
			event.run()
		for var in self.variables.values():
			var.run()
	
	
class Event(): 
	def __init__(self, block, active=False):
		self.block = block
		self.active = active
		self.connections = set()
		
	def activate(self, active=False):
		self.active = active
	
	def run(self):
		for con in self.connections:
			con.activate(self.active)
			
	def add_connection(self, in_event):
		self.connections.add(in_event)


class Variable():
	def __init__(self, block, value=None):
		self.value = value
		self.block = block
		self.connections = set()
	
	def set_value(self, value=None):
		self.value = value
	
	def run(self):
		for con in self.connections:
			con.set_value(self.value)
	
	def add_connection(self, in_var):
		self.connections.add(in_var)

  
class PERMIT(Base_Function_Block):
	def __init__(self, EI, PERMIT, **kwargs):
		super().__init__(**kwargs)
		
		# ~ self.EI = Event(EI)
		self.add_event('EI', Event(self, EI))
		self.add_event('EO', Event(self))	
		
		self.PERMIT = Variable(self, value=PERMIT)
		
	def algorithm(self):
		if self.EI.active and self.PERMIT.value:
			self.EO.active = True 		
		else:
			self.EO.active = False
		self.run()
		
#Contador
class E_CTU(Base_Function_Block):
	def __init__(self, PV, CU, R, **kwargs):
		super().__init__(**kwargs)
		
		self.add_event('CU', Event(self,CU))	
		self.add_event('R', Event(self, R))
		self.add_event('CUO', Event(self))
		self.add_event('RO', Event(self))
		self.add_variable('PV', Variable(self, PV))
		self.add_variable('Q', Variable(self, value=0))
		self.add_variable('CV', Variable(self,self, value=0))
	
	def algorithm(self):
		if self.R.active:
			self.reset()
		else:
			self.RO.active = False
		if self.CU.active:
			self.counter()
		else:
			self.CUO.active = False	
		self.run()
			
	def reset(self):
		RO = True
		self.CV.value = 0
		self.Q.value = 0
	
	def counter(self):
		CUO = True
		self.CV.value += 1
		if CV >= PV:
			self.Q.value = 0
		
#Demultiplexação		
class E_DEMUX(Base_Function_Block):
	def __init__(self, EI, K, **kwargs):
		super().__init__(**kwargs)
		
		self.add_event('EI', Event(self, EI))
		self.add_event('EO0', Event(self))				
		self.add_event('EO1', Event(self))
		self.add_event('EO2', Event(self))
		self.add_event('EO3', Event(self))
		self.add_variable('K', Variable(self, K))
		
	def algorithm(self):
		if self.EI.active:
			k = self.K.value
			if k == 0:
				self.EO0.active = True
				self.EO1.active = False
				self.EO2.active = False
				self.EO3.active = False	
			elif k == 1:
				self.EO0.active = False
				self.EO1.active = True
				self.EO2.active = False
				self.EO3.active = False	
			elif k == 2:
				self.EO0.active = False
				self.EO1.active = False
				self.EO2.active = True
				self.EO3.active = False
			elif k == 3:
				self.EO0.active = False
				self.EO1.active = False
				self.EO2.active = False
				self.EO3.active = True
			self.run()


class E_DELAY(Base_Function_Block):
	def __init__(self, START=False, STOP=False, DT=1, **kwargs):
		super().__init__(**kwargs)
		
		self.add_event('START', Event(self, START))
		self.add_event('STOP', Event(self, STOP))
		self.add_variable('DT', Variable(self, DT))
		self.add_event('EO', Event(self))
		self.first_run = True
		self.start_time = None
		
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
	def __init__(self, COLD=False, WARM=False, STOP=False, **kwargs):
		super().__init__(**kwargs)
		
		self.add_event('COLD', Event(self, COLD))
		self.add_event('WARM', Event(self, WARM))		
		self.add_event('STOP', Event(self, STOP))
	
	def algorithm(self):
		self.run()

class E_CYCLE(Base_Function_Block):
	def __init__(self, DT, STOP, START, **kwargs):
		super().__init__(**kwargs)
		
		self.add_event('START', Event(self, START))
		self.add_event('STOP', Event(self, STOP))
		self.add_event('EO', Event(self))
		self.add_variable('DT', Variable(self, DT))
		self.start_time() = None
		self.running = False
		
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
	def __init__(self, INIT, REQ, QI, PARAMS, SD_1, SD_2, **kwargs):
		super().__init__(**kwargs)
		
		self.add_event('INIT', Event(self, INIT))
		self.add_event('REQ', Event(self, REQ))
		self.add_event('INITO', Event(self))
		self.add_event('CNF', Event(self))
		self.add_variable('QI', Variable(self, QI))
		self.add_variable('PARAMS', Variable(self, PARAMS))
		self.add_variable('SD_1', Variable(self, SD_1)) # output address
		self.add_variable('SD_2', Variable(self, SD_2)) # output value
		self.add_variable('QO', Variable(self))
		self.add_variable('STATUS', Variable(self))
		self.add_variable('RD_1', Variable(self))
		
	def algorithm(self):
		if self.INIT:
			if self.QI and self.REQ:
				write()
				self.CNF = True
			else:
				self.CNF = False # needs to be researched, because both CNF and INITO depend on the proper
								#functioning of the system. No parameters yet introduced can control this.
			INITO = True
		else:
			INITO = False
		self.run
		
	def write(self, SD_1 = self.SD_1, SD_2 = self.SD_2):
		self.SD_2 = self.RD_1
			
class IO_READER(Base_Function_Block):
	def __init__(self, INIT, REQ, QI, PARAMS, SD_1, **kwargs):
		super().__init__(**kwargs)
		
		self.add_event('INIT', Event(self, INIT))
		self.add_event('REQ', Event(self, REQ))
		self.add_event('INITO', Event(self))
		self.add_event('CNF', Event(self))
		self.add_variable('QI', Variable(self, QI))
		self.add_variable('PARAMS', Variable(self, PARAMS))
		self.add_variable('SD_1', Variable(self, SD_1)) # input address
		self.add_variable('QO', Variable(self))
		self.add_variable('STATUS', Variable(self))
		self.add_variable('RD_1', Variable(self))
		
	def algorithm(self):
		if self.INIT:
			if self.QI and self.REQ:
				read()
				self.CNF = True
			else:
				self.CNF = False # needs to be researched, because both CNF and INITO depend on the proper
								#functioning of the system. No parameters yet introduced can control this.
			INITO = True
		else:
			INITO = False
		self.run()
		
	def read(self, SD_1 = self.SD_1):
		pass
		

class PID_SIMPLE(Base_Function_Block):
	def __init__(self, INIT, REQ, **kwargs):
		super().__init__(**kwargs)
		
		self.add_event('INIT', Event(self, INIT))		
		self.add_event('REQ', Event(self, REQ))
		self.add_event('INITO', Event(self))		
		self.add_event('CNF', Event(self))	
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
			self.function_blocks = set()
			# ~ self.graph_1 = dict()
			self.graph = dict()
			# ~ self.path = list()
			self.paths = list()
			
		def add_function_block(self, function_block):
			self.function_blocks.add(function_block)
		
		def remove_function_block(self, function_block):
			self.function_blocks.discard(function_block)
							
		def create_graph(self):
			for block in self.function_blocks:
				for event in block.events.values():
					self.graph[event] = set() 	
					for in_event in event.connections:
						self.graph[event].add(in_event)
		
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
			out_event.add_connection(in_event)
				
		def connect_variables(self, in_var, out_var):
			out_var.add_connection(in_var)
			
		def function_block_states(self):
			for fb in self.function_blocks:
				for event in fb.events.items():
					print(event[0], ':', event[1].active)
		
		def simple_run_through(self, i_fb):
			i_fb.algorithm()
			for event in i_fb.events.values():
				for i_event in event.connections:
					self.simple_run_through(i_event.block)
		
		def execute(self, frequency, i_fb, duration=0):
			timer = time.time()	
			cycler = time.time()
			while(1):
				if duration != 0:
					if time.time()-timer >= duration:
						break		
				if time.time() - cycler >= 1/frequency:
					self.simple_run_through(i_fb)
					self.function_block_states()
					cycler = time.time()		
				
		
		
		
		
			
			