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
        self.scene = scene.Scene(self.root);
        self.scene.init();
        
        self.mainCamera = self.scene.createCamera("MainCamera");
        self.mainCamera.setPosition(0,150,-500);
        self.mainCamera.nearClipDistance = 5;

        # Ifall vi har flera kameror men bara ett fönster så kan inte viewporten täcka hela fönstret
        if self.multipleCameras and not self.multipleWindows:
            inv3 = 1.0/3.0;
            self.mainViewport = self.mainWindow.addViewport(self.mainCamera, 0, inv3, inv3, inv3, inv3);
        else:
            self.mainViewport = self.mainWindow.addViewport(self.mainCamera);

        self.mainViewport.setBackgroundColour(ogre.ColourValue(0.2,0.2,0.2)); # Mörkgrå bakgrund

        # Skapa kameror för höger och vänster ifall vi ska använda flera kameror
        if self.multipleCameras:
            self.leftCamera = self.scene.createCamera("LeftCamera");
            self.rightCamera = self.scene.createCamera("RightCamera");
            
            self.leftCamera.setPosition(0,150,-500);
            self.rightCamera.setPosition(0,150,-500);

            # Storleken på våra viewports varierad beroende på om vi vill rendera all till ett fönster eller flera 
            if self.multipleWindows:
                self.leftViewport = self.leftWindow.addViewport(self.leftCamera);
                self.rightViewport = self.rightWindow.addViewport(self.rightCamera);
            else:
                inv3 = 1.0/3.0;
                self.leftViewport = self.mainWindow.addViewport(self.leftCamera, 1, 0, inv3, inv3, inv3);
                self.rightViewport = self.mainWindow.addViewport(self.rightCamera, 2, 2*inv3, inv3, inv3, inv3);
                
            self.leftViewport.setBackgroundColour(ogre.ColourValue(0.2,0.2,0.2)); # Mörkgrå bakgrund                
            self.rightViewport.setBackgroundColour(ogre.ColourValue(0.2,0.2,0.2)); # Mörkgrå bakgrund
            self.leftCamera.nearClipDistance = 5;
            self.rightCamera.nearClipDistance = 5;

        

        # Skapa vårat input-objekt, och ge den en kamera den kan styra
        if self.multipleCameras:
            self.input = input.Input(self, self.mainWindow, self.mainCamera, self.leftCamera, self.rightCamera);
        else:
            self.input = input.Input(self, self.mainWindow, self.mainCamera, None, None);
        
        self.input.init();
        # Lägg till detta objekt som en framelistener så vi får callbacks varje frame
        self.root.addFrameListener(self); 

    def shutdown(self):
        # Avsluta ogre
        self.root.shutdown();
        del self.root;

    def frameStarted(self, evt):
        # Notifiera input-modulen
        self.input.frame(evt);

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
    multipleCameras = True; # Definerar ifall vi ska ha flera kameror eller inte
    multipleWindows = True; # Definerar ifall vi ska ha flera fönster eller inte

    
    app = Application(multipleCameras, multipleWindows);
    app.run();

