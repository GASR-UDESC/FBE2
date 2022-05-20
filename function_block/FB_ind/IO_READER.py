# Input Reader

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

