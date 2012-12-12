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
        # Skapa en scengraf för den här scenen
        self.sceneMgr = self.root.createSceneManager(ogre.ST_GENERIC, "Scene");
        # Skapa en kamera
        self.camera = self.sceneMgr.createCamera("MainCamera");
        # och en viewport
        self.viewport = self.window.addViewport(self.camera);
        self.viewport = (0.1,0.1,0.1); # Mörkgrå bakgrund

        # Sätt så vi får ett ambient light som lyser upp scenen
        self.sceneMgr.setAmbientLight(ogre.ColourValue(0.3,0.3,0.3));
        # Eftersom scengrafen är som ett träd så hämtar vi root-noden och bygger utifrån den
        self.rootNode = self.sceneMgr.getRootSceneNode();
        # Skapa en entitet från en mesh-fil vi har bland vår media
        self.entity = self.sceneMgr.createEntity("cube", "cube.mesh");
        self.entity.setMaterialName("Examples/RustySteel");
        # Skapa en child node till vår root node
        self.node = self.rootNode.createChildSceneNode();
        # och fäst vår entitet vid den noden
        self.node.attachObject(self.entity);

        # Lägg till ett stort plan (1000x1000)
        plane = ogre.Plane((0, 1, 0), 0);
        ogre.MeshManager.getSingleton().createPlane ("Plane", "General", plane, 1000, 1000,
                                                     1, 1, True, 1, 1, 1, (0,0,1));
        self.planeEntity = self.sceneMgr.createEntity("Plane", "Plane")
        self.planeNode = self.rootNode.createChildSceneNode();
        self.planeNode.attachObject(self.planeEntity);
        
        # Lägg till ett directional light så man ser kuben något bättre
        self.light = self.sceneMgr.createLight("Light");
        self.light.type = ogre.Light.LT_DIRECTIONAL;
        self.light.diffuseColour = (0.9,0.9,0.9);
        self.light.direction = (0.5, 0.5, 0.5);

        self.node.setPosition(0,0,0);

        # Lägg upp kameran så den kollar på våran entitet
        self.camera.setPosition(0,150,-500);
        self.camera.lookAt(0,0,0);
        self.camera.nearClipDistance = 5;
       
        
    #def shutdown(self):
        
    

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
        self.scene = Scene(self.root, self.window);
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

