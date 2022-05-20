# Permissive event propagation

class PERMIT(Base_Function_Block):
    def __init__(self, EI=None, PERMIT=None, name="PERMIT", **kwargs):
        super().__init__(name, **kwargs)

        # ~ self.EI = Event(EI)
        self.add_event('EI', Event(self, EI, in_event=True))
        self.add_event('EO', Event(self))	
		
        self.add_variable('PERMIT', Variable(self, PERMIT, in_var=True))
		
		self.ecc = ECC()
		self.ecc.add_state('EO', State('EO'))
		self.ecc.START.add_connection(self.ecc.EO, self.EI, self.PERMIT, 1)
		self.ecc.EO.add_connection(self.ecc.START, 1)

    def algorithm(self):
        if self.EI.active and self.PERMIT.value:
            self.EO.active = True 		
        else:
            self.EO.active = False
        self.run()
