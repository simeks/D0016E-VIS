# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import input

class Scene:
    # Konstruktor
    #   root    : Ogres root-objekt
    def __init__(self, root, window):
        self.root = root;
        self.window = window;

    def __del__(self):
        del self.sceneMgr;

    def init(self):
        # Skapa en scengraf f�r den h�r scenen
        self.sceneMgr = self.root.createSceneManager(ogre.ST_GENERIC, "Scene");
        # Skapa en kamera
        self.camera = self.sceneMgr.createCamera("MainCamera");
        # och en viewport
        self.viewport = self.window.addViewport(self.camera);
        self.viewport = (0.1,0.1,0.1); # M�rkgr� bakgrund

        # S�tt s� vi f�r ett ambient light som lyser upp scenen
        self.sceneMgr.setAmbientLight(ogre.ColourValue(0.9,0.9,0.9));
        # Eftersom scengrafen �r som ett tr�d s� h�mtar vi root-noden och bygger utifr�n den
        self.rootNode = self.sceneMgr.getRootSceneNode();
        # Skapa en entitet fr�n en mesh-fil vi har bland v�r media
        self.entity = self.sceneMgr.createEntity("cube", "cube.mesh");
        self.entity.setMaterialName("BaseWhite");
        # Skapa en child node till v�r root node
        self.node = self.rootNode.createChildSceneNode();
        # och f�st v�r entitet vid den noden
        self.node.attachObject(self.entity);

        # L�gg till ett stort plan (1000x1000)
        plane = ogre.Plane((0, 1, 0), 0);
        ogre.MeshManager.getSingleton().createPlane ("Plane", "General", plane, 10000, 10000,
                                                     1, 1, True, 1, 1, 1, (0,0,1));
        self.planeEntity = self.sceneMgr.createEntity("Plane", "Plane");
        self.planeEntity.setMaterialName("Examples/RustySteel");
        self.planeNode = self.rootNode.createChildSceneNode();
        self.planeNode.attachObject(self.planeEntity);
        
        # L�gg till ett directional light s� man ser kuben n�got b�ttre
        self.light = self.sceneMgr.createLight("Light");
        self.light.type = ogre.Light.LT_DIRECTIONAL;
        self.light.diffuseColour = (0.9,0.9,0.9);
        self.light.direction = (0.5, 0.5, 0.5);

        self.node.setPosition(0,0,0);

        # L�gg upp kameran s� den kollar p� v�ran entitet
        self.camera.setPosition(0,150,-500);
        self.camera.lookAt(0,0,0);
        self.camera.nearClipDistance = 5;
       
        
    #def shutdown(self):
        
    

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
        self.scene = Scene(self.root, self.window);
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

