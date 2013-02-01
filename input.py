# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import math

from openpyxl.reader.excel import load_workbook

class Input(OIS.KeyListener):

    num_timesteps = 1001;   # Antalet timesteps
    timestep = 0.01;        # Sekunder per timestep
    total_time = 0;         # Totala tiden i v�r animation, startar om n�r vi g�tt igenom all data

    positions = []; # Positioner, ett v�rde per timestep
    angles = [];    # Vinklar i radianer, ett v�rde per timestep
    velocityx = [];
    velocityz = [];    
    # Konstruktor
    #   app     : Objekt f�r v�r huvudapplikation
    #   window  : Objekt f�r v�rat f�nster
    #   cameras : En lista med alla kameror i scenen
    def __init__(self, app, window, mainCamera, leftCamera, rightCamera, cameraAngle):
        OIS.KeyListener.__init__(self);
        self.app = app;
        self.window = window;
        self.mainCamera = mainCamera;
        self.leftCamera = leftCamera;
        self.rightCamera = rightCamera;
        self.cameraAngle = cameraAngle;

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
        for row in ws.range('C3:H'+str(self.num_timesteps+2)):
            self.positions.append(ogre.Vector3(row[0].value, 150, row[1].value));
            self.angles.append(math.radians(row[3].value));
        for row in ws.range('R3:S'+str(self.num_timesteps+2)):
            self.velocityx.append(row[0].value);
            self.velocityz.append(row[1].value);


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

        self.total_time += evt.timeSinceLastFrame;
        # Ifall tiden har g�tt utanf�r v�ran data s� startar vi bara om fr�n t=0 igen
        if(self.total_time > ((self.num_timesteps-1) * self.timestep)):
            self.total_time = 0;

        # R�kna ut n�rmaste timestep
        index = int(round(self.total_time/self.timestep));

        # H�mta ut datan f�r just det timesteppet
        pos = self.positions[index];
        angle = self.angles[index];

        velocityx = ogre.Vector3(self.velocityx[index], 0, 0) * self.mainCamera.getDirection();
        velocityz = self.velocityz[index];

        # Ber�kna v�r rotation utifr�n vinklarna vi f�tt, just nu roterar kameran endast runt Y-axeln
        orientation = ogre.Quaternion(math.pi - angle, (0,1,0));
        orientationx = ogre.Quaternion((5.0*(velocityx.length()/400.0))*(math.pi/180.0), (1,0,0));
        orientationz = ogre.Quaternion((-5.0*(velocityz/1400.0))*(math.pi/180.0), (0,0,1));


        orientation = orientation * orientationx * orientationz;
        
        # Uppdatera kameran

        # Rakt fram
        self.mainCamera.setOrientation(orientation);
        self.mainCamera.setPosition(pos);

        # R�kna ut riktning till v�nster (Ifall vi har en kamera f�r v�nster)
        sqrPt5 = math.sqrt(0.5);
        
        if self.leftCamera != None:
            leftOrientation = orientation * ogre.Quaternion(self.cameraAngle * (math.pi/180.0), (0,1,0));
            self.leftCamera.setOrientation(leftOrientation);
            self.leftCamera.setPosition(pos);

        
        # R�kna ut riktning till h�ger (Ifall vi har en kamera f�r h�ger)
        if self.rightCamera != None:
            rightOrientation = orientation * ogre.Quaternion(-self.cameraAngle * (math.pi/180.0), (0,1,0));
            self.rightCamera.setOrientation(rightOrientation);
            self.rightCamera.setPosition(pos);
        
        
    def keyPressed(self, evt):
        return True
 
    def keyReleased(self, evt):
        return True
    
