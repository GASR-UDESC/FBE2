# Event delayer

class E_DELAY(Base_Function_Block):
    def __init__(self, START=False, STOP=False, DT=1, name='E_DELAY', **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('START', Event(self, START, in_event=True))
        self.add_event('STOP', Event(self, STOP, in_event=True))
        self.add_variable('DT', Variable(self, DT, in_var=True, var_type="INT"))
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
