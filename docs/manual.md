
 KobraPy Manual
 ==============================

 KobraPy is intended as programming exercise.

 It consists in a very simple version of the classical 80s' arcade snake game
 written in Python, that is provided as an initial codebase  that should be 
 further extended by the learner. It was originally created as an educational
 resource to teach open-source development practices, tools and project
 management methodologies to graduate computer sciences students.

 KobraPy is free software and can be distributed under the GNU General Public
 License vr.3 or any later version.

 Requirements
 ------------------------------

 * Python 3
 * Pygame engine (https://www.pygame.org)

 The Game
 ------------------------------

 The game takes place on a rectangular arena where a snake continuously
 move in one of the four orthogonal directions: left, right, up and down;
 it never  stops. The challenge consists in steering the snake using the game
 controls to help it eat apples that are placed in random positions. Once
 consumed, apples appear elsewhere.

 Be careful, though. The arena borders are electrified and would kill the snake
 if touched. Moreover, mind that the snake is poisonous and it will also die if 
 it accidentally bites itself, i.e. if the snake's head crosses its own tail.

 The game score is the count of apples eaten until the game is over, and thus
 one should collect as many as possible.

 But there's a catch: the snake lengthens each time it eats an apple.
 
 CONTROLS

 * `arrow keys`:  move the snake up, down, left, right
 * `Q / q     `:  quits the game at any instant

 When the game ends, press any key to restart or 'q' to quit.

 Contributing to KobraPy
 ------------------------------

 The official repository of KhobraPy is https://github.com/monacofj/khobrapy.

 If you're willing to contribute to this project, suggestions are more than
 welcome.  Important information for contributing code can be found in the
 file `docs/CONTRIBUTING.md`. 

 Otherwise, if you're exploring KhobraPy as a programming exercise, please
 refer to the file `docs/exercise-directions.md`.