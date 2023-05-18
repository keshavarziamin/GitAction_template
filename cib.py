import os
import sys
import getopt
import subprocess
from colorama import Fore

BUILD_DIR = "build"
TEST_BIN_DIR = "build/test"
TEST_BIN_FILE = "test_sort"
COMPILER_TIMEOUT = 10.0

ERROR = 1
SUCCESS = 0

FLAG_BUILD = False
FLAG_REBUILD = False
FLAG_TEST = False
FLAG_CLEAN = False
FLAG_INSTALL = False


def usage():
    print("\nUSAGE:")
    print("python3", sys.argv[0], "< -short_options > | < --long_options >")

    print("\nOPTIONS:")
    print("python3", sys.argv[0], "<-h | --help>        # print usage")
    print("python3", sys.argv[0], "<-c | --clean>       # remove build folder")
    print("python3", sys.argv[0], "<-b | --build>       # build source files")
    print("python3", sys.argv[0],
          "<-r | --rebuild>     # rebuild source files")
    print("python3", sys.argv[0], "<-t | --test>        # run unit tests")
    print("python3", sys.argv[0],
          "<-a | --all>         # rebuild source files and run unit tests ")

    print("\nEXAMPLE:")
    print("python3", sys.argv[0], "-c   or   ",
          "python3", sys.argv[0], "--clean")
    print("python3", sys.argv[0], "-r   or   ",
          "python3", sys.argv[0], "--rebuild")
    print("python3", sys.argv[0], "-b   or   ",
          "python3", sys.argv[0], "--build")
    print("python3", sys.argv[0], "-t   or   ",
          "python3", sys.argv[0], "--test")
    print("python3", sys.argv[0], "-a   or   ",
          "python3", sys.argv[0], "--all")
    print()

# check status of return


def assertReturn(ret):
    output = ret.stdout.decode("utf-8")
    print(output)
    output = ret.stderr.decode("utf-8")
    print(output)

    if ret.returncode != 0:
        print(Fore.RED+"PROCCESS FAILED.\n"+Fore.RESET)
        exit(ERROR)

    print(Fore.GREEN+"PROCCESS SUCCEEDED.\n"+Fore.RESET)


def executeCommond(cmd):
    try:
        ret = subprocess.run(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    except Exception as e:
        print(Fore.RED+"ERROR: EXCUTION OF CMD FAILED."+Fore.RESET, str(e))
        exit(ERROR)

    return ret


# configure and build source files
def updateSystem():
    print(Fore.BLUE+"START UPDATING SYSTEM ...\n"+Fore.RESET)
    ret = executeCommond(["sudo", "apt", "update", "-y"])
    assertReturn(ret)


def upgradeSystem():
    print(Fore.BLUE+"START UPGRADING SYSTEM ...\n"+Fore.RESET)
    ret = executeCommond(["sudo", "apt", "upgrade", "-y"])
    assertReturn(ret)


def installEssensial():
    updateSystem()
    upgradeSystem()

    print(Fore.BLUE+"START INSTALLING ESSENSIAL ...\n"+Fore.RESET)
    ret = executeCommond(["sudo", "apt", "install", "-y",
                         "build-essential", "autoconf", "make", "cmake", "git", "gcc", "g++",
                          "automake", "libtool", "python3", "pip"])
    assertReturn(ret)
    print(Fore.BLUE+"START INSTALLING COLORAMA ...\n"+Fore.RESET)
    ret = executeCommond(["pip", "install", "colorama"])
    assertReturn(ret)


def build():

    print(Fore.BLUE+"START CONFIGURATION ...\n"+Fore.RESET)
    ret = executeCommond(["cmake", "-S", ".", "-B", BUILD_DIR])
    assertReturn(ret)

    print(Fore.BLUE+"START BUILDING ...\n"+Fore.RESET)
    ret = executeCommond(["cmake", "--build", BUILD_DIR])
    assertReturn(ret)


def updateSubmodule():
    # print(Fore.BLUE+"SCAN SSH-KEY ..."+Fore.RESET)
    # ret = executeCommond(
    #     ["ssh-keyscan", "github.com >> ~/.ssh/known_hosts"])
    # assertReturn(ret)
    print(Fore.BLUE+"UPDATING SUBMODULES ..."+Fore.RESET)
    ret = executeCommond(
        ["git", "submodule", "update", "--init", "--recursive"])
    assertReturn(ret)


def runUnitTest():

    print(Fore.BLUE+"START TESTING ...\n"+Fore.RESET)
    utb_path = os.path.join(TEST_BIN_DIR, TEST_BIN_FILE)
    ret = executeCommond([utb_path])
    assertReturn(ret)


def cleanBuild():
    print(Fore.BLUE+"REMOVING BUILD ...\n"+Fore.RESET)
    ret = executeCommond(["rm", "-rf", BUILD_DIR])
    assertReturn(ret)


def getOptions(argv):

    opts, _ = getopt.getopt(
        argv, "hicbrta", ["help", "install", "clean", "build", "rebuild", "test", "all"])

    if opts == []:
        return False

    global FLAG_BUILD, FLAG_TEST, FLAG_REBUILD, FLAG_CLEAN, FLAG_INSTALL

    for opt, _ in opts:

        if opt in ("-r", "--rebuild"):
            FLAG_CLEAN = True
            FLAG_BUILD = True

        elif opt in ("-b", "--build"):
            FLAG_BUILD = True

        elif opt in ("-t", "--test"):
            FLAG_TEST = True

        elif opt in ("-c", "--clean"):
            FLAG_CLEAN = True

        elif opt in ("-i", "--install"):
            FLAG_INSTALL = True

        elif opt in ("-a", "--all"):
            FLAG_CLEAN = True
            FLAG_BUILD = True
            FLAG_TEST = True

        elif opt in ("-h", "--help"):
            usage()
            exit(SUCCESS)

        else:
            return False

    return True


if __name__ == '__main__':

    if getOptions(sys.argv[1:]) == False:
        usage()
        exit(ERROR)

    if FLAG_INSTALL:
        installEssensial()

    if FLAG_CLEAN:
        cleanBuild()

    if FLAG_BUILD:
        updateSubmodule()
        build()

    if FLAG_TEST:
        runUnitTest()

    exit(SUCCESS)
