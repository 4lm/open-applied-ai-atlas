#!/bin/sh
set -eu

# Validation gate for delivery-harness consistency. Keep success output minimal
# and use scripts/delivery-harness-status.sh for human-readable status snapshots.

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT_DIR"

STATUS_FILE=".delivery/STATUS.md"
AUDIT_FILE=".delivery/page-audit.md"

tmp_counts=$(mktemp)
tmp_snapshot=$(mktemp)
tmp_gap_ids=$(mktemp)
tmp_pass_ids=$(mktemp)
trap 'rm -f "$tmp_counts" "$tmp_snapshot" "$tmp_gap_ids" "$tmp_pass_ids"' EXIT

perl -e '
use strict;
use warnings;
my (%type,%mat);
for my $f (glob("docs/*/*.md")) {
  open my $fh, "<", $f or die $!;
  while (my $line = <$fh>) {
    if ($line =~ /^_Page Type: (.+) \| Maturity: (.+)_$/) {
      $type{$1}++;
      $mat{$2}++;
      last;
    }
  }
  close $fh;
}
print "TYPE\n";
for my $k (sort keys %type) { print "$k\t$type{$k}\n"; }
print "MATURITY\n";
for my $k (sort keys %mat) { print "$k\t$mat{$k}\n"; }
' > "$tmp_counts"

perl -ne '
BEGIN { $mode = "" }
if (/^### By Page Type$/) { $mode = "type"; next }
if (/^### By Maturity$/) { $mode = "mat"; next }
if (/^### / || /^## /) { $mode = "" }
if ($mode ne "" && /^- `([^`]+)`: ([0-9]+)$/) {
  print "$1\t$2\n";
}
' "$STATUS_FILE" > "$tmp_snapshot"

while IFS="$(printf '\t')" read -r key value; do
  [ -n "$key" ] || continue
  if ! grep -Fxq "$key	$value" "$tmp_snapshot"; then
    echo "Count drift: $key expected $value in $STATUS_FILE audit snapshot" >&2
    exit 1
  fi
done <<EOF
$(awk '
BEGIN { mode="" }
$0=="TYPE" { mode="type"; next }
$0=="MATURITY" { mode="mat"; next }
mode=="type" { print $0 }
mode=="mat" { print $0 }
' "$tmp_counts")
EOF

awk '
/^\| `G-[0-9][0-9]` / {
  id=$2
  gsub(/`/, "", id)
  print id
}
(/^### `20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]\.[a-z]`$/) {
  id=$2
  gsub(/`/, "", id)
  print id > "'"$tmp_pass_ids"'"
}
' "$STATUS_FILE" > "$tmp_gap_ids"

awk -F'\\|' '
NR <= 13 { next }
/^\| `docs\// {
  path=$2; gsub(/^ +| +$/, "", path); gsub(/`/, "", path)
  gap=$6; gsub(/^ +| +$/, "", gap)
  pass=$7; gsub(/^ +| +$/, "", pass)
  if (gap == "") {
    print "Missing Primary Gap ID for " path > "/dev/stderr"
    exit 1
  }
  cmd = "grep -Fxq \"" gap "\" '"$tmp_gap_ids"'"
  if (system(cmd) != 0) {
    print "Unknown gap ID " gap " for " path > "/dev/stderr"
    exit 1
  }
  if (pass != "") {
    cmd = "grep -Fxq \"" pass "\" '"$tmp_pass_ids"'"
    if (system(cmd) != 0) {
      print "Unknown pass ID " pass " for " path > "/dev/stderr"
      exit 1
    }
  }
}
' "$AUDIT_FILE"

awk -F'\\|' '
/^\| `G-[0-9][0-9]` / {
  gap=$2; gsub(/^ +| +$/, "", gap); gsub(/`/, "", gap)
  status=$6; gsub(/^ +| +$/, "", status)
  closed=$10; gsub(/^ +| +$/, "", closed); gsub(/`/, "", closed)
  if (status == "Closed" && closed == "") {
    print "Closed gap " gap " is missing Closed by pass in " FILENAME > "/dev/stderr"
    exit 1
  }
  if (closed != "") {
    cmd = "grep -Fxq \"" closed "\" '"$tmp_pass_ids"'"
    if (system(cmd) != 0) {
      print "Unknown Closed by pass " closed " for gap " gap > "/dev/stderr"
      exit 1
    }
  }
}
' "$STATUS_FILE"

awk -F'\\|' '
/^\| `G-[0-9][0-9]` / {
  gap=$2; gsub(/^ +| +$/, "", gap); gsub(/`/, "", gap)
  status=$6; gsub(/^ +| +$/, "", status)
  if (status == "Closed") {
    closed[gap]=1
  }
}
END {
  for (g in closed) {
    print g
  }
}
' "$STATUS_FILE" | while IFS= read -r gap; do
  [ -n "$gap" ] || continue
  if awk -F'\\|' -v gap="$gap" '
    /^\| `docs\// {
      action=$5; gsub(/^ +| +$/, "", action)
      rowgap=$6; gsub(/^ +| +$/, "", rowgap)
      if (rowgap == gap && action != "Keep") {
        exit 1
      }
    }
  ' "$AUDIT_FILE"; then
    :
  else
    echo "Closed gap $gap still has non-Keep page rows in $AUDIT_FILE" >&2
    exit 1
  fi
done

echo "delivery harness check: OK"
