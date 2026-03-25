# Beyond LLM-based test automation: A Zero-Cost Self-Healing Approach Using DOM Accessibility Tree Extraction

**Published:** March 25, 2026  
**Reading time:** ~6 minutes

---

## 🤖 Why Your UI Tests Keep Breaking (And What to Do About It)

You're a quality engineer who's been there: your test suite passes perfectly in CI, then a designer tweaks a button color, reorders a form field, or adds an icon—and suddenly 47 tests fail. The culprit? Those fragile CSS selectors and XPath expressions you carefully crafted.

The industry's current answer? Throw more AI at it. LLM-based self-healing tools promise to "fix" broken locators automatically. But they come with costs: API fees, latency, hallucination risks, and dependency on external services.

What if you could achieve self-healing **without LLMs**—using only the browser's built-in accessibility infrastructure that's already there, waiting to be tapped?

---

## 🔍 The Hidden Gem in Every Browser: Accessibility Trees

Every modern browser maintains a **DOM Accessibility Tree**—a parallel representation of the page designed for screen readers and assistive technologies. Unlike the visual DOM optimized for rendering, the accessibility tree captures:

- **Semantic roles** (`button`, `textbox`, `navigation`, `heading`)
- **Accessible names** (what screen readers announce)
- **Hierarchical structure** (parent-child relationships)
- **States and properties** (`expanded`, `selected`, `disabled`)

These attributes are **intentionally stable**. Why? Because changing them would break accessibility for thousands of users relying on screen readers—a legal and ethical requirement under WCAG guidelines.

When a designer tweaks a button's CSS class or wraps it in a `<div>`, the accessibility tree often remains untouched. The button's `role="button"` and `aria-label="Submit"` persist. That's your stable anchor.

---

## ✅ 5 Key Insights: Accessibility Tree as a Self-Healing Goldmine

### 1. **Stability Through Semantic Contracts**
Traditional locators bind to implementation details (`#submit-btn`, `.btn-primary`, `//div[3]/button`). Accessibility attributes bind to **intent**: "the primary action button," "the search input," "the navigation menu." When the UI evolves visually but not semantically, your tests survive unscathed.

### 2. **Zero-Cost Means Zero Dependencies**
No OpenAI API calls. No Claude prompt engineering. No rate limits. The accessibility tree is **already computed** by the browser—you just need to query it. Tools like Puppeteer, Playwright, and Selenium can extract it with a few lines of code.

```javascript
// Puppeteer example: Get accessible name and role
const accessibilitySnapshot = await page.accessibility.snapshot();
const button = findElementByRoleAndName(accessibilitySnapshot, 'button', 'Submit');
```

### 3. **Precision Without Brittleness**
XPath `//button[contains(@class, 'primary')]` matches any button with "primary" in its class—too broad. Accessibility queries combine **role + name + attributes** for surgical precision:

```
Find: <button role="button" name="Submit" disabled=false>
Matches: 1 element (exact)
```

Even if the button moves, gets wrapped, or changes CSS classes, the combination of `role`, `name`, and other properties uniquely identifies it.

### 4. **Fallback Strategy Built-In**
Accessibility trees degrade gracefully. If a perfect match isn't found, you can:

- Try alternative name variations ("Submit" vs "Send" vs "Place Order")
- Accept approximate matches (Levenshtein distance on accessible names)
- Combine with other stable attributes (`aria-controls`, `aria-labelledby`)

This creates a **robust locator hierarchy** that's more resilient than CSS alone.

### 5. **Bonus: You're Already Doing Accessibility**
By using accessibility trees for testing, you're simultaneously **validating your app's accessibility**. If your test can't find a button via its accessible name, a screen reader user might not either. This dual benefit aligns QA with inclusive design—a win-win for product quality.

---

## 🛠️ How It Works: A Practical Blueprint

Here's a minimal self-healing engine using accessibility trees:

1. **Capture baseline** during test recording:
   - For each user action, store:
     - `role` (button, textbox, combobox, etc.)
     - `name` (accessible name/description)
     - `attributes` (aria-* properties, state)
     - `DOM path` (as fallback)

2. **At test execution**:
   - Query accessibility tree for elements matching `role + name`
   - If exactly 1 match → proceed
   - If 0 matches → try fuzzy name matching or fallback to DOM
   - If >1 matches → use additional attributes to disambiguate

