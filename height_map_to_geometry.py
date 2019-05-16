#height_map_to_geometry.py
#This Maya script takes in a heightmap file (prefereably already set in the UV) and using the present vertices, creates geometry to match
#Works well for creating planets
#EG: Create a cube, add a new material, set color to an image using a FILE, run the script, change smooth function to 2, set the FILE name of the maaterial ('file#' default)
#Features a slider to smooth an object if more detail is required
#Features 3 different strength values to determine how much the heigh map affects the geometry
#Property of Alec Cromer

import maya.cmds as cmds
import math
from pymel import *
import pymel.core as pm
import maya.mel as mel

'''Determines if the user selected an item'''
def selection():
    '''The selected object'''
    selection = cmds.ls(sl=True)
    print(selection)
    if selection:
        UI(selection);
    else:
        cmds.confirmDialog( title='Height Map Transfer', message='Please select an object or sphere to transfer the height map to', button=['Ok'])

selection()

'''Creates the UI for the script'''
def UI(selection):
    HeightWindow = cmds.window("Randomly Place", t="Height Map Adjuster",w=300,h=150)
    cmds.columnLayout( adjustableColumn=True )
    cmds.text(label = 'Please be careful')
    cmds.separator(h=15)
    cmds.text(label = 'Too high subdivisions or smooths can SEVERELY slow down your computer')
    cmds.separator(h=15)
    cmds.text(label = 'Recommended to keep below 3')
    cmds.separator(h=15)
    smoothSlider = cmds.intSliderGrp(label = "Smooth (Default 0)", min = 0, max = 5, value=0, field = True)
    cmds.separator(h=15)
    strengthSlider = cmds.intSliderGrp(label = "Strength (Default 1)", min = 0, max = 2, value=1, field = True)
    cmds.separator(h=15)
    cmds.text(label='Name of the FILE for the material') 
    fileName = cmds.textField()
    cmds.separator(h=15)
    cmds.text(label = 'Reshaping WILL delete the history of the object to improve performance')
    cmds.separator(h=15)
    
    '''Reshapes the mesh'''
    def reshapeD(*pArgs):
        name =cmds.textField(fileName, q=True, text=True)
        if len(name)>0:
            try:

                '''The returned amount for smoothing and strength modifier'''
                smooth = cmds.intSliderGrp(smoothSlider, q=True, value = True)
                strength = cmds.intSliderGrp(strengthSlider, q=True, value = True)+1
                if (smooth > 0):
                    cmds.polySmooth(selection, dv=smooth+1)
                if (strength == 0):
                    strength = .5
                    
                '''The number of vertices in the selected object'''
                numOfVertex = cmds.polyEvaluate( v=True)
                print('The number of vertices for '+str(selection[0])+ ' is '+str(numOfVertex))
                cmds.delete(ch = True)
        
                '''For each vertex'''
                for i in range(numOfVertex):
            
                
                    '''defines the vertex'''
                    vertex = cmds.ls(str(selection[0])+'.vtx['+str(i)+']', fl=1)
                    print('Current vertex: '+ str(vertex))
             
                    '''The location/coordinates of the vertex'''
                    vertexLocation = cmds.pointPosition( vertex )
                    x = vertexLocation[0]
                    y = vertexLocation[1]
                    z = vertexLocation[2]
                    #print('X: '+ str(x))
                    #print('Y: '+ str(y))
                    #print('Z: '+ str(z))
            
                
                    '''The UV value of the specific vertex'''
                    UVValues = cmds.polyEditUV(cmds.polyListComponentConversion(vertex, toUV=True)[0], query=True )
                    #print('The UV location ' + str(UVValues))
                
                    '''Color for the height map of the found vertex'''
                    color = 0
                    color = cmds.colorAtPoint( name,u=UVValues[0],v=UVValues[1] )
                    #print('color: '+str(color[0]))
                    #print(x+color[0])
                    #print(y+color[0])
                    #print(z+color[0])
                
                    '''Adjusts the location of the vertex based on the heighmap color 0-1'''
                    cmds.polyMoveVertex(vertex,translate=(x+(x*color[0]*strength),y+(y*color[0]*strength),z+(z*color[0]*strength)))
                    #print('.........')
                    
                '''Deletes the history and deletes the UI menu'''
                cmds.delete(ch = True)
                cmds.deleteUI(HeightWindow)

            except:
                cmds.deleteUI(HeightWindow)
                cmds.confirmDialog( title='Incorrect File Name', message='The file name for the material is incorrect', button=['Ok'])

    '''The 'Reshape' button'''
    cmds.button( label='Reshape', align='center', command=reshapeD)
    
    '''User cancels the script'''
    def cancel(*prgs):
        if cmds.window(HeightWindow, exists=True):
            cmds.deleteUI(HeightWindow)
    
    '''Cancel button'''
    cmds.button(label='Cancel',align='center', command = cancel)
    
    cmds.showWindow(HeightWindow)