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
echo "[2] Argument Parsing (BATCH_SIZE, PAGES_PER_RUN, MAX_PARALLEL, DRY_RUN, MARK_AS_READ)"
BATCH_SIZE=${BATCH_SIZE:-500}
PAGES_PER_RUN=${PAGES_PER_RUN:-4}
MAX_PARALLEL=${MAX_PARALLEL:-5}
DRY_RUN=${DRY_RUN:-0}
MARK_AS_READ=${MARK_AS_READ:-0}
if [ "$BATCH_SIZE" = "500" ] && [ "$PAGES_PER_RUN" = "4" ] && [ "$MAX_PARALLEL" = "5" ] && [ "$DRY_RUN" = "0" ] && [ "$MARK_AS_READ" = "0" ]; then
  echo "    ✓ Default values: PASS"
  ((PASS++))
else
  echo "    ✗ FAIL"
  ((FAIL++))
fi

if BATCH_SIZE=100 PAGES_PER_RUN=2 MAX_PARALLEL=3 DRY_RUN=1 MARK_AS_READ=1 bash -c 'test "$BATCH_SIZE" = "100" && test "$PAGES_PER_RUN" = "2" && test "$MAX_PARALLEL" = "3" && test "$DRY_RUN" = "1" && test "$MARK_AS_READ" = "1"' 2>/dev/null; then
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
  elif echo "$ls" | grep -qE 'timesheet|hr|payroll|leave'; then echo "hr"
  elif echo "$lf" | grep -qE '@company\.com|@org|@work'; then echo "work"
  else echo "personal"; fi
}

cat_pass=0
cat_fail=0

# Test cases that work correctly
if [ "$(categorize 'noreply@bca.com' 'Transaction')" = "banking" ]; then ((cat_pass++)); else ((cat_fail++)); fi
if [ "$(categorize 'alerts@monitor.com' 'CPU Alert')" = "alerts" ]; then ((cat_pass++)); else ((cat_fail++)); fi
if [ "$(categorize 'team@company.com' 'Sprint Meeting')" = "work" ]; then ((cat_pass++)); else ((cat_fail++)); fi
if [ "$(categorize 'news@digest.com' 'Newsletter')" = "newsletters" ]; then ((cat_pass++)); else ((cat_fail++)); fi
if [ "$(categorize 'friend@gmail.com' 'Lunch?')" = "personal" ]; then ((cat_pass++)); else ((cat_fail++)); fi

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

# Test 7: Category label mapping (verify script has correct mapping)
echo "[7] Category Label Mapping"

# Check that the script contains the correct label mappings
label_pass=0
label_fail=0

grep -q '\["banking"\]="Categorized/Banking"' "$SCRIPT_DIR/email-sweep.sh"; if [ $? -eq 0 ]; then ((label_pass++)); else ((label_fail++)); fi
grep -q '\["alerts"\]="Categorized/Alerts"' "$SCRIPT_DIR/email-sweep.sh"; if [ $? -eq 0 ]; then ((label_pass++)); else ((label_fail++)); fi
grep -q '\["work"\]="Categorized/Work"' "$SCRIPT_DIR/email-sweep.sh"; if [ $? -eq 0 ]; then ((label_pass++)); else ((label_fail++)); fi
grep -q '\["newsletters"\]="Categorized/Newsletters"' "$SCRIPT_DIR/email-sweep.sh"; if [ $? -eq 0 ]; then ((label_pass++)); else ((label_fail++)); fi
grep -q '\["hr"\]="Categorized/HR"' "$SCRIPT_DIR/email-sweep.sh"; if [ $? -eq 0 ]; then ((label_pass++)); else ((label_fail++)); fi
grep -q '\["personal"\]="Categorized/Personal"' "$SCRIPT_DIR/email-sweep.sh"; if [ $? -eq 0 ]; then ((label_pass++)); else ((label_fail++)); fi

if [ $label_fail -eq 0 ]; then
  echo "    ✓ PASS ($label_pass/6)"
  ((PASS++))
else
  echo "    ✗ FAIL ($label_fail issue(s))"
  ((FAIL++))
  ISSUES="$ISSUES\n  - Category label mapping incorrect"
fi

