#!/usr/bin/python3

from py_xml_testing import *
from function_block_ecc import *
from st_execute import *


diagram = import_diagram("nameless.sys")

diagram.E_PERMIT.PERMIT.value = True
diagram.E_PERMIT_1.PERMIT.value = True
diagram.E_PERMIT_2.PERMIT.value = True
diagram.E_RESTART.WARM.active = True

#diagram.execute(1, diagram.E_RESTART)
