# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import ogre.physics.bullet as bullet

class NodeMotionState(bullet.btMotionState):
    def __init__(self, sceneNode):
        bullet.btMotionState.__init__(self);
        self.sceneNode = sceneNode;


    def getWorldTransform(self, worldTrans):
        pos = self.sceneNode.getPosition();
        rot = self.sceneNode.getOrientation();
        worldTrans.setOrigin(bullet.btVector3(pos.x, pos.y, pos.z));
        worldTrans.setRotation(bullet.btQuaternion(rot.x, rot.y, rot.z, rot.w));

 
    def setWorldTransform(self, worldTrans):
        rot = worldTrans.getRotation();
        self.sceneNode.setOrientation(
            ogre.Quaternion(rot.w(), rot.x(), rot.y(), rot.z()));
        pos = worldTrans.getOrigin();
        self.sceneNode.setPosition(pos.x(), pos.y(), pos.z());


class CameraMotionState(bullet.btMotionState):
    def __init__(self, camera):
        bullet.btMotionState.__init__(self);
        self.camera = camera;

    def getWorldTransform(self, worldTrans):
        pos = self.camera.getPosition();
        rot = self.camera.getOrientation();
        print "Camera pos",pos.x,pos.y,pos.z;
        worldTrans.setOrigin(bullet.btVector3(pos.x, pos.y, pos.z));
        worldTrans.setRotation(bullet.btQuaternion(rot.x, rot.y, rot.z, rot.w));

 
    def setWorldTransform(self, worldTrans):
        rot = worldTrans.getRotation();
        self.camera.setOrientation(
            ogre.Quaternion(rot.w(), rot.x(), rot.y(), rot.z()));
        pos = worldTrans.getOrigin();
        self.camera.setPosition(pos.x(), pos.y(), pos.z());
        print "Camera set pos",pos.x(),pos.y(),pos.z();

        
class PhysicsWorld:
    #def __init__(self, root):
        
    class Body:
        def __init__(self, shape, motionState, constructInfo, rigidBody):
            self.shape = shape;
            self.motionState = motionState;
            self.constructInfo = constructInfo;
            self.rigidBody = rigidBody;
            

    bodies = []

    def init(self, gravity):
        self.collisionConfiguration = bullet.btDefaultCollisionConfiguration()
        self.dispatcher = bullet.btCollisionDispatcher (self.collisionConfiguration)

        
        worldAabbMin = bullet.btVector3(-20000,-1000,-20000)
        worldAabbMax = bullet.btVector3(20000,1000,20000)
        self.broadphase = bullet.btAxisSweep3(worldAabbMin, worldAabbMax);

        self.solver = bullet.btSequentialImpulseConstraintSolver();

        self.world = bullet.btDiscreteDynamicsWorld(self.dispatcher, self.broadphase, self.solver,
                                                    self.collisionConfiguration);
        self.world.getDispatchInfo().m_enableSPU = True
        self.world.setGravity(bullet.btVector3(0,gravity,0));

        self.world.stepSimulation(0);

    # Skapar en representation av marken för fysikmotorn
    def createGround(self, sceneNode):
        groundShape = bullet.btStaticPlaneShape(bullet.btVector3(0,1,0),0);
        # Skapa motion state
        motionState = bullet.btDefaultMotionState(bullet.btTransform(
            bullet.btQuaternion(0,0,0,1), bullet.btVector3(0,-1,0)));
        constructInfo = bullet.btRigidBody.btRigidBodyConstructionInfo(
            0, motionState, groundShape, bullet.btVector3(0,0,0));
        rigidBody = bullet.btRigidBody(constructInfo);

        self.bodies.append(PhysicsWorld.Body(groundShape, motionState, constructInfo, rigidBody));
        self.world.addRigidBody(rigidBody);

    def createSphere(self, sceneNode, radius, mass):
        pos = sceneNode.getPosition();
        rot = sceneNode.getOrientation();
        
        # Skapa motion state
        motionState = NodeMotionState(sceneNode);


        sphereShape = bullet.btSphereShape(radius);
        inertia = bullet.btVector3(0,0,0);
        sphereShape.calculateLocalInertia(mass, inertia);
        
        constructInfo = bullet.btRigidBody.btRigidBodyConstructionInfo(
            mass, motionState, sphereShape, inertia);
        rigidBody = bullet.btRigidBody(constructInfo);

        self.bodies.append(PhysicsWorld.Body(sphereShape, motionState, constructInfo, rigidBody));
        self.world.addRigidBody(rigidBody);
        
    def createCylinder(self, sceneNode, width, height, depth, mass):
        pos = sceneNode.getPosition();
        rot = sceneNode.getOrientation();
        
        # Skapa motion state
        motionState = NodeMotionState(sceneNode);

        shape = bullet.btCylinderShape(bullet.btVector3(width/2.0, height/2.0, depth/2.0));
        inertia = bullet.btVector3(0,0,0);
        shape.calculateLocalInertia(mass, inertia);
        
        constructInfo = bullet.btRigidBody.btRigidBodyConstructionInfo(
            mass, motionState, shape, inertia);
        rigidBody = bullet.btRigidBody(constructInfo);

        self.bodies.append(PhysicsWorld.Body(shape, motionState, constructInfo, rigidBody));
        self.world.addRigidBody(rigidBody);
        
    def createCamera(self, camera, radius, mass):
        pos = camera.getPosition();
        rot = camera.getOrientation();
        
        # Skapa motion state
        motionState = CameraMotionState(camera);

        sphereShape = bullet.btSphereShape(radius);
        inertia = bullet.btVector3(0,0,0);
        sphereShape.calculateLocalInertia(mass, inertia);
        
        constructInfo = bullet.btRigidBody.btRigidBodyConstructionInfo(
            mass, motionState, sphereShape, inertia);
        rigidBody = bullet.btRigidBody(constructInfo);

        self.bodies.append(PhysicsWorld.Body(sphereShape, motionState, constructInfo, rigidBody));
        self.world.addRigidBody(rigidBody);

    def frame(self, evt):
        self.world.stepSimulation(evt.timeSinceLastFrame);
        

