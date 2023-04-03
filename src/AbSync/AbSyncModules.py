import hashlib, shutil, os, logging


class FileManager:
    """File Manager Class


    Methods
    ----------------------
    absPath(target)
        os.path.abspath() override, returns absolute path

    checkHashes(file1, file2)
        calculates MD5 hashes for file1 and file2 and returns True if same, False if not

    compareFiles(file1, file2)
        compares file1 properties to file2 and returns True if same, False if not

    copy(file, target, destination)
        copies file from target to destination

    createDirectory(directory, location="")
        creates directory at location

    exists(location)
        "overrides" os.path.exists()

    join(target, name)
        os.path.join() override, returns a joined path as a string

    removeDirectory(directory, location)
        removes directory from location using os.rmdir if empty directory,
        and shutil.rmtree if OSError is raised
        
    removeFile(file, location)
        removes file from location

    update(location)
        returns result of os.walk() through location as a dictionary
    """

    @staticmethod
    def absPath(target: str) -> str:

        """os.path.abspath() Override, returns absolute path for the target path"""

        return os.path.abspath(target)

    @staticmethod
    def checkHashes(file1: str, file2: str) -> bool:

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

    @staticmethod
    def compareFiles(file1: str, file2: str) -> bool:

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
        if (not FileManager.checkHashes(file1, file2)):
            return False

        return True

    @staticmethod
    def copy(file, target, destination):

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

    @staticmethod
    def createDirectory(directory: str, location: str = ""):

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

    @staticmethod
    def exists(target: str) -> bool:

        """os.path.exists() override, checks if target exists and returns boolean"""

        return os.path.exists(target)

    @staticmethod
    def join(path, name):
        return os.path.join(path, name)

    @staticmethod
    def removeDirectory(directory: str, location: str):

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

    @staticmethod
    def removeFile(file: str, location: str):

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

        @staticmethod
        def update(location: str) -> dict:
            """Performs os.walk() through location and returns the result as a dictionary


            Parameters:
            ----------------------
            location: str
                target path, passed to os.walk()


            Returns:
            ----------------------
            dict
                a dictionary with a result of os.walk() in a 3-tuple format
            """

            # Set initial variables
            updated = {}

            # Perform os.walk() and append iterations to the updatedList
            for currentDirectory, directories, files in os.walk(os.path.abspath(str(location))):
                updated[currentDirectory] = [directories, files]

            # Return the result of os.walk() as list
            return updated


class Logger:

    def getLogger(location: str):
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
