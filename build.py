import os
import subprocess

TEST_DIR = "src"
OUT_FILE = "example1.c"
COMPILER_TIMEOUT = 10.0

ERROR = 1
SUCCESS = 0

src_path = os.path.join(TEST_DIR, OUT_FILE)
out_path = os.path.join(TEST_DIR, "out")

print("start building ...")
try:
    ret = subprocess.run(["gcc", src_path, "-o", out_path],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         timeout=COMPILER_TIMEOUT)
except Exception as e:
    print("ERROR: Cmpilation failed.", str(e))
    exit(ERROR)

output = ret.stdout.decode("urf-8")
print(output)
output = ret.stderr.decode("utf-8")
print(output)

if ret.returncode != 0:
    print("Compilation failed.")
    exit(ERROR)

print("start running ...")
try:
    ret = subprocess.run([out_path],
                         stdout=subprocess.PIPE,
                         timeout=COMPILER_TIMEOUT)
except Exception as e:
    print("ERROR: Runtime failed.", str(e))
    exit(ERROR)

output = ret.stdout.decode("utf-8")
print("RUBTIME_OUTPUT:", output)

print("ALL TEST PASSED.")
exit(SUCCESS)
