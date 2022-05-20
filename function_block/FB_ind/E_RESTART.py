# 

class E_RESTART(Base_Function_Block):
    def __init__(self, COLD=False, WARM=False, STOP=False, name='E_RESTART', **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('COLD', Event(self, COLD))
        self.add_event('WARM', Event(self, WARM))		
        self.add_event('STOP', Event(self, STOP))

    def algorithm(self):
        self.run()
