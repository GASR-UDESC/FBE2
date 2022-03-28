#!/usr/bin/python

from function_block_edit import *

RESTART = E_RESTART(COLD=True)
PERM1 = PERMIT(EI=False, PERMIT=True)
PERM2 = PERMIT(EI=False, PERMIT=True)
PERM3 = PERMIT(EI=False, PERMIT=True)
PERM4 = PERMIT(EI=False, PERMIT=True)
PERM5 = PERMIT(EI=False, PERMIT=True)
DELAY_1S = E_DELAY(START = False, DT=1)


example = world()

example.add_function_block(PERM1)
example.add_function_block(PERM2)
example.add_function_block(PERM3)
example.add_function_block(PERM4)
example.add_function_block(PERM5)
example.add_function_block(RESTART)
example.add_function_block(DELAY_1S)

example.connect_events(PERM1.EI, RESTART.COLD)
example.connect_events(PERM2.EI,PERM1.EO)
example.connect_events(PERM3.EI,PERM1.EO)
example.connect_events(PERM4.EI,PERM2.EO)
example.connect_events(DELAY_1S.START,PERM4.EO)
example.connect_events(PERM5.EI, DELAY_1S.EO)



example.execute(i_fb=RESTART, frequency=1)