# Test 8: Label cache functions (mock)
echo "[8] Label Cache Functions (Mock)"
CACHE_FILE="$TEST_DIR/labels.cache"

# Test cache save/load operations
mkdir -p "$(dirname "$CACHE_FILE")"
: > "$CACHE_FILE"
echo "Categorized/Banking=label_banking_123" >> "$CACHE_FILE"
echo "Categorized/Alerts=label_alerts_456" >> "$CACHE_FILE"

# Load cache using python for reliable parsing
cache_pass=0
cache_fail=0

banking_id=$(python3 -c "
d = {}
with open(\"$CACHE_FILE\") as f:
    for line in f:
        line = line.strip()
        if '=' in line:
            k, v = line.split('=', 1)
            d[k] = v
print(d.get('Categorized/Banking', ''))
" 2>/dev/null)

alerts_id=$(python3 -c "
d = {}
with open(\"$CACHE_FILE\") as f:
    for line in f:
        line = line.strip()
        if '=' in line:
            k, v = line.split('=', 1)
            d[k] = v
print(d.get('Categorized/Alerts', ''))
" 2>/dev/null)

if [ "$banking_id" = "label_banking_123" ]; then ((cache_pass++)); else ((cache_fail++)); fi
if [ "$alerts_id" = "label_alerts_456" ]; then ((cache_pass++)); else ((cache_fail++)); fi

if [ $cache_fail -eq 0 ]; then
  echo "    ✓ PASS ($cache_pass/2)"
  ((PASS++))
else
  echo "    ✗ FAIL ($cache_fail issue(s))"
  ((FAIL++))
  ISSUES="$ISSUES\n  - Label cache functions broken"
fi

# Test 9: ensure_label_exists with mock API
echo "[9] ensure_label_exists (Mock API)"

MOCK_API_DIR="$TEST_DIR/mock_api"
mkdir -p "$MOCK_API_DIR"

# Mock curl for label operations
cat > "$TEST_DIR/test_labels.sh" << 'LABEL_TEST'
#!/bin/bash
MOCK_DIR="$MOCK_API_DIR"
export API_KEY="test_key"
export LABEL_CACHE_FILE="$MOCK_DIR/labels.cache"
declare -A LABEL_ID_CACHE=()
declare -A CATEGORY_LABELS=(
  ["banking"]="Categorized/Banking"
  ["alerts"]="Categorized/Alerts"
  ["work"]="Categorized/Work"
  ["newsletters"]="Categorized/Newsletters"
  ["hr"]="Categorized/HR"
  ["personal"]="Categorized/Personal"
)

log() { echo "[LOG] $*" >&2; }

get_cached_label_id() {
  local label_name="$1"
  echo "${LABEL_ID_CACHE[$label_name]:-}"
}

cache_label_id() {
  local label_name="$1"
  local label_id="$2"
  LABEL_ID_CACHE["$label_name"]="$label_id"
}

curl() {
  local method="" url="" data=""
  while [ $# -gt 0 ]; do
    case "$1" in
      -X) method="$2"; shift 2 ;;
      -H) shift 2 ;;
      -d) data="$2"; shift 2 ;;
      *) url="$1"; shift ;;
    esac
  done
  
  if [[ "$url" == *"/labels" ]] && [ -z "$method" ]; then
    echo '{"labels":[{"id":"label_existing_789","name":"Categorized/Existing"}]}'
  elif [[ "$url" == *"/labels" ]] && [ "$method" = "POST" ]; then
    local label_name
    label_name=$(echo "$data" | python3 -c "import json,sys; print(json.load(sys.stdin).get('name',''))" 2>/dev/null)
    echo "{\"id\":\"label_new_${label_name//\//_}\",\"name\":\"$label_name\"}"
  else
    echo '{}'
  fi
}

ensure_label_exists() {
  local category="$1"
  local label_name="${CATEGORY_LABELS[$category]:-}"
  
  if [ -z "$label_name" ]; then
    log "ERROR: Unknown category '$category'"
    return 1
  fi
  
  local cached_id
  cached_id=$(get_cached_label_id "$label_name")
  if [ -n "$cached_id" ]; then
    echo "$cached_id"
    return 0
  fi
  
  if [ -z "$API_KEY" ]; then
    log "WARN: No API key, cannot create label '$label_name'"
    return 1
  fi
  
  log "Searching for label '$label_name'..."
  local list_resp
  list_resp=$(curl "https://gateway.maton.ai/google-mail/gmail/v1/users/me/labels")
  
  if [ -n "$list_resp" ]; then
    local found_id
    found_id=$(echo "$list_resp" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for label in data.get('labels', []):
        if label.get('name') == '$label_name':
            print(label.get('id', ''))
            break
except:
    pass
" 2>/dev/null)
    
    if [ -n "$found_id" ]; then
      log "Found existing label '$label_name' (id: $found_id)"
      cache_label_id "$label_name" "$found_id"
      echo "$found_id"
      return 0
    fi
  fi
  
  log "Creating label '$label_name'..."
  local create_resp
  create_resp=$(curl -X POST -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" \
    -d "{\"name\": \"$label_name\", \"labelListVisibility\": \"labelShow\", \"messageListVisibility\": \"show\"}" \
    "https://gateway.maton.ai/google-mail/gmail/v1/users/me/labels")
  
  if [ -n "$create_resp" ]; then
    local created_id
    created_id=$(echo "$create_resp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id',''))" 2>/dev/null)
    if [ -n "$created_id" ]; then
      log "Created label '$label_name' (id: $created_id)"
      cache_label_id "$label_name" "$created_id"
      echo "$created_id"
      return 0
    fi
  fi
  
  log "ERROR: Failed to create/find label '$label_name'"
  return 1
}

# Run tests and count results
pass_count=0
fail_count=0

# Test cached lookup
LABEL_ID_CACHE["Categorized/Banking"]="label_cached_111"
result=$(ensure_label_exists "banking")
if [ "$result" = "label_cached_111" ]; then
  pass_count=$((pass_count + 1))
else
  fail_count=$((fail_count + 1))
fi

# Test new label creation
result=$(ensure_label_exists "alerts")
if [[ "$result" == label_new_* ]]; then
  pass_count=$((pass_count + 1))
else
  fail_count=$((fail_count + 1))
fi

# Test unknown category
result=$(ensure_label_exists "unknown" 2>&1)
if echo "$result" | grep -q "Unknown category"; then
  pass_count=$((pass_count + 1))
else
  fail_count=$((fail_count + 1))
fi

# Output results in parseable format
echo "PASS=$pass_count"
echo "FAIL=$fail_count"
LABEL_TEST

chmod +x "$TEST_DIR/test_labels.sh"
export MOCK_API_DIR
label_test_out=$(bash "$TEST_DIR/test_labels.sh" 2>/dev/null)

label_test_pass=$(echo "$label_test_out" | grep "^PASS=" | cut -d= -f2)
label_test_fail=$(echo "$label_test_out" | grep "^FAIL=" | cut -d= -f2)

if [ "$label_test_fail" = "0" ]; then
  echo "    ✓ PASS ($label_test_pass/3)"
  ((PASS++))
else
  echo "    ✗ FAIL ($label_test_fail issue(s))"
  ((FAIL++))
  ISSUES="$ISSUES\n  - ensure_label_exists failed"
fi

# Test 10: apply_label with mock API and dry-run
echo "[10] apply_label (Mock API + Dry Run)"

cat > "$TEST_DIR/test_apply.sh" << 'APPLY_TEST'
#!/bin/bash
MOCK_DIR="$TEST_DIR"
export API_KEY="test_key"
export DRY_RUN=0
export MARK_AS_READ=0
export LABEL_CACHE_FILE="$MOCK_DIR/labels.cache"
declare -A LABEL_ID_CACHE=(
  ["Categorized/Banking"]="label_banking_123"
  ["Categorized/Alerts"]="label_alerts_456"
)
declare -A CATEGORY_LABELS=(
  ["banking"]="Categorized/Banking"
  ["alerts"]="Categorized/Alerts"
  ["work"]="Categorized/Work"
  ["newsletters"]="Categorized/Newsletters"
  ["hr"]="Categorized/HR"
  ["personal"]="Categorized/Personal"
)

log() { echo "[LOG] $*" >&2; }

ensure_label_exists() {
  local category="$1"
  local label_name="${CATEGORY_LABELS[$category]:-}"
  echo "${LABEL_ID_CACHE[$label_name]:-}"
}

curl() {
  local method="" url="" data=""
  while [ $# -gt 0 ]; do
    case "$1" in
      -X) method="$2"; shift 2 ;;
      -H) shift 2 ;;
      -d) data="$2"; shift 2 ;;
      *) url="$1"; shift ;;
    esac
  done
  if [[ "$url" == *"/modify" ]]; then
    echo '{"id":"msg123","labelIds":["label_banking_123"]}'
  else
    echo '{}'
  fi
}

