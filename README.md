# Intro

Welcome to Wordle bot - a robot that solves wordle puzzles.

You can watch the [video](https://www.youtube.com/watch?v=_QHz_5pqPuo) to see how it works.

[![Demo Video](https://img.youtube.com/vi/_QHz_5pqPuo/0.jpg)](https://www.youtube.com/watch?v=_QHz_5pqPuo)

This code is offered without any support - it runs locally on my machine with my setup - you may or may not be able to get it to run locally on your machine.

# Setup

You'll need python3 installed - check to see what you have with:

```
python3 -v
```

And follow any instructions to install python3.

Run the following to create the virtual environment:

```
python3 -m venv venv
```

And then activate the environment:

Finally, activate the virtual environment:

```
source venv/bin/activate
```

Finally, install the dependencies

```
pip install -r requirements.txt
```

To install the PiCamera dependency (if you want to run everything on the pi):

```
pip install -r requirements_pi.txt
```

# Jupyter notebooks

There are two notebooks that you can use to try out the code:

## image_processing.ipynb

This notebook contains all the image processing code - I've included a couple of sample images to test this out on in the `images` folder.

## solver.ipynb

This contains the code for solving the wordle puzzles.

# Python code

The file `main.py` contains the brains of the robot. This file can be run on a RaspberryPi with direct access to a camera or on the desktop with access to a URL that returns JPEG files.
