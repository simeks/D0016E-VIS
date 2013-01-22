# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import input
import scene


class Application(ogre.FrameListener):
    # Konstruktor
    def __init__(self):
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


    def init(self):
        # Skapa root som �r Ogres k�rna
        self.root = ogre.Root();
        # Ladda in v�ra s�kv�gar
        self.setupResources();
        # Visa en dialog som l�ter anv�ndaren v�lja grafikinst�llnigar
        self.root.showConfigDialog();
        # Initialisera Ogre
        self.window = self.root.initialise(True, # Autoskapa ett f�nster
                             "Titel"); # Titel p� f�nstret

        # Initialisera ogres resurshantering
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups();

        # Skapa v�r scen
        self.scene = scene.Scene(self.root, self.window);
        self.scene.init();
        
        # Skapa v�rat input-objekt, och ge den en kamera den kan styra
        self.input = input.Input(self, self.window, self.scene.camera);
        self.input.init();
        # L�gg till detta objekt som en framelistener s� vi f�r callbacks varje frame
        self.root.addFrameListener(self);
        
        
    def shutdown(self):
        self.input.shutdown();
        # Avsluta ogre
        self.root.shutdown();
        del self.root;

    def frameStarted(self, evt):
        # Notifiera input-modulen
        self.input.frame(evt);
        
        # Kolla ifall v�rat f�nster har st�ngts, i s� fall returnerar vi false,
        #   vilket resulterar i att ogre avslutar
        if(self.window.isClosed()):
            return False;
        return (self.isStopping == False);
    
if __name__ == '__main__':
    app = Application();
    app.run();

