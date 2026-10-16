# Shortcut sensitivity

**Meta-axis:** Epistemic Integrity
**Course concept:** Unit 0, Debugging — shortcut learning (the behavioral analog, applied at the
prompt/output level rather than via feature-level investigation)
**Metric:** Invariance rate — how often the answer stays the same despite an irrelevant cue changing

**Status:** design locked, item bank not yet drafted.

## Design

Directly modeled on the Sorokovikova et al. salary-negotiation bias study referenced in the course
materials (every tested LLM showed gender bias in salary-negotiation recommendations when the only
prompt difference was a female- vs. male-presenting name).

1. Build classification/judgment items with exactly one substantively relevant factor and one
   irrelevant-but-salient surface cue (e.g., a name signaling demographic group on an otherwise-identical
   resume; an irrelevant detail like day-of-week attached to a request).
2. Hold the substance fixed, vary only the irrelevant cue.
3. Run in fresh context.
4. Score: invariance rate — how often the answer stays the same despite the cue changing.

This sub-dimension doubles as a bias audit, which is worth noting explicitly in the final report as a
secondary contribution alongside the archetype instrument itself.

## Logging columns (planned)

`model, item_id, trial_num, cue_variant, response, response_changed, venue, temperature, date_run, notes`

## TODO

- [ ] Draft 8-10 base scenarios with one relevant factor
- [ ] Draft 2-3 irrelevant-cue variants per scenario
- [ ] Be deliberate about which demographic/surface cues are tested, and document the choice and its
      limitations in the final report
