# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import input
import scene


class Application(ogre.FrameListener):
    # Konstruktor
    def __init__(self):
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


    def init(self):
        # Skapa root som är Ogres kärna
        self.root = ogre.Root();
        # Ladda in våra sökvägar
        self.setupResources();
        # Visa en dialog som låter användaren välja grafikinställnigar
        self.root.showConfigDialog();
        # Initialisera Ogre
        self.window = self.root.initialise(True, # Autoskapa ett fönster
                             "Titel"); # Titel på fönstret

        # Initialisera ogres resurshantering
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups();

        # Skapa vår scen
        self.scene = scene.Scene(self.root, self.window);
        self.scene.init();
        
        # Skapa vårat input-objekt, och ge den en kamera den kan styra
        self.input = input.Input(self, self.window, self.scene.camera);
        self.input.init();
        # Lägg till detta objekt som en framelistener så vi får callbacks varje frame
        self.root.addFrameListener(self);
        
        
    def shutdown(self):
        self.input.shutdown();
        # Avsluta ogre
        self.root.shutdown();
        del self.root;

    def frameStarted(self, evt):
        # Notifiera input-modulen
        self.input.frame(evt);
        
        # Kolla ifall vårat fönster har stängts, i så fall returnerar vi false,
        #   vilket resulterar i att ogre avslutar
        if(self.window.isClosed()):
            return False;
        return (self.isStopping == False);
    
if __name__ == '__main__':
    app = Application();
    app.run();

