
from optparse import OptionParser
import os.path
import signal


from naming import *

parser = OptionParser()
parser.add_option("-i", "--input", dest="inDir", help="Input Directory", metavar="DIR")
parser.add_option("-o", "--output", dest="outDir", help="Output Directory", metavar="DIR")
parser.add_option("--flow", dest="flowExecutable", help="Executable for optical flow")
parser.add_option("--forward-only", action="store_true", dest="forwardOnly",  help="Calculate forward flow only")
parser.add_option("--backward-only", action="store_true", dest="backwardOnly",  help="Calculate backward flow only")

(options, args) = parser.parse_args()


def handler(signum, frame) :
    print("Signal %s received at frame %s. Terminating." % (signum, frame))
    exit(signum)
signal.signal(signal.SIGINT, handler)


if options.inDir == None :
    print("Please set an output directory.")
    exit(-1)
if options.outDir == None :
    print("Please set an input directory.")
    exit(-1)
if options.flowExecutable == None :
    print("Executable missing.")
    exit(-1)

if not os.path.exists(options.inDir) :
    print("Input directory does not exist.")
    exit(-2)
if not os.path.isdir(options.inDir) :
    print("Input directory is not a directory.")
    exit(-2)

options.outDir = os.path.abspath(options.outDir)
print("Output files go to %s." % options.outDir)


files = os.listdir(options.inDir)
files.sort()

if not os.path.exists(options.outDir) :
    print("Oputput directory does not exist. Creating it.")
    os.makedirs(options.outDir)


prev = None
for s in files :
    if frameID(s) != None :
        if prev != None :
            leftFile = options.inDir + os.sep + prev
            rightFile = options.inDir + os.sep + s
            
            if not options.backwardOnly :
                outFile = nameForwardFlow(prev, s)
                cmd = "%s %s %s 10 100 %s x" % (options.flowExecutable, leftFile, rightFile, options.outDir + os.sep + outFile)
                ret = os.system(cmd)
                print("%s: Returned %s" % (outFile, ret))
                if ret == 2 :
                    print("SIGINT received, terminating.")
                    exit(2)
            
            if not options.forwardOnly :
                outFile = nameBackwardFlow(prev, s)
                cmd = "%s %s %s 10 100 %s x" % (options.flowExecutable, rightFile, leftFile, options.outDir + os.sep + outFile)
                ret = os.system(cmd)
                print("%s: Returned %s" % (outFile, ret))
                if ret == 2 :
                    print("SIGINT received, terminating.")
                    exit(2)
        prev = s