# Architecture Decision Record

## 2024-08-17

printing output to console (not logging) or to files will be done with a visitor pattern

## 2024-08-18
__main__.py should only contain configuration for click
cli_action.py is the implementation for actions triggered by cli
actions.py are the actions with no visible output other than logging that is suitable for library use too.

