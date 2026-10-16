# Faithfulness

**Meta-axis:** Epistemic Integrity
**Course concept:** Unit 2 Ch. 9 (Faithfulness) + Unit 2 Ch. 8 (chain-of-thought faithfulness)
**Metric:** % of trials where perturbing the cited evidence flips the output in the predicted direction

**Status:** design locked, item bank not yet drafted.

## Design

1. Present a judgment-call scenario requiring the model to weigh evidence (e.g., comparing two
   candidates/options against stated criteria) where it must name the deciding factor.
2. Record the judgment and the cited reason.
3. Build a perturbed variant that flips only the cited factor, holding everything else fixed.
4. Re-run in a fresh context.
5. Check whether the judgment flips as the model's own stated reasoning predicts.

This is the course's own faithfulness test (Unit 2 Ch. 9: intervening on the claimed evidence and
measuring the model's response), applied to the model's self-generated rationale instead of a SHAP
attribution — and it mirrors the chain-of-thought faithfulness concern directly (Unit 2 Ch. 8: "a
coherent chain of thought is weak evidence of faithfulness").

## Logging columns (planned)

`model, item_id, trial_num, original_judgment, cited_reason, perturbed_variant_id, perturbed_judgment,
flipped_as_predicted, venue, temperature, date_run, notes`

## TODO

- [ ] Draft 8-10 base scenarios with a clean single deciding factor
- [ ] Draft the matched perturbed variant for each
- [ ] Pilot on one model to confirm the perturbation reliably isolates the cited factor
