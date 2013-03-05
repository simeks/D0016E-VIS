# -*- coding: cp1252 -*-
import pyinsim
import socket
import time

addrs = [( "127.0.0.1", 13336 )]
outSocket = None

         
def pack_outsimpacket(packet):
    return packet.pack_s.pack(packet.Time, packet.AngVel[0], packet.AngVel[1], packet.AngVel[2],
                         packet.Heading, packet.Pitch, packet.Roll,
                         packet.Accel[0], packet.Accel[1], packet.Accel[2],
                         packet.Vel[0], packet.Vel[1], packet.Vel[2],
                         packet.Pos[0], packet.Pos[1], packet.Pos[2])


def outsim_handler(outsim, packet):
    if(outSocket != None):
        for a in addrs:
            outSocket.sendto(pack_outsimpacket(packet), (a[0], a[1]));



if __name__ == '__main__':
    outSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    pyinsim.outsim('127.0.0.1', 13338, outsim_handler, 30.0);
    while(True):
        pyinsim.run(False);
        # Insim fick timeout, vi väntar 10 sekunder och försöker igen
        print "Insim timeout, retrying in 10 seconds...";
        time.sleep(10);
    
