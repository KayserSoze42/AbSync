import hashlib, shutil, os, sys, logging


class FileManager:
    """File Manager Class


    Methods
    ----------------------
    update(location)
        returns result of os.walk() through location as a list

    compare(target, destination)
        compares target structure list with destination and return a list of differences

    createDirectory(directory, location="")
        creates directory

    compareFiles(file1, file2)
        compares file1 properties to file2 and returns True if same, False if not

    copy(file, target, destination)
        copies file from target to destination

    checkHashes(file1, file2)
        calculates MD5 hashes for file1 and file2 and returns True if same, False if not

    exists(location)
        "overrides" os.path.exists()

    removeDirectory(directory, location)
        removes directory from location using os.rmdir if empty directory,
        and shutil.rmtree if OSError is raised
        
    removeFile(file, location)
        removes file from location
    """

    def __init__(self):
        self.system = os.name

    def update(self, location):

        """Performs os.walk() through location and returns the result as a list


        Parameters:
        ----------------------
        location: str
            target path, passed to os.walk()


        Returns:
        ----------------------
        list
            a list with a result of os.walk()
        """

        # Set initial variables
        updatedList = []

        # Perform os.walk() and append iterations to the updatedList
        for currentDirectory, directories, files in os.walk(os.path.abspath(str(location))):
            updatedList.append([currentDirectory, directories, files])

        # Return the result of os.walk() as list
        return updatedList

    def compare(self, target, destination):

        """Compares two lists and returns a list of missing items


        Parameters:
        ----------------------
        target: list
            a list of location, directories and files of the target structure

        destination: list
            a list of location, directories and files of the destination structure

        Returns:
        ----------------------
        list
            a list of items from target that are not present in destination
        """

        # Re/Set initial variables
        difference = []
        count = 0

        # Check target directory structure
        for currentDirectory, directories, files in target:

            # IndexError Workaround, target has more elements than destination. Assume all to copy/remove
            if (count > len(destination) - 1):
                difDirectories = directories
                difFiles = files
                difference.append([currentDirectory, difDirectories, difFiles])
                continue

            # Re/Set variables for current iteration
            difDirectories = []
            difFiles = []

            # Check for directories in target not present in destination, and append to list
            for directory in directories:

                if (not directory in destination[count][1]):
                    difDirectories.append(directory)

            # Check for files in target not present in destination,
            # Compare files present in both target and destination and append the difference to list
            for file in files:

                # If the file is not present in destination directory
                if (not file in destination[count][2]):

                    # Add file to the list
                    difFiles.append(file)

                # If the file is present in destination directory
                else:

                    # Create full path to the both files
                    currentTarget = os.path.join(os.path.abspath(currentDirectory), file)
                    currentDestination = os.path.join(os.path.abspath(destination[count][0]), file)

                    # Compare files and append to the list if different
                    if (not self.compareFiles(currentTarget, currentDestination)):
                        difFiles.append(file)

            # Append current directory structure to the full list of differences
            difference.append([currentDirectory, difDirectories, difFiles])

            count += 1

        # Return a list of differences with format [[location: str, directories: list, files: list]...]
        return difference

    def createDirectory(self, directory, location=""):

        """Function for creating directory


        Parameters:
        ----------------------
        directory: str
            name of directory, or path to directory
            

        location: str, optional
            path for the directory, if left out current working directory is used
        """

        # Check if location is provided
        if (location == ""):

            # Create full path from current directory
            path = os.path.abspath(directory)

        # If location is provided
        else:

            # Create full path from given location
            path = os.path.join(os.path.abspath(location), directory)

        # Create directory at location
        os.makedirs(path)

    def compareFiles(self, file1, file2):

        """Compares two files and returns True if files are same, else False


        Parameters:
        ----------------------
        file1: str
            path to the file1

        file2: str
            path to the file2

        
        Returns:
        ----------------------
        boolean
            returns False if files compare to different, else it returns True
        """

        # Crude checking for size
        if (os.stat(file1).st_size != os.stat(file2).st_size):
            return False

        # Compare hashes
        if (not self.checkHashes(file1, file2)):
            return False

        return True

    def copy(self, file, target, destination):

        """Copies file from target to destination using shutil.copy2()


        Parameters:
        ----------------------
        file: str
            name of the file to copy

        target: str
            path to the file to copy

        destination: str
            path to the location directory
        """

        # Create full paths for the target and destination
        targetPath = os.path.join(os.path.abspath(target), file)
        destinationPath = os.path.join(os.path.abspath(destination), file)

        # Copy from target to destination
        shutil.copy2(targetPath, destinationPath)

    def checkHashes(self, file1, file2):

        """Calculates MD5 hashes for file1 and file2 and returns boolean comparison


        Parameters:
        ----------------------
        file1: str
            path to the file1

        file2: str
            path to the file2


        Returns:
        ----------------------
        boolean
            returns True if files have same hashes, else returns False
        """

        # Calculate MD5 Hash for file1
        with open(file1, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)

        hash1 = file_hash.digest()

        # Calculate MD5 Hash for file2
        with open(file2, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)

        hash2 = file_hash.digest()

        # Compare and return boolean result
        return hash1 == hash2

    def exists(self, target):

        """os.path.exists() override, checks if target exists and returns boolean"""

        return os.path.exists(target)

    def removeDirectory(self, directory, location):

        """Removes directory from location using os.rmdir, shutil.rmtree if OSError is raised, else it raises an Exception**


        Parameters:
        ----------------------
        directory: str
            name of the directory to be removed

        location: str
            path to the directory


        Raises:
        ----------------------
        Exception**
        """

        # Create full path to the directory
        path = os.path.join(os.path.abspath(location), directory)

        # Removing an empty directory
        try:
            os.rmdir(path)

        # Removing directory with files
        except OSError as OSerror:
            shutil.rmtree(path)

        except Exception as exception:
            raise

    def removeFile(self, file, location):

        """os.remove() override, removes file from location

        Parameters:
        ----------------------
        file: str
            name of the file to be removed

        location: str
            path to the file
        """

        # Create full path to the file
        path = os.path.join(os.path.abspath(location), file)

        # Remove file
        os.remove(path)


class Logger:

    def getLogger(location):
        # Join logfile path with filename for full path
        logPath = os.path.join(os.path.abspath(location), "absync.log")

        # Create logger
        logger = logging.getLogger("AbsyncLogger")
        logger.setLevel(logging.DEBUG)

        # Set File Logger Config and add handler
        file = logging.FileHandler(logPath)
        file.setLevel(logging.INFO)
        fileFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file.setFormatter(fileFormatter)

        logger.addHandler(file)

        # Set Console Output(Stream) Logger Config and add handler
        stream = logging.StreamHandler()
        stream.setLevel(logging.INFO)
        streamFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        stream.setFormatter(streamFormatter)

        logger.addHandler(stream)

        return logger
