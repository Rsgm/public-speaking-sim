env = open('./.env', 'r')
env_sh = open('./.env.sh', 'w')

line = env.readline()
while not line == '':
    line = env.readline()

    if line.startswith('#') or len(line) == 1:
        continue

    env_sh.write('export %s\n' % line)

# probably not needed
env.close()
env_sh.close()
