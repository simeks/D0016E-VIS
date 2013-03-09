# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import ogre.physics.bullet as bullet
import physics

import math

class Camera:

    velocity = ogre.Vector3(0,0,0);
    rigidBody = None;
    
    def __init__(self, app, scene, multipleCameras, multipleWindows, cameraAngle):
        self.application = app;
        self.scene = scene;
        self.multipleCameras = multipleCameras;
        self.multipleWindows = multipleWindows;
        self.cameraAngle = cameraAngle;
        
        self.mainCamera = self.scene.createCamera("MainCamera");
        self.mainCamera.setPosition(100,100,-500);
        self.mainCamera.lookAt(-100,100,-500);
        self.mainCamera.nearClipDistance = 5;
        self.mainCamera.setFOVy(45*(math.pi/180.0));

        self.orientation = self.mainCamera.getOrientation();
        
        self.rigidBody = self.scene.physics.createCameraBody(self, ogre.Vector3(100,100,100), 500);


        # Ifall vi har flera kameror men bara ett fönster så kan inte viewporten täcka hela fönstret
        if self.multipleCameras and not self.multipleWindows:
            inv3 = 1.0/3.0;
            self.mainViewport = self.application.mainWindow.addViewport(self.mainCamera, 0, inv3, inv3, inv3, inv3);
        else:
            self.mainViewport = self.application.mainWindow.addViewport(self.mainCamera);

        self.mainViewport.setBackgroundColour(ogre.ColourValue(0.2,0.2,0.2)); # Mörkgrå bakgrund

        # Skapa kameror för höger och vänster ifall vi ska använda flera kameror
        if self.multipleCameras:
            self.leftCamera = self.scene.createCamera("LeftCamera");
            self.rightCamera = self.scene.createCamera("RightCamera");
            
            self.leftCamera.setPosition(0,150,-500);
            self.leftCamera.setFOVy(45*(math.pi/180.0));
            self.rightCamera.setPosition(0,150,-500);
            self.rightCamera.setFOVy(45*(math.pi/180.0));

            # Storleken på våra viewports varierad beroende på om vi vill rendera all till ett fönster eller flera 
            if self.multipleWindows:
                self.leftViewport = self.application.leftWindow.addViewport(self.leftCamera);
                self.rightViewport = self.application.rightWindow.addViewport(self.rightCamera);
            else:
                inv3 = 1.0/3.0;
                self.leftViewport = self.application.mainWindow.addViewport(self.leftCamera, 1, 0, inv3, inv3, inv3);
                self.rightViewport = self.application.mainWindow.addViewport(self.rightCamera, 2, 2*inv3, inv3, inv3, inv3);
                
            self.leftViewport.setBackgroundColour(ogre.ColourValue(0.2,0.2,0.2)); # Mörkgrå bakgrund                
            self.rightViewport.setBackgroundColour(ogre.ColourValue(0.2,0.2,0.2)); # Mörkgrå bakgrund
            self.leftCamera.nearClipDistance = 5;
            self.rightCamera.nearClipDistance = 5;


    def update(self, pos, orientation, acceleration, velocity):
        if(self.rigidBody != None):
            #self.rigidBody.applyForce(physics.toBtVector3(acceleration), physics.toBtVector3(pos));
            self.rigidBody.proceedToTransform(bullet.btTransform(physics.toBtQuaternion(ogre.Quaternion(0, (0, 1, 0))), physics.toBtVector3(pos)));
            self.rigidBody.setAngularVelocity(bullet.btVector3(0,0,0));
            self.rigidBody.setLinearVelocity(bullet.btVector3(0,0,0));

            
        self.orientation = orientation;
        acceleration = orientation * acceleration;
        self.velocity = orientation*velocity;

        orientationx = ogre.Quaternion((5.0*(acceleration.z*0.001))*(math.pi/180.0), (1,0,0));
        orientationz = ogre.Quaternion((5.0*(acceleration.x*0.001))*(math.pi/180.0), (0,0,1));        

        orientation = orientation * orientationx * orientationz;
        self.mainCamera.setOrientation(orientation);

            
        self.mainCamera.setPosition(pos);


        if self.multipleCameras:
            sqrPt5 = math.sqrt(0.5);
            
            leftOrientation = orientation * ogre.Quaternion(self.cameraAngle * (math.pi/180.0), (0,1,0));
            self.leftCamera.setOrientation(leftOrientation);
            self.leftCamera.setPosition(pos);
                    
            rightOrientation = orientation * ogre.Quaternion(-self.cameraAngle * (math.pi/180.0), (0,1,0));
            self.rightCamera.setOrientation(rightOrientation);
            self.rightCamera.setPosition(pos);
                    

    def getPosition(self):
        return self.mainCamera.getPosition();

    def getVelocity(self):
        return self.velocity;

    def getOrientation(self):
        return self.orientation;

    
