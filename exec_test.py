#!/usr/bin/python3

from types_and_conversions.conversions.py_xml import *
from types_and_conversions.conversions.st_execute import *


diagram, fb_import_list = import_diagram("/home/admin/FBE2/types_and_conversions/diagrams/nameless.sys")

diagram.E_PERMIT.PERMIT.value = True
diagram.E_PERMIT_1.PERMIT.value = True
diagram.E_PERMIT_3.PERMIT.value = True
diagram.E_CTU.PV.value = 4
diagram.E_CTU.CV.value = 0
diagram.E_RESTART.WARM.active = True

#diagram.execute(1, diagram.E_RESTART)
