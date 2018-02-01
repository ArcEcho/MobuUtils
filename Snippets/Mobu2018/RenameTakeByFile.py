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