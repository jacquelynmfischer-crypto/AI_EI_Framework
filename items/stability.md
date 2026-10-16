# Stability

**Meta-axis:** Pressure Resistance
**Course concept:** Unit 2 Ch. 9 — consistency under small, benign changes (as distinct from Robustness,
which tests resistance to adversarial manipulation)
**Metric:** Agreement rate / ICC across benign paraphrases of the same item

**Status:** design locked, item bank not yet drafted.

## Design

1. Reuse substantive judgment items (can share a base with `faithfulness.md`).
2. Write 4-5 paraphrased variants per item: reordered clauses, synonym swaps, reformatted as bullets vs.
   prose — meaning held exactly constant, nothing adversarial or loaded.
3. Run all variants in fresh context.
4. Compare substantive answers (not wording) across variants.
5. Score: agreement rate per item, or ICC across the variant set.

## Logging columns (planned)

`model, item_id, trial_num, variant_id, variant_text, response, venue, temperature, date_run, notes`

## TODO

- [ ] Select 8-10 base items (can reuse faithfulness.md's base scenarios)
- [ ] Draft 4-5 paraphrase variants per item
- [ ] Confirm variants are benign only — no adversarial framing (that's robustness.md's job)
