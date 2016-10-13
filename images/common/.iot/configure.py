import os
import json
import subprocess
import logging

logging.basicConfig(filename='virt_iot.log', level=logging.INFO, format='%(asctime)s %(message)s')
home_dir = os.getenv('HOME', '/')
config_file_loc = os.getenv('DEVICE_CONFIG_FILE', home_dir + '/.iot/default-config.json')
virt_dev_loc = os.getenv('VIRTUAL_SERIAL_RUNNER', home_dir + '/.iot/node/virt_dev.js')
virt_gpio_loc = os.getenv('VIRTUAL_GPIO_RUNNER', home_dir + '/.iot/node/virt_gpio.js')
pids_file_loc = os.getenv('VIRTUAL_DEVICES_PIDS_FILE', home_dir + '/.iot/DEV_PIDS')

with open(config_file_loc) as config_file:
	config = json.load(config_file)

if 'devices' in config:
	device_pids = []
	devices = config['devices']
	logging.info('Devices to start: ' + str(devices))
	for device in devices:
		if 'type' in device and 'path' in device and 'name' in device:
			if device['type'] == 'serial':
				logging.info('Starting device: ' + device['name'] + ':' + device['port'])
				buff_size = device['buffer_size'] if 'buffer_size' in device else '1'
				exec_cmd = "socat -d -d pty,raw,echo=0,link=\'%s\' EXEC:\'node %s %s %s %s %s\',pty,stderr,echo=0,fdin=3" % (device['path'], virt_dev_loc, device['name'], str(buff_size), device['port'], device['type'])
				pid = device_pids.append(str(os.system(exec_cmd + " & disown")))
			if device['type'] == 'GPIO':
				exec_cmd = "node %s %s %s %s %s" % (virt_gpio_loc, device['name'], device['path'], device['port'], device['type'])
				device_pids.append(str(os.system(exec_cmd + " &")))
				logging.info("start cmd: " + exec_cmd)
	with open(pids_file_loc, 'w+') as pids_file:
		logging.info('Devices PIDS:' + ','.join(device_pids))
		pids_file.write(','.join(device_pids))

