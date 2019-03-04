import subprocess
import sys
sys.path.append("../drawing")
from os import listdir
from os.path import isfile, join

#run this from inside the testing directory to avoid looking for bpy (supplied by blender at normal runtime)
python_path = 'python'
test_path = "./"

if len(sys.argv) > 1:
    python_path = sys.argv[1]

for file in [f for f in listdir(test_path) if isfile(join(test_path, f))]:
    if file != __file__[2:]:
        print("\n" + file)
        subprocess.call([python_path, test_path+file])
