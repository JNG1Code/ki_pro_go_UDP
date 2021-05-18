# About

This Python Code is an example code created to use the UDP broadcast method to trigger an application within LAN connectivity.

The address that the device is sending to can be found in the WriteInfo.txt file - in the example the address is IpAddress = 172.16.101.17
The IpAddress needs to match the address in the application you are sending the signal to. If your address is not the same as the one in the example you will need to update the address.

The startrecord section will trigger the AJA Ki Pro Go to start record.
The ipaddress in this section should match the address on the AJA Ki Pro Go - see https://www.aja.com/assets/support/files/8155/en/AJA_Ki_Pro_Go_Manual_v3.0r2.pdf

## Requirements

### Site Packages:
Time
Socket
Requests