# Change Log

## [v1.1.0](https://github.com/thewizardplusplus/git-earliest-date/tree/v1.1.0) (2023-05-27)

Add filtering of the results by person kind (optional) and perform refactoring.

- collecting data:
  - filter the results by person kind (optionally);
  - simplified version (by person kind):
    - for a repository group:
      - earliest simplified repository (may be null);
      - flag indicating that the earliest simplified repository is null;
    - for a repository:
      - repo directory;
      - earliest simplified root commit (may be null);
      - flag indicating that the earliest simplified root commit is null;
    - for a commit:
      - hash (in the hexadecimal format);
      - person;
      - datetime (in the ISO 8601 format);
      - message (may be empty);
- perform refactoring:
  - add the `_select_dirs_by_repo_status()` function;
  - add the `_min_or_none()` function;
  - remove the redundant yield expressions.

## [v1.0.0](https://github.com/thewizardplusplus/git-earliest-date/tree/v1.0.0) (2022-11-05)

Major version.