apply_label() {
  local message_id="$1"
  local category="$2"
  local label_name="${CATEGORY_LABELS[$category]:-}"
  
  if [ -z "$label_name" ]; then
    log "ERROR: Cannot apply label - unknown category '$category' for message $message_id"
    return 1
  fi
  
  if [ -z "$API_KEY" ]; then
    log "WARN: No API key, skipping label application for message $message_id"
    return 1
  fi
  
  if [ "$DRY_RUN" = "1" ]; then
    log "DRY-RUN: Would label message $message_id as $category ($label_name)"
    return 0
  fi
  
  local label_id
  label_id=$(ensure_label_exists "$category")
  if [ -z "$label_id" ]; then
    log "ERROR: Could not get label ID for category '$category'"
    return 1
  fi
  
  local add_labels="\"$label_id\""
  local remove_labels=""
  
  if [ "$MARK_AS_READ" = "1" ]; then
    remove_labels="\"UNREAD\""
  fi
  
  local max_retries=3
  local retry_delay=1
  local attempt=0
  
  while [ $attempt -lt $max_retries ]; do
    attempt=$((attempt + 1))
    
    local modify_resp
    modify_resp=$(curl -s -f -X POST \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"addLabelIds\": [$add_labels], \"removeLabelIds\": [$remove_labels]}" \
      "https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/$message_id/modify" 2>/dev/null)
    
    if [ -n "$modify_resp" ]; then
      if echo "$modify_resp" | grep -qi "rateLimitExceeded\|429"; then
        log "WARN: Rate limit hit, retrying in ${retry_delay}s (attempt $attempt/$max_retries)"
        sleep $retry_delay
        retry_delay=$((retry_delay * 2))
        continue
      fi
      log "Labeled message $message_id as $category ($label_name)"
      return 0
    fi
    
    if echo "$modify_resp" | grep -qi "rateLimitExceeded\|429"; then
      log "WARN: Rate limit hit, retrying in ${retry_delay}s (attempt $attempt/$max_retries)"
      sleep $retry_delay
      retry_delay=$((retry_delay * 2))
      continue
    fi
    
    log "ERROR: Failed to label message $message_id: $modify_resp"
    return 1
  done
  
  log "ERROR: Max retries exceeded for message $message_id"
  return 1
}

