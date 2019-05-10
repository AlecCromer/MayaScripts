#random_object_placer.py
#This Maya script is used to take a selected object(s), and randomly duplicate them within a specified X,Y,Z area from a specified number of duplicate objects
#Property of Alec Cromer

import maya.cmds as cmds
import functools
import random as rand

rand.seed(10)

'''Determines if the user selected an item'''
def selection():
    selection = cmds.ls(sl=True)
    if selection:
        UI(selection);
    else:
        cmds.confirmDialog( title='Randomly Duplicate Selected Objects', message='Please select and object to duplicate', button=['Ok'])

selection()

def UI(selection):
    RandomWindow = cmds.window("Randomly Place", t="Randomly Duplicate Selected Objects",w=300,h=150)
    print(selection)
    cmds.columnLayout( adjustableColumn=True )
    cmds.separator(h=15)
    
    '''Number of randomly placed items'''
    randomAmount = 0
    slider = cmds.intSliderGrp(label = "Number of Duplicated Objects", min = 0, max = 100, field = True)
    sliderXMin = cmds.intSliderGrp(label = "X Minimum", min = -20, max = 20, field = True, value = -10)
    sliderXMax = cmds.intSliderGrp(label = "X Maximum", min = -20, max = 20, field = True, value = 10)
    sliderYMin = cmds.intSliderGrp(label = "Y Minimum", min = -20, max = 20, field = True, value = -10)
    sliderYMax = cmds.intSliderGrp(label = "Y Maximum", min = -20, max = 20, field = True, value = 10)
    sliderZMin = cmds.intSliderGrp(label = "Z Minimum", min = -20, max = 20, field = True, value = -10)
    sliderZMax = cmds.intSliderGrp(label = "Z Maximum", min = -20, max = 20, field = True, value = 10)
    cmds.separator(h=15)

    def generateItems(*pArgs):
        
        '''Saves the XYZ boundary, and number of objects from the sliders'''
        randomAmount = cmds.intSliderGrp(slider, q=True, value = True)
        xMin = cmds.intSliderGrp(sliderXMin, q=True, value = True)
        xMax = cmds.intSliderGrp(sliderXMax, q=True, value = True)
        yMin = cmds.intSliderGrp(sliderYMin, q=True, value = True)
        yMax = cmds.intSliderGrp(sliderYMax, q=True, value = True)
        zMin = cmds.intSliderGrp(sliderZMin, q=True, value = True)
        zMax = cmds.intSliderGrp(sliderZMax, q=True, value = True)
        if (xMin > xMax) or (yMin > yMax) or (zMin > zMax):
            cmds.confirmDialog( title='Randomly Duplicate Selected Objects', message='Please make sure your minimums are not greater than your maximums', button=['Ok'])
        else:
            
            '''Complete array of the random locations'''
            completeList=[]
        
            '''The lower and upperbounds for the selected object'''
            lower = 0
            upper = randomAmount
            '''A loop for however many objects are selected'''
            for j in range(len(selection)):
                i = 0
                '''A loop for however many items the user requested to be generated'''
                for i in range(lower, upper):
                    '''A randomly generated XYZ location'''
                    xyz = str(rand.randint(xMin,xMax))+","+str(rand.randint(yMin,yMax))+","+str(rand.randint(zMin,zMax))
                    
                    '''If the location is not found in the complete list, add it, and create the duplicate object'''
                    if xyz not in completeList:
                        object = cmds.duplicate(selection[j-1])
                        list = xyz.split(",")
                        cmds.move(list[0],list[1],list[2], object)
                        completeList.append(xyz)
                        
                    else:
                        '''If the location is already in the complete list, decrement the counter to allow the loop to go forward once more'''
                        i+=-1;
                        
                '''Once the selected item completes, it adds to the upperbound to generate new values'''
                '''adds to the lower bound to ignore the original values'''
                lower+=randomAmount
                upper+=randomAmount
                
                
            '''Debugging, diplays the entire list of coordinates, and number of items'''
            print(completeList)
            print(len(completeList))
            cmds.deleteUI(RandomWindow)
   
    cmds.button( label='Generate', align='center', command=generateItems)

    '''User cancels the script'''
    def cancel(*prgs):
        if cmds.window(RandomWindow, exists=True):
            cmds.deleteUI(RandomWindow)
            

    cmds.button(label='Cancel',align='center', command = cancel)

    cmds.showWindow(RandomWindow)
