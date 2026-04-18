#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT_DIR"

STATUS_FILE=".delivery/STATUS.md"

fail() {
  echo "$1" >&2
  exit 1
}

last_pass=$(awk -F'\\|' '/^\| Last completed pass ID / { value=$3; gsub(/^ +| +$/, "", value); gsub(/`/, "", value); print value; exit }' "$STATUS_FILE")
[ -n "$last_pass" ] || fail "Missing Last completed pass ID in $STATUS_FILE"

snapshot_date=$(perl -ne 'if (/^Snapshot date: `([^`]+)`$/) { print "$1\n"; exit }' "$STATUS_FILE")
[ -n "$snapshot_date" ] || fail "Missing Snapshot date in $STATUS_FILE"

current_tranche=$(awk -F'\\|' '/^\| Current tranche / { value=$3; gsub(/^ +| +$/, "", value); print value; exit }' "$STATUS_FILE")
[ -n "$current_tranche" ] || fail "Missing Current tranche in $STATUS_FILE"

current_recommendation=$(awk -F'\\|' '/^\| Current recommendation / { value=$3; gsub(/^ +| +$/, "", value); gsub(/`/, "", value); print value; exit }' "$STATUS_FILE")
[ -n "$current_recommendation" ] || fail "Missing Current recommendation in $STATUS_FILE"

page_types=$(awk '
  /^### By Page Type$/ { mode="type"; next }
  /^### By Maturity$/ { mode="" }
  mode=="type" && /^- `/ {
    if (out != "") out = out ", "
    split($0, parts, "`")
    value = $0
    sub(/^.*: /, "", value)
    out = out parts[2] " " value
  }
  END { print out }
' "$STATUS_FILE")
[ -n "$page_types" ] || fail "Missing page-type counts in $STATUS_FILE"

maturity_counts=$(awk '
  /^### By Maturity$/ { mode="mat"; next }
  /^### / && mode=="mat" { mode="" }
  /^## / && mode=="mat" { mode="" }
  mode=="mat" && /^- `/ {
    if (out != "") out = out ", "
    split($0, parts, "`")
    value = $0
    sub(/^.*: /, "", value)
    out = out parts[2] " " value
  }
  END { print out }
' "$STATUS_FILE")
[ -n "$maturity_counts" ] || fail "Missing maturity counts in $STATUS_FILE"

gap_counts=$(awk -F'\\|' '
  /^\| `G-[0-9][0-9]` / {
    status=$6
    gsub(/^ +| +$/, "", status)
    if (status == "Open") open++
    else if (status == "Closed") closed++
    else if (status == "Active") active++
    else if (status == "Deferred") deferred++
  }
  END { print open+0 "\t" closed+0 "\t" active+0 "\t" deferred+0 }
' "$STATUS_FILE")
open_gaps=$(printf '%s\n' "$gap_counts" | awk -F'\t' '{print $1}')
closed_gaps=$(printf '%s\n' "$gap_counts" | awk -F'\t' '{print $2}')

next_queue=$(awk '
  /^## Next Queue$/ { mode=1; next }
  /^## / && mode==1 { mode=0 }
  mode==1 && /^[0-9]+\./ {
    split($0, parts, "`")
    if (parts[2] != "" && count < 5) {
      queue[++count] = parts[2]
    }
  }
  END {
    for (i = 1; i <= count; i++) {
      if (i > 1) printf ", "
      printf "%s", queue[i]
    }
    printf "\n"
  }
' "$STATUS_FILE")
[ -n "$next_queue" ] || fail "Missing next queue in $STATUS_FILE"

printf '%s\n' "delivery harness status"
printf '%s\n' "snapshot date: $snapshot_date"
printf '%s\n' "last completed pass: $last_pass"
printf '%s\n' "current tranche: $current_tranche"
printf '%s\n' "recommendation: $current_recommendation"
printf '\n'
printf '%s\n' "counts"
printf '%s\n' "page types: $page_types"
printf '%s\n' "maturity: $maturity_counts"
printf '\n'
printf '%s\n' "gaps"
printf '%s\n' "open: $open_gaps"
printf '%s\n' "closed: $closed_gaps"
printf '%s\n' "next: $next_queue"
