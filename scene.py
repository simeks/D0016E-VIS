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
        #self.walkSpeed = 200.0 # Objektets hastighet
        #self.direction = ogre.Vector3().ZERO # Objektets riktning
        #self.distance = 0.0 # Distansen mellan objektet och punkten dit objektet är påväg

        # 
        #self.walklist = []
        #self.walklist.append(ogre.Vector3(-4350, 0, -550))
        #self.walklist.append(ogre.Vector3(-3350, 0, 550))

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

        # Initialisera fysikvärlden
        self.physics.init(-1000);
        
        # Skapa en entitet från en mesh-fil vi har bland vår media
        #self.entity = self.sceneMgr.createEntity("Sinbad", "robot.mesh");
        #self.entity.setCastShadows(True);
        # Skapa en child node till vår root node
        #self.node = self.rootNode.createChildSceneNode('SinbadNode', (-4350, 0, -550));
        # och fäst vår entitet vid den noden
        #self.node.attachObject(self.entity);
        #self.node.setScale(10, 10, 10);
        
        
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
        self.createRoad(ogre.Vector3(7000, 1, -10000), ogre.Vector3(7000, 1, 10000))

        # Skapa hus
        rot = ogre.Quaternion(math.pi/2.0, (0, 1, 0));
        for i in range(0, 10):
            self.createHouse(10000+(math.sin(i)*1000), -2000+(i*800), rot);

        for i in range(0, 10):
            self.createHouse(11500+(math.sin(i)*1000), -1500+(i*800), rot);
        
        self.createWindmill(0, 15000);
        self.createWindmill(1500, 13000);
        self.createWindmill(2300, 12000);

        # Skapa staket
        self.createFence(ogre.Vector3(78,0,-5527), ogre.Vector3(2727,0,-10866));
        self.createFence(ogre.Vector3(2727,0,-10866), ogre.Vector3(2963,0,-11459));
        self.createFence(ogre.Vector3(2963,0,-11459), ogre.Vector3(4496,0,-14595)); 
        self.createFence(ogre.Vector3(4435,0,-14536), ogre.Vector3(4994,0,-14997)); 
        self.createFence(ogre.Vector3(4994,0,-14997), ogre.Vector3(5470,0,-15118)); 
        self.createFence(ogre.Vector3(5470,0,-15118), ogre.Vector3(5885,0,-15046)); 
        self.createFence(ogre.Vector3(5885,0,-15046), ogre.Vector3(9340,0,-13314));
        self.createFence(ogre.Vector3(9340,0,-13314), ogre.Vector3(10044,0,-13251));      
        self.createFence(ogre.Vector3(9925,0,-13222), ogre.Vector3(10216,0,-12885)); 
        self.createFence(ogre.Vector3(10216,0,-12885), ogre.Vector3(10468,0,-12662));        
        self.createFence(ogre.Vector3(10468,0,-12662), ogre.Vector3(10940,0,-12401));        
        self.createFence(ogre.Vector3(10940,0,-12401), ogre.Vector3(11225,0,-11865)); 
        self.createFence(ogre.Vector3(11225,0,-11865), ogre.Vector3(11183,0,-11662)); 
        self.createFence(ogre.Vector3(11183,0,-11662), ogre.Vector3(7588,0,-4514)); 
        self.createFence(ogre.Vector3(7588,0,-4514), ogre.Vector3(6773,0,-2665)); 
        self.createFence(ogre.Vector3(6773,0,-2665), ogre.Vector3(6628,0,-2234));
        self.createFence(ogre.Vector3(6628,0,-2234), ogre.Vector3(6613,0,2343));         
        self.createFence(ogre.Vector3(6613,0,2343), ogre.Vector3(6684,0,3972)); 
        self.createFence(ogre.Vector3(6684,0,3972), ogre.Vector3(6600,0,4770)); 
        self.createFence(ogre.Vector3(6600,0,4770), ogre.Vector3(6169,0,5278)); 
        self.createFence(ogre.Vector3(6169,0,5278), ogre.Vector3(220,0,5297)); 
        self.createFence(ogre.Vector3(220,0,5297), ogre.Vector3(-85,0,5019)); 
        self.createFence(ogre.Vector3(-85,0,5019), ogre.Vector3(-431,0,4603)); 
        self.createFence(ogre.Vector3(-431,0,4603), ogre.Vector3(-555,0,4239)); 
        self.createFence(ogre.Vector3(-555,0,4239), ogre.Vector3(-555,0,-1141));  
        self.createFence(ogre.Vector3(-555,0,-1141), ogre.Vector3(-603,0,-1979)); 
        self.createFence(ogre.Vector3(-603,0,-1979), ogre.Vector3(-525,0,-3899)); 
        self.createFence(ogre.Vector3(-525,0,-3899), ogre.Vector3(-828,0,-4550)); 
        self.createFence(ogre.Vector3(-840,0,-4489), ogre.Vector3(-415,0,-5301));  
        self.createFence(ogre.Vector3(-486,0,-5302), ogre.Vector3(78,0,-5527)); 

        # skapa tunnor
        for b in range(1, 10):
            self.createBarrel(2000, 50, 1300-b*200);

        for b in range(1, 10):
            self.createBarrel(2500, 50, 1300-b*200);

        for b in range(1, 10):
            self.createBarrel(3000, 50, 1300-b*200);

        for b in range(1, 10):
            self.createBarrel(3500, 50, 1300-b*200);
        #
        #animationState = self.entity.getAnimationState('Idle')
        #animationState.setLoop(True)
        #animationState.setEnabled(True)



        #for i in range(1, 6):
        #    for j in range(1, i):
        #        half = 100.0 / float(j+1);
        #        self.createBarrel(4000+half, 60, -1500-i*100);
        #        half += 100.0 / float(j+1);




        

        # Lägg till ett directional light så man ser kuben något bättre
        self.light = self.sceneMgr.createLight("Light");
        self.light.setCastShadows(True);
        self.light.type = ogre.Light.LT_DIRECTIONAL;
        self.light.diffuseColour = (0.8,0.8,0.9);
        self.light.direction = (0.5, -0.5, 0.5);

        
    def createCamera(self, name):
        camera = self.sceneMgr.createCamera(name);
        return camera;

    roadCreated = False;
    def createRoad(self, p2, p1):
        dir = p2 - p1;
        roadLength = 1000;
        num = (dir.length() / roadLength)+1;
        dir.normalise();

        #quatx = ogre.Quaternion(math.pi, (1,0,0)); # Rotera 180 grader så att staketet inte är upp och ned
        quaty = dir.getRotationTo(ogre.Vector3(0,0,-1));
        quat = quaty;

        if(self.roadCreated == False):
            plane = ogre.Plane((0, 1, 0), 0);
            ogre.MeshManager.getSingleton().createPlane ("Road", "General", plane, 800, roadLength,
                                                         100, 100, True, 1, 1, 1, (0,0,1));
            self.roadCreated = True;

        rootNode = self.rootNode.createChildSceneNode(str("road_root_"+str(self.fenceNumber)));
        pos = ogre.Vector3(0,0,0);
        for i in range(0, int(num)):
            roadEntity = self.sceneMgr.createEntity(str("road_")+str(self.fenceNumber)+"_"+str(i), "Road");
            roadEntity.setMaterialName("Road");
            roadNode = rootNode.createChildSceneNode(str("road_")+str(self.fenceNumber)+"_"+str(i));
            roadNode.setPosition(pos);
            roadNode.setOrientation(ogre.Quaternion(math.pi/2,(0,1,0)));
            roadNode.attachObject(roadEntity);
            pos.x += roadLength;
            
        rootNode.setPosition(p2);
        rootNode.setOrientation(quat);
        self.fenceNumber += 1;

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
    
    
##    def nextLocation(self):
##      if len(self.walklist) == 0:
##         return False
##      self.destination = self.walklist.pop(0) # Plocka objektet högst upp i listan
##      self.walklist.append(self.destination) # Lägg tillbaka längst bak i listan
##      self.direction = self.destination - self.node.getPosition()
##      self.distance = self.direction.normalise()
## 
##      src = self.node.getOrientation() * ogre.Vector3().UNIT_X
##      if 1.0 + src.dotProduct(self.direction) < 0.0001:
##         self.node.yaw(ogre.Degree(180))
##      else:
##         quat = src.getRotationTo(self.direction)
##         self.node.rotate(quat)
##      return True


    def frame(self, evt):
        # Kör ett steg av fysiksimuleringen
        self.physics.frame(evt);
        #if self.direction == ogre.Vector3().ZERO:
            #if self.nextLocation():
                # Set walking animation
                #self.animationStateTop = self.entity.getAnimationState('Walk')
                #self.animationStateTop.setLoop(True)
                #self.animationStateTop.setEnabled(True)
                
        #else:
            #move = self.walkSpeed * evt.timeSinceLastFrame;
            #self.distance -= move
            #if self.distance <= 0.0:
                #self.node.setPosition(self.destination)
                #self.direction = ogre.Vector3().ZERO
                #if not self.nextLocation():
                    # Set Idle animation
                    #self.animationStateTop = self.entity.getAnimationState('Idle')
                    #self.animationStateTop.setLoop(True)
                    #self.animationStateTop.setEnabled(True)
            #else:
                #self.node.translate(self.direction * move)
        #self.animationStateTop.addTime(evt.timeSinceLastFrame)
        
    #def shutdown(self):
        

