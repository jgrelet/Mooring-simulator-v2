# Mooring simulator design version 2

See the [roadmap](https://github.com/users/jgrelet/projects/1).

A redesign of the GUI Mooring Simulator application based on [python-menus-toolbar](https://realpython.com/python-menus-toolbars/) that shows how to create and use menus, toolbars, and status bars using Python and PyQt.

## Prequisites for Windows

You must install the following tools:

- Visual Studio Code (<https://code.visualstudio.com/>)
- Git (<https://git-scm.com/downloads>)
- miniconda3 (<https://docs.conda.io/en/latest/miniconda.html>)
- chocolatey (<https://chocolatey.org/install>) and install GNU Make package (<https://community.chocolatey.org/packages/make>)

## Installation based on an YAML environment file

``` bash
conda env create -f environment<OS>.yml -n <new_env_name>
```

example:

``` bash
conda env create -f environment-windows.yml -n ms2
```

## Installation from scratch

We will use VSC as a development tool with conda and python 3.8

```sh
conda create -n ms2 python=3.8
conda activate ms2
conda install -c conda-forge appdirs toml xlrd
pip install PyQt5 qt5-applications qt5-tools

```

## Export your environment

Duplicate your environment on other computer or OS, just export it to a YAML file:

```sh
conda env export --no-builds > environment-linux.yml
```

## Update the environment

```sh
conda env update --prefix ./ms2 --file environment-linux.yml --prune
```

## Remove an environment

```sh
conda env remove --name <env>
```

## Linux and wsl specificities

If you get the following error message when running the program:

*qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.*

it is necessary to reinstall the following program:

```sh
sudo apt-get install --reinstall libxcb-xinerama0
```

## How to Run this Application

To run this application by executing the following command:

```sh
python Mooring-simulator.py
python Mooring-simulator.py -h
python Mooring-simulator.py --lib library\test.xls

usage: 
python MooringSimulator.py --file <file> --lib <file> -d -h   

Mooring simulator program

optional arguments:
  -h, --help            show this help message and exit       
  --file FILE           Mooring design file
  --lib LIB             Libray definition file, Excel or JSON 
  -s SIZE [SIZE ...], --size SIZE [SIZE ...]
                        select screen size, default is 800 x 600
  -r, --reset           reset toml configuration file to default
  -d, --debug           display debug informations
```

This command will launch the application, so you'll be able to experiment with it.

## Makefile

If you have installed make, you can run the following commands to automate processes:

```sh
make res
make test
make run
make lib
make build
make runc
make clean
```

Make for Windows, see [Chocolatey](https://chocolatey.org/), The Package Manager for Windows and [GNU make 4.3](https://community.chocolatey.org/packages/make)

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

Generate ressource file from makefile:

```sh
make res
```

## About the Author

## License

- This application is distributed under the MIT license. See `LICENSE` for details.
