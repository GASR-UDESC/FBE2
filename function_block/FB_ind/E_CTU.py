# Event-driven Up Counter

class E_CTU(Base_Function_Block):
    def __init__(self, PV=None, CU=None, R=None, Q=None, CV=None, name="E_CTU", **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('CU', Event(self,CU, in_event=True))	
        self.add_event('R', Event(self, R, in_event=True))
        self.add_event('CUO', Event(self))
        self.add_event('RO', Event(self))
        self.add_variable('PV', Variable(self, PV, in_var=True, var_type="INT"))
        self.add_variable('Q', Variable(self, Q, in_var=True))
        self.add_variable('CV', Variable(self, CV, in_var=True, var_type="INT"))
        
        self.ecc = ECC()
        self.ecc.add_state('CUO', State('CUO'))
		self.ecc.START.add_connection(self.ecc.CUO, self.CU, self.CV, self.PV)
		self.ecc.add_state('RO', State('RO'))
		self.ecc.START.add_connection(self.ecc.EO, self.R)
		self.ecc.RO.add_connection(self.ecc.START, 1)
		self.ecc.CUO.add_connection(self.ecc.START, 1)
		
		
    def algorithm(self):
        if self.R.active:
            self.reset()
            RO = True
        else:
            self.RO.active = False
        if self.CU.active:
            self.counter()
        else:
            self.CUO.active = False	
        self.run()

    def reset(self):
        self.CV.value = 0
        self.Q.value = 0

    def counter(self):
        CUO = True
        self.CV.value += 1
        if CV >= PV:
            self.Q.value = 0
