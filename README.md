# GeoPlotter
Simple plotting tool for ternary and quaternary graphs.
# Features
* Importing CSV files with data
* Automatic data normalization
* Color customization
* Label renaming
* Plot image saving
# Installation
```
git clone https://github.com/rsedxcftvgyhbujnkiqwe/geoplotter
cd geoplotter
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
# Usage
You need to make sure you enter your virtual environment each time you initialize a terminal session.
```
cd geoplotter
source .venv/bin/activate
```
Then run the application
```
python3 geoplotter.py
```
## Notes
Ensure that your csv files:
* Have a header
* Are either 3, or 4 columns
* Are entirely int/float data (aside from headers)
# Credits
Made with ChatGPT for my friend who needed it.

[python-ternary](https://github.com/marcharper/python-ternary) - marcharper

[python-quaternary](https://github.com/sachour/python-quaternary) - sachour
