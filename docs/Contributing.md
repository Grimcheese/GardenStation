# Contributing to GardenStation
This project is my own personal project and I don't expect any outside contributes however this document will give a brief rundown on how I intend to manage contributions to this project (This includes how I make changes and add new features).


# Project Workflow
Any new work or fix should begin with an issue created on the github repo's page. Whenever a bug becomes apparent or there is a new feature idea to implement an issue must be created to describe the fix/feature, what the goal is, and how it should be implemented. The issue can then have a history for any discussion or updates related to it. From an issue, I can assign myself to work on it and then begin work on a new branch with the issue number and name (e.g. The branch name for Example Issue #1 would be 1-example-issue).

The main branch is protected and cannot be pushed to directly, new changes must be submitted via pull requests. 

Pull requests trigger a Github workflow to run pytest on the merged code to ensure that the build will continue to work once the pull request is merged into main. It will also create a new issue requesting documentation for the new feature being implemented to ensure that the wiki is kept up to date as development progresses.

## Versions
GardenStation follows the Semantic Versioning format of X.X.X (Major.Minor.Patch). Due to the sporadic nature of development on this project version numbers are not tied to any interval of time, instead they are only related to new changes and their perceived scale of change (Represent a new release, minor change within a release, or a new change to the code base). Where each update to main from a pull request can represent an increment to the patch portion of the version number. 

Changes to the documentation or wiki are not considered in the version numbering.

ALL pre 1.0.0 versions are considered as 'in-development'.

# Misc