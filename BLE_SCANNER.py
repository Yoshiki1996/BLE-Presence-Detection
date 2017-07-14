'''
Python API using raspbian bluetoothctl for fetching the BLE devices
available with its associated real-time capture
'''

# Operating systems (In my case):
# ('Linux', 'pi', '4.9.35-v7+','#1014 SMP Fri Jun 30 14:47:43 BST 2017', 'armv7l')

import subprocess as sub
import pexpect as exp
import time

class BluetoothctlError(Exception):
    pass

class Bluetoothctl:
    
    def __init__(self):
        self.child = exp.spawn('bluetoothctl',echo=False)
        
    def send_command(self,command,pause=0):
        self.child.send(command + '\n')
        time.sleep(pause)

        start_failed = self.child.expect(['bluetooth',exp.EOF])

        if start_failed:
            raise BluetoothctlError('Bluetoothctl Fail After Running:' + command)

        return self.child.before.split('\r\n')

    def start_scan(self,scan_time):
        """Instantiate to scan for devices. The
        first try statement will run the scan for
        scan_time [seconds]"""

        try:
            out = self.send_command('scan on')
            # Timer
            while scan_time >= 0:
                time.sleep(1)
                scan_time -= 1
                
        except BluetoothctlError, e:
            print(e)
            return None

    def get_device_info_list(self,command = 'devices'):
        
        """Parse a string corresponding to a device.
           and obtain the list containing and mac & name"""

        '''Example output (prior to parsing) using the devices command:
        [']\x1b[0m# Discovery started', '[\x1b[0;93mCHG\x1b[0m] Controller B8:27:EB:1E:B4:9C Discovering: yes',
        '[\x1b[0;93mCHG\x1b[0m] Device 00:13:EF:D5:FA:20 RSSI: -89', '[\x1b[0;93mCHG\x1b[0m] Device B8:8A:60:F3:38:AF RSSI: -96',
        '[\x1b[0;93mCHG\x1b[0m] Device B8:8A:60:F3:38:AF RSSI: -88', 'Device 00:13:EF:D5:FA:20 00-13-EF-D5-FA-20',
        'Device B8:8A:60:F3:38:AF KST-L-DBERRY', "Device 98:4F:EE:0D:16:6E Baptiste's BLE",
        'Device 48:DB:50:8A:AB:A1 Nexus 6P', '\x1b[0;94m[']'''

        output = self.send_command(command)[2:-1]

        #Obtain the Devices only
        output_temp = [devices for devices in output if devices.find('[\x1b[0;93mCHG\x1b[0m]') == -1]
        list_of_devices = [devices.replace('Device ','') for devices in output_temp]
        
        return list_of_devices

    def get_device_info_dict(self):
        '''obtain the dictionary instead of list.
           It is more useful as {key:value} = {mac:name}
        '''
        dict_devices = {}
        list_devices= self.get_device_info_list()

        for devices in list_devices:
            # Change to dict and update
            device = devices.split(' ',1)
            device = zip(*[iter(device)]*2)
            dict_device = dict(device)

            dict_devices.update(dict_device)
            
        return dict_devices

    def remove_devices(self,dict_devices):
        '''remove all the existing {key:value} pairs in the
            dictionary produced by get_device_info_dict
        '''
        empty_dict = dict_devices.clear()
        
        return empty_dict

if __name__ == '__main__':
    
    bl = Bluetoothctl()
    for i in range(0,2):
        if i == 1:
            print('init bluetooth...')
        bl.start_scan(scan_time = 5)  

    devices = bl.get_device_info_dict()
    print(devices)
    #print(bl.remove_devices(dict_devices=devices))
