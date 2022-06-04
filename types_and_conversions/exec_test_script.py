from function_block_ecc import *

perm1 = PERMIT(PERMIT=True, name="PERMIT_1")
count = E_CTU(PV=4)
restart = E_RESTART(COLD=True)
count2 = E_CTU(P=4, name='count2')
perm2 = PERMIT(PERMIT=False, name="PERMIT_2")
perm3 = PERMIT(PERMIT=True, name="PERMIT_3")

diagram = world()

diagram.add_function_block(count)
diagram.add_function_block(perm1)
diagram.add_function_block(restart)
diagram.add_function_block(perm2)
diagram.add_function_block(perm3)
diagram.connect_events(restart.COLD, perm1.EI)
diagram.connect_events(perm1.EO, perm2.EI)
diagram.connect_events(perm1.EO, count.CU)
diagram.connect_variables(count.Q, perm2.PERMIT)
diagram.connect_events(count.R, perm2.EO)
diagram.connect_events(count.RO, perm3.EI)

diagram.execute(1,restart,100)






