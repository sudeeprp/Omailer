

GROUP_ASSESSMENT_MAP = {
    'A: Anticipated cust.needs': '''In addtion to understanding the requirements, the team took effort to anticipate future customer needs.''',
    'B: Seek cust.need': '''In addition to understanding the requirements, the team sought to understand the customer context.''',
    'C: Goals clear but no cust.link': '''The team understood their goals clearly. In future, they could use the opportunity to understand the customer context and anticipate their needs.''',
    'D: Goals unclear / impl.driven': '''The team implemented the specified functionality. In future, they could clarify the goals pro-actively and focus on the customer context.''',

    'A: Multiple improvements done': '''The team made multiple improvements to the code they inherited, in areas of warnings, linting, complexity, duplication and readability.<br>They have applied clean-coding learnings effectively.''',
    'B: At least one improvement': '''The team improved the code they received in terms of readability.<br>They have demonstrated basic application of clean-code principles. They can practice giving it continuous attention, going forward.''',
    'C: No improvement implemented': '''The team built on the code they received, complying to existing patterns.''',

    'A: Persisted in adversity': '''The team took effort to research clean design and implementation, even when they encountered obstacles.''',
    'B: Ownership of modules': '''The team took ownership of the application, modifying it to suit their needs.''',
    'C: Just made it work': '''The team did the required work to function on top of existing code. In future, they could focus on improving the code-quality during maintenance.''',

    'A: Cover all unit-risk': '''The team covered all major risks in unit-testing, achieving a solid base of the test-pyramid.''',
    'B: Coverage >75%': '''The team achieved coverage >75%, covering all the risky aspects of the system.''',
    'C: Covered easy part': '''The team covered the code that was easy to cover. In future, they could focus on refactoring for testability.''',

    "A: Auto'd all possible": '''The team has automated all test flows and checks.''',
    "B: Auto'd unit&API checks": '''The team has automated unit and API-level tests along with relevant checks.''',
    "C: Auto'd with manual checks": '''The team has automated test execution, while the checks have remained manual. In future, they could design to automate the checks at the start itself.''',
    "D: Minimal or no automation": '''The team tested everything manually. In future, they could focus on automating the flows, along with checks and asserts.'''
}