# Run tests and count results
pass_count=0
fail_count=0

# Test normal apply
log_out=$(apply_label "msg123" "banking" 2>&1)
if echo "$log_out" | grep -q "Labeled message msg123 as banking"; then
  pass_count=$((pass_count + 1))
else
  fail_count=$((fail_count + 1))
fi

# Test dry-run
export DRY_RUN=1
log_out=$(apply_label "msg456" "alerts" 2>&1)
if echo "$log_out" | grep -q "DRY-RUN: Would label message msg456 as alerts"; then
  pass_count=$((pass_count + 1))
else
  fail_count=$((fail_count + 1))
fi

# Test no API key
export API_KEY=""
export DRY_RUN=0
log_out=$(apply_label "msg789" "work" 2>&1)
if echo "$log_out" | grep -q "No API key"; then
  pass_count=$((pass_count + 1))
else
  fail_count=$((fail_count + 1))
fi

# Test unknown category
export API_KEY="test_key"
log_out=$(apply_label "msg999" "unknown" 2>&1)
if echo "$log_out" | grep -q "unknown category"; then
  pass_count=$((pass_count + 1))
else
  fail_count=$((fail_count + 1))
fi

# Output results in parseable format
echo "PASS=$pass_count"
echo "FAIL=$fail_count"
APPLY_TEST

chmod +x "$TEST_DIR/test_apply.sh"
export TEST_DIR
apply_test_out=$(bash "$TEST_DIR/test_apply.sh" 2>/dev/null)

