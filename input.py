# -*- coding: cp1252 -*-
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

class Input(OIS.KeyListener):

    velocity_x = 0;
    velocity_z = 0;
    
    # Kontruktor
    #   app     : Objekt för vår huvudapplikation
    #   window  : Objekt för vårat fönster
    def __init__(self, app, window, camera):
        OIS.KeyListener.__init__(self);
        self.app = app;
        self.window = window;
        self.camera = camera;

    def __del__(self):
        self.shutdown();    

    def init(self):
        # Skapa och initialisera OIS, som är vårat bibliotek för indata från
        #   saker som tagentbord och mus.
        hWnd = self.window.getCustomAttributeInt("WINDOW"); # Handle för vårat fönster
        self.inputSystem = OIS.createPythonInputSystem([("WINDOW",str(hWnd))]);
        # Skapa objekt för input från tagentbord
        self.keyboard = self.inputSystem.createInputObjectKeyboard(OIS.OISKeyboard,True);
        # Lägg detta objekt för callbacks 
        self.keyboard.setEventCallback(self);

    def shutdown(self):
        # Städa upp allt vi skapat med OIS
        if(self.keyboard):
            self.inputSystem.destroyInputObjectKeyboard(self.keyboard);
        OIS.InputManager.destroyInputSystem(self.inputSystem);
        self.inputSystem = 0;

    # Denna anropas från vårat applikations-objekt en gång varje frame så att vi får
    # en chans att göra saker som att läsa indata eller flytta kameran
    #   evt     : FrameEvent, samma data som kommer i Ogre::FrameListener::frameStarted
    def frame(self, evt):
        # Läs in input-data
        if(self.keyboard):
            self.keyboard.capture();
        # Uppdatera kamerans position
        pos = self.camera.getPosition();
        # Multiplicera med timeSinceLastFrame så vi får en jämn unit/s
        pos += self.camera.getRight() * (self.velocity_x * evt.timeSinceLastFrame);
        pos += self.camera.getDirection() * (self.velocity_z * evt.timeSinceLastFrame);
        self.camera.setPosition(pos);
        # Uppdatera så att kameran sen alltid kollar i mitten
        self.camera.lookAt(0,0,0);
    
        
    def keyPressed(self, evt):
        # Avsluta ifall escape trycks ned
        if evt.key == OIS.KC_ESCAPE:
            self.app.stop();
        if evt.key == OIS.KC_W: # Frammåt
            self.velocity_z = 150; 
        if evt.key == OIS.KC_S: # Bakåt
            self.velocity_z = -150;
        if evt.key == OIS.KC_A: # Vänster
            self.velocity_x = -250;
        if evt.key == OIS.KC_D: # Höger
            self.velocity_x = 250;
        
        return True
 
    def keyReleased(self, evt):
        if evt.key == OIS.KC_W: # Frammåt
            self.velocity_z = 0; 
        if evt.key == OIS.KC_S: # Bakåt
            self.velocity_z = 0;
        if evt.key == OIS.KC_A: # Vänster
            self.velocity_x = 0;
        if evt.key == OIS.KC_D: # Höger
            self.velocity_x = 0;
        return True
    
