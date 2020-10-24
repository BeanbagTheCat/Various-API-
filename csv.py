import pandas as pd
import csv
import os


_defaultPath = os.getcwd()


def setDefaultPath(path):
    global _defaultPath

    _defaultPath = path

def getDefaultPath():
    return _defaultPath


class AbstractCSVHandler:

    def __init__(self, child, pathHandler=None):
        self.pathHandler = pathHandler
        if pathHandler is not None:
            self.setPathHandler(pathHandler)
        self.csvName = child.__class__.__name__ + '.csv'
        self.setData(child)
        self.template = _defaultPath + '\\templates\\' + self.csvName

    def getTemplateHeaders(self):
        try:
            self.csvHeaders = pd.read_csv(self.template).columns.values
            self.isTemplate = True

            return

        except:
            self.isTemplate = False

            return

        finally:

            return

    def setPathHandler(self, handler):
        self.pathHandler = handler

        return

    def setData(self, parent):
        if self.pathHandler is not None:
            self.pathHandler.addToPath(self.csvName)
            self.csvPathName = self.pathHandler.path
        else:
            self.csvPathName = _defaultPath + '\\{}'.format(self.csvName)

        try:
            self.dataFrame()
            self.isData = True

        except:
            self.isData = False

            return

        finally:

            return

    def dataFrame(self):
        self.df = pd.read_csv(self.csvPathName)
        self.df = pd.DataFrame(self.df)

        return self.df


class CSV_Creator:

    def __init__(self, csvClass):
        self.csvClass = csvClass
        self.csvPathName = self.csvClass.csvPathName
        self.template = self.csvClass.template

    def create(self):
        try:
            open(self.csvPathName, 'r')
            print('File Already Exists @ {}'.format(self.csvPathName))

        except:

            with open(self.csvPathName, 'w+') as newCSV, open(self.template, 'r') as temp:
                reader = csv.reader(temp)
                writer = csv.writer(newCSV)
                for row in reader:
                    writer.writerow(row)

        finally:

            return

    def addRow(self, *row):
        try:
            open(self.csvPathName, 'r')

            with open(self.csvPathName, 'a') as csvFile:
                writer = csv.writer(csvFile, lineterminator='\n')
                writer.writerow(row)

        except:
            print('''
            Error Opening File @ {}\n\n
            Please Ensure The File Exists And Is Accessible
            '''.format(self.csvPathName))
            
            return
        
        finally:
            
            return

    def updateRow(self):

        pass


