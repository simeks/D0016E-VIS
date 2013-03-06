# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import math
import physics



class Scene:
    # Konstruktor
    #   root    : Ogres root-objekt
    def __init__(self, root):
        self.root = root;

        # default värden
        self.walkSpeed = 200.0 # Objektets hastighet
        self.direction = ogre.Vector3().ZERO # Objektets riktning
        self.distance = 0.0 # Distansen mellan objektet och punkten dit objektet är påväg

        # 
        self.walklist = []
        self.walklist.append(ogre.Vector3(-4350, 0, -550))
        self.walklist.append(ogre.Vector3(-3350, 0, 550))

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
        self.sceneMgr.setAmbientLight(ogre.ColourValue(0.5,0.5,0.5));
        fadeColor = ogre.ColourValue(0.9, 0.9, 0.9);
        self.sceneMgr.setFog(ogre.FOG_LINEAR, fadeColor, 0.0, 10000, 80000);
        
        # Eftersom scengrafen är som ett träd så hämtar vi root-noden och bygger utifrån den
        self.rootNode = self.sceneMgr.getRootSceneNode();

        # Initialisera fysikvärlden
        self.physics.init(-1000);
        
        # Skapa en entitet från en mesh-fil vi har bland vår media
        self.entity = self.sceneMgr.createEntity("Sinbad", "robot.mesh");
        self.entity.setCastShadows(True);
        # Skapa en child node till vår root node
        self.node = self.rootNode.createChildSceneNode('SinbadNode', (-4350, 0, -550));
        # och fäst vår entitet vid den noden
        self.node.attachObject(self.entity);
        self.node.setScale(10, 10, 10);
        
        
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


        # Skapa väg
        self.createRoad(ogre.Vector3(10000, 1, 0), ogre.Vector3(-10000, 1, 0), 1000)

        # Skapa hus
        self.createHouse(-5000, -800);
        self.createHouse(-5000, 0);

        # Skapa staket
        self.createFence(ogre.Vector3(9448,0,-13190), ogre.Vector3(5863,0,-14857));
        

        # skapa tunnor
        #self.createBarrel(-3000, 120, -800);
        self.createBarrel(-3000, 120, 0);
        self.createBarrel(-1000, 120, -800);
        self.createBarrel(-1000, 120, 0);

        for b in range(1, 100):
            self.createBarrel(2000, 120, 1300-b*200);
        for b in range(1, 100):
            self.createBarrel(2000, 200, 1300-b*200);
        for b in range(1, 100):
            self.createBarrel(2000, 320, 1300-b*200);

        #
        animationState = self.entity.getAnimationState('Idle')
        animationState.setLoop(True)
        animationState.setEnabled(True)

        # Lägg till ett directional light så man ser kuben något bättre
        self.light = self.sceneMgr.createLight("Light");
        self.light.setCastShadows(True);
        self.light.type = ogre.Light.LT_DIRECTIONAL;
        self.light.diffuseColour = (0.9,0.9,0.9);
        self.light.direction = (0.5, -0.5, 0.5);

        
    def createCamera(self, name):
        camera = self.sceneMgr.createCamera(name);
        return camera;

    def createRoad(self, startPos, endPos, width):
        plane = ogre.Plane((0, 1, 0), 0);
        if(startPos.x == endPos.x):
            ogre.MeshManager.getSingleton().createPlane ("Road", "General", plane, width, startPos.z-endPos.z,
                                                         100, 100, True, 1, 1, 1, (0,0,1));
            self.roadEntity = self.sceneMgr.createEntity("Road", "Road");
            self.roadEntity.setMaterialName("Road");
            self.roadNode = self.rootNode.createChildSceneNode();
            self.roadNode.attachObject(self.roadEntity);
            self.roadNode.setPosition(startPos.x,1,startPos.z+((endPos.z-startPos.z)/2));
            
        elif(startPos.z == endPos.z):
            ogre.MeshManager.getSingleton().createPlane ("Road", "General", plane, width, startPos.x-endPos.x,
                                                         100, 100, True, 1, 1, 1, (1,0,0));
            self.roadEntity = self.sceneMgr.createEntity("Road", "Road");
            self.roadEntity.setMaterialName("Road");
            self.roadNode = self.rootNode.createChildSceneNode();
            self.roadNode.attachObject(self.roadEntity);
            self.roadNode.setPosition(startPos.x+((endPos.x-startPos.x)/2),1,startPos.z);
        #else:
            # sne väg...

    def createHouse(self, x, z):
        houseEnt = self.sceneMgr.createEntity(str("house")+str(self.houseNumber), "tudorhouse.mesh");
        houseNode = self.rootNode.createChildSceneNode(str("house")+str(self.houseNumber));
        houseNode.setPosition(x, 550, z);
        houseNode.attachObject(houseEnt);
        self.houseNumber += 1;

    def createFence(self, p1, p2):
        delta = p2 - p1;
        fenceLength = 300;
        num = delta.length() / fenceLength;
        pos = p1;
        for i in range(0, int(num)):
            fenceEnt = self.sceneMgr.createEntity(str("fence_")+str(self.fenceNumber)+"_"+str(i), "fence.mesh");
            fenceNode = self.rootNode.createChildSceneNode(str("fence_")+str(self.fenceNumber)+"_"+str(i));
            fenceNode.setPosition(pos);
            fenceNode.setScale(10, 15, 2);
            fenceNode.attachObject(fenceEnt);
            quatx = ogre.Quaternion(math.pi, (1,0,0));
            angle = math.acos(abs(delta.x) / delta.length());
            
            quaty = ogre.Quaternion(angle, (0,1,0));
            quatx = quatx * quaty;
            fenceNode.setOrientation(quatx);
            pos += (delta / num);

        self.fenceNumber += 1;

    
   # def createFence(self, x, z):
   #     fenceEnt = self.sceneMgr.createEntity(str("fence")+str(self.fenceNumber), "fence2.mesh");
   #     fenceNode = self.rootNode.createChildSceneNode(str("fence")+str(self.fenceNumber));
   #     fenceNode.setPosition(x, 120, z);
   #     fenceNode.setScale(10, 20, 2);
   #     fenceNode.attachObject(fenceEnt);
   #     self.fenceNumber += 1;        

    def createBarrel(self, x, y, z):
        ent = self.sceneMgr.createEntity(str("barrel")+str(self.barrelNumber), "Barrel.mesh");
        node = self.rootNode.createChildSceneNode(str("konNode")+str(self.barrelNumber));
        node.setPosition(x, y, z); 
        node.attachObject(ent);
        node.setScale(20, 25, 20);            
        aabb = ent.getMesh().getBounds();
        self.physics.createCylinder(node, 20*aabb.getSize().x, (25*aabb.getSize().y)-3, 20*aabb.getSize().z, 200);
        self.barrelNumber += 1;
    
    
    def nextLocation(self):
      if len(self.walklist) == 0:
         return False
      self.destination = self.walklist.pop(0) # Plocka objektet högst upp i listan
      self.walklist.append(self.destination) # Lägg tillbaka längst bak i listan
      self.direction = self.destination - self.node.getPosition()
      self.distance = self.direction.normalise()
 
      src = self.node.getOrientation() * ogre.Vector3().UNIT_X
      if 1.0 + src.dotProduct(self.direction) < 0.0001:
         self.node.yaw(ogre.Degree(180))
      else:
         quat = src.getRotationTo(self.direction)
         self.node.rotate(quat)
      return True


    def frame(self, evt):
        # Kör ett steg av fysiksimuleringen
        self.physics.frame(evt);
        if self.direction == ogre.Vector3().ZERO:
            if self.nextLocation():
                # Set walking animation
                self.animationStateTop = self.entity.getAnimationState('Walk')
                self.animationStateTop.setLoop(True)
                self.animationStateTop.setEnabled(True)
                #self.animationStateBase = self.entity.getAnimationState('RunBase')
                #self.animationStateBase.setLoop(True)
                #self.animationStateBase.setEnabled(True)
        else:
            move = self.walkSpeed * evt.timeSinceLastFrame;
            self.distance -= move
            if self.distance <= 0.0:
                self.node.setPosition(self.destination)
                self.direction = ogre.Vector3().ZERO
                if not self.nextLocation():
                    # Set Idle animation
                    self.animationStateTop = self.entity.getAnimationState('Idle')
                    self.animationStateTop.setLoop(True)
                    self.animationStateTop.setEnabled(True)
                    #self.animationStateBase = self.entity.getAnimationState('IdleBase')
                    #self.animationStateBase.setLoop(True)
                    #self.animationStateBase.setEnabled(True)
            else:
                self.node.translate(self.direction * move)
        self.animationStateTop.addTime(evt.timeSinceLastFrame)
     # self.animationStateBase.addTime(evt.timeSinceLastFrame)
        
    #def shutdown(self):
        

