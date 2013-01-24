# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import input
import scene


class Application(ogre.FrameListener):
    # Konstruktor
    def __init__(self, multipleCameras, multipleWindows):
        # Definerar ifall vi ska ha flera kameror eller inte
        self.multipleCameras = multipleCameras;
        self.multipleWindows = multipleWindows;
        
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
        
        self.mainCamera = self.scene.createCamera("MainCamera");
        self.mainCamera.setPosition(0,150,-500);
        self.mainCamera.nearClipDistance = 5;

        # Ifall vi har flera kameror men bara ett f�nster s� kan inte viewporten t�cka hela f�nstret
        if self.multipleCameras and not self.multipleWindows:
            inv3 = 1.0/3.0;
            self.mainViewport = self.mainWindow.addViewport(self.mainCamera, 0, inv3, inv3, inv3, inv3);
        else:
            self.mainViewport = self.mainWindow.addViewport(self.mainCamera);

        self.mainViewport.setBackgroundColour(ogre.ColourValue(0.2,0.2,0.2)); # M�rkgr� bakgrund

        # Skapa kameror f�r h�ger och v�nster ifall vi ska anv�nda flera kameror
        if self.multipleCameras:
            self.leftCamera = self.scene.createCamera("LeftCamera");
            self.rightCamera = self.scene.createCamera("RightCamera");
            
            self.leftCamera.setPosition(0,150,-500);
            self.rightCamera.setPosition(0,150,-500);

            # Storleken p� v�ra viewports varierad beroende p� om vi vill rendera all till ett f�nster eller flera 
            if self.multipleWindows:
                self.leftViewport = self.leftWindow.addViewport(self.leftCamera);
                self.rightViewport = self.rightWindow.addViewport(self.rightCamera);
            else:
                inv3 = 1.0/3.0;
                self.leftViewport = self.mainWindow.addViewport(self.leftCamera, 1, 0, inv3, inv3, inv3);
                self.rightViewport = self.mainWindow.addViewport(self.rightCamera, 2, 2*inv3, inv3, inv3, inv3);
                
            self.leftViewport.setBackgroundColour(ogre.ColourValue(0.2,0.2,0.2)); # M�rkgr� bakgrund                
            self.rightViewport.setBackgroundColour(ogre.ColourValue(0.2,0.2,0.2)); # M�rkgr� bakgrund
            self.leftCamera.nearClipDistance = 5;
            self.rightCamera.nearClipDistance = 5;

        

        # Skapa v�rat input-objekt, och ge den en kamera den kan styra
        if self.multipleCameras:
            self.input = input.Input(self, self.mainWindow, self.mainCamera, self.leftCamera, self.rightCamera);
        else:
            self.input = input.Input(self, self.mainWindow, self.mainCamera, None, None);
        
        self.input.init();
        # L�gg till detta objekt som en framelistener s� vi f�r callbacks varje frame
        self.root.addFrameListener(self); 

    def shutdown(self):
        # Avsluta ogre
        self.root.shutdown();
        del self.root;

    def frameStarted(self, evt):
        # Notifiera input-modulen
        self.input.frame(evt);

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
    multipleCameras = True; # Definerar ifall vi ska ha flera kameror eller inte
    multipleWindows = True; # Definerar ifall vi ska ha flera f�nster eller inte

    
    app = Application(multipleCameras, multipleWindows);
    app.run();

