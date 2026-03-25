```python
#!/usr/bin/env python3
"""
Beyond LLM-based test automation: A Zero-Cost Self-Healing Approach Using DOM Accessibility Tree Extraction

Demonstrates resilient element location using accessibility tree instead of brittle CSS/XPath.
"""

class A11yNode:
    def __init__(self, role, name, children=None, parent=None):
        self.role = role
        self.name = name
        self.children = children or []
        self.parent = parent
        for c in self.children:
            c.parent = self

def find_element(root, target_role, target_name, exact=True):
    """Search accessibility tree for element with given role and name."""
    stack = [root]
    while stack:
        node = stack.pop()
        if node.role == target_role:
            if exact:
                if node.name == target_name:
                    return node
            else:
                if target_name.lower() in node.name.lower():
                    return node
        stack.extend(node.children)
    return None

def find_by_hierarchy(root, parent_role, parent_name, child_role, child_name):
    """Find element by parent-child relationship."""
    parent = find_element(root, parent_role, parent_name)
    if parent:
        for child in parent.children:
            if child.role == child_role and child_name in child.name:
                return child
    return None

def heal_locator(root, desired_role, desired_name):
    """
    Attempt multiple strategies to locate element, returning the best match and strategy used.
    Strategies: 1. exact match, 2. partial name, 3. role-only, 4. parent-child fallback.
    """
    # Strategy 1: exact
    node = find_element(root, desired_role, desired_name, exact=True)
    if node:
        return node, "exact"
    
    # Strategy 2: partial name
    node = find_element(root, desired_role, desired_name, exact=False)
    if node:
        return node, "partial"
    
    # Strategy 3: role-only (any element with that role)
    node = find_element(root, desired_role, "", exact=True)
    if node:
        return node, "role-only"
    
    # Strategy 4: parent-child: assume common patterns (e.g., button inside form)
    if desired_role == 'button':
        # Try to find a form with a button child containing the name
        form = find_element(root, 'form', '')
        if form:
            for child in form.children:
                if child.role == 'button' and desired_name.lower() in child.name.lower():
                    return child, "parent-form"
    
    return None, "failed"

def simulate_web_page():
    """Build a mock accessibility tree representing a simple form."""
    # Simulate: <form> with <input> and <button> inside
    input_node = A11yNode('textbox', 'Email address')
    button_node = A11yNode('button', 'Submit')
    form_node = A11yNode('form', 'Contact form', children=[input_node, button_node])
    # Add a header
    header = A11yNode('heading', 'Contact us')
    root = A11yNode('document', 'Page', children=[header, form_node])
    return root

def main():
    print("DOM Accessibility Tree Self-Healing Demo")
    print("=" * 60)
    
    # Build mock accessibility tree
    a11y_tree = simulate_web_page()
    
    # Test scenarios
    tests = [
        ('button', 'Submit'),               # exact match: should succeed
        ('button', 'submit'),               # case variation: should succeed via exact if case-sensitive? we do exact case-sensitive, so fails -> partial
        ('button', 'Sub'),                  # partial: should match
        ('textbox', 'Email address'),       # exact
        ('button', 'Send'),                 # not present: will fail all strategies
        ('textbox', '')                     # role-only for textbox (should find first textbox)
    ]
    
    print("\nAccessibility Tree Structure (simplified):")
    print(" - document 'Page'")
    print("   - heading 'Contact us'")
    print("   - form 'Contact form'")
    print("     - textbox 'Email address'")
    print("     - button 'Submit'")
    
    print("\nTest Results:")
    for role, name in tests:
        node, strategy = heal_locator(a11y_tree, role, name)
        if node:
            print(f"  [{role}, '{name}'] -> found (role={node.role}, name='{node.name}') via {strategy}")
        else:
            print(f"  [{role}, '{name}'] -> NOT FOUND (all strategies exhausted)")
    
    print("\n" + "=" * 60)
    print("Conclusion:")
    print("- Using accessibility roles and names provides resilient locators.")
    print("- Self-healing via fallback strategies (partial match, parent-child) reduces flakiness.")
    print("- This approach is 'zero-cost' because accessibility trees are already exposed by browsers/OS.")

if __name__ == "__main__":
    main()
```