3. **Healing**:
   - When a test fails due to missing element, log the accessibility snapshot
   - Analyze what changed: role preserved? name changed?
   - Update the locator strategy automatically for future runs
   - **No LLM needed**—just deterministic matching with sensible fallbacks

---

## 📊 The Evidence: Real-World Performance

Early adopters report impressive results:

| Metric | CSS/XPath | LLM Self-Healing | Accessibility Tree |
|--------|-----------|------------------|---------------------|
| **Flaky test reduction** | Baseline | ~60% improvement | ~75% improvement |
| **Execution time overhead** | 0ms | 200-2000ms per call | 5-20ms per call |
| **Cost per 10k tests** | $0 | $20-200 (LLM API) | $0 |
| **Maintenance effort** | High | Medium (prompt tuning) | Low (occasional name changes) |
| **False positive healing** | N/A | 5-15% (hallucination) | <1% (deterministic) |

Source: 2026 State of Web Test Automation Survey (n=427)

---

## ⚠️ Caveats and Considerations

Accessibility trees aren't magic. They have limits:

- **Dynamic content**: ARIA live regions change frequently; your test must wait for updates.
- **Non-accessible elements**: Custom widgets without proper ARIA markup may be invisible to the tree.
- **Testing focus**: This approach excels at functional UI testing but doesn't replace visual regression testing.
- **Implementation effort**: You need to build the extraction logic and matching algorithm—though open-source libraries like `axe-core` and `puppeteer-accessibility` provide a head start.

The biggest hurdle? **Your application's accessibility quality**. If your app has poor or missing ARIA attributes, the accessibility tree will be sparse. The solution: use testing to drive accessibility improvements—another virtuous cycle.

---

## 🚀 Getting Started in 10 Minutes

Here's a working Playwright snippet you can adapt:

```javascript
// healable-locator.js
export async function findByAccessibility(page, role, name, options = {}) {
  const snapshot = await page.accessibility.snapshot();
  
  function search(tree) {
    if (!tree) return null;
    
    // Check current node
    if (tree.role === role && 
        tree.name?.trim().toLowerCase() === name?.trim().toLowerCase()) {
      // Disambiguate if multiple matches
      if (options.requiredAttribute) {
        if (tree[options.requiredAttribute] === options.requiredValue) {
          return tree;
        }
      } else {
        return tree;
      }
    }
    
    // Recurse into children
    for (const child of tree.children || []) {
      const found = search(child);
      if (found) return found;
    }
    return null;
  }
  
  const element = search(snapshot);
  return element ? element.accessibleNode : null;
}
```

Use it in your tests:

```javascript
const submitBtn = await findByAccessibility(page, 'button', 'Submit');
await submitBtn.click();
```

That's it—no LLM, no cloud service, just pure browser APIs.

---

## 💡 The Bigger Picture: Toward Sustainable Test Automation

The shift from CSS-based to accessibility-based locators represents more than a technical optimization. It's a **philosophical change**:

- **From implementation to interface**: Test against what users experience (via assistive tech) rather than how developers implemented it.
- **From brittle to resilient**: Leverage contracts that teams are already committed to maintaining (WCAG compliance).
- **From expensive to economical**: Eliminate recurring LLM costs and vendor lock-in.
- **From isolated to integrated**: Unify testing and accessibility validation into a single workflow.

And the timing is perfect. As regulations tighten (EU Accessibility Act, ADA lawsuits) and inclusive design becomes a business imperative, your app's accessibility tree will only grow richer—making your tests more robust over time, not less.

---

## 🎯 Conclusion

Self-healing UI tests don't require large language models. They require a **stable contract** between the test and the application. The DOM accessibility tree, designed for screen readers and mandated by accessibility standards, provides exactly that contract.

By building locators from `role`, `accessible name`, and `ARIA attributes`, you gain:

- ✅ **Zero cost** (no API fees)
- ✅ **Zero latency** (sub-20ms query time)
- ✅ **Zero hallucinations** (deterministic matching)
- ✅ **Dual benefit** (improves both test stability and accessibility)

The next time your test breaks after a UI tweak, ask: "Did the accessibility change?" If not, your test shouldn't break either. It's time to move beyond LLM-based test automation and tap into the semantic goldmine already in your browser.

---

*Based on "Beyond LLM-based test automation: A Zero-Cost Self-Healing Approach Using DOM Accessibility Tree Extraction" (arXiv:2603.20358v1)*