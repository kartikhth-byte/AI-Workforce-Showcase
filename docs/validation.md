# Validation and evidence

The project uses evidence packages, deterministic proofs, focused tests, full runtime regressions, strict typing, linting, and hash-bound review checkpoints. This page reports the strongest current results and their limits.

## Runtime and workflow validation

| Check | Result | Interpretation |
| --- | ---: | --- |
| Full runtime regression | 234 passed | Current private suite on macOS with access to the local signer socket |
| Fixed workflow definitions | 3 | Research, research-to-article, research-to-opportunity-fit |
| Coordinator lifecycle | start, status, resume, cancel | Fixed public interface; no arbitrary graph editing |
| Ambiguous dispatch recovery | 1 attempt | A committed Broker effect is reconciled before retry |
| Article workflow replay | exact match | Research and draft artifacts retain exact parent lineage |
| Jev observability checkpoint | 25 focused tests passed | Append-only predictions, privacy controls, and separate labels |

The runtime suite includes Unix-domain-socket integration with a local signer authority. Review runs inside a restricted sandbox first observed expected socket denials; the exact permitted local reruns passed. This is an environment boundary, not evidence of multi-host or hosted deployment.

## Jev evaluation

TypeSafe Jev System One was evaluated as a narrow probabilistic classifier, not as a general safety oracle. Every retained path is advisory-only and defers low-confidence results to review.

| Contract | Cases / calls | Recorded result | Operational use |
| --- | ---: | --- | --- |
| Pepper inbound routing | 25 / 50 | 100% raw accuracy and repeat agreement; 90% confidently correct | Suggest one of five routes; low confidence becomes `pepper_review` |
| Kent source type | 25 / 50 | 100% accuracy and repeat agreement | Classify supplied source metadata into one of five types |
| Kent claim/evidence relation | 24 / 48 | 95.83% raw accuracy; 72.92% confident coverage; 100% confident precision and repeat agreement | Classify one of four evidence relationships; never accept a claim |
| SpongeBob opportunity type | 25 / 50 | 100% kind accuracy and repeat agreement | Structural opportunity classification only; no personal-fit decision |

An additional task-specific-value signal for skill governance reached 91.67% accuracy across 24 cases / 48 calls and **did not meet** its 95% gate. It remains a non-authorizing observation inside mandatory human review.

Earlier broader designs were rejected after evaluation. Jev is not used to decide overall trustworthiness, evidence sufficiency, skill acceptance, or automatic disposition. This narrowing is itself an engineering result: the system kept only uses supported by contract-specific evidence.

## Privacy and authority checks

- Jev prediction inputs are logged as locally salted HMAC-SHA-256 digests, not raw text.
- Human labels are separate append-only events and cannot overwrite predictions.
- Credentials are retrieved through the Keychain boundary and are not placed in repository configuration.
- Private second-brain inputs are excluded from public model routes unless an explicit local redaction contract permits a projection.
- Browser, messaging, publishing, application submission, schedules, and unattended actions are denied by default and selectively exposed only through reviewed contracts.
- All model and harness results remain subordinate to deterministic Broker checks.

## Bounded live evidence

Selected checkpoints used live provider calls under explicit cost caps:

- a five-agent synthetic OpenRouter canary reported USD 0.000187;
- a supervised five-step OpenRouter workflow reported USD 0.000216;
- an inert browser executor proof reported USD 0.003496;
- a supervised public browser proof reported USD 0.001349;
- one end-to-end research-to-opportunity-fit workflow completed under a user-approved USD 0.10 cap.

These are bounded integration proofs, not load tests or forecasts of normal monthly spend. Provider pricing and availability can change.

## Evidence quality rubric

The project distinguishes:

1. **Structural proof** — configuration and code enforce a declared boundary.
2. **Synthetic functional proof** — deterministic data exercises behavior without external access.
3. **Bounded live proof** — a real provider, model, or public page is used under a fixed cap.
4. **Operational evidence** — append-only observations accumulate during actual use.

Passing a structural or synthetic proof does not imply live production readiness. The documentation names the proof type instead of collapsing them into a single “works” claim.

## Known limitations

- Four agents are currently configured; Skippy is deferred.
- The system runs on one local macOS host; distributed coordination is not claimed.
- Workflows are fixed, not dynamically composed.
- LinkedIn remains supervised/read-only and is not represented as a completed official API connector.
- The second brain is deliberately local and unsynchronized.
- Human review remains required for publishing, applications, outreach, purchases, and other consequential actions.
- Model-quality metrics cover synthetic contract cases, not the full distribution of real work.

Machine-readable aggregate figures are available in [`evidence/metrics.json`](../evidence/metrics.json).
