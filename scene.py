# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre

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
                                                     100, 100, True, 1, 1, 1, (0,0,1));
        self.planeEntity = self.sceneMgr.createEntity("Plane", "Plane");
        self.planeEntity.setMaterialName("Floor");
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
        

