#!/usr/bin/python3

import xml.etree.ElementTree as ET
from function_block_ecc import *

# ~ tree = ET.parse('Basic2.fbt')
# ~ root = tree.getroot()

# ~ for in_events in root.iter("EventInputs"):
	# ~ ET.SubElement(in_events, "Event",  {"Comment": "", "Name": "EI0", "Type": "Event"})
	# ~ ET.SubElement(in_events, "Event",  {"Comment": "", "Name": "EI1", "Type": "Event"})
	# ~ ET.SubElement(in_events, "Event",  {"Comment": "", "Name": "EI2", "Type": "Event"})
# ~ for in_events in root.iter("EventOutputs"):
	# ~ ET.SubElement(in_events, "Event",  {"Comment": "", "Name": "EO", "Type": "Event"})
# ~ for in_events in root.iter("InputVars"):
	# ~ ET.SubElement(in_events, "VarDeclaration",  {"Comment": "", "Name": "PERMIT", "Type": "BOOL"})


# ~ tree.write('output.xml')


def convert_basic_fb_xml(fb, name):
	tree = ET.parse("Basic.fbt")
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
	
	tree.write(name+".xml")
	
PERM = PERMIT(EI=False, PERMIT=True)
convert_basic_fb_xml(PERM, "Saved1")

