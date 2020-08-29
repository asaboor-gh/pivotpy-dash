import sys
import os 

path = os.path.dirname(__file__)
app_path = os.path.join(path,'index.py')

if len(sys.argv) > 1:
    os.system("python {} {}".format(app_path,sys.argv[1]))
else:
    os.system("python {}".format(app_path))