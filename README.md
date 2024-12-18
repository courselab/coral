
Copyright 2023 Monaco F. J. <monaco@usp.br> 
Copyright 2024 The Authors of Coral

Coral is free software and is distributed under the terms of the
GNU General Public License 3.0.

Coral - Snake game challenge
==============================

Coral is intended as a programming exercise.

It consists of a very simple version of the classic 80s arcade snake game
written in Python, provided as an initial codebase that the learner should
further extend. It was originally created as an educational resource to teach
open-source development practices, tools, and project management methodologies
to graduate computer science students. 

The exercise consists of:

a) Fixing the listed known issues (bugs and requested features).

b) Improving the game by adding some exciting new features.

Important information for developers can be found in the file
docs/CONTRIBUTING.md. Please read it before starting your contribution. 

Getting started
------------------------------

User instructions are available in the file `docs/manual.md`.

If you're exploring Coral as a programming exercise, please refer to
the file `docs/challenge.md` for directions. 

And if you like it, feel free to let the author know.

Contributing
------------------------------

Your contribution will be greatly appreciated.

See `docs/CONTRIBUTING.md` for further information.

Playing
------------------------------

You can download a packaged executable of the game from [Releases](https://github.com/courselab/coral/releases). Pick a version compatible with your operating system, extract the contents of the zip file, an run the executable `coral` file. Otherwise follow the installation instructions bellow to run it using the source code.


Installing
------------------------------

### Prerequisites

Coral requires the installation of `python3`, the libary [`pygame`](https://pypi.org/project/pygame/),  and optionally the libary [`pyinstaller`](https://pypi.org/project/pyinstaller/). Instructions on how to obtain these are covered below.

#### Installation Steps

##### 1. Clone the repository:

First, clone the Coral repository to your local machine by running the following command in your terminal:

```bash
git clone https://github.com/courselab/coral.git
``` 

##### 2. Navigate to the project folder: Once the repository is cloned, navigate to the `coral` folder:

```bash
cd coral
```

##### 3. Install Python and required libraries

> [!note]
> All dependencies are described in the `flake.nix` file, so that:
>   - the game can be executed with `nix run`
>   - A development environment with all required dependencies can be accessed with `nix develop`
> That's it, you're done. Skip all following steps.

- Installing python

  - Linux users: You can use `apt` to install Python:  
    ```bash
    sudo apt update
    sudo apt install python3
    ```  

    Note: The exact installation process may vary depending on your Linux distribution. Check your distribution's documentation if needed.  

  - Windows/Mac Users: You can download it from the official Python [website](https://www.python.org/downloads/).  


- Installing dependencies using pip (recommended for most users):

```bash
pip install -r requirements.txt
```

##### 4. Running the game

You can start the game by running the coral.py file. Run the following command:

```bash
python coral.py
```
