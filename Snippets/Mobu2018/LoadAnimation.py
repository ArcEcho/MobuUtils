from pyfbsdk import *

lFbxOptions = FBFbxOptions( True )

lFbxOptions.TransferMethod = FBCharacterLoadAnimationMethod.kFBCharacterLoadRetarget
lPlotOptions = FBPlotOptions()

lAnimFile = 'F:\DesktopBak\Test\Animation_Scripts_and_Files\Assets\mia_fkik_runstopturn.fbx'
lTargetCharacter = FBApplication().CurrentCharacter
FBApplication().LoadAnimationOnCharacter( lAnimFile, lTargetCharacter, lFbxOptions, lPlotOptions )
