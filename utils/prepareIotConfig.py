import json, sys, getopt

config_file_loc = ''
batch = False
container_name = ''
image_name = ''

try:
	opts, args = getopt.getopt(sys.argv[1:],"bc:n:i:")
except getopt.GetoptError:
	print 'error parsing options'
	sys.exit(2)

for opt, arg in opts:
	if opt == '-c':
		config_file_loc = arg
	elif opt == '-b':
		batch = True
	elif opt == '-n':
		container_name = arg
	elif opt == '-i':
		image_name = arg

with open(config_file_loc) as config_file:
	config = json.load(config_file)

commands = ''

if not batch:
	volumes = []
	if 'devices' in config:
		devices = config['devices']
		for device in devices:
			if 'type' in device and 'path' in device and 'name' in device:
				if device['type'] == 'gpio':
					volumes += [device['path'] + ':' + device['path']]
	commands += 'LAST_ID=$(sudo docker run --privileged ' + ' '.join(map(lambda x: '-v '+x, volumes)) + ' --name ' + container_name + ' -t -d ' + image_name + ')\n'
	
with open('RUN_SCRIPT.tmp', 'w') as command_file:
	command_file.write(commands)
