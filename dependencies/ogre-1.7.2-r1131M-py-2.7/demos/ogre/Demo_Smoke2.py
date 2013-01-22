# This code is in the Public Domain
# -----------------------------------------------------------------------------
# This source file is part of Python-Ogre
# For the latest info, see http://python-ogre.org/
#
# It is likely based on original code from OGRE and/or PyOgre
# For the latest info, see http://www.ogre3d.org/
#
# You may use this sample code for anything you like, it is not covered by the
# LGPL.
# -----------------------------------------------------------------------------
import sys
sys.path.insert(0,'..')
sys.path.append(r"c:\python25\lib\site-packages")
import PythonOgreConfig
import ogre.renderer.OGRE as ogre
import ogre.renderer.ogresdksample as sdksample


class Sample_Smoke(sdksample.SdkSample):
    def __init__( self ):
        sdksample.SdkSample.__init__(self)
       
        self.mInfo["Title"] = "Smoke"
        self.mInfo["Description"] = "Demonstrates depth-sorting of particles in particle systems."
        self.mInfo["Thumbnail"] = "thumb_smoke.png"
        self.mInfo["Category"] = "Unsorted"
        self.mInfo["Help"] = "Proof that OGRE is just the hottest thing. Bleh. So there. ^_^"
    
    def frameRenderingQueued(self, evt):
        # spin the head around and make it float up and down
        #mPivot.setPosition(0, Math::Sin(mRoot.getTimer().getMilliseconds() / 150.0) * 10, 0)
        #mPivot.yaw(Radian(-evt.timeSinceLastFrame * 1.5))
        return SdkSample.frameRenderingQueued(self, evt)
        
    def setupContent( self ):
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
        
    def __del__(self):
        ##del self.particleSystem2
        sf.Application.__del__(self)     
                
if __name__ == '__main__':
    try:
        application = Sample_Smoke()
        print "\n\n", application, "\n\n"
        print dir(application)
        print "\n"
        print dir(sdksample)
        #application.go()
    except ogre.OgreException, e:
        print e
