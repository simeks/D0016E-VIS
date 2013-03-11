# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import math
import pyinsim
import time
import Queue
import threading
import socket
import select
import asyncore
from threading import Thread


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

class Input(OIS.KeyListener):

    num_timesteps = 75;   # Antalet timesteps
    timestep = 0.25;        # Sekunder per timestep
    total_time = 0;         # Totala tiden i vår animation, startar om när vi gått igenom all data

    velocity_forward = 0;
    turn_left = 0;
    
    # Konstruktor
    #   app     : Objekt för vår huvudapplikation
    #   window  : Objekt för vårat fönster
    #   cameras : En lista med alla kameror i scenen
    def __init__(self, app, window, camera):
        OIS.KeyListener.__init__(self);
        self.app = app;
        self.window = window;
        self.camera = camera
        self.realInput = True;
        self.velocity = ogre.Vector3(0, 0, 0);
        self.position = ogre.Vector3(0, 100, 0);
        self.offset = -ogre.Vector3(-19746, 0, -796);
        
    def __del__(self):
        self.shutdown();

    def init(self):
        # Skapa och initialisera OIS, som är vårat bibliotek för indata från
        #   saker som tagentbord och mus.
        hWnd = self.window.getCustomAttributeInt("WINDOW"); # Handle för vårat fönster
        self.inputSystem = OIS.createPythonInputSystem([("WINDOW",str(hWnd))]);
        # Skapa objekt för input från tagentbord
        self.keyboard = self.inputSystem.createInputObjectKeyboard(OIS.OISKeyboard,True);
        # Lägg detta objekt för callbacks 
        self.keyboard.setEventCallback(self);

        self.server = OutSimListener(13336, self.outsim_handler);
        #insim = pyinsim.insim_init('130.240.5.130', 13337, UDPPort=13338)
        #insim.bind_event(pyinsim.EVT_OUTSIM, self.outsim_handler);
        #pyinsim.outsim_init('127.0.0.1', 13338, self.outsim_handler, 30.0)
        #pyinsim.main_loop(True)
        self.position = ogre.Vector3(0,100,0);
        self.lastPacket = 0;

        rot = ogre.Quaternion(-math.pi, (0, 1, 0));
        self.camera.update(self.position, rot, ogre.Vector3(0,0,0),ogre.Vector3(0,0,0));


    def shutdown(self):
        # Städa upp allt vi skapat med OIS
        if(self.keyboard):
            self.inputSystem.destroyInputObjectKeyboard(self.keyboard);
        OIS.InputManager.destroyInputSystem(self.inputSystem);
        self.inputSystem = 0;

    
    
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
        self.total_time += evt.timeSinceLastFrame;
        # Läs in input-data
        if(self.keyboard):
            self.keyboard.capture();

        # Behandla all inkommande data
        asyncore.loop(count = 1);

        if(self.realInput):
            pos = self.camera.getPosition();
            pos += (self.velocity_forward * evt.timeSinceLastFrame) * (self.camera.getOrientation() * ogre.Vector3(0,0,-1));
            orientation = self.camera.getOrientation();
            if(self.turn_left != 0):
                yaw = ogre.Quaternion(self.turn_left * evt.timeSinceLastFrame, (0, 1, 0));
                orientation = orientation * yaw;
        
            self.camera.update(pos, orientation, ogre.Vector3(0,0,0), ogre.Vector3(0,0,0));



        
    def keyPressed(self, evt):
        if(self.realInput):
            if(evt.key == OIS.KC_UP):
                self.velocity_forward = 1000;
                
            if(evt.key == OIS.KC_DOWN):
                self.velocity_forward = -1000;
                
            if(evt.key == OIS.KC_LEFT):
                self.turn_left = 1.0;
                
            if(evt.key == OIS.KC_RIGHT):
                self.turn_left = -1.0;
        
        return True
 
    def keyReleased(self, evt):
        if(self.realInput):
            if(evt.key == OIS.KC_UP):
                self.velocity_forward = 0;
                
            if(evt.key == OIS.KC_DOWN):
                self.velocity_forward = 0;
                
            if(evt.key == OIS.KC_LEFT):
                self.turn_left = 0;
                
            if(evt.key == OIS.KC_RIGHT):
                self.turn_left = 0;
            
        return True
    