class PathHandler:

    def __init__(self):
        self.setDefaultPath(_defaultPath)
        self.__pathDirectories = []
        self.__subDirectories = []
        self.__savedPaths = []
        self.__savedSubPaths = []
        self.__constructPath()

    class __Carpenter:

        def __init__(self, model, pathHandler):
            self.model = model
            self.pathHandler = pathHandler
            self.__treePaths = []
            self.__treeConstructor()

        def __iter__(self):
            self.i = 0

            return self

        def __next__(self):

            if self.i == len(self.__treePaths):
                raise StopIteration

            else:
                cI = self.i
                self.i = self.i + 1
                return self.__treePaths[cI]

        def __branchConstructor(self, branches):
            for branch in branches:
                self.pathHandler.addToPath(branch)
                self.__saveTreePath()
                self.pathHandler.removeFromPath(branch)

        def __saveTreePath(self):
            self.__treePaths.append(self.pathHandler.path)

        def __subRootConstructor(self, subRoot):
            root = subRoot.getRoot()
            self.pathHandler.addToPath(root)

            sB = subRoot.getBranches()
            if len(sB) != 0:
                self.__branchConstructor(sB)

            sR = subRoot.getSubRoots()
            if len(sR) != 0:
                for sub in sR:
                    self.__subRootConstructor(sub)

            self.pathHandler.removeFromPath(root)

        def __treeConstructor(self):
            mainRoots = self.model.getMainRoots()

            for mR in mainRoots:

                root = mR.getRoot()

                self.pathHandler.addToPath(root)

                tB = mR.getBranches()
                if len(tB) != 0:
                    self.__branchConstructor(tB)

                tR = mR.getTopRoots()
                if len(tR) != 0:
                    for sub in tR:
                        self.__subRootConstructor(sub)

                self.pathHandler.removeFromPath(root)

            return

        def getTreePaths(self):

            return self.__treePaths

    def clearPath(self):
        self.__pathDirectories.clear()

        return

    def setSubPaths(self, *subDirectories):
        pass


    def savePath(self):
        self.__savedPaths.append(self.path)

        return


    def setDefaultPath(self, defaultPath):
        self.defaultPath = defaultPath

        return


    def getDefaultPath(self):
        
        return self.defaultPath


    def __addToPathDir(self, directory):
        self.__pathDirectories.append(directory)

        return

    def __removeFromPathDir(self, directory):
        if directory in self.__pathDirectories:
            ind =  self.__pathDirectories.index(directory)
            self.__pathDirectories.pop(ind)

            self.__constructPath()

            return

        return

    def __constructPath(self):
        self.path = self.defaultPath + '\\' + '\\'.join(self.__pathDirectories)

        return

    def __constructSubPaths(self):
        subPaths = []
        if len(self.__subDirectories) != 0:
            for subPath in self.__subDirectories:
                self.__addToPathDir(subPath)
                self.__constructPath()
                subPaths.append(self.path)
                self.__removeFromPathDir(subPath)

        return subPaths

    def getSavedPaths(self):
        savedPaths = [x for x in self.__savedPaths]

        return savedPaths

    def getSubPaths(self):
        paths = self.__constructSubPaths()

        return paths

    def getPath(self):
        
        return self.path

    def addToPath(self, *additions):
        for directory in additions:
            self.__addToPathDir(directory)

        self.__constructPath()

        return

    def removeFromPath(self, directory):
        self.__removeFromPathDir(directory)

        return

    def __checkDir(self, path):
        self.isDir = os.path.isdir(path)

        return self.isDir

    def __createDir(self, path):
        if not self.__checkDir(path):
            os.makedirs(path)

            return
        return

    def makePath(self):
        self.__createDir(self.path)

        return

    def makeSubPaths(self):
        for subPath in self.__constructSubPaths():
            self.__createDir(subPath)

        return

    def __getCarpenter(self, model):
        carpenter = self.__Carpenter(model, self)

        return carpenter

    def getTreePaths(self, model):
        carpenter = self.__getCarpenter(model)

        return carpenter.getTreePaths()

    def makeTreePaths(self, model):
        carpenter = self.__getCarpenter(model)

        for path in carpenter:
            self.__createDir(path)


class TreeModel:

    def __init__(self):
        self.__mainRoots = []

    class MainRoot:

        def __init__(self, root, branches):
            self.__root  = root
            self.__branches = []
            self.__topLevelRoots = []
            self.__subRootIndex = []
            self.setBranches(branches)

        def setBranches(self, branches):
            [self.__branches.append(branch) for branch in branches]

        def getRoot(self):

            return self.__root

        def addSubRoot(self, subRoot, parent=None, parents=None):
            sR = subRoot
            self.__subRootIndex.append(sR)

            if parent is None and parents is None:
                self.__topLevelRoots.append(sR)

            else:
                 if parent is not None:
                     parent.getSubRoots().append(sR)
                     sR.setParent(parent)

                 if parents is not None:
                     [p.getSubRoots().append(sR) for p in parents]
                     sR.setParents(parents)

            return

        def getTopRoots(self):

            return self.__topLevelRoots

        def getSubRootIndex(self):

            return self.__subRootIndex

        def getBranches(self):

            return self.__branches

    class SubRoot:

        def __init__(self, subRoot, *branches):
            self.__root = subRoot
            self.__branches = []
            self.__subRoots = []
            self.__parents = []
            if len(branches) != 0:
                [self.__branches.append(branch) for branch in branches]

        def setParent(self, parent):
            self.__parents.append(parent)

        def setParents(self, *parents):
            [self.__parents.append(parent) for parent in parents]

        def getSubRoots(self):

            return self.__subRoots

        def getBranches(self):

            return self.__branches

        def getRoot(self):

            return self.__root

        def getParents(self):

            return self.__parents

        @classmethod
        def __new(cls, root, branches):
            newInst = cls(root)
            newInst.setBranchList(branches)

            return newInst

        def copy(self):
            root = self.__root
            branches = self.__branches
            newCopy = self.__new(root, branches)

            return newCopy

        def setBranchList(self, branches):
            [self.__branches.append(branch) for branch in branches]

    def addMainRoot(self, root, *branches):
        mRoot = self.MainRoot(root, branches)
        self.__mainRoots.append(mRoot)

        return mRoot

    def getMainRoots(self):

        return self.__mainRoots

