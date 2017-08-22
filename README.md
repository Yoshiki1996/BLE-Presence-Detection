# BLE SCANNER AND DATA GENERATOR USING RASPBERRY PI3

Code is run on Python V2.x and Raspberry Pi3 Bluetoothctl environment

To run any of the code, type: "sudo python CODENAME.py" in terminal

1. BLE_SCANNER: Scans all available BLE devices within the proximity. Python fetches
                Raspberry Pi3 Bluetoothctl environment.
   
2. BLE_TABLE: Generates a table for each BLE device in MySQL. If you notice that the name of the device is a little changed,
              this was necessary in order to store make it sql-syntax friendly. However, not much is changed. 

3. BLE_DATA: Compiles all the BLE code above into one (calling this file will execute all functions above automatically).
   Stores the present date, time, mac address and presence (detected or non-detected) string upon scan real-time. 
   It dynamically retrieves the BLE device every call, hence detects whether a new BLE device is present, 
   or if a pre-existing device disappears.

Note: From experiment it seems the maximum presence detection is within 15-20 [meters]. Enough to detect
      any BLE device in a single room.
   
# Requirements
1. Raspberry Pi3
2. Python V2.x
3. pymysql python module
   
   
   
   
