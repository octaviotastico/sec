import angr

proj = angr.Project('r1')
stat = proj.factory.entry_state()
simm = proj.factory.simgr(stat)
ress = simm.explore(find=0x08048570, avoid=0x0804852d)
flag = ress.found[0].posix.dumps(0)

print(f'Flag is: {flag}')
f = open('flag.in', 'wb')
f.write(flag)
f.close()
