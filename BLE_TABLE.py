'''
This Python Code will generate a table which are stored
into a MySQL database called, 'DATA'.
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

class MYSQL_TABLE:

    def table_generator(self,device_dict):
        '''
        function which creates a table called BLE_INFO
        stores: {DATE@SCAN,TIME@SCAN,MAC,NAME}
        '''

        try:
            # Commit every data as by default it is False
            connection.autocommit(True)
            
            # Create a cursor object
            cursorObject = connection.cursor()

            # Fetch all existing data and create a list of it called
            # tables
            cursorObject.execute('SHOW TABLES')
            tables_info = cursorObject.fetchall()
            tables = [table[0] for table in tables_info]
            
            # Get device names
            device_names = device_dict.values()
            ch_subset = [' ','(',')','\'']
            
            for device in device_names:
                for ch in [' ','\\','`','*','{','}','[',']','(',')','>','#','+','-','.','!','$','\'']:
                    if ch in device:
                        if ch in ch_subset:
                            device = device.replace(ch,'')
                        else:
                            device = device.replace(ch,'_')
                    else:
                        pass

                if device not in tables: 
                    # Table commands: Create a table for each device
                    # Get proper string name for use in MySQL 
                    sqlCreateTableCommand = ('CREATE TABLE ' + device + ' (DATA DATE,TIME TIME,MAC varchar(20), AVAILABILITY varchar(5))')
                    cursorObject.execute(sqlCreateTableCommand)
                else:
                    pass

        except (KeyboardInterrupt, SystemExit):
            print("Goodbye!")
            sys.exit(0)
            
        except Exception as e:
            '''Uncomment below to show what type of error was produced.'''
            print(type(e))
            print("Exeception occured:{}".format(e))
            pass 

        finally:
            connection.close()

if __name__ == '__main__':
    
    bl = Bluetoothctl()
    
    for i in range(0,2):
        if i == 1:
            print('init bluetooth...')
        bl.start_scan(scan_time = 5)
    
    devices = bl.get_device_info_dict()
    print(devices)
    # Run the function within the class
    table_gen = MYSQL_TABLE()
    table_gen.table_generator(device_dict = devices)
