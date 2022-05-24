from function_block_ecc import *

perm1 = PERMIT(PERMIT=True)
count = E_CTU(PV=4)
restart = E_RESTART(COLD=True)
count2 = E_CTU(P=4, name='count2')

diagram = world()

diagram.add_function_block(count)
diagram.add_function_block(perm1)
diagram.add_function_block(restart)
diagram.add_function_block(count2)
diagram.connect_events(restart.COLD, perm1.EI)
diagram.connect_events(perm1.EO, count.CU)
diagram.connect_events(count.CUO, count2.R)

diagram.execute(1,restart,100)






