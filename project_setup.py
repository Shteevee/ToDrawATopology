import subprocess
import sys

def main():
    required_packages = ["scikit-image", "matplotlib", "svgwrite"]
    if len(sys.argv) > 2:
        pip_path = sys.argv[1]
    else:
        pip_path = '../../../python/scripts/pip'

    if sys.argv[-1] == 'install':
        for required_package in required_packages:
            subprocess.call([pip_path, 'install', required_package])

    elif sys.argv[-1] == 'uninstall':
        for required_package in required_packages:
            subprocess.call([pip_path, 'uninstall', required_package])

if __name__ == '__main__':
    main()
