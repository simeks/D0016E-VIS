import ogre.renderer.OGRE as ogre
from ogre.renderer.ogresdksample import Sample
from ogre.renderer.ogresdksample import SampleContext

import math
class Sample_Smoke (Sample): 
    def __init__ (self):
        Sample.__init__ ( self )
        print dir ()
        print dir ( self )
        mInfo = self.getInfo ()
        mInfo["Title"] = "Smoke"
        mInfo["Description"] = "Demonstrates depth-sorting of particles in particle systems."
        mInfo["Thumbnail"] = "thumb_smoke.png"
        mInfo["Category"] = "Effects"
        mInfo["Help"] = "Proof that OGRE is just the hottest thing. Bleh. So there. ^_^"

    def frameRenderingQueued(self, evt):
        # spin the head around and make it float up and down
        self.mPivot.setPosition(0, math.sin(self.mRoot.getTimer().getMilliseconds() / 150.0) * 10, 0)
        self.mPivot.yaw(Radian(-evt.timeSinceLastFrame * 1.5))
        return SdkSample.frameRenderingQueued(evt)
    
    def setupContent( self ):

        print dir ( self )
        self.mSceneMgr = self.getSceneManager()
        self.mSceneMgr.setSkyBox(True, "Examples/EveningSkyBox")

        # dim orange ambient and two bright orange lights to match the skybox
        self.mSceneMgr.setAmbientLight(ogre.ColourValue(0.3, 0.2, 0))
        light = self.mSceneMgr.createLight()
        light.setPosition(2000, 1000, -1000)
        light.setDiffuseColour(1, 0.5, 0)
        light = self.mSceneMgr.createLight()
        light.setPosition(-2000, 1000, 1000)
        light.setDiffuseColour(1, 0.5, 0)

        self.mPivot = self.mSceneMgr.getRootSceneNode().createChildSceneNode()  # create a pivot node

        # create a child node and attach an ogre head and some smoke to it
        headNode = self.mPivot.createChildSceneNode(ogre.Vector3(100, 0, 0))
        headNode.attachObject(self.mSceneMgr.createEntity("Head", "ogrehead.mesh"))
        headNode.attachObject(self.mSceneMgr.createParticleSystem("Smoke", "Examples/Smoke"))

        self.mCamera.setPosition(0, 30, 350)
        
if __name__ == '__main__':
    
    #try:
        context = SampleContext()
        sample = Sample_Smoke()
        context.go( sample )
        #p1 = mp.Process(target=test,args=(q,))
        #p1.start()
        
        
    #except e: # OgreException, e:
    #    print e
        
    