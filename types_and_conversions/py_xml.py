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
		for read in root.iter("Event"):	
			fb.add_event(read.get("Name"), Event(fb, None, in_event=True))
	# With variable statement missing!!!
	for read in root.iter("EventOutputs"):
		for read in root.iter("Event"):
			fb.add_event(read.get("Name"), Event(fb))

	for read in root.iter("InputVars"):
		for read in root.iter("VarDeclaration"):	
			fb.add_variable(read.get("Name"), Variable(fb, None, in_var=True))
	for read in root.iter("OutputVars"):
		for read in root.iter("VarDeclaration"):
			fb.add_variable(read.get("Name"), Variable(fb))
	for read in root.iter("ECState"):
		fb.ecc.add_state(read.get("Name"), State(read.get("Name")))
		i = 0
		while i>=0:
			print(i)
			try:
				getattr(fb.ecc, read.get("Name")).ec_actions=((read[i].get("Algorithm"), None, read[i].get("Output")))
				i = i+1
# This does NOT handle cases where there are multiple ec_actions, I think... 				
			except:
				break
	transitions = list()
	for read in root.iter("ECTransition"):
		transition_list = list()
		transition = read.get("Condition")
		if transition[0] == "[":
			transition_list = transition.split()
			transition.remove("]") 
			transition.remove("[") 
		elif transition[0] != 1:
			transition.replace("[", " ")
			transition.replace("]", " ")
			transition_list = transition.split()
		else:
			transition_list = [1]
						
		transition_list.append(read.get("Destination"))
		transition_list.append(read.get("Source"))
		transitions.append(transition_list)
		
	for transition in transitions:
		getattr(fb.ecc, transition[2]).add_connection(transition[1], transitions[0], )
		
	return fb, transitions
	
	
		
PERM = PERMIT(EI=False, PERMIT=True)
COUNT = E_CTU()
# ~ convert_basic_fb_xml(COUNT)
# ~ convert_xml_basic_fb("types/E_DEMUX.fbt")
