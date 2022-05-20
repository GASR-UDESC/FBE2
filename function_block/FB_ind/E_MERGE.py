# Event Merger

class E_MERGE(Base_Function_Block):
    def __init__(self, name="E_MERGE", **kwargs):
        super().__init__(name, **kwargs)		

        self.add_event("EO", Event(self))

    def algorithm(self):
        for event in vars(self).values():
            if event.active == True:
                self.EO = True
            else:
                self.EO = False 
