#!/usr/bin/python3

import xml.etree.ElementTree as ET
from function_block_ecc import *



def convert_basic_fb_xml(fb):
	tree = ET.parse("types/Basic.fbt")
	root = tree.getroot()
	for read in root.iter("EventInputs"):
            for event in fb.events.items():
                if event[1].in_event:
                    ET.SubElement(read, "Event", {"Comment": "", "Name": event[0], "Type": "Event"})
	for read in root.iter("EventOutputs"):
            for event in fb.events.items():
                if event[1].in_event==0:
                    ET.SubElement(read, "Event", {"Comment": "", "Name": event[0], "Type": "Event"})
	for read in root.iter("InputVars"):
            for variable in fb.variables.items():
                if variable[1].in_var:
                    ET.SubElement(read, "VarDeclaration", {"Comment": "", "Name": variable[0], "Type": variable[1].type})
	for read in root.iter("OutputVars"):
            for variable in fb.variables.items():
                if variable[1].in_var==0:
                    ET.SubElement(read, "VarDeclaration", {"Comment": "", "Name": variable[0], "Type": variable[1].type})
	for read in root.iter("ECC"):
            for state in fb.ecc.states:
                ET.SubElement(read, "ECState", {"Comment":"", "Name": state.name})
                for read_2 in root.iter("ECState"):
                    print("yes")
                    print(state.ec_actions)
                    if state.ec_actions is not None and read_2.get("Name")==state.name:
                        for ec_action in state.ec_actions:
                            if ec_action[0] is not None:
                                ET.SubElement(read_2, "ECAction", {"Algorithm": ec_action[0], "Output": ec_action[2]})
                            else:
                                ET.SubElement(read_2, "ECAction", {"Output": ec_action[2]})
	for read in root.iter("BasicFB"):
            for state in fb.ecc.states:
                if state.ec_actions is not None:
                    for alg in state.ec_actions:
                        if alg[0] is not None:	
                            ET.SubElement(read, "Algorithm", {"Comment": "", "Name": alg[0]})
	
	tree.write(fb.name+".xml")
	
	
def convert_xml_basic_fb(xml):
	name_xml = None
	events = dict()
	tree = ET.parse(xml)
	root = tree.getroot()
	for read in root.iter("FBType"):
            name_xml = read.get("Name")
	fb = Base_Function_Block(name=name_xml)
	fb.type = "Basic"
	fb.ecc = ECC(fb)
	
	for read in root.iter("EventInputs"):
		for read_1 in read.iter("Event"):	
			event_name = read_1.get("Name")
			print(event_name)
			fb.add_event(event_name, Event(fb, None, in_event=True))
			# ~ print(getattr(fb, read_1.get("Name")).with_vars)
			# ~ print("hi")
			getattr(fb, event_name).with_vars = list()
			for read_2 in read_1.iter("With"):
				getattr(fb, read_1.get("Name")).with_vars.append(read_2.get("Var"))
				print(getattr(fb, read_1.get("Name")).with_vars)
				print(read_2.get("Var"))
				
	for read in root.iter("EventOutputs"):
		for read_1 in read.iter("Event"):	
			event_name = read_1.get("Name")
			print(event_name)
			fb.add_event(event_name, Event(fb, None, in_event=False))
			# ~ print(getattr(fb, read_1.get("Name")).with_vars)
			# ~ print("hi")
			getattr(fb, event_name).with_vars = list()
			for read_2 in read_1.iter("With"):
				getattr(fb, read_1.get("Name")).with_vars.append(read_2.get("Var"))
				print(getattr(fb, read_1.get("Name")).with_vars)
				print(read_2.get("Var"))
			
	for read in root.iter("InputVars"):
		for read in root.iter("VarDeclaration"):	
			fb.add_variable(read.get("Name"), Variable(fb, None, in_var=True))
	for read in root.iter("OutputVars"):
		for read in root.iter("VarDeclaration"):
			fb.add_variable(read.get("Name"), Variable(fb))
	for read in root.iter("ECState"):
		fb.ecc.add_state(read.get("Name"), State(read.get("Name")))
		getattr(fb.ecc, read.get("Name")).ec_actions = list()
		for read_2 in read.iter("ECAction"):
			getattr(fb.ecc, read.get("Name")).ec_actions.append((read_2.get("Algorithm"), None, read_2.get("Output")))
			
	transitions = list()
	for read in root.iter("ECTransition"):
		transition_list = list()
		transition = read.get("Condition")
		if transition[0] == "[":
			transition = transition.replace("[", "") 
			transition = transition.replace("]", "") 
			transition_list = transition.split()
			transition_list.insert(0, "1") # [1, var, cond_stmnt, cond]
			 
		elif transition[0] != "1":
			transition = transition.replace("[", " ")
			transition = transition.replace("]", " ")
			transition_list = transition.split()
		else:
			transition_list = ["1"]
						
		transition_list.append(read.get("Destination"))
		transition_list.append(read.get("Source"))
		transitions.append(transition_list)
		
	for transition in transitions:
		if transition[0] == "1" and len(transition)==3:
			getattr(fb.ecc, transition[2]).add_connection(getattr(fb.ecc, transition[1]), 1)
		elif transition[0] == "1" and len(transition)>3:
			getattr(fb.ecc, transition[5]).add_connection(getattr(fb.ecc, transition[4]), 1, getattr(fb, transition[1]), transition[2], transition[3])
		
		elif len(transition)>3:
			getattr(fb.ecc, transition[5]).add_connection(getattr(fb.ecc, transition[4]), getattr(fb.ecc, transition[0]), getattr(fb, transition[1]), transition[2], transition[3])
		else:
			getattr(fb.ecc, transition[2]).add_connection(getattr(fb.ecc, transition[1]), getattr(fb, transition[0]))
		
	algorithms = dict()
		
	for read in root.iter("Algorithm"):
		alg = read[0].get("Text")
		algorithms[read.get("Name")] = alg.split("\r\n") 
	new = dict()
	for element in algorithms.items():
		elmnt = list()
		for alg in element[1]:
			elmnt.append(alg.replace(";", ""))
		new[element[0]] = elmnt
	algorithms = new
	
		
	return fb, algorithms
	
	
		
# ~ PERM = PERMIT(EI=False, PERMIT=True)
# ~ COUNT = E_CTU()
# ~ convert_basic_fb_xml(COUNT)
rb = convert_xml_basic_fb("types/E_CTU.fbt")
print(getattr(rb[0].ecc, "CU").ec_actions)

