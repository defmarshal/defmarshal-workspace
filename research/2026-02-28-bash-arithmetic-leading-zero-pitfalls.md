# Bash Arithmetic Pitfalls: Leading Zero "value too great for base" Error

**Generated:** 2026-02-28 02:04 UTC  
**Agent:** research-agent (bug analysis)  
**Topic:** Bash scripting error patterns and fixes  
**Severity:** Medium (non-fatal but noisy; can cause incorrect calculations if unhandled)

---

## Problem Statement

When running bash arithmetic with numbers containing leading zeros (e.g., `08`, `09`), the shell throws:

```
bash: 08: value too great for base (error token is "08")
```

This error appeared in `agents/linkedin-pa-agent.sh` during cycles that ran at 08:xx or 09:xx UTC.

### Observed Impact

- **LinkedIn PA agent:** Warnings logged but cycle continued; content generation unaffected.
- **Root cause:** Bash interprets numbers with leading zeros as **octal** (base-8). Valid octal digits: 0–7. `08` and `09` are invalid octal numbers, hence the error.
- **Frequency:** Hourly cycles at 08:xx and 09:xx UTC produce the error daily.

---

## Technical Explanation

Bash inherits C-language behavior: in arithmetic expansion `$((...))`, any number that begins with `0` is treated as octal.

```bash
$ echo $((08))
bash: 08: value too great for base (error token is "08")
$ echo $((07))  # valid octal
7
$ echo $((010)) # octal 10 = decimal 8
8
```

When you use `date +%H` or `date +%m`, you get two-digit strings with leading zeros (`01`–`12`, `00`–`23`). Using these directly in arithmetic can break at `08` and `09`.

---

## Solutions

### 1. Explicit decimal base with `10#` (recommended)

Prefix the variable or value with `10#` to force base-10 interpretation:

```bash
HOUR=$(date -u +%H)
# Wrong: HOUR_INT=$((HOUR))            # breaks at 08/09
# Good: HOUR_INT=$((10#$HOUR))         # always decimal
```

Works with expressions too:

```bash
INDEX=$(( (10#$DAY_OF_WEEK * 24 + 10#$HOUR) % 6 ))
```

### 2. Strip leading zeros

Remove leading zeros before arithmetic:

```bash
HOUR=$(date -u +%H)
HOUR_NO_ZERO=${HOUR#0}   # removes one leading zero if present
INDEX=$(( DAY_OF_WEEK * 24 + HOUR_NO_ZERO ))
```

Or use `$((10#$value))` which is more concise and handles multi-digit values correctly.

### 3. Use `date +%-H` (GNU date) to omit leading zero

If your environment supports GNU date:

```bash
HOUR=$(date -u +%-H)   # no leading zero
INDEX=$(( DAY_OF_WEEK * 24 + HOUR ))
```

*Portable across Linux, not macOS/BSD.* Use `10#` for maximum portability.

---

## Applied Fix: linkedin-pa-agent.sh

**Location:** Line 31 (as of 2026-02-27)

**Before:**
```bash
HOUR=$(( $(date -u +%H) ))   # breaks at 08, 09
```

**After:**
```bash
HOUR=$((10#$(date -u +%H)))  # forces decimal interpretation
```

This single change eliminates the error for all hours 00–23.

---

## Checklist for Bash Date/Time Arithmetic

When using `date` output in calculations:

- [ ] **Always** use `10#` prefix if the string may have leading zeros
- [ ] Alternatively, use `date +%-H` / `+%-d` / `+%-m` on GNU systems
- [ ] Test your script for hours `08` and `09` (and months `08`–`09`) to verify
- [ ] Avoid using `date +%m` or `%d` directly in arithmetic without conversion

### Common Pitfall Patterns

```bash
# Bad – will break at month 08, 09
MONTH=$(date +%m)
MONTH_PLUS_ONE=$((MONTH + 1))

# Good – force decimal
MONTH=$(date +%m)
MONTH_PLUS_ONE=$((10#$MONTH + 1))

# Good – strip leading zero
MONTH=$(date +%m)
MONTH_PLUS_ONE=$(( ${MONTH#0} + 1 ))
```

---

## Detection & Prevention

Add a lint step to CI to catch unary `0` in arithmetic contexts:

```bash
# Simple grep check
grep -n '\$\((' script.sh | grep -E '[^10#]0[0-9]' && echo "Potential octal trap!"
```

Or use ShellCheck (static analysis tool):

```bash
shellcheck script.sh
# SC2053: Use $(...) instead of backticks in $(...)
# SC2086: Double quote to prevent globbing and word splitting
# Also warns about octal literals
```

---

## Impact Assessment (Our Environment)

- **Affected scripts:** `agents/linkedin-pa-agent.sh` (now fixed)
- **Other candidates:** Scan workspace for `$(( $(date` without `10#`
- **Severity:** Low — error is non-fatal but pollutes logs and may cause wrong arithmetic in edge cases

### Recommended Scan

```bash
grep -rn '\$\((' agents/ research/ scripts/ 2>/dev/null | grep -v '10#' | grep -E '[^a-zA-Z]0[0-9]' || echo "No obvious octal traps"
```

---

## Conclusion

The "value too great for base" error is a classic bash gotcha. The fix is simple: **always use `10#`** when expanding variables that may contain leading zeros. This pattern should be part of every bash coding guideline. With the fix applied in `linkedin-pa-agent.sh`, the hourly LinkedIn PA agent will no longer emit these warnings during 08:xx and 09:xx UTC cycles.

---

## References

- Bash manual: Arithmetic Expansion — numbers with leading `0` are octal
- Stack Overflow: "Value too great for base (error token is "09") in bash"
- Greg's Wiki (Wooledge): ArithmeticExpression — "numbers with leading zeroes are treated as octal"
- Medium article: Explaining “08: value too great for base” in Bash (Pavol Z. Kutaj)

*End of report*
