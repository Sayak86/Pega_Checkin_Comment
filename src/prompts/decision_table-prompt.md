## Specific Instructions for Decision Table

You are analysing changes to a **Decision Table** rule. Use the sections below to decide what is worth reporting and how to phrase it. The generic instructions already told you how to read `pxChangeType`, `pxCurrentValue`, and `pxPreviousValue` — do not repeat that mechanic, just apply it.

Report only features that actually changed in the diff. Do not describe anything that did not change. Ignore metadata (history, UUIDs, timestamps, labels).

=====================================================================

## WHAT TO TRACK

Track changes only in terms of Decision Table structure:
1. **Rows** — inserted, removed, moved, or modified condition rows and decision rows.
2. **Columns** — inserted, removed, moved, or modified condition columns.
3. **Conditions** — the condition expression mapped to a column (property, operator, value).
4. **Operators** — comparison operator changes on a condition.
5. **Results / Actions** — the result column value or action returned by a row.
6. **Column preferences** — ordering or preference changes across columns.
7. **OR-list entries** — alternate values grouped under a single condition cell.
8. **When-change / trigger** — addition or change of a when condition or change trigger.

If a feature is not in the list above, do not report it.

=====================================================================

## HOW TO PHRASE CHANGES (mandatory)

**Use indices to locate every change. Reference structure, not raw Pega internals:**
- Rows  → `Row <n>`
- Columns → `Column <k>`
- Result columns → `Result column <k>`
- Column preferences → `Column preferences <k>`
- OR-list entries → shorthand `Column <k> condition <n>.<m>` (e.g. `Column 1 condition 1.7`)

**Moves** — show the index transition with an arrow: `Column-1 conditions 2,4 -> 13,14`.

**Inserts** — list the positions inserted at: `inserted at 2,4,6,8,10,12`.

**Consolidate** — combine multiple edits on the same Row or Column into one sentence, separated by commas.

**Literal values** — you MAY name a business identifier (e.g. a message family, type code, or mapped property) when it is the subject of the change and naming it makes the comment meaningful for a developer. Do not dump every literal; name only what identifies the change. Never expose raw Pega property references, GUIDs, or class names.

=====================================================================

## EXAMPLES (gold standard — match this style)

1. Inserted Column-1 conditions (19-21) for the CAMT110/111 family, added corresponding Column-2 BusinessService conditions, modified Column-2 property and datatype, and inserted results/actions for the CAMT110/111 parsing classes.

2. Modified Column-1 OR condition row mapping, inserted Column-2 conditions (rows 1-2), Column-3 conditions (rows 1-2), Results (rows 1-2), and added a when condition (row 3).

3. Column-1 conditions 2,4 -> 13,14, inserted at 2,4,6,8,10,12, Column-2 OR group reorganized (row numbers updated), Column-2 conditions moved 7,8,9,10,11 -> 1,6,12,14,7, inserted at 2,3,4,5,8,9, several existing indices updated, Results moved 2,4 -> 15,17, inserted at 3,5,7,9,11,13, task status updated, empty action inserted.

4. Added new decision rows for the PAIN and CAMT message families with types 001 and 055, mapping both to PaymentInformationId, updated OR-condition grouping in Column 1, and added a when-change trigger.

=====================================================================

## CONSTRAINTS

- Focus only on changed features. Do not add anything that did not change in the diff.
- Output one sentence per affected Row, Column, Result column, or Column preferences group, then close with one business-friendly commit sentence in past tense (like the examples above).
- Do not use semicolons — use commas only.
- Do not use backslashes anywhere in the output.
- Do not expose raw Pega property references, GUIDs, or class names — use indices and human-friendly identifiers.

## OUTPUT

Compose one concise, business-friendly commit sentence in past tense covering all changes.
