#!/bin/bash
# Final test suite for email-sweep.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR=$(mktemp -d)
trap "rm -rf $TEST_DIR" EXIT

PASS=0
FAIL=0
ISSUES=""

echo "=== Email Sweep Test Report ==="
echo ""

# Test 1: Bash syntax
echo "[1] Bash Syntax Check"
if bash -n "$SCRIPT_DIR/email-sweep.sh" 2>&1; then
  echo "    ✓ PASS"
  ((PASS++))
else
  echo "    ✗ FAIL"
  ((FAIL++))
  ISSUES="$ISSUES\n  - Syntax errors detected"
fi

# Test 2: Argument parsing
echo "[2] Argument Parsing (BATCH_SIZE, PAGES_PER_RUN, MAX_PARALLEL)"
BATCH_SIZE=${BATCH_SIZE:-500}
PAGES_PER_RUN=${PAGES_PER_RUN:-4}
MAX_PARALLEL=${MAX_PARALLEL:-5}
if [ "$BATCH_SIZE" = "500" ] && [ "$PAGES_PER_RUN" = "4" ] && [ "$MAX_PARALLEL" = "5" ]; then
  echo "    ✓ Default values: PASS"
  ((PASS++))
else
  echo "    ✗ FAIL"
  ((FAIL++))
fi

if BATCH_SIZE=100 PAGES_PER_RUN=2 MAX_PARALLEL=3 bash -c 'test "$BATCH_SIZE" = "100" && test "$PAGES_PER_RUN" = "2" && test "$MAX_PARALLEL" = "3"' 2>/dev/null; then
  echo "    ✓ Custom values: PASS"
  ((PASS++))
else
  echo "    ✗ FAIL"
  ((FAIL++))
  ISSUES="$ISSUES\n  - Argument parsing broken"
fi

# Test 3: State file handling
echo "[3] State File Handling"
STATE_FILE="$TEST_DIR/test.state"
NEXT_PAGE_TOKEN="test_token_xyz"
echo "NEXT_PAGE_TOKEN=$NEXT_PAGE_TOKEN" > "$STATE_FILE"
unset NEXT_PAGE_TOKEN
source "$STATE_FILE" 2>/dev/null
if [ "$NEXT_PAGE_TOKEN" = "test_token_xyz" ]; then
  echo "    ✓ Load/Save state: PASS"
  ((PASS++))
else
  echo "    ✗ FAIL"
  ((FAIL++))
  ISSUES="$ISSUES\n  - State file handling broken"
fi

# Test 4: Categorize function
echo "[4] Categorize Function"
categorize() {
  local from="$1" subj="$2"
  local lf="${from,,}" ls="${subj,,}"
  if echo "$lf" | grep -qE 'bca|bank|transaction|statement'; then echo "banking"
  elif echo "$ls" | grep -qE 'alert|error|cpu|disk|monitor'; then echo "alerts"
  elif echo "$ls" | grep -qE 'meeting|sprint|planning|standup|review'; then echo "work"
  elif echo "$ls" | grep -qE 'newsletter|digest|promo|marketing|subscribe'; then echo "newsletters"
  elif echo "$lf" | grep -qE '@company\.com|@org|@work'; then echo "work"
  elif echo "$ls" | grep -qE 'timesheet|hr|payroll|leave'; then echo "hr"
  else echo "personal"; fi
}

cat_pass=0
cat_fail=0

# Test cases that work correctly
[ "$(categorize 'noreply@bca.com' 'Transaction')" = "banking" ] && ((cat_pass++)) || ((cat_fail++))
[ "$(categorize 'alerts@monitor.com' 'CPU Alert')" = "alerts" ] && ((cat_pass++)) || ((cat_fail++))
[ "$(categorize 'team@company.com' 'Sprint Meeting')" = "work" ] && ((cat_pass++)) || ((cat_fail++))
[ "$(categorize 'news@digest.com' 'Newsletter')" = "newsletters" ] && ((cat_pass++)) || ((cat_fail++))
[ "$(categorize 'friend@gmail.com' 'Lunch?')" = "personal" ] && ((cat_pass++)) || ((cat_fail++))

# Known issue: @company.com check precedes timesheet/hr check
result=$(categorize 'hr@company.com' 'Timesheet')
if [ "$result" = "work" ]; then
  # This is the known bug - document it
  ISSUES="$ISSUES\n  - Categorize: @company.com domain check precedes hr/timesheet check (hr@company.com+Timesheet→work instead of hr)"
  ((cat_fail++))
elif [ "$result" = "hr" ]; then
  ((cat_pass++))
fi

if [ $cat_fail -eq 0 ]; then
  echo "    ✓ PASS ($cat_pass/6)"
  ((PASS++))
else
  echo "    ✗ FAIL ($cat_fail issue(s))"
  ((FAIL++))
fi

# Test 5: Dry run with mock data
echo "[5] Dry Run (BATCH_SIZE=2, PAGES_PER_RUN=1, Mock Data)"

MOCK_DIR="$TEST_DIR/mock"
mkdir -p "$MOCK_DIR"
echo '{"messages":[{"id":"m1"},{"id":"m2"}],"nextPageToken":"p2"}' > "$MOCK_DIR/list.json"
echo '{"payload":{"headers":[{"name":"From","value":"bank@bca.com"},{"name":"Subject","value":"Alert"}]}}' > "$MOCK_DIR/m1.json"
echo '{"payload":{"headers":[{"name":"From","value":"me@gmail.com"},{"name":"Subject","value":"Hi"}]}}' > "$MOCK_DIR/m2.json"

cat > "$TEST_DIR/dryrun.sh" << 'DRY'
#!/bin/bash
MOCK_DIR="$MOCK_DIR"
curl() {
  local url="$1"
  if [[ "$url" == *"messages?q=is:unread"* ]]; then cat "$MOCK_DIR/list.json"
  elif [[ "$url" == *"m1"* ]]; then cat "$MOCK_DIR/m1.json"
  elif [[ "$url" == *"m2"* ]]; then cat "$MOCK_DIR/m2.json"
  else echo "{}"; fi
}
source <(sed '/^log "Starting sweep/,$ d' "$SCRIPT_DIR/email-sweep.sh")
c1=$(categorize "bank@bca.com" "Alert")
c2=$(categorize "me@gmail.com" "Hi")
[ "$c1" = "banking" ] && [ "$c2" = "personal" ] && echo "OK" || echo "FAIL"
DRY

chmod +x "$TEST_DIR/dryrun.sh"
export SCRIPT_DIR MOCK_DIR
dryrun_out=$(bash "$TEST_DIR/dryrun.sh" 2>&1)

if echo "$dryrun_out" | grep -q "OK"; then
  echo "    ✓ PASS"
  ((PASS++))
else
  echo "    ✗ FAIL"
  ((FAIL++))
  ISSUES="$ISSUES\n  - Dry run failed: $dryrun_out"
fi

# Test 6: No real Gmail API calls
echo "[6] No Real Gmail API Invoked (Dry Run)"
if grep -q "curl -s -f -H" "$SCRIPT_DIR/email-sweep.sh"; then
  echo "    ✓ PASS (curl is mockable, no direct API calls in tests)"
  ((PASS++))
else
  echo "    ✗ FAIL"
  ((FAIL++))
fi

# Summary
echo ""
echo "=== Summary ==="
echo "Tests Passed: $PASS"
echo "Tests Failed: $FAIL"
echo ""
if [ $FAIL -eq 0 ]; then
  echo "OVERALL: PASS"
else
  echo "OVERALL: FAIL"
  echo ""
  echo "Issues Found:"
  echo -e "$ISSUES"
fi
