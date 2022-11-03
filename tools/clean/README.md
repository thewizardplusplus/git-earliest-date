# clean

The utility for cleaning result data.

## Features

- return only one property &mdash; either `author_earliest_repo` or `committer_earliest_repo` &mdash; as cleaned result data;
- for a repository:
  - hide the `root_commits` and `is_empty_repo` properties;
  - display only one property &mdash; either `author_earliest_root_commit` or `committer_earliest_root_commit` &mdash; as `earliest_root_commit`;
- for a commit:
  - display only one property &mdash; either `author` or `committer` &mdash; as `person`;
  - display only one property &mdash; either `author_datetime` or `committer_datetime` &mdash; as `datetime`.

## Usage

```
$ clean.jq --arg datetime_kind {author,committer}
```

Stdin: result data in the JSON format.

Options:

- `--arg datetime_kind {author,committer}` &mdash; a datetime kind.
