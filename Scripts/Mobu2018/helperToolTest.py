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

class HelperToolTest:
    
    def __init__(self):
        self.tool = FBCreateUniqueTool('Helper Tool Test')
        self.tool.StartSizeX = 650
        self.tool.StartSizeY = 650
        self.PopulateconfigLayout(self.tool)
        
        ShowTool(self.tool)
        
        # register when this tool is destroyed
        self.tool.OnUnbind.Add(self.OnToolDestroy)
        
    def PopulateconfigLayout(self, mainLayout):
        # Define config region
        x = FBAddRegionParam(10, FBAttachType.kFBAttachLeft, '')
        y = FBAddRegionParam(20, FBAttachType.kFBAttachTop, '')
        w = FBAddRegionParam(-10, FBAttachType.kFBAttachRight, '')
        h = FBAddRegionParam(300, FBAttachType.kFBAttachNone, '')
        mainLayout.AddRegion('Config', 'Config', x, y, w, h)
        
        configLayout = FBVBoxLayout()
        mainLayout.SetControl('Config', configLayout)
        mainLayout.SetBorder('Config', FBBorderStyle.kFBStandardBorder ,True, True,2,2,200,0)
          
        # Model file
        modelFileEditContainer = FBHBoxLayout()

        modelFileEditLabel = FBLabel()
        modelFileEditLabel.Caption ='Model File:'
        modelFileEditContainer.Add(modelFileEditLabel, 180)

        self.modelFileEdit = FBEdit()
        modelFileEditContainer.Add(self.modelFileEdit, 370)

        modelFileOpenButton = FBButton()
        modelFileOpenButton.Look = FBButtonLook.kFBLookColorChange
        modelFileOpenButton.OnClick.Add(self.OpenModelFile)
        modelFileOpenButton.Caption = 'Open'
        modelFileEditContainer.Add(modelFileOpenButton, 50)

        configLayout.Add(modelFileEditContainer, 30)

        # Skeleton definition template:
        skeletonDefinitionTemplateEditContainer = FBHBoxLayout()

        skeletonDefinitionTemplateEditLabel = FBLabel()
        skeletonDefinitionTemplateEditLabel.Caption = 'Skeleton definition template:'
        skeletonDefinitionTemplateEditContainer.Add(skeletonDefinitionTemplateEditLabel, 180)

        self.skeletonDefinitionTemplateEdit = FBEdit()
        skeletonDefinitionTemplateEditContainer.Add(self.skeletonDefinitionTemplateEdit, 370)

        skeletonDefinitionTemplateButton = FBButton()
        skeletonDefinitionTemplateButton.Look = FBButtonLook.kFBLookColorChange
        skeletonDefinitionTemplateButton.OnClick.Add(self.OpenSkeletonDefinitionTemplateFile)
        skeletonDefinitionTemplateButton.Caption = 'Open'
        skeletonDefinitionTemplateEditContainer.Add(skeletonDefinitionTemplateButton, 50)

        configLayout.Add(skeletonDefinitionTemplateEditContainer, 30)

        # T Pose Config
        TPoseConfigEditContainer = FBHBoxLayout()

        TPoseConfigLabel = FBLabel()
        TPoseConfigLabel.Caption = 'T Pose Config:'
        TPoseConfigEditContainer.Add(TPoseConfigLabel, 180)

        self.TPoseConfigEdit = FBEdit()
        TPoseConfigEditContainer.Add(self.TPoseConfigEdit, 370)

        openTPoseConfigButton = FBButton()
        openTPoseConfigButton.Look = FBButtonLook.kFBLookColorChange
        openTPoseConfigButton.OnClick.Add(self.OpenTPoseConfigFilePath)
        openTPoseConfigButton.Caption = 'Open'
        TPoseConfigEditContainer.Add(openTPoseConfigButton, 50)

        configLayout.Add(TPoseConfigEditContainer, 30)

        # Animation repository
        animationRepositoryEditContainer = FBHBoxLayout()

        animationRepositoryEditLabel = FBLabel()
        animationRepositoryEditLabel.Caption = 'Animation repository:'
        animationRepositoryEditContainer.Add(animationRepositoryEditLabel, 180)

        self.animationRepositoryEdit = FBEdit()
        animationRepositoryEditContainer.Add(self.animationRepositoryEdit, 370)

        animationRepositoryOpenButton = FBButton()
        animationRepositoryOpenButton.Look = FBButtonLook.kFBLookColorChange
        animationRepositoryOpenButton.OnClick.Add(self.OpenAimationRepositoryFolder)
        animationRepositoryOpenButton.Caption = 'Open'
        animationRepositoryEditContainer.Add(animationRepositoryOpenButton, 50)

        configLayout.Add(animationRepositoryEditContainer, 30)

       # Output file path
        outputEditContainer = FBHBoxLayout()

        outputEditLabel = FBLabel()
        outputEditLabel.Caption = 'Output:'
        outputEditContainer.Add(outputEditLabel, 180)

        self.outputEdit = FBEdit()
        outputEditContainer.Add(self.outputEdit, 370)

        outputOpenButton = FBButton()
        outputOpenButton.Look = FBButtonLook.kFBLookColorChange
        outputOpenButton.OnClick.Add(self.OpenOutputFolder)
        outputOpenButton.Caption = 'Open'
        outputEditContainer.Add(outputOpenButton, 50)

        configLayout.Add(outputEditContainer, 30)

        self.foundlAnimationFileList = FBList()
        self.foundlAnimationFileList.Style = FBListStyle.kFBVerticalList
        self.foundlAnimationFileList.MultiSelect = False
        self.foundlAnimationFileList.Select = False
        configLayout.Add(self.foundlAnimationFileList, 200)

        # workflow region
        x = FBAddRegionParam(10, FBAttachType.kFBAttachBottom, 'Config')
        y = FBAddRegionParam(20, FBAttachType.kFBAttachBottom, 'Config')
        w = FBAddRegionParam(-10, FBAttachType.kFBAttachRight, '')
        h = FBAddRegionParam(-10, FBAttachType.kFBAttachBottom, '')
        mainLayout.AddRegion('Workflow', 'Workflow', x, y, w, h)

        workflowLayout = FBVBoxLayout()
        mainLayout.SetControl('Workflow', workflowLayout)
        mainLayout.SetBorder('Workflow', FBBorderStyle.kFBStandardBorder ,True, True,2,2,200,0)

        loadModelFileButton = FBButton()
        loadModelFileButton.Look = FBButtonLook.kFBLookColorChange
        loadModelFileButton.OnClick.Add(self.LoadModelFile)
        loadModelFileButton.Caption = 'Load model file'
        workflowLayout.Add(loadModelFileButton, 30)

        defineSkeletonButton = FBButton()
        defineSkeletonButton.Look = FBButtonLook.kFBLookColorChange
        defineSkeletonButton.OnClick.Add(self.DefineSkeleton)
        defineSkeletonButton.Caption = 'Define skeleton'
   
        workflowLayout.Add(defineSkeletonButton, 30)

        setTPoseButton = FBButton()
        setTPoseButton.Look = FBButtonLook.kFBLookColorChange
        setTPoseButton.OnClick.Add(self.SetTPose)
        setTPoseButton.Caption = 'Set T Pose'
        workflowLayout.Add(setTPoseButton, 30)
        
        characterizeButton = FBButton()
        characterizeButton.Look = FBButtonLook.kFBLookColorChange
        characterizeButton.OnClick.Add(self.Characterize)
        characterizeButton.Caption = 'Characterize'
        workflowLayout.Add(characterizeButton, 30)
        
        plotToControlRigButton = FBButton()
        plotToControlRigButton.Look = FBButtonLook.kFBLookColorChange
        plotToControlRigButton.OnClick.Add(self.PlotToControlRig)
        plotToControlRigButton.Caption = 'Plot to control rig'
        workflowLayout.Add(plotToControlRigButton, 30)

        findAnimationButton = FBButton()
        findAnimationButton.Look = FBButtonLook.kFBLookColorChange
        findAnimationButton.OnClick.Add(self.FindAnimationInRepositoryFolder)
        findAnimationButton.Caption = 'Find animation in repository'
        workflowLayout.Add(findAnimationButton, 30)

        loadAnimationForRetargetingButton = FBButton()
        loadAnimationForRetargetingButton.Look = FBButtonLook.kFBLookColorChange
        loadAnimationForRetargetingButton.OnClick.Add(self.LoadAnimationForRetargeting)
        loadAnimationForRetargetingButton.Caption = 'Load animation for retargeting'
        workflowLayout.Add(loadAnimationForRetargetingButton, 30)

        executeTestButton = FBButton()
        executeTestButton.Look = FBButtonLook.kFBLookColorChange
        executeTestButton.OnClick.Add(self.ExecuteTest)
        executeTestButton.Caption = 'Workflow Test'
        workflowLayout.Add(executeTestButton, 30)
        
    def LoadConfigHistory(self):
        self.modelFileEdit.Text = ''
        self.skeletonDefinitionTemplateEdit.Text = ''
        self.TPoseConfigEdit.Text = ''
        self.animationRepositoryEdit.Text = ''
        self.outputEdit.Text = ''
        
    def OpenModelFile(self, contorl, event):
        # Create the popup and set necessary initial values.
        filePopup = pyfbsdk.FBFilePopup()
        filePopup.Caption = 'Select your original animation file'
        filePopup.Style = pyfbsdk.FBFilePopupStyle.kFBFilePopupOpen
        
        filePopup.Filter = '*.fbx'
        
        # Set the default path(Assuming we are using windows OS).
        filePopup.Path = GetWindowsOSDesktopPath()

        # Get the GUI to show.
        bResult = filePopup.Execute()
        
        # If we select files, show them, otherwise indicate that the selection was canceled.
        if bResult:
            self.modelFileEdit.Text = filePopup.FullFilename

    def OpenSkeletonDefinitionTemplateFile(self, contorl, event):
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
            self.skeletonDefinitionTemplateEdit.Text= filePopup.FullFilename
        
        # Cleanup.
        #del( filePopup, bResult, FBFilePopup, FBFilePopupStyle, FBMessageBox )

    def OpenTPoseConfigFilePath(self, contorl, event):
        # Create the popup and set necessary initial values.
        filePopup = pyfbsdk.FBFilePopup()
        filePopup.Caption = 'Select your T pose config file'
        filePopup.Style = pyfbsdk.FBFilePopupStyle.kFBFilePopupOpen
        
        filePopup.Filter = '*.xml'
        
        # Set the default path(Assuming we are using windows OS).
        filePopup.Path = GetWindowsOSDesktopPath()

        # Get the GUI to show.
        bResult = filePopup.Execute()
        
        # If we select files, show them, otherwise indicate that the selection was canceled.
        if bResult:
            self.TPoseConfigEdit.Text= filePopup.FullFilename
        
        # Cleanup.
        #del( filePopup, bResult, FBFilePopup, FBFilePopupStyle, FBMessageBox )

    def OpenAimationRepositoryFolder(self, contorl, event):
        # Create the popup and set necessary initial values.
        folderPopup = pyfbsdk.FBFolderPopup()
        folderPopup.Caption = 'Select your animation repository folder'

        # Set the default path. Good for a PC only... will have to be different for Mac.
        folderPopup.Path = GetWindowsOSDesktopPath()

        # Get the GUI to show.
        result = folderPopup.Execute()

        # If we select a folder, show its name, otherwise indicate that the selection was canceled.
        if result:
            self.animationRepositoryEdit.Text = folderPopup.Path

    def OpenOutputFolder(self, contorl, event):
        # Create the popup and set necessary initial values.
        folderPopup = pyfbsdk.FBFolderPopup()
        folderPopup.Caption = 'Select your output folder'

        # Set the default path. Good for a PC only... will have to be different for Mac.
        folderPopup.Path = GetWindowsOSDesktopPath()

        # Get the GUI to show.
        result = folderPopup.Execute()

        # If we select a folder, show its name, otherwise indicate that the selection was canceled.
        if result:
            self.outputEdit.Text = folderPopup.Path

    def LoadModelFile(self, control, event):   
        targetFilepath = self.modelFileEdit.Text
        if targetFilepath == '':
            FBMessageBox( 'Config','No model file path.', 'OK', None, None )
            return
        
        app = FBApplication()
        app.FileNew()
        loadOption = FBFbxOptions(True)
        app.FileOpen(targetFilepath, True, loadOption)

    def DefineSkeleton(self, control, event):
        skeletonDefinitionTemplateFilepath = self.skeletonDefinitionTemplateEdit.Text
       
        if skeletonDefinitionTemplateFilepath == '':
            FBMessageBox( 'Config', 'No skeleton definition template file path.', 'OK', None, None )
            return

        # todo need validating operation here

        currentCharacter = FBApplication().CurrentCharacter
        
        # If there is no character just create one.
        if currentCharacter == None:     
            currentCharacter = FBCharacter('Character')
            FBApplication().CurrentCharacter = currentCharacter

        tree = ET.parse(skeletonDefinitionTemplateFilepath)
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

    def IsAnimationFileValid(self, animationFileFullFilename):
         # Get target mesh file name.
        targetMeshFullFilename = self.modelFileEdit.Text
        targetMeshBasename = os.path.basename(targetMeshFullFilename)
        targetMeshName,_ = os.path.splitext(targetMeshBasename)

        baseName = os.path.basename(animationFileFullFilename)
        fileNameWithoutExtention,_ = os.path.splitext(baseName)

        parttern = targetMeshName + r'_Ani_\w+'
        match = re.search(parttern, fileNameWithoutExtention ) 
        result = not match == None

        return  result
    
    def FindAnimationInRepositoryFolder(self, control, event):
        self.foundlAnimationFileList.Items.removeAll()
       
        animationRepositoryFolder = self.animationRepositoryEdit.Text
        bValidFolderPath = os.path.isdir(animationRepositoryFolder)
        if not bValidFolderPath:
            FBMessageBox( 'Config','Invalid animation repository folder.', 'OK', None, None )
            return
            
        foundFbxFiles = glob.glob(animationRepositoryFolder +'/*.fbx')
        for f in foundFbxFiles:
            if self.IsAnimationFileValid(f):
                self.foundlAnimationFileList.Items.append(f)
        
        # todo alert if there is not animation file found.
        if self.foundlAnimationFileList.Items.len == 0:
            print('No animation found')
            return

    # Set Skeleton T pose by config file. 
    def SetTPose(self, control, event): 
        configFilepath = self.TPoseConfigEdit.Text

        if configFilepath == '':
            FBMessageBox( 'Config', 'No T pose config file path.', 'OK', None, None )
            return

        # todo need validating operation here

        tree = ET.parse(configFilepath)
        root = tree.getroot()
        for child in root:
            targetBoneName = child.attrib['BoneName']
            newRotationVectorX = float(child.attrib['rotationVectorX'])
            newRotationVectorY = float(child.attrib['rotationVectorY'])
            newRotationVectorZ = float(child.attrib['rotationVectorZ'])
           
            targetBoneModel = FBFindModelByLabelName(targetBoneName)
            newRotationVector = FBVector3d(newRotationVectorX, newRotationVectorY, newRotationVectorZ)
            targetBoneModel.SetVector(newRotationVector, FBModelTransformationType.kModelRotation) 
       
    def Characterize(self, control, event):
        currentCharacter = FBApplication().CurrentCharacter
        
        if currentCharacter == None:
            FBMessageBox( 'Config', 'No character defined', 'OK', None, None )
            return 

        # Here True means characterizing as biped creature.
        currentCharacter.SetCharacterizeOn(True)
        FBSystem().Scene.Evaluate()
        
    def PlotToControlRig(self, control, event):
        currentCharacter = FBApplication().CurrentCharacter
        
        if currentCharacter == None:
            FBMessageBox( 'Config', 'No character defined', 'OK', None, None )
            return 

        # Disable and delete control rig
        currentCharacter.ActiveInput = False
        controlRig = currentCharacter.GetCurrentControlSet()
        
        # If there is no control rig, just create a new one. 
        if not controlRig:
            # Create a control rig using Forward and Inverse Kinematics,as specified by the 'True' parameter.
            bCreationResult = currentCharacter.CreateControlRig(True)
            if not bCreationResult:
                print('Faild to create a new contorl rig in PlotToControlRig,please check.')

        plotOptions = FBPlotOptions()
        plotOptions.ConstantKeyReducerKeepOneKey = False
        plotOptions.PlotAllTakes = True 
        plotOptions.PlotOnFrame = True
        plotOptions.PlotPeriod = FBTime( 0, 0, 0, 1 )
        plotOptions.PlotTranslationOnRootOnly = False
        plotOptions.PreciseTimeDiscontinuities = False
        plotOptions.RotationFilterToApply = FBRotationFilter.kFBRotationFilterUnroll
        plotOptions.UseConstantKeyReducer = False
        currentCharacter.PlotAnimation (FBCharacterPlotWhere.kFBCharacterPlotOnControlRig,plotOptions )
        
        
    def LoadAnimationForRetargeting(self, control, event):
        fbxOptions = FBFbxOptions( True )
        fbxOptions.TransferMethod = FBCharacterLoadAnimationMethod.kFBCharacterLoadRetarget
        plotOptions = FBPlotOptions()
        animFile = 'F:\DesktopBak\Test\Animation_Scripts_and_Files\Assets\mia_fkik_runstopturn.fbx'
        currentCharacter = FBApplication().CurrentCharacter
        FBApplication().LoadAnimationOnCharacter( animFile, currentCharacter, fbxOptions, plotOptions )


    def ExecuteTest(self, control, event): 

        # Firstly, clear scene and open target mesh file.

        # Define from skeleton template 

        # Characterize 

        # Plot to Control rig

        # Specify animation file

        # Load animation

        self.FindAnimationInRepositoryFolder()       
            
    def OnToolDestroy(self, control, event):
        FBSystem().Scene.OnChange.Remove(SceneChanged)
        
HelperToolTest()
    
        