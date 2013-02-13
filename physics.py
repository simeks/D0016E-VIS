# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import ogre.physics.bullet as bullet

class NodeMotionState(bullet.btMotionState):
    def __init__(self, initialPos, sceneNode):
        bullet.btMotionState.__init__(self);
        self.sceneNode = sceneNode;
        self.pos = initialPos;
        print "getWorldTransform x:",initialPos.getOrigin().x(),"y:",initialPos.getOrigin().y(),"z:",initialPos.getOrigin().z();

    def getWorldTransform(self, worldTrans):
        worldTrans = self.pos;
        print "getWorldTransform x:",worldTrans.getOrigin().x(),"y:",worldTrans.getOrigin().y(),"z:",worldTrans.getOrigin().z();
 
    def setWorldTransform(self, worldTrans):
        rot = worldTrans.getRotation();
        self.sceneNode.setOrientation(
            ogre.Quaternion(rot.w(), rot.x(), rot.y(), rot.z()));
        pos = worldTrans.getOrigin();
        self.sceneNode.setPosition(pos.x(), pos.y(), pos.z());
        print "setWorldTransform x:",pos.x(),"y:",pos.y(),"z:",pos.z();
        
class PhysicsWorld:
    #def __init__(self, root):
        

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
        self.groundShape = bullet.btStaticPlaneShape(bullet.btVector3(0,1,0),1);
        # Skapa motion state
        self.motionState2 = bullet.btDefaultMotionState(bullet.btTransform(
            bullet.btQuaternion(0,0,0,1), bullet.btVector3(0,-1,0)));
        self.constructInfo2 = bullet.btRigidBody.btRigidBodyConstructionInfo(
            0, self.motionState2, self.groundShape, bullet.btVector3(0,0,0));
        self.rigidBody2 = bullet.btRigidBody(self.constructInfo2);

        self.world.addRigidBody(self.rigidBody2);

    def createSphere(self, sceneNode, radius, mass):
        pos = sceneNode.getPosition();
        rot = sceneNode.getOrientation();
        
        # Skapa motion state
        self.motionState = NodeMotionState(bullet.btTransform(
            bullet.btQuaternion(rot.x,rot.y,rot.z,rot.w),
            bullet.btVector3(pos.x,pos.y,pos.z)), sceneNode);

        self.sphereShape = bullet.btSphereShape(radius);
        inertia = bullet.btVector3(0,0,0);
        self.sphereShape.calculateLocalInertia(mass, inertia);
        
        self.constructInfo = bullet.btRigidBody.btRigidBodyConstructionInfo(
            mass, self.motionState, self.sphereShape, inertia);
        self.rigidBody = bullet.btRigidBody(self.constructInfo);

        self.world.addRigidBody(self.rigidBody);
        

    def frame(self, evt):
        self.world.stepSimulation(evt.timeSinceLastFrame);
        

