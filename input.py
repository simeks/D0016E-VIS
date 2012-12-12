# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

from openpyxl.reader.excel import load_workbook

class Input(OIS.KeyListener):

    num_timesteps = 1001;
    timestep = 0.01;
    positions = [];
    total_time = 0;

    # Kontruktor
    #   app     : Objekt f�r v�r huvudapplikation
    #   window  : Objekt f�r v�rat f�nster
    def __init__(self, app, window, camera):
        OIS.KeyListener.__init__(self);
        self.app = app;
        self.window = window;
        self.camera = camera;

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
        for row in ws.range('C3:D'+str(self.num_timesteps+2)):
            self.positions.append(ogre.Vector3(row[0].value, 150, row[1].value));

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
        # Ifall tiden har g�tt utanf�r v�ran data s� startar vi bara om fr�n t=0 igen
        if(self.total_time > ((self.num_timesteps-1) * self.timestep)):
            self.total_time = 0;

        index = int(round(self.total_time/self.timestep));

        pos = self.positions[index];
        self.camera.setPosition(pos);     
        # L�s in input-data
        if(self.keyboard):
            self.keyboard.capture();
        # Uppdatera kamerans position
        #pos = self.camera.getPosition();
        # Multiplicera med timeSinceLastFrame s� vi f�r en j�mn unit/s
        #pos += self.camera.getRight() * (self.velocity_x * evt.timeSinceLastFrame);
        #pos += self.camera.getDirection() * (self.velocity_z * evt.timeSinceLastFrame);
        #self.camera.setPosition(pos);
        # Uppdatera s� att kameran sen alltid kollar i mitten
        #self.camera.lookAt(0,0,0);
    
        
    def keyPressed(self, evt):
        # Avsluta ifall escape trycks ned
        if evt.key == OIS.KC_ESCAPE:
            self.app.stop();
        if evt.key == OIS.KC_W: # Framm�t
            self.velocity_z = 150; 
        if evt.key == OIS.KC_S: # Bak�t
            self.velocity_z = -150;
        if evt.key == OIS.KC_A: # V�nster
            self.velocity_x = -250;
        if evt.key == OIS.KC_D: # H�ger
            self.velocity_x = 250;
        
        return True
 
    def keyReleased(self, evt):
        if evt.key == OIS.KC_W: # Framm�t
            self.velocity_z = 0; 
        if evt.key == OIS.KC_S: # Bak�t
            self.velocity_z = 0;
        if evt.key == OIS.KC_A: # V�nster
            self.velocity_x = 0;
        if evt.key == OIS.KC_D: # H�ger
            self.velocity_x = 0;
        return True
    
