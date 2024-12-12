# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Static obstacles to the map (PR #160)
- Ability to make the snake "run" by pressing space bar (#84)
- Support for multiple languages(#141)
- Instruction screen (#88)
- Movement controls using the WASD keys (#55)
- A configuration menu with volume controls (#56)
- Installation instructions to README (#77)
- The ability to mute/unmute the game's audio (#35)
- The ability to save locally and display the current highscore (#26)
- Background music and sound effects (#24)
- A "Hard" difficulty setting with increased movement speed (#21)
- The snake consumes vital energy while moving, shown in an energy bar (#18)
- Constraints to the snake's spawn position and direction (#11)

### Changed

- Visual feedback at the config menu (#130)
- Changed the font to one licensed under open source terms (#148)
- Refactored some code (#116)
- Apple restores a random amount of energy, within certain bounds (#101)
- Updated text to the main menu (#74)
- Updated apple graphics (#73, #78)
- Updated graphics for the snake's body (#44)
- Updated graphics for the paused state (#13)

### Fix

- Already available option to mute audio added to the game's instructions (#179)
- Prevented fruits from spawning over obstacles (#175)
- Text is scaled so that it doesn't get clipped after changing the font (#148)
- Obstacles kill on contact, instead of causing the game to pause (#166)
- Speed modifier from the snake "running" is correctly reset upon death (#120)
- Sprites are correctly scaled to the different board sizes (#124)
- WASD directional movement now also works on menus (#163)
- Bug where the background music stops looping after the snake dies (#108)
- Solved naming issues and typos in the documentation (#113)
- Game crash caused by byte to int conversion when saving the highscore (#99)
- Draw order bug that allows the Snake to cover its energy bar (#39)
- Instruction screen (#88)
- Interrupt game over background music immediately upon respawning (#41)
- Added a movement buffer, preventing another method of reversing the snake's movement (#3)
- Bug where the choice to play in hard mode is irreversible (#33)
- Energy bar works as intended independently of its set initial value (#31)
- Window scales to accommodate different screen resolutions (#10)
- Bug where apples spawn on top of the snake (#4)
- Snake no longer able to immediately revert its movement direction (#3)

## [0.1.0] - 2024-10-01

### Added

- Initial code imported code code from KobraPy.
