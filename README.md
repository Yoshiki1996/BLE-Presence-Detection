# BLE SCANNER AND DATA GENERATOR USING RASPBERRY PI

Code is run on Python V2.x and Raspberry Pi Bluetoothctl environment

1. BLE_SCANNER: Scans all available BLE devices within the proximity. Python fetches
   Raspberry Pi Bluetoothctl environment.
   
2. BLE_TABLE: Generates a table for each BLE device. 

3. BLE_DATA: Compiles all the BLE code above into one (calling this file will execute all functions above automatically).
   Stores the present date, time and mac and presence string upon scan. It dynamically retrieves the BLE device every call,
   hence detects whether a new BLE device is present, or if a pre-existing device disappears.
   
