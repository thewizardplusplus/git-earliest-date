#!/usr/bin/env bash

declare -r script_name="$(basename "$0")"
# it's necessary to separate the declaration and definition of the variable
# so that the `declare` command doesn't hide an exit code of the defining expression
declare options
options="$(
  getopt \
    --name "$script_name" \
    --options "hs" \
    --longoptions "help,simplified" \
    -- "$@"
)"
if [[ $? != 0 ]]; then
  echo "error: incorrect option" 1>&2
  exit 1
fi

declare simplified=FALSE
eval set -- "$options"
while [[ "$1" != "--" ]]; do
  case "$1" in
    "-h" | "--help")
      echo "Usage:"
      echo "  $script_name -h | --help"
      echo "  $script_name [options]"
      echo
      echo "Stdin: result data in the JSON format."
      echo
      echo "Options:"
      echo "  -h, --help        - show the help message and exit;"
      echo "  -s, --simplified  - validate the simplified version."

      exit 0
      ;;
    "-s" | "--simplified")
      simplified=TRUE
      ;;
  esac

  shift
done

declare schema_prefix=""
if [[ $simplified == TRUE ]]; then
  schema_prefix="simplified_"
fi

declare -r data_file="$(mktemp --tmpdir "XXXXXXXXXXXX.json")"
trap 'rm "$data_file"' EXIT

cat > "$data_file"

declare -r script_dir="$(dirname "$0")"
npx ajv-cli@5.0.0 validate \
  --spec "draft2020" \
  --strict true \
  -s "$script_dir/../../docs/schemas/${schema_prefix}repo_info_group.schema.json" \
  -r "$script_dir/../../docs/schemas/person_info.schema.json" \
  -r "$script_dir/../../docs/schemas/$schema_prefix{repo_info,commit_info}.schema.json" \
  -d "$data_file"
