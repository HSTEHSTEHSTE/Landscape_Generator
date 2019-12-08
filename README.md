# Landscape_Generator
Description: 
Toy project that generates a landscape. 

Usage: 
cd Landscape_Generator
python.exe main.py

Interface:
* Welcome Page
* Left panel: 
  * main: shows ground height, sea depth
  * landmass: shows ground and sea
* Right panel:
  * new: generates new landscape
  * load: loads current landscape
  * save: saves current landscape

Dependencies: 
* python3.7+
* python packages: noise, numpy, random, arcade (used for the graphic UI, consider switching for better performance)
* Microsoft Excel: storage is currently implemented through Excel, in order to achieve better portability and allow participation for people from non-technological background. Consider switching in the future to database + editing GUI
