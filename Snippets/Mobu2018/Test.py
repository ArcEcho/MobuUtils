from pyfbsdk import *
from pyfbsdk_additions import *
import glob
import os.path
import os

def MergeTakesFromFile(filepath):
    options = FBFbxOptions(True, filepath)     

    # Discard all elements, we only need animations
    options.SetAll(FBElementAction.kFBElementActionDiscard, True)

    takeCount = options.GetTakeCount()
    # for takeIndex in range(takeCount):
    #     takeName = options.GetTakeName(takeIndex)

    options.ResetDOF = True
    FBApplication().FileImport( filepath , True, False)


def RenameTakeByFile(filepath, outputDirectory):
    FBApplication().FileNew()

    loadOption = FBFbxOptions(True)
    FBApplication().FileOpen(filepath, True, loadOption)
    
    baseName = os.path.basename(filepath)
    fileNameWithoutExtention,_ = os.path.splitext(baseName)
    
    sceneTakes = FBSystem().Scene.Takes
    takeCount = len(sceneTakes)
    for takeIndex in range(takeCount):
        targetTake = sceneTakes[takeIndex]
        takeName = targetTake.Name
        newTakeName = fileNameWithoutExtention + '_' + takeName
        targetTake.Name = newTakeName
    
    outputFilepath = os.path.join(outputDirectory, baseName)
    FBApplication().FileSave(outputFilepath) 

def ExecuteTest(modelFilepath, animFilesFolder):
    
    outputDirectory = os.path.join(animFilesFolder, 'TakeRenamed')
    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)

    # Specify the animation files folder. We will merge takes in all of these files.
    # So make sure all animations use the hierarchy of the T Pose file.
    foundFbxFilepaths = glob.glob(animFilesFolder +'/*.fbx')
    for filepath in foundFbxFilepaths:
        RenameTakeByFile(filepath, outputDirectory)

    # Specify the file which only contains the T Pose Take and open it.
    FBApplication().FileNew()

    loadOption = FBFbxOptions(True)
    FBApplication().FileOpen(modelFilepath, True, loadOption)

    foundFbxFilepaths = glob.glob(outputDirectory + '/*.fbx')
    for filepath in foundFbxFilepaths:
        MergeTakesFromFile(filepath)

modelFilepath = 'F:\DesktopBak\MobuTest\SK_Mannequin.FBX'
animFilesFolder = 'F:\DesktopBak\MobuTest\Anim2'  
ExecuteTest(modelFilepath, animFilesFolder)
