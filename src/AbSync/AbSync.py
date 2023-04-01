import sys, schedule, time
from .AbSyncModules import FileManager, Logger


class AbSync:
    """AbSync Manager/Scheduler Class


    Attributes:
    ----------------------
    target: str
        path to the target directory

    destination: str
        path to the destination directory

    interval: int
        delay in seconds between synchronizations

    logLocation: str
        path to the logfile directory


    Methods:
    ----------------------
    clean(items)
        remove directories and files from the items list

    copy(items)
        create directories and copy files from the items list

    scheduleSync()
        schedules AbSync.sync() at AbSync.interval seconds

    sync()
        updates structures and performs AbSync.clean() and Absync.copy()

    updateStructures()
        updates target and destination directory structures 
    """

    def __init__(self, target, destination, interval, logLocation):

        print(">>AbSync v1.0")

        # Initialize values
        self.target = target
        self.destination = destination
        self.interval = interval
        self.logLocation = logLocation

        # Set FileManager
        self.fileManager = FileManager()

        logCreated = False

        # Check if logfile directory exists, and create if needed
        if (not self.fileManager.exists(self.logLocation)):
            self.fileManager.createDirectory(self.logLocation)
            logCreated = True

        # Set Logger
        self.logger = Logger.getLogger(self.logLocation)

        if (logCreated):
            self.logger.info("Created Directory: " + str(self.logLocation))

        self.targetStructure = []
        self.destinationStructure = []

        # Check if destination and target directories exists, and create if needed
        if (not self.fileManager.exists(self.destination)):
            self.fileManager.createDirectory(self.destination)
            self.logger.info("Created Directory: " + str(self.destination))

        if (not self.fileManager.exists(self.target)):
            self.fileManager.createDirectory(self.target)
            self.logger.info("Created Directory: " + str(self.target))

        # Log RunInfo
        self.logger.info("Target Folder: " + str(self.target))
        self.logger.info("Destination Folder: " + str(self.destination))
        self.logger.info("Sync Interval: " + str(self.interval))
        self.logger.info("Logs Location: " + str(self.logLocation))

    def scheduleSync(self):

        """Schedule AbSync.sync() at self.interval seconds"""

        schedule.every(self.interval).seconds.do(self.sync)

    def sync(self):

        """AbSync Synchronization Function

        Updates directory structure for self.target and self.destination
        
        Checks for differences and stores them in copyList and removeList
        
        Removes directories and files from removeList

        Creates directories and copies files from copyList
        """

        self.updateStructures()

        copyList = self.fileManager.compare(self.targetStructure, self.destinationStructure)
        removeList = self.fileManager.compare(self.destinationStructure, self.targetStructure)

        if (len(removeList) > 0):
            self.clean(removeList[::-1])

        if (len(copyList) > 0):
            self.copy(copyList)

        self.logger.info("Completed Sync")

    def clean(self, items):

        """Clean-up function

        Removes directories and files from items list
        """

        for currentDirectory, directories, files in items:

            # Create full path to current destination directory
            destinationDirectory = currentDirectory.replace(self.target, self.destination)

            # Remove all directories from the list
            for directory in directories:
                self.fileManager.removeDirectory(directory, destinationDirectory)
                self.logger.info("Removed Directory: " + str(directory) + " From: " + str(destinationDirectory))

            # Remove all files from the list
            for file in files:
                self.fileManager.removeFile(file, destinationDirectory)
                self.logger.info("Removed File: " + str(file) + " From: " + str(destinationDirectory))

    def copy(self, items):

        """Copying function

        Creates directories and copies files from items list
        """

        for currentDirectory, directories, files in items:

            # Create full path to current destination directory
            destinationDirectory = currentDirectory.replace(self.target, self.destination)

            # Create all directories from the list
            for directory in directories:
                self.fileManager.createDirectory(directory, destinationDirectory)
                self.logger.info("Created Directory: " + str(directory) + " In: " + str(destinationDirectory))

            # Copy all files from the list
            for file in files:
                self.fileManager.copy(file, currentDirectory, destinationDirectory)
                self.logger.info("Copied File: " + str(file) + " To: " + str(destinationDirectory))

    def updateStructures(self):

        """Updates target and destination directory structure"""

        self.targetStructure = self.fileManager.update(self.target)
        self.destinationStructure = self.fileManager.update(self.destination)

