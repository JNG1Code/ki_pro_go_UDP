from socket import *
import time
import requests

class UDPBroadcast( object ):

  
  def BroadcastStart(object ):
    """The BroadcastStart() function will send a UDP datagram from a single source to all connected applications within the LAN conectivity. 
    The address that the device is sending to can be found in the WriteInfo.txt file - in the example the address is IpAddress = 172.16.101.17
    The IpAddress needs to match the address in the application you are sending the signal to. If your address is not the same as the one in the example you will need to update the address.

    The startrecord section will trigger the AJA Ki Pro Go to start record.
    The ipaddress in this section should match the address on the AJA Ki Pro Go - see https://www.aja.com/assets/support/files/8155/en/AJA_Ki_Pro_Go_Manual_v3.0r2.pdf
    """
    cs = socket(AF_INET, SOCK_DGRAM)
    cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
  
    data = r'<?xml version="1.0" encoding="utf-8" standalone="no"?>'
    data += r'<CaptureStart>'
    data += ( r'<PacketID VALUE="{}"/>' ).format( int(UDPBroadcast.PacketID) )
    data += ( r'<Name VALUE="TestCapture{}"/>' ).format( int( UDPBroadcast.PacketID) )
    data += r'<Notes VALUE=""/>'
    data += r'<Description VALUE=""/>'
    data += ( r'<DatabasePath VALUE="{}"/>' ).format( UDPBroadcast.CapturePath )
    data += r'</CaptureStart>'
    newdata = data.encode()
    print (UDPBroadcast.CaptureName)
    cs.sendto(newdata, (UDPBroadcast.IpAddress, int(UDPBroadcast.Port)))

    # Start Record: record trigger being sent to the Ki Pro Go - ensure that the IP address matches the address on the devices
    startrecord = requests.get("http://192.168.0.2/config?action=set&paramid=eParamID_TransportCommand&value=3")

    
  def BroadcastStop(object ):
    """The BroadcastStop() function will send a stop UDP datagram from a single source to all connected applications within the LAN conectivity. 
    The address that the device is sending to can be found in the WriteInfo.txt file - in the example the address is IpAddress = 172.16.101.17
    The IpAddress needs to match the address in the application you are sending the signal to. If your address is not the same as the one in the example you will need to update the address.

    The stoprecord section will trigger the AJA Ki Pro Go to stop record.
    The ipaddress in this section should match the address on the AJA Ki Pro Go - see https://www.aja.com/assets/support/files/8155/en/AJA_Ki_Pro_Go_Manual_v3.0r2.pdf
    """

    cs = socket(AF_INET, SOCK_DGRAM)
    cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    
    data = r'<?xml version="1.0" encoding="utf-8" standalone="no"?>'
    data += r'<CaptureStop>'
    data += ( r'<PacketID VALUE="{}"/>' ).format( int(UDPBroadcast.PacketID)+1 )
    data += ( r'<Name VALUE="TestCapture{}"/>' ).format( int(UDPBroadcast.LastCapture) )
    data += ( r'<DatabasePath VALUE="{}"/>' ).format( UDPBroadcast.CapturePath )
    data += r'<TimeCode VALUE="10 25 26 5 0 0 0 2"/>'
    data += r'</CaptureStop>'
    newdata = data.encode()
    cs.sendto(newdata, (UDPBroadcast.IpAddress , int( UDPBroadcast.Port )))
    # Stop Record: trigger being sent to the Ki Pro Go
    stoprecord = requests.get("http://192.168.0.2/config?action=set&paramid=eParamID_TransportCommand&value=4")

    print ("Broadcast Stop")
    
  def CheckDataFile(a ):
    """The CheckDataFile() function reads all the information in the WriteInfo.txt file and use this information for the Broadcast commands."""
    try:
      f = open("WriteInfo.txt",'r')
      CaptureName = f.readline()
      CaptureName = CaptureName.split(" = ",1)[1]
      CaptureName =  CaptureName[:-1]
      UDPBroadcast.CaptureName  = CaptureName
      packetID = f.readline()
      packetID = packetID.split(" = ",1)[1]
      packetID = packetID[:-1] 
      UDPBroadcast.PacketID = packetID
      ipAdd = f.readline()
      ipAdd = ipAdd.split(" = ",1)[1]
      ipAdd = ipAdd[:-1]
      UDPBroadcast.IpAddress = ipAdd
      port = f.readline()
      port= port.split(" = ",1)[1]
      port = port[:-1]
      UDPBroadcast.Port = port
      lastCapture = f.readline()
      lastCapture = lastCapture.split(" = ",1)[1]
      lastCapture = lastCapture[:-1]
      UDPBroadcast.LastCapture = lastCapture
      capturePath = f.readline()
      capturePath = capturePath.split(" = ",1)[1]
      capturePath = capturePath[:-1]
      UDPBroadcast.CapturePath = capturePath
      captureTime = f.readline()
      captureTime = captureTime.split(" = ",1)[1]
      captureTime = captureTime[:-1]
      UDPBroadcast.CaptureTime = captureTime

      print ('Info found...')
    except:
      print ("WriteInfo file error, file missing or format error")
    finally:
      f.close()

  def UpdateDataFile(a ):
    """The UpdateDataFile() function updates the PacketId information in the WriteInfo.txt file and use this information for the next trigger in the Broadcast commands."""
    try:
      with open('WriteInfo.txt', 'r') as file:
        data = file.readlines() 
        packet = data[1]
        packet = packet.split(" = ",1)[1]
        packet = int(packet[:-1])
        data[1] = str("PacketID = ") + str(packet + 2) + "\n"

      with open('WriteInfo.txt', 'w') as file:
        file.writelines( data )
    except:
      print ("Unable to update packetID in writeInfo.txt")
      
if __name__=='__main__':
    
  a = UDPBroadcast()
  a.CheckDataFile() # Check the data file information
  time.sleep(1) # While checking the command the system waits for 1 second
  a.BroadcastStart() # Start record
  recordLength = float(a.CaptureTime) # Read the capture time length entered into the WriteInfo.txt file in seconds
  time.sleep(recordLength) # Command to wait for the duration of the recording before send the stop broadcast signal
  a.BroadcastStop() # Stop record
  print ("Data Captured for {} seconds" .format(recordLength))
  a.UpdateDataFile() # Update WriteInfo.txt for the next capture