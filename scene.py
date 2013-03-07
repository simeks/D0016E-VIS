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
        self.sceneMgr.setAmbientLight(ogre.ColourValue(0.5,0.5,0.5));
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
        self.createRoad(ogre.Vector3(10000, 1, 0), ogre.Vector3(-10000, 1, 0), 1000)

        # Skapa hus
        self.createHouse(-5000, -800);
        self.createHouse(-5000, 0);

        # Skapa staket
        #self.createFence(ogre.Vector3(6584,0,4072), ogre.Vector3(6132,0,5040));
        #self.createFence(ogre.Vector3(6132,0,5040), ogre.Vector3(404,0,5181));
        #self.createFence(ogre.Vector3(404,0,5181), ogre.Vector3(-12,0,4985));
        #self.createFence(ogre.Vector3(-12,0,4985), ogre.Vector3(-310,0,4703));
        #self.createFence(ogre.Vector3(-310,0,4703), ogre.Vector3(-400,0,4239));
        #self.createFence(ogre.Vector3(-400,0,4239), ogre.Vector3(-455,0,-941));        
        #self.createFence(ogre.Vector3(-455,0,-941), ogre.Vector3(-501,0,-1571));
        #self.createFence(ogre.Vector3(-501,0,-1571), ogre.Vector3(-458,0,-3827));        
        #self.createFence(ogre.Vector3(-458,0,-3827), ogre.Vector3(-664,0,-4423));
        #self.createFence(ogre.Vector3(-664,0,-4423), ogre.Vector3(-367,0,-5129));        
        #self.createFence(ogre.Vector3(-367,0,-5129), ogre.Vector3(180,0,-5357));
        #self.createFence(ogre.Vector3(180,0,-5357), ogre.Vector3(4583,0,-14480));        
        #self.createFence(ogre.Vector3(4583,0,-14480), ogre.Vector3(4919,0,-14849));
        #self.createFence(ogre.Vector3(4919,0,-14849), ogre.Vector3(5325,0,-14989));        
        #self.createFence(ogre.Vector3(5325,0,-14989), ogre.Vector3(5767,0,-14962));
        #self.createFence(ogre.Vector3(5767,0,-14962), ogre.Vector3(9340,0,-13214));        
        #self.createFence(ogre.Vector3(9340,0,-13214), ogre.Vector3(9702,0,-13179));
        #self.createFence(ogre.Vector3(9702,0,-13179), ogre.Vector3(10103,0,-13006));        
        #self.createFence(ogre.Vector3(10103,0,-13006), ogre.Vector3(10330,0,-12724));
        #self.createFence(ogre.Vector3(10330,0,-12724), ogre.Vector3(10779,0,-12452));        
        #self.createFence(ogre.Vector3(10779,0,-12452), ogre.Vector3(11049,0,-12122));
        #self.createFence(ogre.Vector3(11049,0,-12122), ogre.Vector3(11083,0,-11762));
        #self.createFence(ogre.Vector3(11083,0,-11762), ogre.Vector3(7588,0,-4714));
        #self.createFence(ogre.Vector3(7588,0,-4714), ogre.Vector3(6673,0,-2765));        
        #self.createFence(ogre.Vector3(6673,0,-2765), ogre.Vector3(6528,0,-2334));
        #self.createFence(ogre.Vector3(6528,0,-2334), ogre.Vector3(6513,0,2443));        
        #self.createFence(ogre.Vector3(6513,0,2443), ogre.Vector3(6584,0,4072));
            
        self.createFence(ogre.Vector3(-1000,0,-1000), ogre.Vector3(-1000,0, 1000));
        self.createFence(ogre.Vector3(-1000,0, 1000), ogre.Vector3( 1000,0, 1000));
        self.createFence(ogre.Vector3( 1000,0, 1000), ogre.Vector3( 1000,0,-1000));
        self.createFence(ogre.Vector3( 1000,0,-1000), ogre.Vector3(-1000,0,-1000));

        # skapa tunnor
        #self.createBarrel(-3000, 120, -800);
        self.createBarrel(-3000, 120, 0);
        self.createBarrel(-1000, 120, -800);
        self.createBarrel(-1000, 120, 0);

        for b in range(1, 10):
            self.createBarrel(2000, 160, 1300-b*200);

        #
        #animationState = self.entity.getAnimationState('Idle')
        #animationState.setLoop(True)
        #animationState.setEnabled(True)

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
        dir = p2 - p1;
        fenceLength = 290;
        num = (dir.length() / fenceLength)+1;
        dir.normalise();

        quatx = ogre.Quaternion(math.pi, (1,0,0)); # Rotera 180 grader så att staketet inte är upp och ned
        anglec = math.acos(dir.x / dir.length()); # Beräkna vinkeln mellan våra två punkter
        angles = math.asin(dir.z / dir.length());

        angledot = math.acos(dir.dotProduct(ogre.Vector3(1, 0, 0)));

        print "P1:",p1.x,p1.z,"P2:",p2.x,p2.z;
        print "Angle:",(anglec*(180/math.pi)),(angles*(180/math.pi));
        print "Angle dot:",(angledot*(180/math.pi));


        #quaty = ogre.Quaternion(angledot, (0,-1,0));
        quaty = dir.getRotationTo(ogre.Vector3(1,0,0)) * ogre.Vector3(1, 0, 0);
        quat = quatx * quaty;

        rootNode = self.rootNode.createChildSceneNode(str("fence_root_"+str(self.fenceNumber)));

        pos = ogre.Vector3(0,0,0);
        for i in range(0, int(num)):
            fenceEnt = self.sceneMgr.createEntity(str("fence_")+str(self.fenceNumber)+"_"+str(i), "fence.mesh"); 
            aabb = fenceEnt.getMesh().getBounds();
            fenceNode = rootNode.createChildSceneNode(str("fence_")+str(self.fenceNumber)+"_"+str(i));
            fenceNode.setPosition(pos);
            fenceNode.setScale(10, 12, 2);
            fenceNode.attachObject(fenceEnt);
            #fenceNode.setOrientation(quat);
            pos.x += fenceLength;
            
        rootNode.setPosition(p1);
        rootNode.setOrientation(quat);
        self.fenceNumber += 1;
    
   

    def createBarrel(self, x, y, z):
        ent = self.sceneMgr.createEntity(str("barrel")+str(self.barrelNumber), "Barrel.mesh");
        node = self.rootNode.createChildSceneNode(str("konNode")+str(self.barrelNumber));
        node.setPosition(x, y, z); 
        node.attachObject(ent);
        node.setScale(20, 25, 20);            
        aabb = ent.getMesh().getBounds();
        self.physics.createCylinder(node, 20*aabb.getSize().x, (25*aabb.getSize().y)-3, 20*aabb.getSize().z, 50);
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
        

