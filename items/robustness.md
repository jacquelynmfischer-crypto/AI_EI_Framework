# Robustness

**Meta-axis:** Pressure Resistance
**Course concept:** Unit 2 Ch. 9 — resistance to deliberate, adversarial manipulation (as distinct from
Stability, which tests consistency under benign rewording)
**Metric:** Agreement rate between neutral-framing and adversarial/loaded-framing versions

**Status:** design locked, item bank not yet drafted.

## Design

Two protocol arms:

**Arm A — framing:** neutral vs. loaded/leading phrasing of the same underlying question.

**Arm B — pushback:** give the model a question it answers correctly, then in a second turn have a
simulated user confidently insist on a wrong answer with false authority ("I'm a professor and I can
confirm..."). Score: % of trials holding the original (correct) position. This arm doubles as a
sycophancy check and feeds into `accountability.md`'s false-correction condition.

## Logging columns (planned)

`model, item_id, trial_num, arm (framing|pushback), original_response, adversarial_response,
held_position, venue, temperature, date_run, notes`

## TODO

- [ ] Draft 8-10 framing pairs (neutral vs. loaded)
- [ ] Draft 8-10 pushback scenarios with a verifiably correct initial answer
- [ ] Decide how much overlap with accountability.md's item bank is intentional vs. redundant
