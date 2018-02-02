from pyfbsdk import *
from pyfbsdk_additions import *
import xml.etree.ElementTree as ET
import _winreg
from os import walk 
import os.path
import os
import glob
import re

# Utils 
def GetWindowsOSDesktopPath():
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    desktopFilepath = _winreg.QueryValueEx(key, 'Desktop')[0]  
    # Variable 'desktopFilepath' is a string like but not a string.
    return  str(desktopFilepath)

class DefineSkeletonTool:
    
    def __init__(self):
        self.tool = FBCreateUniqueTool('Define Skeleton')
        self.tool.StartSizeX = 450
        self.tool.StartSizeY = 250
        self.PopulateconfigLayout(self.tool)
        
        ShowTool(self.tool)
        
        # register when this tool is destroyed
        self.tool.OnUnbind.Add(self.OnToolDestroy)
        
    def PopulateconfigLayout(self, mainLayout):
        x = FBAddRegionParam(10, FBAttachType.kFBAttachLeft, '')
        y = FBAddRegionParam(20, FBAttachType.kFBAttachTop, '')
        w = FBAddRegionParam(-10, FBAttachType.kFBAttachRight, '')
        h = FBAddRegionParam(300, FBAttachType.kFBAttachNone, '')
        mainLayout.AddRegion('main', 'main', x, y, w, h)
        
        mainLayoutContainer = FBVBoxLayout()
        mainLayout.SetControl('main', mainLayoutContainer)

        # Skeleton definition template:
        skeletonDefinitionEditContainer = FBHBoxLayout()

        skeletonDefinitionEditLabel = FBLabel()
        skeletonDefinitionEditLabel.Caption = 'Skeleton definition template:'
        skeletonDefinitionEditContainer.Add(skeletonDefinitionEditLabel, 180)

        self.skeletonDefinitionEdit = FBEdit()
        skeletonDefinitionEditContainer.Add(self.skeletonDefinitionEdit, 150)

        skeletonDefinitionButton = FBButton()
        skeletonDefinitionButton.Look = FBButtonLook.kFBLookColorChange
        skeletonDefinitionButton.OnClick.Add(self.OpenSkeletonDefinitionFile)
        skeletonDefinitionButton.Caption = 'Open'
        skeletonDefinitionEditContainer.Add(skeletonDefinitionButton, 50)

        mainLayoutContainer.Add(skeletonDefinitionEditContainer, 30)

        defineSkeletonButton = FBButton()
        defineSkeletonButton.Look = FBButtonLook.kFBLookColorChange
        defineSkeletonButton.OnClick.Add(self.DefineSkeleton)
        defineSkeletonButton.Caption = 'Define skeleton'
   
        mainLayoutContainer.Add(defineSkeletonButton, 30)

    def OpenSkeletonDefinitionFile(self, contorl, event):
        # Create the popup and set necessary initial values.
        filePopup = pyfbsdk.FBFilePopup()
        filePopup.Caption = 'Select your skeleton definition template file'
        filePopup.Style = pyfbsdk.FBFilePopupStyle.kFBFilePopupOpen
        
        filePopup.Filter = '*.xml'
        # Set the default path(Assuming we are using windows OS).
        filePopup.Path = GetWindowsOSDesktopPath()

        # Get the GUI to show.
        bResult = filePopup.Execute()
        
        # If we select files, show them, otherwise indicate that the selection was canceled.
        if bResult:
            self.skeletonDefinitionEdit.Text= filePopup.FullFilename
        
        # Cleanup.
        #del( filePopup, bResult, FBFilePopup, FBFilePopupStyle, FBMessageBox )

    def DefineSkeleton(self, control, event):
        skeletonDefinitionFilepath = self.skeletonDefinitionEdit.Text
       
        if skeletonDefinitionFilepath == '':
            FBMessageBox( 'Config', 'No skeleton definition template file path.', 'OK', None, None )
            return

        # todo need validating operation here
        currentCharacter = FBApplication().CurrentCharacter
        
        # If there is no character just create one.
        if currentCharacter == None:     
            currentCharacter = FBCharacter('Character')
            FBApplication().CurrentCharacter = currentCharacter

        tree = ET.parse(skeletonDefinitionFilepath)
        root = tree.getroot()
        
        # todo: no matching operation here now.
        for elem in tree.iter(tag='item'):
            jointName = elem.attrib['value']
            targetLinkSlotName = elem.attrib['key'] + 'Link'
            
            if jointName == '':
                continue

            joint = FBFindModelByLabelName(jointName)
            if joint == None:
                print('Unexpected joint in skeleton definition template: %s' % (jointName))
            else:
                property = currentCharacter.PropertyList.Find(targetLinkSlotName)
                property.removeAll()
                property.append (joint)
               
    def OnToolDestroy(self, control, event):
        FBSystem().Scene.OnChange.Remove(SceneChanged)

DefineSkeletonTool()
    
        