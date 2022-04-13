from function_block_edit import *
import math

def get_fb_measurements(fb):
        in_events = list()
        out_events = list()
        in_vars = list()
        out_vars = list()
        z = list()

        for event in fb.events.keys():
            if fb.events[event].in_event:
                in_events.append(event)
            else:
                out_events.append(event)

        for var in fb.variables.keys():
            if fb.variables[var].in_var:
                in_vars.append(var)
            else:
                out_vars.append(var)

        for i in range(len(in_events)):
            try:
                z.append(in_events[i]+out_events[i])
            except:
                try:
                    z.append(in_events[i])
                except:
                    z.append(out_events[i])

        for i in range(len(in_vars)):
            try:
                z.append(in_vars[i]+out_vars[i])
            except:
                try:
                    z.append(in_vars[i])
                except:
                    z.append(out_vars[i])
                    
        h_length = int(math.ceil(0.4*len(max(z, key=len))))+2
        t_vert_length = max(len(in_events), len(out_events))
        b_vert_length = max(len(in_vars), len(out_vars))			

        return h_length, t_vert_length, b_vert_length	
