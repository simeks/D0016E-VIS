# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import input
import scene
import camera
import gui

import math

import ConfigParser

class Application(ogre.FrameListener):
    # Konstruktor
    def __init__(self, config):
        self.config = config;
        
        # Ladda in inställningar från konfigurations-filen
        if(config.has_option("application", "multiple_cameras")):
            self.multipleCameras = config.getboolean("application", "multiple_cameras");
        else:
            self.multipleCameras = False;

        if(config.has_option("application", "multiple_windows")):
            self.multipleWindows = config.getboolean("application", "multiple_windows");
        else:
            self.multipleWindows = False;

        if(config.has_option("application", "camera_angle")):
            self.cameraAngle = config.getfloat("application", "camera_angle");
        else:
            self.cameraAngle = 58;

        ogre.FrameListener.__init__(self);
        # Håller koll på om applikationen håller på avslutas
        self.isStopping = False;

    # Får applikationen att avslutas vid nästa "frameStarted"-callback
    def stop(self):
        self.isStopping = True;
    
    def run(self):
        # Initialisera programmet
        self.init();
        # Börja rendera, det här anropet returnerar inte förens programmet avslutas
        self.root.startRendering();
        # Städa upp
        self.shutdown();

    # Laddar alla våra sökvägar för resurser från resources.cfg och lägger in dem i Ogre
    def setupResources(self):
        cfg = ogre.ConfigFile();
        cfg.load("resources.cfg");
        itr = cfg.getSectionIterator();
        while itr.hasMoreElements():
            secName = itr.peekNextKey();
            settings = itr.getNext();
            for item in settings:
                typeName = item.key;    # Typen av sökväg, filsystem, zip, etc
                archName = item.value;  # Själva sökvägen
                ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName);

    # Initialiserar applikationen
    # Params:
    #   multipleCamereas : Ifall true så renderar applikationen till flera kamerar för vänster, höger och mitten.
    def init(self):
        
        # Skapa root som är Ogres kärna
        self.root = ogre.Root();
        # Ladda in våra sökvägar
        self.setupResources();
        # Visa en dialog som låter användaren välja grafikinställnigar
        self.root.showConfigDialog();
        # Initialisera Ogre
        self.mainWindow = self.root.initialise(True, # Autoskapa ett fönster
                             "Titel"); # Titel på fönstret

        winWidth = self.mainWindow.getWidth();
        winHeight = self.mainWindow.getHeight();

        # Skapa 2 fönster för höger och vänster ifall vi använder flera kameror
        if self.multipleWindows:
            self.leftWindow = self.root.createRenderWindow("LeftWindow", winWidth, winHeight, False);
            self.rightWindow = self.root.createRenderWindow("RightWindow", winWidth, winHeight, False);
                        

        # Initialisera ogres resurshantering
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups();

        # Skapa vår scen
        self.scene = scene.Scene(self.config, self.root);
        self.scene.init();
        
        self.camera = camera.Camera(self, self.scene, self.multipleCameras, self.multipleWindows, self.cameraAngle);
        self.input = input.Input(self.config, self.mainWindow, self.camera);

        self.input.init();
        # Lägg till detta objekt som en framelistener så vi får callbacks varje frame
        self.root.addFrameListener(self);

        self.gui = gui.GUI();
        self.gui.addTextBox("position", "1,2,3", 5, 5, 400, 20);
        self.gui.addTextBox("velocity", "1,2,3", 5, 30, 400, 20);

    def shutdown(self):
        # Avsluta ogre
        self.root.shutdown();
        del self.root;

    def frameStarted(self, evt):
        #if(evt.timeSinceLastFrame != 0):
        #    fps = 1 / (evt.timeSinceLastFrame);
        #    print "fps:",fps;
        # Notifiera input-modulen
        self.input.frame(evt);
        
        self.scene.frame(evt);
        self.gui.setText("position", "Position: (X: %d, Y: %d, Z: %d)" %
                         (self.camera.getPosition().x, self.camera.getPosition().y, self.camera.getPosition().z));
        self.gui.setText("velocity", "Velocity: %d (km/h)" % (abs(self.camera.getVelocity().z*36.0))); # Hastigheten är i m/s ursprungligen
        
        # Kolla ifall vårat fönster har stängts, i så fall returnerar vi false,
        #   vilket resulterar i att ogre avslutar
        if(self.mainWindow.isClosed()):
            return False;

        if(self.multipleWindows):
            if(self.leftWindow.isClosed()):
                return False;
            if(self.rightWindow.isClosed()):
                return False;
        
        # Ser till att vi renderar till fönstret även fast det är inaktivt
        if(self.mainWindow.isActive() == False):
            self.mainWindow.update();

        if(self.multipleWindows):
            if(self.leftWindow.isActive() == False):
                self.leftWindow.update();
            if(self.rightWindow.isActive() == False):
                self.rightWindow.update();

        
        return (self.isStopping == False);
    
if __name__ == '__main__':
    config = ConfigParser.RawConfigParser();
    files = config.read("settings.ini");
    if(len(files) == 0):
        print "settings.ini not found";
    else:
        app = Application(config);
        app.run();

