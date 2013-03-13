# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import math
import physics
import json


class Scene:
    # Konstruktor
    #   root    : Ogres root-objekt
    def __init__(self, config, root):
        self.config = config;
        self.root = root;

        self.physics = physics.PhysicsWorld();
        self.houseNumber = 0;
        self.fenceNumber = 0;
        self.barrelNumber = 0;

    def __del__(self):
        del self.sceneMgr;

    def init(self):
        # Skapa en scengraf för den här scenen
        self.sceneMgr = self.root.createSceneManager(ogre.ST_GENERIC, "Scene");
        self.sceneMgr.setShadowTechnique(ogre.SHADOWTYPE_STENCIL_ADDITIVE);
        # Skapa himmelen
        self.sceneMgr.setSkyDome (True, "Examples/CloudySky", 24, 16, 50000)
        # Sätt så vi får ett ambient light som lyser upp scenen
        self.sceneMgr.setAmbientLight(ogre.ColourValue(0.7,0.7,0.8));
        fadeColor = ogre.ColourValue(0.9, 0.9, 0.9);
        self.sceneMgr.setFog(ogre.FOG_LINEAR, fadeColor, 0.0, 10000, 80000);
        
        # Eftersom scengrafen är som ett träd så hämtar vi root-noden och bygger utifrån den
        self.rootNode = self.sceneMgr.getRootSceneNode();


        # Ladda in nivån
        if(self.config.has_option("scene", "level")):
            levelFile = self.config.get("scene", "level");
        else:
            print "Missing level file"
            return;

        levelFh = open("assets/"+levelFile); 
        level = json.load(levelFh);
        
        # Initialisera fysikvärlden
        self.physics.init(level["gravity"]);

        for o in level["objects"]:
            if(o["type"] == "barrel"):
                self.createBarrel(o["pos"][0],o["pos"][1],o["pos"][2]);
            elif(o["type"] == "windmill"):
                self.createWindmill(o["pos"][0],o["pos"][1]);
            elif(o["type"] == "house"):
                self.createHouse(o["pos"][0],o["pos"][1],
                            ogre.Quaternion(o["rot"][0],o["rot"][1],o["rot"][2],o["rot"][3]));
            elif(o["type"] == "fence"):
                self.createFence(ogre.Vector3(o["pos1"][0],o["pos1"][1],o["pos1"][2]), ogre.Vector3(o["pos2"][0],o["pos2"][1],o["pos2"][2]));

        
        # Lägg till ett stort plan (20000x20000)
        plane = ogre.Plane((0, 1, 0), 0);
        ogre.MeshManager.getSingleton().createPlane ("Plane", "General", plane, 2000000, 2000000,
                                                     100, 100, True, 1, 1, 1, (0,0,1));
        self.planeEntity = self.sceneMgr.createEntity("Plane", "Plane");
        self.planeEntity.setMaterialName("Floor");
        self.planeNode = self.rootNode.createChildSceneNode();
        self.planeNode.attachObject(self.planeEntity);

        # Skapa en representation av marken i fysikvärlden
        self.physics.createGround(self.planeNode);
        

        # Lägg till ett directional light så man ser kuben något bättre
        self.light = self.sceneMgr.createLight("Light");
        self.light.setCastShadows(True);
        self.light.type = ogre.Light.LT_DIRECTIONAL;
        self.light.diffuseColour = (0.8,0.8,0.9);
        self.light.direction = (0.5, -0.5, 0.5);

        
    def createCamera(self, name):
        camera = self.sceneMgr.createCamera(name);
        return camera;


    def createHouse(self, x, z, orientation):
        houseEnt = self.sceneMgr.createEntity(str("house")+str(self.houseNumber), "tudorhouse.mesh");
        houseNode = self.rootNode.createChildSceneNode(str("house")+str(self.houseNumber));
        houseNode.setPosition(x, 550, z);
        houseNode.setOrientation(orientation);
        houseNode.attachObject(houseEnt);
        self.houseNumber += 1;
        
    def createWindmill(self, x, z):
        windmillEnt = self.sceneMgr.createEntity(str("windmill")+str(self.houseNumber), "windmill.mesh");
        windmillNode = self.rootNode.createChildSceneNode(str("windmill")+str(self.houseNumber));
        windmillNode.setPosition(x, 2000, z);
        windmillNode.setScale(50, 50, 50);
        windmillNode.setOrientation(ogre.Quaternion(-math.pi/3.0, (0,1,0))*ogre.Quaternion(math.pi/2.0, (1,0,0)));
        windmillNode.attachObject(windmillEnt);
        self.houseNumber += 1;

    def createFence(self, p2, p1):
        dir = p2 - p1;
        fenceLength = 290;
        num = (dir.length() / fenceLength)+1;
        dir.normalise();

        quatx = ogre.Quaternion(math.pi, (1,0,0)); # Rotera 180 grader så att staketet inte är upp och ned
        quaty = dir.getRotationTo(ogre.Vector3(1,0,0));
        quat = quatx * quaty;

        rootNode = self.rootNode.createChildSceneNode(str("fence_root_"+str(self.fenceNumber)));
        pos = ogre.Vector3(0,0,0);
        for i in range(0, int(num)):
            fenceEnt = self.sceneMgr.createEntity(str("fence_")+str(self.fenceNumber)+"_"+str(i), "fence.mesh"); 
            aabb = fenceEnt.getMesh().getBounds();
            fenceNode = rootNode.createChildSceneNode(str("fence_")+str(self.fenceNumber)+"_"+str(i));
            fenceNode.setPosition(pos);
            fenceNode.setScale(10, 10, 2);
            fenceNode.attachObject(fenceEnt);
            pos.x += fenceLength;
            
        rootNode.setPosition(p1);
        rootNode.setOrientation(quat);
        self.fenceNumber += 1;
    
   

    def createBarrel(self, x, y, z):
        ent = self.sceneMgr.createEntity(str("barrel")+str(self.barrelNumber), "Barrel.mesh");
        node = self.rootNode.createChildSceneNode(str("konNode")+str(self.barrelNumber));
        node.setPosition(x, y, z); 
        node.attachObject(ent);
        node.setScale(12, 17, 12);
        aabb = ent.getMesh().getBounds();
        self.physics.createCylinder(node, 12*aabb.getSize().x, (17*aabb.getSize().y)-3, 12*aabb.getSize().z, 250);
        self.barrelNumber += 1;
    

    def frame(self, evt):
        # Kör ett steg av fysiksimuleringen
        self.physics.frame(evt);

        

