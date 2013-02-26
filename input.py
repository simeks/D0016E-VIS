# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import math

import camera

from openpyxl.reader.excel import load_workbook

class Input(OIS.KeyListener):

    num_timesteps = 75;   # Antalet timesteps
    timestep = 0.25;        # Sekunder per timestep
    total_time = 0;         # Totala tiden i v�r animation, startar om n�r vi g�tt igenom all data

    accelerations = []
    positions = []; # Positioner, ett v�rde per timestep
    angles = [];    # Vinklar i radianer, ett v�rde per timestep
    velocityx = [];
    velocityz = [];

    velocity_forward = 0;
    turn_left = 0;
    
    # Konstruktor
    #   app     : Objekt f�r v�r huvudapplikation
    #   window  : Objekt f�r v�rat f�nster
    #   cameras : En lista med alla kameror i scenen
    def __init__(self, app, window, camera):
        OIS.KeyListener.__init__(self);
        self.app = app;
        self.window = window;
        self.camera = camera
        self.realInput = False;
        self.velocity = ogre.Vector3(0, 0, 0);
        self.position = ogre.Vector3(0, 200, 0);
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
        # Ladda in data fr�n v�rat excel-dokument
        self.wb = load_workbook(filename = r'assets/indata.xlsx');
        ws = self.wb.get_active_sheet();
        for row in ws.range('D3:F'+str(self.num_timesteps+2)):
            #self.positions.append(ogre.Vector3(row[0].value, 150, row[1].value));
            self.angles.append(ogre.Vector3(row[0].value, row[1].value, row[2].value));
        for row in ws.range('A3:C'+str(self.num_timesteps+2)):
            self.accelerations.append(0.01*ogre.Vector3(row[0].value, row[1].value, row[2].value));


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
        self.total_time += evt.timeSinceLastFrame;
        # L�s in input-data
        if(self.keyboard):
            self.keyboard.capture();

        if(self.realInput):
            pos = self.camera.getPosition();
            pos += (self.velocity_forward * evt.timeSinceLastFrame) * (self.camera.getOrientation() * ogre.Vector3(0,0,-1));
            orientation = self.camera.getOrientation();
            if(self.turn_left != 0):
                yaw = ogre.Quaternion(self.turn_left * evt.timeSinceLastFrame, (0, 1, 0));
                orientation = orientation * yaw;
            
            self.camera.update(pos, orientation, ogre.Vector3(0,0,0));

        else:
            # Ifall tiden har g�tt utanf�r v�ran data s� startar vi bara om fr�n t=0 igen
            if(self.total_time > ((self.num_timesteps-1) * self.timestep)):
                self.total_time = 0;

            # R�kna ut n�rmaste timestep
            index = int(round(self.total_time/self.timestep));

            self.velocity += self.accelerations[index] * self.timestep;
            self.position += self.velocity * self.timestep;
            
            # H�mta ut datan f�r just det timesteppet
            #pos = self.positions[index];
            angle = self.angles[index];
            orientationx = ogre.Quaternion(0, (1,0,0));
            orientationy = ogre.Quaternion((math.pi/2)+angle.z * (math.pi/180.0), (0,1,0));
            orientationz = ogre.Quaternion(0, (0,0,1));

            orientation = orientationx * orientationy * orientationz;
            #velocityx = self.velocityx[index];
            #velocityz = self.velocityz[index];

            self.camera.update(self.position, orientation, self.velocity);


        
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
    
