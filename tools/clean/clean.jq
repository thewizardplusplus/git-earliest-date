#!/usr/bin/env -S jq -f

$ARGS.named.datetime_kind as $datetime_kind
| if $datetime_kind == null then
  error("datetime kind is required")
else
  . # TODO: use the short form as of the next jq version
end
| if $datetime_kind | IN(["author", "committer"][]) | not then
  error(@json "unknown datetime kind \($datetime_kind)")
else
  . # TODO: use the short form as of the next jq version
end

| .[$datetime_kind + "_earliest_repo"] as $earliest_repo
| $earliest_repo | .[$datetime_kind + "_earliest_root_commit"] as $earliest_root_commit
| {
  repo_dir: $earliest_repo | .repo_dir,
  earliest_root_commit: {
    hash: $earliest_root_commit | .hash,
    person: $earliest_root_commit | .[$datetime_kind],
    datetime: $earliest_root_commit | .[$datetime_kind + "_datetime"],
    message: $earliest_root_commit | .message,
  },
}
