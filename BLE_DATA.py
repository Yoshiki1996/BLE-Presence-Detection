'''Python API for using BLE_SCANNER and obtaining the
retrieved data from the scan: It will store into MySQL
the time and date it was retrieved from, mac and name of the
device

NOTE: This code includes table generator and thus, you do
not have to run BLE_TABLE.py seperately all the time.

This code should not be plagarized nor used for credential/academic purposes
unless stated otherwise by the owner. Modification and usage is accepted
upon approval.

For more details contact: yoshiki.shoji@mail.utoronto.ca
'''

import pymysql
from BLE_SCANNER import Bluetoothctl
from BLE_TABLE import MYSQL_TABLE

# Connect to database
connection = pymysql.connect(host = 'localhost',
                             user = 'root',
                             passwd = 'ditpwd',
                             db = 'DATA')

# Commit every data as by default it is False
connection.autocommit(True)

# Create Cursor Object
cursorObject = connection.cursor()

class DATA:

    def refresh(self):
        '''A function which removes all the devices from bluetoothctl
           Necessary protocol whenever we execute the code again'''
        
        print('Hold on please. Getting BLE SCAN ready...''')
        
        bl = Bluetoothctl()
        devices = bl.get_device_info_dict()
        bl.remove_devices_KV(devices)

        return 
        
    def newly_detected(self,devices_prior,devices_updated):
        '''Conditions must be made for checking whether device is
           available or not within its vicinity'''

        DETECTED = 'DETECTED'
        
        # First check if the device is new - detected new device
        # Devices still commonly shared - still detected no update needed in table
        available = list(set(devices_prior.keys()) & set(devices_updated.keys()))

        # Uncommon devices between the two dicts
        new_devices = list(set(devices_updated.keys()) ^ set(available))
        # print(new_devices)
        if new_devices == []:
            print('No new devices seen')
            
        else:
            print('new devices seen - go to table for more info')
            for new in new_devices:
                insertStatement = ("INSERT INTO "+new+"(DATE,TIME,MAC,AVAILABILITY)"
                                   "VALUES(CURDATE(),CURTIME()," +"'"+ devices_updated[new] +"'"+", '"+DETECTED+"')")
                cursorObject.execute(insertStatement)
        return

    def check_disappearance(self,devices_prior,devices_updated):
        '''To check disappearance, compare the prior and updated list lengths'''
        
        delta = len(devices_prior.keys()) - len(devices_updated.keys())
        NON_DETECTED = 'NON-DETECTED'

        # Whenever we lose a device, the new one has smaller dimension
        # Deal with other conditions
        if delta <= 0:
            return
        else:
            disp_dev = [dev for dev in devices_prior.keys() if dev not in devices_updated.keys()]
            #print('all devices in' disp_dev 'disappeared')

            for dev in disp_dev:
                insertStatement = ("INSERT INTO "+dev+"(DATE,TIME,MAC,AVAILABILITY)"
                                    "VALUES(CURDATE(),CURTIME()," +"'"+ devices_prior[dev] +"'"+", '"+NON_DETECTED+"')")
                cursorObject.execute(insertStatement)

        return
    
    def data_gen(self,blscan_time,totalscan_time1,totalscan_time2):
        
        try:
            
            # Reset all pre-existing devices in bluetoothctl devices folder
            self.refresh()
            
            # Instantiate the table generator variables
            # and initiate bluetoothctl
            table_gen = MYSQL_TABLE()
            
            while totalscan_time1 >= 0:
                # Outer loop is used whenever the break statement is executed in the inner loop.
                # Note the O(n^2) run time.
                
                init = True
                bl = Bluetoothctl()
                print('scanning again as no device was detected')
                      
                while totalscan_time2 >= 0:
                    # Base case - always executed once
                    if init == True:
                        print('init bluetooth...')
        
                        for i in range(0,2):
                            bl.start_scan(blscan_time)
                        
                        devices_dict = bl.get_device_info_dict()
                        if devices_dict == {}:
                            print('No devices seen. Scan again')
                            break
                        
                        tablenames = table_gen.table_generator(devices_dict)[0]
                        devices_mydict = table_gen.table_generator(devices_dict)[1]
                        print(devices_mydict)
                        
                        # Remove all devices from bluetoothctl - This is what will enable us to
                        # 'Dynamically' check the presence of the device
                        bl.remove_devices_VK(devices_mydict)

                        DETECTED = 'DETECTED'
                        # All the devices are available in the room (Insert Availability as DETECTED)                    
                        for table in tablenames:
                            insertStatement = ("INSERT INTO "+table+" (DATE,TIME,MAC,AVAILABILITY) "
                                               "VALUES(CURDATE(),CURTIME(),"+"'"+devices_mydict[table]+"'"+" ,'"+DETECTED+"')")
                            cursorObject.execute(insertStatement)
                            
                    # Build on from the base case - Check to see if devices_dict is changing
                    # Which consequently means tablenames is changing (ie. len difference)

                    else:
                        print('init bluetooth...')
            
                        bl = Bluetoothctl()
                        for i in range(0,2):
                            bl.start_scan(blscan_time)

                        devices_dict_updated = bl.get_device_info_dict()

                        if devices_dict_updated == {}:
                            print('No devices seen. Scan again')
                            break
                        
                        tablenames_updated = table_gen.table_generator(devices_dict_updated)[0]
                        devices_mydict_updated = table_gen.table_generator(devices_dict_updated)[1]
                        print(devices_mydict_updated)
                    
                        bl.remove_devices_VK(devices_mydict_updated)

                        # Store all 'newly' detected devices
                        self.newly_detected(devices_mydict,devices_mydict_updated)

                        # Check for disappeared devices: NON-DETECTED case
                        self.check_disappearance(devices_mydict,devices_mydict_updated)

                        # Update
                        devices_mydict = devices_mydict_updated

                    init = False
                    totalscan_time2 -= 1

                totalscan_time1 -= 1
            
        except (KeyboardInterrupt,SystemExit):
            print('Scanning Completed. Goodbye!')
            
        except Exception as e:
            '''Uncomment below to show what type of error was produced.'''
            print(type(e))
            print("Exeception occured:{}".format(e))
            pass 

        finally:
            connection.close()

if __name__ == '__main__':

    bldata = DATA()
    bldata.data_gen(blscan_time=5,totalscan_time1=30,totalscan_time2=30)
