'''
This Python Code will generate a table which are stored
into a MySQL database called, 'DATA'.

This code should not be plagarized nor used for credential/academic purposes
unless stated otherwise by the owner. Modification and usage is accepted
upon approval.

For more details contact: yoshiki.shoji@mail.utoronto.ca
'''

# PYMYSQL MODULES
import pymysql
import pymysql.cursors

# BLE_SCANNER
from BLE_SCANNER import Bluetoothctl

# Connect to the database
connection = pymysql.connect(host="localhost",
                            user='root',
                            passwd='ditpwd',
                            db="DATA")

# Commit every data as by default it is False
connection.autocommit(True)

# Create a cursor object
cursorObject = connection.cursor()

class MYSQL_TABLE:

    def table_mysql(self,device_dict,mysql_tables):
        
        # Get device names
        device_names = device_dict.values()
        device_mac = device_dict.keys()
        
        device_tablename = []
        device_newdict = {}
        ch_subset = [' ','(',')','\'']

        # Getting a cleaner string for the names - Required for proper syntax use in MySQL
        for device in device_names:
            for ch in [' ','\\','`','*','{','}','[',']','(',')','>','#','+','-','.','!','$','\'']:
                if ch in device:
                    if ch in ch_subset:
                        device = device.replace(ch,'')
                    else:
                        device = device.replace(ch,'_')
                else:
                    pass

            device_tablename.append(device)    
            
            if device not in mysql_tables: 
                # Table commands: Create a table for each device
                # Get proper string name for use in MySQL 
                sqlCreateTableCommand = ('CREATE TABLE ' + device + ' (DATE DATE,TIME TIME,MAC varchar(20),AVAILABILITY varchar(20))')
                cursorObject.execute(sqlCreateTableCommand)
            else:
                pass

        for i in range(len(device_mac)):
            device_newdict[device_tablename[i]] = device_mac[i]

        return device_tablename,device_newdict

    def table_generator(self,device_dict):
        '''
        function which creates a table called BLE_INFO
        stores: {DATE@SCAN,TIME@SCAN,MAC,NAME}

        Returns a tuple: list of tablenames in MySQL,new dictionary {key:value} = {tablename:mac}

        Note: The new dictionary was required in order to make another python code easier to
        implement. 
        '''

        try:

            # Fetch all existing data and create a list of it called
            # tables
            cursorObject.execute('SHOW TABLES')
            tables_info = cursorObject.fetchall()
            tables = [table[0] for table in tables_info]
            
            tablenames,newdict = self.table_mysql(device_dict,tables)

        except (KeyboardInterrupt, SystemExit):
            print("Goodbye!")
            sys.exit(0)
            
        except Exception as e:
            '''Uncomment below to show what type of error was produced.'''
            print(type(e))
            print("Exeception occured:{}".format(e))
            pass

        return [tablenames,newdict]


if __name__ == '__main__':

    print('init bluetooth...')
    bl = Bluetoothctl()
    
    for i in range(0,2):
        bl.start_scan(scan_time = 5)
    
    devices = bl.get_device_info_dict()
    print(devices)
    # Run the function within the class
    table_gen = MYSQL_TABLE()
    a = table_gen.table_generator(devices)
    print(a)
