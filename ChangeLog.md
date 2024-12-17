---
SPDX-FileCopyrightText: 2023 Monaco F. J. <monaco@usp.br>
SPDX-FileCopyrightText: 2024 Coral authors <git@github.com/courselab/coral>
SPDX-License-Identifier: GPL-3.0-or-later
---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Generated binary for Linux running in x86-64 architecture(#220)
- Licensing compatible with the SPDX specification (#145)
- Static obstacles to the map (PR #160)
- Ability to make the snake "run" by pressing space bar (#84)
- Support for multiple languages(#141)
- Oranges as a variety of fruit that increases the snake (#93)
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

- Bug where apples spawn on top of the snake (#4)
- Snake no longer able to immediately revert its movement direction (#3)

## [0.1.0] - 2024-10-01

### Added

- Initial code imported code code from KobraPy.
