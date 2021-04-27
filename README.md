# Sample PyQt Application

A sample GUI application [python-menus-toolbar](https://realpython.com/python-menus-toolbars/) that shows how to create and use menus, toolbars, and status bars using Python and PyQt.

## How to Run this Application

To run this application, you need to [install `PyQt5`](https://realpython.com/python-pyqt-gui-calculator/#installing-pyqt) on your Python environment. To do that, you can run the following commands in a terminal or command prompt:

```sh
pip3 install PyQt5
```
or if you have conda installed

```sh
conda install -c conda-forge qt qtpy qt5-applications qt5-tools xlrd
```

Once you have [PyQt](https://www.riverbankcomputing.com/static/Docs/PyQt5/) installed, you can run the application by executing the following command:

```sh
python Mooring-simulator.py
python Mooring-simulator.py -h
usage: 
python MooringSimulator.py --file <file> --lib <file> -d -h   

Mooring simulator program

optional arguments:
  -h, --help            show this help message and exit       
  --file FILE           Mooring design file
  --lib LIB             Libray definition file, Excel or JSON 
  -s SIZE [SIZE ...], --size SIZE [SIZE ...]
                        select screen size, default is 800 x 600
  -d, --debug           display debug informations
```

This command will launch the application, so you'll be able to experiment with it.

## Using Icons and Resources in PyQt

Remove libpng warning: iCCP: known incorrect sRGB profile:

```sh
find . -type f -name "*.png" -exec convert {} -strip {} \;
```

To convert .png to .svg, see [How to convert a PNG image to a SVG?](https://stackoverflow.com/questions/1861382/how-to-convert-a-png-image-to-a-svg)

The Qt library includes the Qt resource system, which is a convenient way of adding binary files such as icons, images, translation files, and other resources to your applications.

To use the resource system, you need to list your resources in a resource collection file, or a .qrc file. A .qrc file is an XML file that contains the location, or path, of each resource in your file system.

Program pyrcc5 reads a .qrc file and produces a Python module that contains the binary code for all your resources:

```sh
pyrcc5 -o qrc_resources.py resources.qrc
```

This command will read resources.qrc and generate qrc_resources.py containing the binary code for each resource. You’ll be able to use those resources in your Python code by importing qrc_resources.

## About the Author

## License

- This application is distributed under the MIT license. See `LICENSE` for details.
