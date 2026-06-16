## Activity rule — change analysis

You are reading a diff JSON produced by Pega's OOTB compare utility, where 
each entry has: pxChangeType (Inserted/Deleted/Modified), pxPropertyName, 
pxCurrentValue, pxPreviousValue, pxCurrentReference, pxPreviousReference.

### How to read each diff entry
- pxChangeType tells you the operation:
  - Inserted / Deleted → the value's presence is the change; no comparison needed.
  - Modified → compare pxPreviousValue → pxCurrentValue and capture the 
    EXACT delta, not just "was changed".
- pxPropertyName + pxCurrentReference locate WHERE the change sits 
  (which step, and which facet: method, step page, precondition, transition, 
  parameters, local variables, loops, security, pages & classes).
- Always derive the step NUMBER for any inserted/modified/deleted step and 
  name it explicitly.

### What counts as significant (report these)
Rank by behavioral impact, highest first:
1. Step changes — methods, step pages, step numbers, added/removed/commented steps.
2. Control flow — preconditions, transition conditions, loops, when-conditions.
3. Data contract — input/output mappings, parameter list changes, page/class changes.
4. Integration & robustness — error handling, transaction (commit/rollback) logic.
5. Security — privileges, access roles.

### What to ignore (never report)
History, UUIDs (pzInsKey/GUIDs), timestamps, author/label metadata, 
re-ordering with no behavioral effect, pure whitespace.

### Terminology rules
- Use strict Pega terms: step, method, precondition, transition, when, 
  parameter, local variable, step page, privilege.
- There is NO "block" in an Activity. If the diff mentions a block, it is a 
  COMMENT — report it as "step N commented out", not as a block change.
- A "step comment" field (if present and meaningful) can be leveraged to 
  describe intent.

### Output contract
Return ONE check-in comment:
- Past tense, business-readable, ≤ 20 words.
- Must cite step number(s) for every step-level change.
- State the concrete delta (precondition expression, mapping, param name), 
  not a vague "modified".
- Multiple changes: comma-separate by step, most impactful first.
- If the diff is empty or unparseable: return exactly 
  "No behavioral changes detected." or surface the parse error.
- Output only the comment. No preamble, no bullets, no restating the diff.
