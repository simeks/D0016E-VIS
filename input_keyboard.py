# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import math
import time

import camera


class KeyboardInput(OIS.KeyListener):

    velocity_forward = 0;
    turn_left = 0;
    
    # Konstruktor
    #   app     : Objekt f�r v�r huvudapplikation
    #   window  : Objekt f�r v�rat f�nster
    #   cameras : En lista med alla kameror i scenen
    def __init__(self, config, window, camera):
        OIS.KeyListener.__init__(self);
        self.config = config;
        self.window = window;
        self.camera = camera    
        
        
    def __del__(self):
        self.shutdown();

    def init(self):
        # Skapa och initialisera OIS, som �r v�rat bibliotek f�r indata fr�n
        #   saker som tagentbord och mus.
        hWnd = self.window.getCustomAttributeInt("WINDOW"); # Handle f�r v�rat f�nster
        self.inputSystem = OIS.createPythonInputSystem([("WINDOW",str(hWnd))]);
        # Skapa objekt f�r input fr�n tagentbord
        self.keyboard = self.inputSystem.createInputObjectKeyboard(OIS.OISKeyboard,True);
        # L�gg detta objekt f�r callbacks 
        self.keyboard.setEventCallback(self);

        rot = ogre.Quaternion(-math.pi, (0, 1, 0));
        self.camera.update(ogre.Vector3(0,100,0), rot, ogre.Vector3(0,0,0),ogre.Vector3(0,0,0));


    def shutdown(self):
        # St�da upp allt vi skapat med OIS
        if(self.keyboard):
            self.inputSystem.destroyInputObjectKeyboard(self.keyboard);
        OIS.InputManager.destroyInputSystem(self.inputSystem);
        self.inputSystem = 0;


    # Denna anropas fr�n v�rat applikations-objekt en g�ng varje frame s� att vi f�r
    # en chans att g�ra saker som att l�sa indata eller flytta kameran
    #   evt     : FrameEvent, samma data som kommer i Ogre::FrameListener::frameStarted
    def frame(self, evt):
        # L�s in input-data
        if(self.keyboard):
            self.keyboard.capture();

        pos = self.camera.getPosition();
        pos += (self.velocity_forward * evt.timeSinceLastFrame) * (self.camera.getOrientation() * ogre.Vector3(0,0,-1));
        orientation = self.camera.getOrientation();
        if(self.turn_left != 0):
            yaw = ogre.Quaternion(self.turn_left * evt.timeSinceLastFrame, (0, 1, 0));
            orientation = orientation * yaw;
        
        self.camera.update(pos, orientation, ogre.Vector3(0,0,0), ogre.Vector3(0,0,0));



        
    def keyPressed(self, evt):
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
        if(evt.key == OIS.KC_UP):
            self.velocity_forward = 0;
                
        if(evt.key == OIS.KC_DOWN):
            self.velocity_forward = 0;
                
        if(evt.key == OIS.KC_LEFT):
            self.turn_left = 0;
                
        if(evt.key == OIS.KC_RIGHT):
            self.turn_left = 0;
            
        return True
    
