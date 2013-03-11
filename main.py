# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import input
import scene
import camera
import gui

import math

from optparse import OptionParser;

class Application(ogre.FrameListener):
    # Konstruktor
    def __init__(self, multipleCameras, multipleWindows, cameraAngle):
        # Definerar ifall vi ska ha flera kameror eller inte
        self.multipleCameras = multipleCameras;
        self.multipleWindows = multipleWindows;
        self.cameraAngle = cameraAngle;
        
        ogre.FrameListener.__init__(self);
        # H�ller koll p� om applikationen h�ller p� avslutas
        self.isStopping = False;

    # F�r applikationen att avslutas vid n�sta "frameStarted"-callback
    def stop(self):
        self.isStopping = True;
    
    def run(self):
        # Initialisera programmet
        self.init();
        # B�rja rendera, det h�r anropet returnerar inte f�rens programmet avslutas
        self.root.startRendering();
        # St�da upp
        self.shutdown();

    # Laddar alla v�ra s�kv�gar f�r resurser fr�n resources.cfg och l�gger in dem i Ogre
    def setupResources(self):
        cfg = ogre.ConfigFile();
        cfg.load("resources.cfg");
        itr = cfg.getSectionIterator();
        while itr.hasMoreElements():
            secName = itr.peekNextKey();
            settings = itr.getNext();
            for item in settings:
                typeName = item.key;    # Typen av s�kv�g, filsystem, zip, etc
                archName = item.value;  # Sj�lva s�kv�gen
                ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName);

    # Initialiserar applikationen
    # Params:
    #   multipleCamereas : Ifall true s� renderar applikationen till flera kamerar f�r v�nster, h�ger och mitten.
    def init(self):
        
        # Skapa root som �r Ogres k�rna
        self.root = ogre.Root();
        # Ladda in v�ra s�kv�gar
        self.setupResources();
        # Visa en dialog som l�ter anv�ndaren v�lja grafikinst�llnigar
        self.root.showConfigDialog();
        # Initialisera Ogre
        self.mainWindow = self.root.initialise(True, # Autoskapa ett f�nster
                             "Titel"); # Titel p� f�nstret

        winWidth = self.mainWindow.getWidth();
        winHeight = self.mainWindow.getHeight();

        # Skapa 2 f�nster f�r h�ger och v�nster ifall vi anv�nder flera kameror
        if self.multipleWindows:
            self.leftWindow = self.root.createRenderWindow("LeftWindow", winWidth, winHeight, False);
            self.rightWindow = self.root.createRenderWindow("RightWindow", winWidth, winHeight, False);
                        

        # Initialisera ogres resurshantering
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups();

        # Skapa v�r scen
        self.scene = scene.Scene(self.root);
        self.scene.init();
        
        self.camera = camera.Camera(self, self.scene, self.multipleCameras, self.multipleWindows, self.cameraAngle);
        self.input = input.Input(self, self.mainWindow, self.camera);

        self.input.init();
        # L�gg till detta objekt som en framelistener s� vi f�r callbacks varje frame
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
        self.gui.setText("velocity", "Velocity: %d (km/h)" % (abs(self.camera.getVelocity().z*36.0))); # Hastigheten �r i m/s ursprungligen
        
        # Kolla ifall v�rat f�nster har st�ngts, i s� fall returnerar vi false,
        #   vilket resulterar i att ogre avslutar
        if(self.mainWindow.isClosed()):
            return False;

        if(self.multipleWindows):
            if(self.leftWindow.isClosed()):
                return False;
            if(self.rightWindow.isClosed()):
                return False;
        
        # Ser till att vi renderar till f�nstret �ven fast det �r inaktivt
        if(self.mainWindow.isActive() == False):
            self.mainWindow.update();

        if(self.multipleWindows):
            if(self.leftWindow.isActive() == False):
                self.leftWindow.update();
            if(self.rightWindow.isActive() == False):
                self.rightWindow.update();

        
        return (self.isStopping == False);
    
if __name__ == '__main__':
    parser = OptionParser();
    parser.add_option("--multi-camera", action="store_true", dest="multicamera", default=False);
    parser.add_option("--multi-window", action="store_true", dest="multiwindow", default=False);
    parser.add_option("--camera-angle", action="store", type="int", dest="angle", default=58);

    (options, args) = parser.parse_args();
    
    multipleCameras = options.multicamera; # Definerar ifall vi ska ha flera kameror eller inte
    multipleWindows = options.multiwindow; # Definerar ifall vi ska ha flera f�nster eller inte
    cameraAngle = options.angle;
    
    app = Application(multipleCameras, multipleWindows, cameraAngle);
    app.run();

