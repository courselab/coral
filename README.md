
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

 Installation
 ------------------------------

 Follow these steps to set up and run the Coral Snake Game:

 ### Prerequisites

- Python 3: Make sure you have Python 3 installed on your machine.   
  - Linux Users: You can use `apt` to install Python:  
    ```bash
    sudo apt update
    sudo apt install python3
    ```  
    Note: The exact installation process may vary depending on your Linux distribution. Check your distribution's documentation if needed.  
  
  - Windows/Mac Users: You can download it from the official Python [website](https://www.python.org/downloads/).  

 - Pygame: The game requires the Pygame library, which can be installed using `pip` or other package managers like `pacman` on Arch Linux.

 ### Installation Steps
 
 1. Clone the repository:

 First, clone the Coral repository to your local machine by running the following command in your terminal:

 ```bash
 git clone git@github.com:courselab/coral.git
 ``` 

 2. Navigate to the project folder: Once the repository is cloned, navigate to the `coral` folder:
 
 ```bash
 cd coral
 ```

 3. Install dependencies: To install the required dependencies, you'll need to install Pygame. Run the following command:
 
 - Using pip (recommended for most users):
 
 ```bash
 pip install pygame
 ```

 - Alternatively, if you're on an Arch-based system, you can install Pygame using pacman:

 ```bash
 sudo pacman -S python-pygame
 ```

 4. Run the game: After installing Pygame, you can start the game by running the coral.py file. Run the following command:

 ```bash
 python coral.py
 ```