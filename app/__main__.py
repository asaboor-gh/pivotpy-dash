import sys
import os 

path = os.path.dirname(__file__)
app_path = os.path.join(path,'index.py')

try:
    interpreter = sys.executable
except:
    interpreter = "python"

if len(sys.argv) > 1:
    print("Running Pivotpy-Dash App using '{}'".format(interpreter))
    os.system("{} {} {}".format(interpreter, app_path,sys.argv[1]))
else:
    print("Running Pivotpy-Dash App using '{}'".format(interpreter))
    os.system("{} {}".format(interpreter, app_path))