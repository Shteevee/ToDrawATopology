# ToDrawATopology [![Build Status](https://travis-ci.com/Shteevee/ToDrawATopology.svg?token=qze7gzxfs4nesEue56KP&branch=master)](https://travis-ci.com/Shteevee/ToDrawATopology)

## Installation
* I recommend installing this on Blender 2.79b as it is the only tested version.

* Clone this repository in to the add-ons folder of your Blender installation. The folder can be found at `YourBlenderFolder/2.79/scripts/addons` for Blender version 2.79x.

* Navigate into the `ToDrawATopology` folder and run the command `python3 project_setup.py "PathToYourBlender/2.79/python/bin/pip" install`. A pip path shouldn't be needed for Windows. This will install the necessary packages to run the add-on. 

* If the system cannot find pip on Windows for some reason then run the command `PathToBlender/2.79/python/bin/python -m ensurepip` to make sure pip is installed in Blender. When inside the project folder `../../../python/bin/python -m ensurepip` should also work.

* If the system cannot find pip on Linux for some reason then run the command `PathToBlender/2.79/python/bin/python3.5m -m ensurepip` to make sure pip is installed in Blender. When inside the project folder `../../../python/bin/python3.5m -m ensurepip` should also work.

* Now that the dependancies are installed, the plug-in can be used. You can find it in the render tab of the add-ons.
