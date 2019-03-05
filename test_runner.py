import subprocess
import sys
sys.path.append("../drawing")
from os import listdir
from os.path import isfile, join

#run this from inside the testing directory to avoid looking for bpy (supplied by blender at normal runtime)
def main():
    blender_path = '../../../../blender'
    test_path = "Tests/"

    if len(sys.argv) > 1:
        blender_path = sys.argv[1]

    for file in [f for f in listdir(test_path) if isfile(join(test_path, f))]:
        if file != __file__[2:]:
            print("\n" + test_path+file)
            subprocess.call([blender_path,'-b', '-P', test_path+file])

if __name__ == "__main__":
    main()
