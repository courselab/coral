# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fix

- Already available option to mute audio added to the game's instructions (#179)
- Prevented fruits from spawning over obstacles (#175)

## [0.10.1] - 2024-12-10

### Fix

- Text is scaled so that it doesn't get clipped after changing the font (#148)
- Obstacles kill on contact, instead of causing the game to pause (#166)
- Speed modifier from the snake "running" is correctly reset upon death (#120)
- Sprites are correctly scaled to the different board sizes (#124)
- WASD directional movement now also works on menus (#163)

## [0.10.0] - 2024-12-6

### Added

- Static obstacles to the map (PR #160)


## [0.9.0] - 2024-12-04

### Added

- Ability to make the snake "run" by pressing space bar (#84)
- Support for multiple languages(#141)

### Changed

- Visual feedback at the config menu (#130)
- Changed the font to one licensed under open source terms (#148)

## [0.8.3] - 2024-11-25

### Changed

- Refactored some code (#116)

### Fix

- Bug where the background music stops looping after the snake dies (#108)
- Solved naming issues and typos in the documentation (#113)

## [0.8.2] - 2024-11-21

### Changed

- Apple restores a random amount of energy, within certain bounds instructions (#101)

### Fix

- Game crash caused by byte to int conversion when saving the highscore (#99)

## [0.8.1] - 2024-11-18

### Fixed

- Draw order bug that allows the Snake to cover its energy bar (#39)

## [0.8.0] - 2024-11-14

### Added

- Instruction screen (#88)

### Fixed

- Bug where the snake immediately dies after respawning from a wall collision (#71)

## [0.7.0] - 2024-11-13

### Added

- Movement controls using the WASD keys (#55)
- A configuration menu with volume controls (#56)
- Installation instructions to README (#77)

### Changed

- Updated text to the main menu (#74)
- Updated apple graphics (#73, #78)

## [0.6.0] - 2024-11-12

### Added

- The ability to mute/unmute the game's audio (#35)

### Changed

- Updated graphics for the snake's body (#44)

### Fixed

- Interrupt game over background music immediately upon respawning (#41)
- Added a movement buffer, preventing another method of reversing the snake's movement (#3)
- Bug where the choice to play in hard mode is irreversible (#33)
- Energy bar works as intended independently of its set initial value (#31)

## [0.5.0] - 2024-11-04

### Added

- The ability to save locally and display the current highscore (#26)

## [0.4.0] - 2024-10-30

### Added

- Background music and sound effects (#24)

## [0.3.0] - 2024-10-29

### Added

- A "Hard" difficulty setting with increased movement speed (#21)
- The snake consumes vital energy while moving, shown in an energy bar (#18)

### Changed

- Updated graphics for the paused state (#13)

## [0.2.1] - 2024-10-28

### Fixed

- Window scales to accommodate different screen resolutions (#10)

## [0.2.0] - 2024-10-23

### Added

- Constraints to the snake's spawn position and direction (#11)

## [0.1.2] - 2024-10-18

### Fixed

- Bug where apples spawn on top of the snake (#4)

## [0.1.1] - 2024-10-17

### Fixed

- Snake no longer able to immediately revert its movement direction (#3)

## [0.1.0] - 2024-10-01

### Added

- Initial code imported code code from KobraPy.


Added
Changed
Deprecated
Removed
Fixed
Security

MAJOR.MINOR.PATCH
    MAJOR version when you make incompatible API changes
    MINOR version when you add functionality in a backward compatible manner
    PATCH version when you make backward compatible bug fixes
