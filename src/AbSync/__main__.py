import  sys
from .AbSync import AbSync

args = sys.argv
target = str(args[1])
destination = str(args[2])
interval = int(args[3])
logLocation = str(args[4])

absync = AbSync(target, destination, interval, logLocation)

absync.sync()

absync.scheduleSync()

absync.run()
