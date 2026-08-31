Title: Add power operator, math functions and comment support

This pull request adds the following improvements to the calculator DSL:

- Add `**` operator for exponentiation (right-associative).
- Add safe mathematical function calls: sin, cos, tan, sqrt, pow, log, exp, abs.
- Add line comments starting with `#` which are ignored by the lexer.

Files changed (in branch add/power-functions-comments):
- src/calculadora_dsl.py
- examples/USAGE.md
- README.md

Testing notes:
- Install dependencies: `pip install ply`
- Switch to branch: `git checkout add/power-functions-comments`
- Run the GUI and try expressions like `2 ** 3`, `pow(2,3)`, `sqrt(16)`, `a = 5` then `a * 2`.

If you'd like additional functions or to change the operator symbol (e.g., `^`), I can update the branch before merge.
