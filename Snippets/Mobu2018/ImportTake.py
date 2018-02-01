from pyfbsdk import *
from pyfbsdk_additions import *
import glob
import os.path
import os

# Three seems to be three ways to import/merge takes into scene:
# + Importing motion file
# + Loadinf animation on character
# + Merging from file
# Indeed they may have the same results. But there is still something unlear with the Mobu python api,
# For example, if the imported take has no model file, it will make the original take's model invisble
# and the model will be rotated at about 90 degrees of x-axis.
# I finally choose importing motion file. But we shoud preprocess the files which provide the takes correspondingly. 
#
# Before we import take from other file, we should make sure these prerequisites:
# + All files should the same character hierarchy, but they needn't to be characterized.
# + Each take should have a global unique name.
# + Specify the model file at first.


# Indeed this is the same as merging
# def ImportTakesFromFile(filepath):
#     options = FBFbxOptions(True, filepath)     

#     # Discard all elements, we only need animations
#     options.SetAll(FBElementAction.kFBElementActionDiscard, True)

#     takeCount = options.GetTakeCount()
#     # for takeIndex in range(takeCount):
#     #     takeName = options.GetTakeName(takeIndex)

#     options.ResetDOF = True
#     FBApplication().FileImport( filepath , True, False)

# We must characterize the target file rightly.
# It is very complex procedure. So I don't use this
# def LoadAnimationOnCharacter():

# 
def ImportTakesFromFile(filepath):
    # Attention: we can only import just one file each time, event though we can set multiple files here.
    # Thus caused by we cannot figure out which file is the take from in python script.
    targetMotionFileList = FBStringList()
    targetMotionFileList.Add(filepath)

    # Config motion file import options as we set in the options window.
    motionFileOptions = FBMotionFileOptions(targetMotionFileList)
    
    # Attention: this property's true meaning is against its literal. It is weird.
    motionFileOptions.CreateInsteadOfMerge = True                  # Use merge method here, because we just animtion data from the motion files.
    motionFileOptions.IgnoreModelType = False
    motionFileOptions.CreateUnmatchedModels = True
    motionFileOptions.ImportScaling = True
    motionFileOptions.ImportDOF = False

    # motionFileOptions. ModelSelection = FBModelSelection.kFBAllModels
    motionFileOptions.TakeStartEnd = FBTakeSpanOnLoad.kFBFrameAnimation

    bImportSuccessfully = FBApplication().FileImportWithOptions(motionFileOptions)

    return bImportSuccessfully
   
#motionFile1 = 'F:\DesktopBak\BladeAndSword\Resources\Models\Mannequin\New folder (2)\SK_Test_Anim_Punching - Copy.fbx'
motionFile = 'F:\DesktopBak\MobuTest\Anim2\TakeRenamed\Crouch_Idle_Rifle_Ironsights.FBX'
ImportMotionFile(motionFile)