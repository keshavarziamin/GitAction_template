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
    print("""
USAGE:
python3 {} < -short_options > | < --long_options >

OPTIONS:
python3 {} <-h | --help>        # print usage
python3 {} <-c | --clean>       # remove build folder
python3 {} <-b | --build>       # build source files
python3 {} <-r | --rebuild>     # rebuild source files
python3 {} <-t | --test>        # run unit tests
python3 {} <-a | --all>         # rebuild source files and run unit tests

EXAMPLE:
python3 {} -c   or   python3 {} --clean
python3 {} -r   or   python3 {} --rebuild
python3 {} -b   or   python3 {} --build
python3 {} -t   or   python3 {} --test
python3 {} -a   or   python3 {} --all
    """.format(sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0]))


def assert_return(ret):
    output = ret.stdout.decode("utf-8")
    print(output)
    output = ret.stderr.decode("utf-8")
    print(output)

    if ret.returncode != 0:
        print(Fore.RED + "PROCCESS FAILED.\n" + Fore.RESET)
        exit(ERROR)

    print(Fore.GREEN + "PROCCESS SUCCEEDED.\n" + Fore.RESET)


def execute_command(cmd):
    try:
        ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(Fore.RED + "ERROR: EXECUTION OF CMD FAILED." + Fore.RESET, str(e))
        exit(ERROR)

    return ret


def update_system():
    print(Fore.BLUE + "START UPDATING SYSTEM ...\n" + Fore.RESET)
    ret = execute_command(["sudo", "apt", "update", "-y"])
    assert_return(ret)


def upgrade_system():
    print(Fore.BLUE + "START UPGRADING SYSTEM ...\n" + Fore.RESET)
    ret = execute_command(["sudo", "apt", "upgrade", "-y"])
    assert_return(ret)


def install_essential():
    update_system()
    upgrade_system()

    print(Fore.BLUE + "START INSTALLING ESSENTIAL ...\n" + Fore.RESET)
    ret = execute_command(["sudo", "apt", "install", "-y", "build-essential", "autoconf", "make", "cmake", "git", "gcc", "g++", "automake", "libtool", "python3", "pip"])
    assert_return(ret)

    print(Fore.BLUE + "START INSTALLING COLORAMA ...\n" + Fore.RESET)
    ret = execute_command(["pip", "install", "colorama"])
    assert_return(ret)


def build():
    print(Fore.BLUE + "START CONFIGURATION ...\n" + Fore.RESET)
    ret = execute_command(["cmake", "-S", ".", "-B", BUILD_DIR])
    assert_return(ret)

    print(Fore.BLUE + "START BUILDING ...\n" + Fore.RESET)
    ret = execute_command(["cmake", "--build", BUILD_DIR])
    assert_return(ret)


def update_submodule():
    print(Fore.BLUE + "UPDATING SUBMODULES ..." + Fore.RESET)
    ret = execute_command(["git", "submodule", "update", "--init", "--recursive"])
    assert_return(ret)


def run_unit_test():
    print(Fore.BLUE + "START TESTING ...\n" + Fore.RESET)
    utb_path = os.path.join(TEST_BIN_DIR, TEST_BIN_FILE)
    ret = execute_command([utb_path])
    assert_return(ret)


def clean_build():
    print(Fore.BLUE + "REMOVING BUILD ...\n" + Fore.RESET)
    ret = execute_command(["rm", "-rf", BUILD_DIR])
    assert_return(ret)


def get_options(argv):
    opts, _ = getopt.getopt(argv, "hicbrta", ["help", "install", "clean", "build", "rebuild", "test", "all"])

    if not opts:
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
    if not get_options(sys.argv[1:]):
        usage()
        exit(ERROR)

    if FLAG_INSTALL:
        install_essential()

    if FLAG_CLEAN:
        clean_build()

    if FLAG_BUILD:
        update_submodule()
        build()

    if FLAG_TEST:
        run_unit_test()

    exit(SUCCESS)
