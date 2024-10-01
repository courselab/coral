
 Directions for the programming exercise
 =======================================
 
 KobraPy is intended as a programming exercise.

 It consists of a very simple version of the classic 80s arcade snake
 game written in Python, provided as an initial codebase that the
 learner should further extend. It was originally created as an
 educational resource to teach open-source development practices,
 tools, and project management methodologies to graduate computer
 science students.  

 The exercise consists of:

 a) Fixing the listed known issues (bugs and requested features).

 b) Improving the game by adding some exciting new features.

 Important information for developers can be found in the file
 docs/CONTRIBUTING.md. Please read it before starting your
 contribution. 

 Known issues (that you should resolve)
 --------------------------------------

 __KNOWN BUGS__

 * In the current implementation, reversing movement (e.g. if the snake moving
   right and the player press the left key), is not an illegal move, although
   a bad one, as it causes the snake to bite itself (this adds to the game
   challenge). However, there is a bug that causes the self-bite not to be
   detected by the game if the snake's tail has only one segment.

 * There is a small random chance that an apple be dropped onto the snake, and
   trying to eat it would be detected as self-bite. The probability is small
   but it increases as the snake lengthens.  

 __WISHED FEATURES__

 * In some versions of the snake game, as the snake moves, it looses energy
   and, if all of it is exhausted, the snake dies. To restore energy, the
   snake needs to eat apples. The snake should be born with 100% energy level
   and gradually expend energy as it moves. An energy meter should be shown.

 * Before the game starts, the user might have the possibility of choosing
   some game parameters such as

	  * the size of the grid
	  * the snake speed
   	  * the number of apples in the arena. 
	  * whether reversing the snake is allowed or not
	  * whether apples disappear after some time
	  * whether there may be poisoned apples that degrades energy

 * Before the game starts, the user should have the option of choosing
   the level of difficulty --- which might include some preset combinations
   of the former game parameters. Another possibility would be to choose
   whether the difficulty level increases as the score is raised.

 * The game should save the highest score.
  
 * The snake should start in a random position (but not too close to the
   border where it is heading to).

 Directions for this exercise
 ------------------------------

 The official repository of KobraPy is https://github.com/monacofj/kobrapy.

 To start working on the exercise:

 * create (don't fork) a new public repository in the online SCM platform;

 * give the development team access to the newly created repository;

 * clone your repository and copy KobraPy source into your work tree;

 * follow the instructions given in `docs/CONTRIBUTING.md`;

 * make the necessary changes 

 * commit your changes and proceed therefrom.
 

 Other steps you **must** take
 ------------------------------

 __Name your project__

 You have the arduous task of choosing a cool, catchy, awesome name
 for your amazing new project (KobraPy is taken :)

 * Edit the documentation and the source code accordingly.
    
 * Rename file `kobra.py` to match your project's name.

 __Revise copyright information__ 

 Bear in mind that the programming challenge is not about
 contributing to KobraPy. Of course, you are welcome to contribute if
 you wish; however, the proposed exercise is to create a brand-new
 program. Even if it's built on KobraPy's codebase, your project will
 be a separate piece of software, and when it comes to intellectual
 rights, you will be the author of your new creation.

 That being so, you are expected to take some steps before uploading
 your code into the public repository.

   * Update the author and copyright information in every source file.

     As for this step, you should  **add** (not replace) the copyright
     note with your (your team's) name.

   * Update `AUTHORS` so that it identifies you as an author.

 __Other actions__

 During the project development you may be asked to take several
 actions that are relevant in FOSS development, including

 * provide a code of conduct document;
 
 * revise the contributor guidelines;

 * comply with SDPX [1] and REUSE [2] standards;

 * maintain a ChangeLog file

 * create issue and pull-request templates;

 and other steps.


  References
  ------------------------------

  [1] SDPX System Package Data Exchange, https://spdx.dev

  [2] REUSE Software, https://reuse.software
