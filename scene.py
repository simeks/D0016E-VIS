# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre

class Scene:
    # Konstruktor
    #   root    : Ogres root-objekt
    def __init__(self, root):
        self.root = root;

        # default värden
        self.walkSpeed = 35.0 # Objektets hastighet
        self.direction = ogre.Vector3().ZERO # Objektets riktning
        self.distance = 0.0 # Distansen mellan objektet och punkten dit objektet är påväg

        # 
        self.walklist = []
        self.walklist.append(ogre.Vector3(550, 0, 50))
        self.walklist.append(ogre.Vector3(-100, 0, -200))

    def __del__(self):
        del self.sceneMgr;

    def init(self):
        # Skapa en scengraf för den här scenen
        self.sceneMgr = self.root.createSceneManager(ogre.ST_GENERIC, "Scene");

        # Sätt så vi får ett ambient light som lyser upp scenen
        self.sceneMgr.setAmbientLight(ogre.ColourValue(0.9,0.9,0.9));
        # Eftersom scengrafen är som ett träd så hämtar vi root-noden och bygger utifrån den
        self.rootNode = self.sceneMgr.getRootSceneNode();
        
        # Skapa en entitet från en mesh-fil vi har bland vår media
        self.entity = self.sceneMgr.createEntity("Robot", "robot.mesh");
        # Skapa en child node till vår root node
        self.node = self.rootNode.createChildSceneNode('robotNode', (-1500, 100, 0));
        # och fäst vår entitet vid den noden
        self.node.attachObject(self.entity);

        ent2 = self.sceneMgr.createEntity("barrel", "Barrel.mesh");
        node2 = self.rootNode.createChildSceneNode("konNode");
        node2.setPosition(-600, 50, 10); 
        node2.attachObject(ent2);
        node2.setScale(20, 20, 20);
        
        # Lägg till ett stort plan (1000x1000)
        plane = ogre.Plane((0, 1, 0), 0);
        ogre.MeshManager.getSingleton().createPlane ("Plane", "General", plane, 10000, 10000,
                                                     100, 100, True, 1, 1, 1, (0,0,1));
        self.planeEntity = self.sceneMgr.createEntity("Plane", "Plane");
        self.planeEntity.setMaterialName("Floor");
        self.planeNode = self.rootNode.createChildSceneNode();
        self.planeNode.attachObject(self.planeEntity);

        #
        self.animationState = self.entity.getAnimationState('Idle')
        self.animationState.setLoop(True)
        self.animationState.setEnabled(True)

        # Lägg till ett directional light så man ser kuben något bättre
        self.light = self.sceneMgr.createLight("Light");
        self.light.type = ogre.Light.LT_DIRECTIONAL;
        self.light.diffuseColour = (0.9,0.9,0.9);
        self.light.direction = (0.5, 0.5, 0.5);


    def createCamera(self, name):
        return self.sceneMgr.createCamera(name);
        
    
    def nextLocation(self):
      if len(self.walklist) == 0:
         return False
      self.destination = self.walklist.pop()
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
      if self.direction == ogre.Vector3().ZERO:
         if self.nextLocation():
            # Set walking animation
            self.animationState = self.entity.getAnimationState('Walk')
            self.animationState.setLoop(True)
            self.animationState.setEnabled(True)
      else:
         move = self.walkSpeed * evt.timeSinceLastFrame;
         self.distance -= move
         if self.distance <= 0.0:
            self.node.setPosition(self.destination)
            self.direction = ogre.Vector3().ZERO
            if not self.nextLocation():
               # Set Idle animation
               self.animationState = self.entity.getAnimationState('Idle')
               self.animationState.setLoop(True)
               self.animationState.setEnabled(True)
         else:
            self.node.translate(self.direction * move)
      self.animationState.addTime(evt.timeSinceLastFrame)
        
    #def shutdown(self):
        

