# Simple PID Function Block

class PID_SIMPLE(Base_Function_Block):
    def __init__(self, INIT=None, REQ=None, name="PID_SIMPLE", **kwargs):
        super().__init__(name, **kwargs)

        self.add_event('INIT', Event(self, INIT, in_event=True))		
        self.add_event('REQ', Event(self, REQ, in_event=True))
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
