import os

def createFolder(filename):
    try:
        foldername = filename[:filename.rfind("/")]
        if not os.path.isdir(foldername):
            os.makedirs(foldername)
    except:
        print "ERROR: Failed creating folder for '" + filename + "'"


def saveToFile(filename, text):
    """
    """
    try:
        createFolder(filename)
#        if not isAscii(text):
        archiveFile = open(filename, 'w+')
#        else:
#            archiveFile = codecs.open(filename, encoding='utf-8', mode='w+')
        #print "file opened: '" + filename + "'"
    
        archiveFile.write(text)
    
        archiveFile.close()
    except Exception as e:
        print "Error: failed saving to file"
        print type(e)
        print e

def getFileText(filename):
    """
    """
    try:
        archiveFile = open(filename, 'r')
        text = archiveFile.read()
        archiveFile.close()
        
        return text
    except Exception as e:
        print "Error: failed reading file"
        print type(e)
        print e
        return ""

def getFolderNames(folder):
    if not os.path.isdir(folder):
        return []

    res = []
    files = os.listdir(folder)

    for filename in files:
        if os.path.isdir(folder + "/" + filename):
            res.append(filename)

    return res


def getFileNames(folder, level=0, prefix=""):
    if not os.path.isdir(folder) or (level < 0):
        return []
    
    res = []
    files = os.listdir(folder)
    
    if (level == 0):
        for filename in files:
            if os.path.isfile(folder + "/" + filename):
                res.append(prefix + filename)
    else:
        for filename in files:
            if os.path.isdir(folder + "/" + filename):
                res.extend(getFileNames(folder + "/" + filename, level - 1, filename + "/"))

    return sorted(res)

if __name__ == "__main__":
    for filename in getFileNames("/home/ofir/Downloads", level=2):
        print filename

