# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import math
import pyinsim
import time
import socket
import select
import asyncore


import camera

class OutSimListener(asyncore.dispatcher):
    def __init__(self, port, packetCallback):
        asyncore.dispatcher.__init__(self);
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM);
        self.bind(("0.0.0.0", port));
        self.packetCallback = packetCallback;


    #def handle_connect(self):
       
    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(512)
        if(data == None):
            return;
        packet = pyinsim.OutSimPack();
        packet.unpack(data);
        if(self.packetCallback != None):
            self.packetCallback(packet);
        

    # Actually sends the message if there was something in the buffer.
    #def handle_write(self):

class OutsimInput:

    # Konstruktor
    #   app     : Objekt för vår huvudapplikation
    #   window  : Objekt för vårat fönster
    #   cameras : En lista med alla kameror i scenen
    def __init__(self, config, window, camera):
        self.config = config;
        self.window = window;
        self.camera = camera;

        if(config.has_option("input", "net_port")):
            self.outsimPort = config.getint("input", "net_port");
        else:
            self.outsimPort = 13336;

        self.velocity = ogre.Vector3(0, 0, 0);
        self.position = ogre.Vector3(0, 100, 0);
        self.offset = -ogre.Vector3(-19746, 0, -796);
        
    def __del__(self):
        self.shutdown();

    def init(self):
        self.server = OutSimListener(self.outsimPort, self.outsim_handler);
        self.position = ogre.Vector3(0,100,0);
        self.lastPacket = 0;

        rot = ogre.Quaternion(-math.pi, (0, 1, 0));
        self.camera.update(self.position, rot, ogre.Vector3(0,0,0),ogre.Vector3(0,0,0));


    #def shutdown(self):

    
    
    def outsim_handler(self, packet):
        delta = packet.Time - self.lastPacket; # Tid i millisekunder sedan senaste paketet
        self.lastPacket = packet.Time;
        scale = 0.001

        # Beräkna hastighet och acceleration över intervallet 1 sekund 
        #   eftersom datan i paketen är över intervallet beräknat för delta

        acceleration = ogre.Vector3(packet.Accel[0]*scale, 0, packet.Accel[1]*scale) * (1000.0 / float(delta));
        velocity = ogre.Vector3(packet.Vel[0]*scale,0,packet.Vel[1]*scale) * (1000.0 / float(delta));
        
        quatx = ogre.Quaternion(0, (1,0,0));
        quaty = ogre.Quaternion(packet.Heading, (0,1,0));
        quatz = ogre.Quaternion(0, (0,0,1));
        quat = quatx * quaty * quatz;
        
        self.position = self.offset + ogre.Vector3(packet.Pos[0]*scale, 60, -packet.Pos[1]*scale);
        
        self.camera.update(self.position, quaty, acceleration, velocity);

    # Denna anropas från vårat applikations-objekt en gång varje frame så att vi får
    # en chans att göra saker som att läsa indata eller flytta kameran
    #   evt     : FrameEvent, samma data som kommer i Ogre::FrameListener::frameStarted
    def frame(self, evt):
        asyncore.loop(count = 1);



    