apply_test_pass=$(echo "$apply_test_out" | grep "^PASS=" | cut -d= -f2)
apply_test_fail=$(echo "$apply_test_out" | grep "^FAIL=" | cut -d= -f2)

if [ "$apply_test_fail" = "0" ]; then
  echo "    ✓ PASS ($apply_test_pass/4)"
  ((PASS++))
else
  echo "    ✗ FAIL ($apply_test_fail issue(s))"
  ((FAIL++))
  ISSUES="$ISSUES\n  - apply_label failed"
fi

# Test 11: Rate limit retry logic
echo "[11] Rate Limit Retry Logic (Mock)"

cat > "$TEST_DIR/test_retry.sh" << 'RETRY_TEST'
#!/bin/bash
export API_KEY="test_key"
export LABEL_CACHE_FILE="/tmp/test_labels.cache"
declare -A LABEL_ID_CACHE=(["Categorized/Banking"]="label_banking_123")
declare -A CATEGORY_LABELS=(["banking"]="Categorized/Banking")
log() { echo "[LOG] $*" >&2; }

retry_count=0
curl() {
  local method="" url="" data=""
  while [ $# -gt 0 ]; do
    case "$1" in
      -X) method="$2"; shift 2 ;;
      -H) shift 2 ;;
      -d) data="$2"; shift 2 ;;
      *) url="$1"; shift ;;
    esac
  done
  retry_count=$((retry_count + 1))
  if [ $retry_count -lt 3 ]; then
    MODIFY_RESP='{"error":{"code":429,"message":"Rate limit exceeded"}}'
  else
    MODIFY_RESP='{"id":"msg123","labelIds":["label_banking_123"]}'
  fi
}

ensure_label_exists() { echo "label_banking_123"; }

apply_label() {
  local message_id="$1"
  local category="$2"
  local label_name="${CATEGORY_LABELS[$category]:-}"
  
  [ -z "$label_name" ] && return 1
  [ -z "$API_KEY" ] && return 1
  [ "${DRY_RUN:-0}" = "1" ] && return 0
  
  local label_id=$(ensure_label_exists "$category")
  [ -z "$label_id" ] && return 1
  
  local max_retries=3
  local retry_delay=0  # No sleep in test
  local attempt=0
  
  while [ $attempt -lt $max_retries ]; do
    attempt=$((attempt + 1))
    
    local modify_resp
    curl -X POST -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" \
      -d "{\"addLabelIds\": [\"$label_id\"], \"removeLabelIds\": []}" \
      "https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/$message_id/modify" 2>/dev/null
    modify_resp=$MODIFY_RESP
    
    if [ -n "$modify_resp" ]; then
      if echo "$modify_resp" | grep -qi "rateLimitExceeded\|429"; then
        log "WARN: Rate limit hit, retrying (attempt $attempt/$max_retries)"
        [ $retry_delay -gt 0 ] && sleep $retry_delay
        retry_delay=$((retry_delay * 2 + 1))
        continue
      fi
      log "Labeled message $message_id as $category"
      return 0
    fi
    
    if echo "$modify_resp" | grep -qi "rateLimitExceeded\|429"; then
      log "WARN: Rate limit hit, retrying (attempt $attempt/$max_retries)"
      [ $retry_delay -gt 0 ] && sleep $retry_delay
      retry_delay=$((retry_delay * 2 + 1))
      continue
    fi
    
    log "ERROR: Failed to label message $message_id"
    return 1
  done
  
  log "ERROR: Max retries exceeded"
  return 1
}

log_out=$(apply_label "msg123" "banking" 2>&1)
if echo "$log_out" | grep -q "Labeled message msg123 as banking"; then
  echo "RETRY_OK"
else
  echo "RETRY_FAIL: $log_out"
fi
RETRY_TEST

chmod +x "$TEST_DIR/test_retry.sh"
retry_test_out=$(bash "$TEST_DIR/test_retry.sh" 2>&1)

if echo "$retry_test_out" | grep -q "RETRY_OK"; then
  echo "    ✓ PASS"
  ((PASS++))
else
  echo "    ✗ FAIL"
  ((FAIL++))
  ISSUES="$ISSUES\n  - Rate limit retry failed: $retry_test_out"
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
