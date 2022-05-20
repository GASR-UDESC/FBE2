# Cyclical event releaser 

class E_CYCLE(Base_Function_Block):
    def __init__(self, DT=None, STOP=None, START=None, name='E_CYCLE', **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('START', Event(self, START, in_event=True))
        self.add_event('STOP', Event(self, STOP, in_event=True))
        self.add_event('EO', Event(self))
        self.add_variable('DT', Variable(self, DT, in_var=True, var_type="INT"))
        self.start_time = 0
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
