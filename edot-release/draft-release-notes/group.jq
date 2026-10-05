# Group the pull requests of a pr-range.sh result into the release-note JSON.
# Labels `dependencies`, `enhancement`, and `bug` are matched case-insensitively.
# `dependencies` wins over the other two; `bug` wins over `enhancement`; a PR
# with none of the three is `uncategorized`.

def has_label($name):
  any(.labels[]?; ascii_downcase == $name);
def item:
  {message: .title, prId: (.number | tostring)};
# Title with every standalone number token removed, so "Bump foo from 1.2 to
# 1.3" and "Bump foo from 1.3 to 1.4" dedupe to one entry, and so do
# Dependabot's major-only "from 4 to 5" and grouped "with 2 updates" titles.
# Digits inside a name such as log4j stay, because they are not standalone.
def dependency_key:
  .title
  | ascii_downcase
  | gsub("\\bv?[0-9]+(\\.[0-9]+)*([-+][0-9a-z.-]+)?\\b"; "")
  | gsub("[[:space:]]+"; " ")
  | gsub("^[[:space:]]+|[[:space:]]+$"; "");
.pullRequests as $included
# Keep the last merged update of each dependency: a later PR with the same
# key replaces the earlier one, in merge order.
| (
    reduce ($included[] | select(has_label("dependencies"))) as $pr
      ([];
        ($pr | dependency_key) as $key
        | map(select(.key != $key))
        + [{key: $key, item: ($pr | item)}])
  ) as $dependencies
| {
    dependencies: [$dependencies[].item],
    featuresEnhancements: [
      $included[]
      | select((has_label("dependencies") or has_label("bug")) | not)
      | select(has_label("enhancement"))
      | item
    ],
    fixes: [
      $included[]
      | select(has_label("dependencies") | not)
      | select(has_label("bug"))
      | item
    ],
    uncategorized: [
      $included[]
      | select(
          (
            has_label("dependencies")
            or has_label("enhancement")
            or has_label("bug")
          )
          | not
        )
      | item
    ]
  }
