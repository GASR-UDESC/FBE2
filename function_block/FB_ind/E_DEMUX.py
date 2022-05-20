# Event-driven Demultiplexer

class E_DEMUX(Base_Function_Block):
    def __init__(self, EI=None, K=None, name='E_DEMUX', **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('EI', Event(self, EI, in_event=True))
        self.add_event('EO0', Event(self))				
        self.add_event('EO1', Event(self))
        self.add_event('EO2', Event(self))
        self.add_event('EO3', Event(self))
        self.add_variable('K', Variable(self, K, in_var=True, var_type="INT"))
		
		self.ecc = ECC()
		self.ecc.add_state('EO0', State('EI'))
		self.ecc.add_state('EO1', State('EI'))
		self.ecc.add_state('EO2', State('EI'))
		self.ecc.add_state('EO3', State('EI'))
		self.ecc.START.add_connection(self.ecc.EO0, self.EI, self.K, 0)
		self.ecc.START.add_connection(self.ecc.EO1, self.EI, self.K, 1)
		self.ecc.START.add_connection(self.ecc.EO2, self.EI, self.K, 2)
		self.ecc.START.add_connection(self.ecc.EO3, self.EI, self.K, 3)
		self.EO0.add_connection(self.ecc.START, 1)
		self.EO1.add_connection(self.ecc.START, 1)
		self.EO2.add_connection(self.ecc.START, 1)
		self.EO3.add_connection(self.ecc.START, 1)
		
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
