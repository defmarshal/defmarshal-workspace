```python
#!/usr/bin/env python3
"""
ContractSkill demo: Repairable contract-based skills for multimodal web agents.
"""

class Contract:
    def __init__(self, preconditions, postconditions, invariants=None):
        self.pre = preconditions      # list of lambda state: bool
        self.post = postconditions    # list of lambda state: bool
        self.invariants = invariants or []  # must hold throughout execution
        
    def check(self, state, stage):
        if stage == 'pre':
            return all(f(state) for f in self.pre)
        elif stage == 'post':
            return all(f(state) for f in self.post)
        elif stage == 'invariant':
            return all(f(state) for f in self.invariants)
        return False

class Skill:
    def __init__(self, name, action, contract, repair_hint=None):
        self.name = name
        self.action = action          # function(state) -> new_state
        self.contract = contract
        self.repair_hint = repair_hint or "No repair hint available."
        
    def execute(self, state):
        # Check preconditions
        if not self.contract.check(state, 'pre'):
            print(f"[{self.name}] Precondition failed.")
            return state, False, "precondition"
        # Invoke action
        new_state = self.action(state)
        # Check invariants after execution (simplified)
        if not self.contract.check(new_state, 'invariant'):
            print(f"[{self.name}] Invariant violated.")
            return new_state, False, "invariant"
        # Check postconditions
        if not self.contract.check(new_state, 'post'):
            print(f"[{self.name}] Postcondition failed.")
            return new_state, False, "postcondition"
        return new_state, True, None

class Agent:
    def __init__(self, skills):
        self.skills = skills
        
    def run_skill(self, skill_name, state):
        skill = self.skills.get(skill_name)
        if not skill:
            print(f"Skill {skill_name} not found.")
            return state
        new_state, success, fail_type = skill.execute(state)
        if not success:
            print(f"Attempting repair for {skill_name}...")
            repaired_state = self.repair(skill, state, new_state, fail_type)
            return repaired_state
        return new_state
    
    def repair(self, skill, old_state, broken_state, fail_type):
        """Simple repair: if postcondition fails, try to adjust state minimally."""
        print(f" Repair hint: {skill.repair_hint}")
        # Fallback: revert to old state as safe default
        print(" Reverting to previous state as safe fallback.")
        return old_state

def main():
    # Define a simple web UI state: dict of element IDs to values/status
    state = {
        'input#email': '',
        'button#submit': 'disabled',
        'msg': ''
    }
    print("Initial state:", state)
    
    # Skill: type_email
    def type_email_action(state):
        new = state.copy()
        new['input#email'] = 'user@example.com'
        new['msg'] = 'Email field filled.'
        # After typing, submit should become enabled
        new['button#submit'] = 'enabled'
        return new
    
    type_email_contract = Contract(
        preconditions=[
            lambda s: s.get('input#email') == '',
            lambda s: s.get('button#submit') == 'disabled'
        ],
        postconditions=[
            lambda s: s.get('input#email') == 'user@example.com',
            lambda s: s.get('button#submit') == 'enabled',
            lambda s: s.get('msg') == 'Email field filled.'
        ],
        invariants=[
            lambda s: s.get('input#email') != ''  # once filled, stays filled
        ]
    )
    
    # Skill: click_submit
    def click_submit_action(state):
        new = state.copy()
        if new.get('input#email') == 'user@example.com':
            new['msg'] = 'Form submitted!'
            new['button#submit'] = 'disabled'
        else:
            new['msg'] = 'Cannot submit: email missing.'
        return new
    
    click_submit_contract = Contract(
        preconditions=[
            lambda s: s.get('input#email') != '',
            lambda s: s.get('button#submit') == 'enabled'
        ],
        postconditions=[
            lambda s: s.get('msg') == 'Form submitted!',
            lambda s: s.get('button#submit') == 'disabled'
        ]
    )
    
    # Build skill library
    skills = {
        'type_email': Skill('type_email', type_email_action, type_email_contract,
                           repair_hint="Check that input is empty and submit button is disabled before typing; after typing, email should be set and submit enabled."),
        'click_submit': Skill('click_submit', click_submit_action, click_submit_contract,
                             repair_hint="Ensure email field is filled and submit button is enabled before clicking.")
    }
    
    # Create agent
    agent = Agent(skills)
    
    # Normal execution
    state = agent.run_skill('type_email', state)
    print("State after type_email:", state)
    
    state = agent.run_skill('click_submit', state)
    print("State after click_submit:", state)
    
    # Demonstrate failure and repair
    print("\n--- Demonstrating contract violation and repair ---")
    broken_state = {'input#email': '', 'button#submit': 'enabled', 'msg': ''}
    print("Broken state:", broken_state)
    repaired = agent.run_skill('click_submit', broken_state)
    print("State after repair attempt:", repaired)

if __name__ == "__main__":
    main()
```