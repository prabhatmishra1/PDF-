This is a quick guide to getting started with the codebase for pdf editor.

## Pre-requirements
The system should have Python 3.x and pip installed for Python 3.x

## Getting Started with the codebase
Unzip the Program File and from the command prompt/terminal go inside the directory using
`cd fitz_pdf_editor`.
Make sure your directory is python executable.



As a convention, it is advisible to work under a virtual environment for every project.
You can install virtualenv using
`sudo apt install virtualenv` for ubuntu
`pip install virtualenv` for windows
or if your system follows `pip3`use:
`pip3 install virtualenv`

Once you create the virtual environment, activate it using the command:
`source env/bin/activate` for ubuntu
`source \env\Scripts\activate.bat`

For more information on installing and activating virtual env you can checkout(VirtualEnvWrapper-win is not needed): https://www.liquidweb.com/kb/how-to-setup-a-python-virtual-environment-on-windows-10/

## Installing Essentials
`requirements.txt` file contains all the needed libraries. You can simply pip install them from the directory containing the requirements file. I would highly recommend to use virtual env before doing any pip install
```
pip install -r requirements.txt
```
or if your system follows `pip3`use:
```
pip3 install -r requirements.txt
```
## Follow the guide next
Once your dependencies are installed. Look over the directory(folder) and you'll get 2 directory:
- input: Put the input pdf file under this directory.
- output: You'll get the corresponding output pdf file in this directory once the program runs.


## Running the program
Run the python file:
```
python3 pdf_replace.py
```
### Code Inputs:
- It will prompt you to input the filename of the PDF. Remember to put only the filename and `Not` the filepath **Make sure to use the exact file name including the extension.** ***If you are not sure of the full name you can check it out using:***
    `ls input` for ubuntu
    `dir input` for windows

That's it. The program will then process the files.
## 🎉 Happy Editing your PDF. 🎉
