# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
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

        #for i in range(0, 3):
        #    for j in range(0, 3):
        #        ent2 = self.sceneMgr.createEntity(str("barrel")+str(i)+str(j), "Barrel.mesh");
        #        node2 = self.rootNode.createChildSceneNode(str("konNode")+str(i)+str(j));
        #        node2.setPosition(-3000, 120+(i*160), -800+(j*120)); 
        #        node2.attachObject(ent2);
        #        node2.setScale(20, 25, 20);            
        #        aabb = ent2.getMesh().getBounds();
        #        self.physics.createCylinder(node2, 20*aabb.getSize().x, (25*aabb.getSize().y)-3, 20*aabb.getSize().z, 200);


        for j in range(0, 10):
            ent2 = self.sceneMgr.createEntity(str("barrel")+str(j), "Barrel.mesh");
            node2 = self.rootNode.createChildSceneNode(str("konNode")+str(j));
            node2.setPosition(-3000, 120+(j*160), -800+(j*10)); 
            node2.attachObject(ent2);
            node2.setScale(20, 25, 20);            
            aabb = ent2.getMesh().getBounds();
            self.physics.createCylinder(node2, 20*aabb.getSize().x, (25*aabb.getSize().y)-3, 20*aabb.getSize().z, 200);


       # self.ent2 = self.sceneMgr.createEntity("barrel", "Barrel.mesh");
       # self.node2 = self.rootNode.createChildSceneNode("konNode");
       # self.node2.setPosition(-800, 150, 10); 
        #self.node2.attachObject(self.ent2);
        #self.node2.setScale(20, 25, 20);
     
      #  aabb = self.ent2.getMesh().getBounds();
       # self.physics.createCylinder(self.node2, 20*aabb.getSize().x, 25*aabb.getSize().y, 20*aabb.getSize().z, 10);




        #self.ent3 = self.sceneMgr.createEntity("barrel2", "Barrel.mesh");
        #self.node3 = self.rootNode.createChildSceneNode("konNode2");
        #self.node3.setPosition(-4200, 70, -700); 
        #self.node3.attachObject(self.ent3);
        #self.node3.setScale(20, 25, 20);
        
        
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


        # Vägen
        ogre.MeshManager.getSingleton().createPlane ("Road", "General", plane, 1000, 20000,
                                                     100, 100, True, 1, 1, 1, (1,0,0));
        self.roadEntity = self.sceneMgr.createEntity("Road", "Road");
        self.roadEntity.setMaterialName("Road");
        self.roadNode = self.rootNode.createChildSceneNode();
        self.roadNode.attachObject(self.roadEntity);
        self.roadNode.setPosition(0,1,0);


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
        

