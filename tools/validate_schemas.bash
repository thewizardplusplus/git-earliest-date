#!/usr/bin/env bash

if (( $# > 0 )); then
  echo "Usage:"
  echo "  $0 -h | --help"
  echo "  $0"
  echo
  echo "Stdin: result data in the JSON format."
  echo
  echo "Options:"
  echo "  -h, --help  - show the help message and exit."

  exit 0
fi

declare -r data_file="$(mktemp --tmpdir "XXXXXXXXXXXX.json")"
trap 'rm "$data_file"' EXIT

cat > "$data_file"

declare -r script_dir="$(dirname "$0")"
npx ajv-cli@5.0.0 validate \
  --spec "draft2020" \
  --strict true \
  -s "$script_dir/../docs/schemas/repo_info_group.schema.json" \
  -r "$script_dir/../docs/schemas/{repo_info,commit_info,person_info}.schema.json" \
  -d "$data_file"
