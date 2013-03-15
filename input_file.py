# -*- coding: cp1252 -*-
import math
import camera

import ogre.renderer.OGRE as ogre
from openpyxl.reader.excel import load_workbook


class FileInput:

    # Total tid som g�tt, anv�nds f�r att best�mma vilket timestep som ska anv�ndas
    total_time = 0;


    num_timesteps = 1001;
    timestep = 0.01;

    # Lista f�r inl�sta positioner, positionerna representeras av en ogre.Vector3 d�r Y-axeln pekar upp�t.
    positions = [];
    # Lista �ver vinklarna i radianer och i formen (rX, rY, rZ)
    angles = [];

    def __init__(self, config, window, camera):
        self.config = config;
        self.window = window;
        self.camera = camera;

    # Anropas n�r applikationen startas
    def init(self):
        inputFile = "";
        if(self.config.has_option("input", "input_file")):
            inputFile = self.config.get("input", "input_file");
        else:
            return;

        # Ladda in data fr�n excel-fil
        wb = load_workbook('assets/indata.xlsx');
        ws = wb.get_active_sheet();
        for row in ws.range('C3:H'+str(self.num_timesteps+2)): 
            self.positions.append(ogre.Vector3(row[0].value, row[2].value, row[1].value));
            self.angles.append((math.radians(row[4].value)-(math.pi/2), math.pi - math.radians(row[3].value), math.radians(row[5].value)));



    # Anropas n�r applikationen avslutas
    #def shutdown(self):

    
    # Denna anropas fr�n v�rat applikations-objekt en g�ng varje frame s� att vi f�r
    # en chans att g�ra saker som att l�sa indata eller flytta kameran
    #   evt     : FrameEvent, samma data som kommer i Ogre::FrameListener::frameStarted
    def frame(self, evt):
        self.total_time += evt.timeSinceLastFrame;

        # Ifall tiden har g�tt utanf�r v�ran data s� startar vi bara om fr�n t=0 igen
        if(self.total_time > ((self.num_timesteps-1) * self.timestep)):
            self.total_time = 0;

        # R�kna ut n�rmaste timestep
        index = int(round(self.total_time/self.timestep));

        # H�mta ut datan f�r just det timesteppet
        pos = self.positions[index];
        angle = self.angles[index];

        orientationx = ogre.Quaternion(angle[0], (1,0,0));
        orientationy = ogre.Quaternion(angle[1], (0,1,0));
        orientationz = ogre.Quaternion(angle[2], (0,0,1));
        orientation = orientationx * orientationy * orientationz;

        self.camera.update(pos, orientation, ogre.Vector3(0,0,0), ogre.Vector3(0,0,0));
