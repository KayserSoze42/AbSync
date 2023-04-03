import schedule, time
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

    compare()
        compares directory structures and updates AbSync.copyList and AbSync.cleanList

    copy(items)
        create directories and copy files from the items list

    scheduleSync()
        schedules AbSync.sync() at AbSync.interval seconds

    sync()
        updates structures and performs AbSync.compare(), AbSync.clean() and AbSync.copy()

    run()
        runs the schedule.run_pending() in a while True loop**

    updateStructures()
        updates target and destination directory structures
    """

    copyList = []
    cleanList = []

    targetStructure: dict = {}
    destinationStructure: dict = {}

    def __init__(self, target: str, destination: str, interval: int, logLocation: str):

        # Initialize values
        self.target = FileManager.absPath(target)
        self.destination = FileManager.absPath(destination)
        self.interval = interval
        self.logLocation = FileManager.absPath(logLocation)

        logCreated = False

        # Check if logfile directory exists, and create if needed
        if (not FileManager.exists(self.logLocation)):
            FileManager.createDirectory(self.logLocation)
            logCreated = True

        # Set Logger
        self.logger = Logger.getLogger(self.logLocation)

        if (logCreated):
            self.logger.info("Created Directory: " + str(self.logLocation))

        # Check if destination and target directories exists, and create if needed
        if (not FileManager.exists(self.destination)):
            FileManager.createDirectory(self.destination)
            self.logger.info("Created Directory: " + str(self.destination))

        if (not FileManager.exists(self.target)):
            FileManager.createDirectory(self.target)
            self.logger.info("Created Directory: " + str(self.target))

        # Log RunInfo
        self.logger.info("Target Folder: " + str(self.target))
        self.logger.info("Destination Folder: " + str(self.destination))
        self.logger.info("Sync Interval: " + str(self.interval))
        self.logger.info("Logs Location: " + str(self.logLocation))

    def clean(self, items: list):

        """Clean-up Method

        Removes directories and files from items list
        """

        # Set log counters
        removedDirs = 0
        removedFiles = 0

        for currentDirectory, directories, files in items:

            # Create full path to current destination directory
            destinationDirectory = currentDirectory.replace(self.target, self.destination)

            # Remove all directories from the list
            for directory in directories:
                FileManager.removeDirectory(directory, destinationDirectory)
                self.logger.info("Removed Directory: " + str(directory) + " From: " + str(destinationDirectory))
                removedDirs+=1

            # Remove all files from the list
            for file in files:
                FileManager.removeFile(file, destinationDirectory)
                self.logger.info("Removed File: " + str(file) + " From: " + str(destinationDirectory))
                removedFiles+=1

        self.logger.info("Removed " + str(removedDirs) + " Directory/ies, And " + str(removedFiles) + " File(s)")

    def compare(self):

        """Comparison Method

        Compares target and destination structure for differences

        Directories to be created and files to be copied are stored in AbSync.copyList
        Directories and files to be removed are stored in AbSync.cleanList
        """

        # Get a list of paths from target and destination directory structures
        targetPaths = list(self.targetStructure.keys())
        destinationPaths = list(self.destinationStructure.keys())

        # Re/Set initial values
        self.copyList = []
        self.cleanList = []

        # For paths in target directories
        for path in targetPaths:

            # Set initial values
            copyDirs = []
            copyFiles = []

            # Create destination path from current path
            currentDestinationPath = path.replace(self.target, self.destination)

            # If path exists in destination directory
            if currentDestinationPath in destinationPaths:

                # Optimization attempt
                sameContent = True

                # For all directories and files in current path
                # Check if directory exists
                for dir in self.targetStructure[path][0]:

                    # If directory is present at both target and destination, continue
                    if dir in self.destinationStructure[currentDestinationPath][0]:
                        continue

                    # Else, mark it for creation
                    else:
                        sameContent = False
                        copyDirs.append(dir)

                # Check if file exists
                for file in self.targetStructure[path][1]:

                    # Create target and destination full paths
                    fileTarget = FileManager.join(path, file)
                    fileDestination = FileManager.join(currentDestinationPath, file)

                    # If file is present at both target and destination, compare them
                    if file in self.destinationStructure[currentDestinationPath][1]:

                        # If both files compare to same, continue
                        if FileManager.compareFiles(fileTarget, fileDestination):
                            continue

                        # Else, mark it for copying
                        else:
                            sameContent = False
                            copyFiles.append(file)

                    # If file is not present, add it to the list
                    else:

                        copyFiles.append(file)

                # Optimization attempt
                if sameContent and self.targetStructure[path] == self.destinationStructure[currentDestinationPath]:
                    destinationPaths.pop(destinationPaths.index(currentDestinationPath))

            # Else, if target path is not present at destination
            else:

                # Add path and all content to the copy list
                self.copyList.append([path, self.targetStructure[path][0], self.targetStructure[path][1]])
                continue

            # Add directories and files from copyDirs and copyFiles to copyList
            self.copyList.append([path, copyDirs, copyFiles])

        # For paths in destination directory
        for path in destinationPaths:

            # Set initial values
            cleanDirs = []
            cleanFiles = []

            # Create destination path from current path
            currentTargetPath = path.replace(self.destination, self.target)

            # Previous IndexError Fix/Workaround
            if not currentTargetPath in targetPaths:
                continue

            # Check for extra directories
            for dir in self.destinationStructure[path][0]:

                if not dir in self.targetStructure[currentTargetPath][0]:

                    cleanDirs.append(dir)

            # Check for extra files
            for file in self.destinationStructure[path][1]:

                if not file in self.targetStructure[currentTargetPath][1]:

                    cleanFiles.append(file)

            # Add paths, directories and files to the clean list
            self.cleanList.append([path, cleanDirs, cleanFiles])

    def copy(self, items: list):

        """Copying Method

        Creates directories and copies files from items list
        """

        # Set log counters
        createdDirs = 0
        copiedFiles = 0

        for currentDirectory, directories, files in items:

            # Create full path to current destination directory
            destinationDirectory = currentDirectory.replace(self.target, self.destination)

            # Create all directories from the list
            for directory in directories:
                FileManager.createDirectory(directory, destinationDirectory)
                self.logger.info("Created Directory: " + str(directory) + " In: " + str(destinationDirectory))
                createdDirs+=1

            # Copy all files from the list
            for file in files:
                FileManager.copy(file, currentDirectory, destinationDirectory)
                self.logger.info("Copied File: " + str(file) + " To: " + str(destinationDirectory))
                copiedFiles+=1

        if createdDirs > 0 or copiedFiles > 0:
            self.logger.info("Created " + str(createdDirs) + " Directory/ies, And Copied " + str(copiedFiles) + " File(s)")

    def scheduleSync(self):

        """Schedule AbSync.sync() at self.interval seconds"""

        schedule.every(self.interval).seconds.do(self.sync)

    def sync(self):

        """AbSync Synchronization Method

        Updates directory structure for AbSync.target and AbSync.destination
        
        Checks for differences and stores them in AbSync.copyList and AbSync.cleanList
        
        Removes directories and files from cleanList

        Creates directories and copies files from copyList
        """

        self.updateStructures()

        self.compare()

        if (len(self.cleanList) > 0):
            self.clean(self.cleanList[::-1])

        if (len(self.copyList) > 0):
            self.copy(self.copyList)

        self.logger.info("Completed Sync")

    def run(self):

        """Runs the scheduled sync until interrupted"""

        while True:
            schedule.run_pending()
            time.sleep(1)

    def updateStructures(self):

        """Updates target and destination directory structure"""

        self.targetStructure = FileManager.update(self.target)
        self.destinationStructure = FileManager.update(self.destination)

