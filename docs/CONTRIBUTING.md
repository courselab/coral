
Contributing to Coral
==============================
 
 Coral is open source and you are welcome and encouraged to contribute.

 These are a few guidelines.

 Contribution workflow
 ------------------------------

 The official Coral repository is at https://github.com/monaco/kobrapy
   
 To start contributing, make sure you've read the essential documentation
 thoroughly:

    - `docs/exercise-directions.md`      
    - `docs/CONTRIBUTING.md`             

 Then, go through the following steps.

 1. Open an issue at the repository explaining the problem
 
    or suggestion you are addressing.

 2. If you want to contribute a solution for your (or anyone else's) issue:

    * fork the project (if you're an external contributor)
    * create a branch for the issue (see branch naming below).
    * edit the code/documentation in that branch
    * run lint check (see 'Developer tools' below)
    * make a pull/merge request (push your branch)
    * go to GitHub and create a PR/MR request

    Do not submit a PR/MR that is not related to an open issue.

 3. Go have a treat—you’ve earned it.

 Project standards
 ------------------------------

 To keep things consistent, when applicable, we aim at some some standards.

 - REUSE specification vr. 3 [1]
 
 - GitFlow branching strategy [2]

 - Semantic versioning 2.0.0 [3]

 Code convention
 ------------------------------

 Oh, that.

 Code convention always tend to be a sensitive topic among programmers as it calls
 forth personal convictions and the weight of beloved traditions. As often,
 preferences vary largely. With that, we humbly as you to be indulgent about the
 choices made in this project.
 
 * Symbol names, comments, file names etc. always in English.

 * Casing, indentation, block alignment etc.: stick to the common conventions.

 * Comments are text. Use caption and punctuation accordingly.


 Attribution and licensing
 ------------------------------

 If you have substantially modified an existing source or documentation
 file --- say it's considerably more than a simple typo correction or
 small bug fix --- you are entitled to have your name added to the copyright
 notice [1] and to the `AUTHORS` file, should you desire.

 By submitting your contribution you agree that it will be available under the
 same license as SYSeg (GNU GPL vr. 3 or later).

 Contribution purpose
 ------------------------------

 When applicable, use the following convention for commit messages and branch
 names:

 PERMANENT BRANCHES

 The repository contains the two GitFlow permanent branches:
 
 - `main`   : the stable branch 
 - `dev`    : the unstable branch (aka `develop`)

 SUPPORT BRANCH NAMES (for PR/MR)

 When creating an ephemeral branch, use the following keywords to indicate the
 branch type:

 - `feat`  : extend of modify feature (GitFlow `feature`)
 - `hot`   : carry on maintenance on former releases  (GitFlow `hotfix`)
 - `rel`   : prepare a new release (GitFlow `release`)
 - `wip`   : work-in-progress branch (unrelated to any issue)
 - `adoc`  : critical maintance bypassing the regular workflow

 For `feat` and `hot` branches, use the scheme

 ```
    <type>/<issue-number>/<short-descriptive-note>
 ```
 Use lowercase alphanumeric ASCII characters, underscores, and hyphens in
 place of spaces. No punctuation.

  Example:

 ```
  feat/42/modify-option-help

  fix/66/crash-on-negative-input

 ```
 It's usually preferrable that the PR/MR be linked to an existing issue.
 Sometimes, however, we admit that ad hoc changes may be pragmatically
 justifiable. In this case, if the PR/MR is not linked to an issue,
 the simplified form
 
  `<purpose>/<short-descriptive-mnemonic>`

 is acceptable (this is most appropriate for 'wip' and 'exp' types).

 For `rel` branches, use `rel/<release-number>`.
 For `wip` and `adhoc`, use `<purpose>/<short-description>`

 COMMIT MESSAGES

 When editing the commit message, use the following keywords, inspired on a 
 lax version of  Conventional Commits [4], to describe the purpose of your
 contribution:
 
 - `code`     :   advance code (add of modify a feature)
 - `fix`      :   fix a bug or an unmeat requirement.
 - `ref`      :   refactor code for quality or compliance
 - `doc`      :   modify or extend documentation
 - `build`    :   improve the build process
 - `repo`     :   tide up the repository and organization
 - `minor`    :   something too simple as typo or cosmetics
 - `other`    :   something else

 The suggested commit messages is

 `<purpose> : short description`

 where 'purpose' is one of the contribution purposes listed above.

 The short description should be in imperative form (fix, add, remove etc.)
 rather than past (fixed, added) or present (fixes, adds) --- as if ordering
 what the change should do (mind the capitalization). Do not punctuate.
 
Example:

 ```
   fix: correct wrong file name

   fix: fix missing semicolon

   doc: update user manual

   repo: removed object files

```
 
 Ideally, each commit should be of only one type. In practice, though,
 it's reasonable to group changes in a single commit if they are naturally
 related (e.g. you modifying a function's argument type and edit the developer
 documentation to reflect the change). In those cases, it's ok to use

 ```
  <purpose 1> : short description 1
  
  <purpose 2> : short description 2
  ...
 ```

 Purpose indication in commit messages is suggested, but not mandatory (if not
 used, capitalize the first letter. Leave a blank line between statements.
 
 If it helps to understand the context, do not refrain from adding a paragraph
 further explaining the commit. This is normal text, so, capitalize and
 punctuate accordingly.
 

 PR/MR MERGING
 
 In the regular workflow, contributions in the form PR/MRs should be submitted
 to the mainstream repository, then analyzed and merged into the destination
 branch. Bypassing the regular protocols is exceptionally acceptable, at the
 discretion of the project maintainers, to address urgent demands such as
 critical repository maintenance or emergency bug fixes.


 OTHER CONVENTIONS

 Compliance to Keep a ChangeLog [5] is under consideration.


References
 ------------------------------

 [1] REUSE Software, https://reuse.software

 [2] GitFlow, https://nvie.com/posts/a-successful-git-branching-model/

 [3] Semantic Versioning, https://semver.org/

 [4] Conventional Commits, https://www.conventionalcommits.org/en/v1.0.0/

 [5] Keep a ChangeLog, https://keepachangelog.com/en/1.0.0/


