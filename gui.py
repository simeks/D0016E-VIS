# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import input
import scene
import camera

import math

class GUI:
    def __init__(self):
        self.overlayMgr = ogre.OverlayManager.getSingletonPtr();
        self.overlay = self.overlayMgr.create("gui");
        self.panel = self.overlayMgr.createOverlayElement("Panel", "panel1");
        self.panel.setMetricsMode(ogre.GMM_PIXELS);
        self.panel.setDimensions(400,200);
        self.panel.setPosition(0,0);
        #self.panel.setMaterialName("Floor");
        self.overlay.add2D(self.panel);
        self.overlay.show();

    def addTextBox(self, id, text, x, y, w, h):
        textBox = self.overlayMgr.createOverlayElement("TextArea", id);
        textBox.setMetricsMode(ogre.GMM_PIXELS);
        textBox.setPosition(x,y);
        textBox.setWidth(w);
        textBox.setHeight(h);

        textBox.setParameter("font_name", "BlueHighway");
	textBox.setParameter("char_height", "19");
        textBox.setColour(ogre.ColourValue(0,0,0,1));

        textBox.setCaption(text);
        self.panel.addChild(textBox);
        textBox.show();

    def setText(self, id, text):
        textBox = self.overlayMgr.getOverlayElement(id);
        textBox.setCaption(text);


        
