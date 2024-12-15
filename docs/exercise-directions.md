
 Directions for the programming exercise
 =======================================
 
 KobraPy is intended as programming exercise.

 It consists in a very simple version of the classical 80s' arcade snake game
 written in Python, that is provided as an initial codebase  that should be 
 further extended by the learner. It was originally created as an educational
 resource to teach open-source development practices, tools and project
 management methodologies to graduate computer sciences students.

   The practice consists in

   a) fixing the listed known issues (bugs and requested features);
   
   b) improving the game by adding some awesome new features.

 Important information for developers can be found in the file
 `docs/CONTRIBUTING.md`. Please, **do read it** before starting your
 contribution.

 Known issues (that you should resolve)
 --------------------------------------

 KNOWN BUGS

 * In the current implementation, reversing movement (e.g. if the snake moving
   right and the player press the left key), is not an illegal move, although
   a bad one, as it causes the snake to bite itself (this adds to the game
   challenge). However, there is a bug that causes the self-bite not to be
   detected by the game if the snake's tail has only one segment.

 * There is a small random chance that an apple be dropped onto the snake, and
   trying to eat it would be detected as self-bite. The probability is small
   but it increases as the snake lengthens.  

 REQUESTED FEATURES

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

 The official repository of KobraPy is https://github.com/monacofj/khobrapy.

 To start working on the exercise:

 * create (don't fork) a new public repository in the online SCM platform;

 * give the development team access to the newly created repository;

 * clone your repository and copy KobraPy source into your work tree

 * follow the instructions given in `docs/CONTRIBUTING.md`.

 * make the necessary changes (see Copyright and attribution below)

 * commit your changes (GitFlow) and proceed therefrom.

 Author rights **(VERY IMPORTANT)**
 -------------------------------

 Bear in mind that the programming challenge is not contributing to KobraPy.
 Surely, you may contribute and are welcome to if you're willing so; the
 proposed exercise, however, is to create a brand new program. Even if built
 on KobraPy's codebase, your project will be a another piece of software and,
 when it comes to intellectual rights, you will be the author of your new
 creation. 

 That being so, you are expected to take some steps before uploading your code
 into the public repository.


 1) Name your project.

    You have the arduous task of choosing a cool, catchy, awesome name
    for your amazing new project (KobraPy is taken :)

    * Edit the documentation and the source code accordingly.
    
    * Preferably, rename file `khobra.py` as you wish.

 2) Edit your project's documentation properly.
 
   * Rewrite `README.md` providing information on your project.

   * Rewrite or replace `manual.md` according to your program.

 3) Provide copyright and attribution information.
   
   * Update the author and copyright information in every source file.

     As for this step, you should edit the author and copyright information
     in every source file. See, for instance, the heading comment at the
     top of `khobra.py`. You should **add** (not replace) a copyright note
     with the release date and copyright holder, e.g. you, your team or your
     organization (this is indeed a both requirement of GNU GPL and a standard
     practice). 

     Also, once you're reusing code from KobraPy, your software is considered
     a derivative work. You're therefore expected to make proper attribution
     to the original author.

     To comply with both those demands, the comment at the top of your source
     files should look something like 

     ```
     Copyright (c) 2003 by Monaco F. J. 
     Copyright (c) <year> by Foo Authors

     This file is part of Foo.

     Foo  is a derivative work of the code from KobraPy by Monaco F. J.,
     distributed under GNU GPL vr3. KnobraPy source code can be found at
     https://github.com/monacofj/khobrapy. The main changes applied to the
     original code are listed in the file Changelog.

     Foo is free software... (and the remaining terms of the top comment)
      ```
       
   * Update `AUTHORS` so that it identify you as the author.

     In this file, list the names of everyone who has make significant
     contributions to your project. 

     Also, repeat the attribution note as exemplified before

     ```
     Foo  is a derivative work of the code from KobraPy by Monaco F. J.,
     distributed under GNU GPL vr3. KnobraPy source code can be found at
     https://github.com/monacofj/khobrapy. The main changes applied to the
     original code are listed in the file Changelog.
     ```

     Keep this file updated, at least at every public (pre)release.



Happy coding.