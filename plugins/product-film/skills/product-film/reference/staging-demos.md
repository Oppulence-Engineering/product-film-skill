# Staging demos: Eigenn, Conduitt, Cadense

Use this profile for recordings from these three products. A staging hostname does not prove that data is synthetic or that email, bank, payment, and webhook integrations are disabled.

## Environment and session

| Product | Allowed origin | Candidate story, subject to live verification |
|---|---|---|
| Eigenn | `https://staging.eigenn.io` | Review cash or a scenario, inspect an assumption, and show the observed decision context. |
| Conduitt | `https://staging.conduitt.io` | Open a demo invoice, inspect its timeline and owner, and preview the next follow-up. |
| Cadense | `https://staging.cadense.io` | Inspect invoice intake, extracted fields, an approval requirement, or a payment-readiness exception. Prefer a visibly labeled practice flow when available. |

- Select the requested product's exact HTTPS origin. Require equality of parsed scheme, hostname, and effective port with its table entry (HTTPS, the exact staging hostname, port 443), not a prefix or substring: `staging.eigenn.io.example.com`, a URL with that name only in its path, a different port, and production are not allowed targets. Paths within the matching origin remain valid. Inspect visible link destinations before navigation and recheck the actual URL after redirects, new tabs, and workspace changes. Do not remove `staging.` to work around an error.
- Reuse the user's existing browser profile. Use an existing matching tab if it is safe to inspect; open an isolated tab in that profile if the user has an unfinished editor. Do not copy cookies, extract tokens, create an account, recover credentials, or change auth settings.
- At login, MFA, an interactive challenge, or a browser security warning, stop that product's capture and retain the tab for human handoff. Do not follow an identity-provider redirect or fill credentials as part of this profile. A passive page check may finish without interaction; it does not justify bypassing a challenge.
- Start from the staging root or an observed matching tab. Discover routes from current navigation. Do not assume all apps have `/dashboard`, share tenant IDs, or use the same locale or auth paths. Cadense routes can include `/workspace/<id>/`; obtain the ID from the signed-in UI, never hard-code a previous user's ID.
- Confirm the current workspace, role, and fixture before capture and before any mutation. Use only approved demo records. A marketing screenshot, sample card, cached page, or disabled control is not evidence of a completed workflow.
- Keep production access out of the workflow. If an unexpected redirect reaches it, stop, record the exception truthfully, and exclude that footage. Report `Production accessed: NO` only if supported by the actual run.

## Rehearse one truthful journey

1. Inspect the selected feature in the live staging UI and the product's available brand/claims sources. Scope the film to one job, one starting state, and one observable result.
2. Record the fixture's safe label/ID and route in the local capture log. Prefer read-only inspection or draft previews. If approved test data is missing, return `BLOCKED_TEST_FIXTURE`; do not substitute customer data or invent a result.
3. Rehearse navigation, modal placement, loading time, and the final state before recording. List any action that changes state. A staging demo request permits routine navigation and local recording/editing, not unspecified external effects.

   Record access gates separately from product failures. A signed-in session can still show a plan restriction. A practice button can first open a role/goal setup guide; reaching that guide is not completion of the practice workflow. Inspect the next control and its effects before continuing. Recheck these conditions in the current workspace rather than assuming prior test results apply.
4. Capture before/action/after continuity. For an authorized saved change, re-open or refresh safely to confirm persistence. Do not claim durable success from a toast alone. If the recording omits a long wait, disclose the time cut when it affects a performance claim.

## Product boundaries

**Eigenn:** Favor financial questions, assumptions, forecasts, scenarios, and decision review. Read current chart labels, units, dates, and scenario names. Do not turn simulated forecasts into guaranteed outcomes or imply that an Eigenn scenario sent a collections reminder. Inspect whether scenario changes autosave before editing; use an approved disposable copy when needed.

**Conduitt:** Favor an invoice, its customer conversation, owner, next action, and recorded history. A reminder preview is not a sent reminder; a recorded payment is not proof that a reminder caused it. Stop before `Create & Send`, reminders, invitations, SMS, or any action that can notify a real recipient unless explicitly authorized for the exact test fixture and destination. For a Conduitt financial test send, obtain one-time confirmation immediately before the send. If the result is uncertain, inspect history; never retry the send blindly. Stop if sandbox status or the recipient is unverified.

**Cadense:** Favor intake and review: invoice fields, vendor matching, exceptions, approval requirements, and payment readiness. Discover the current labels instead of treating this list as proof that features work. A practice flow must be labeled as practice in the demo; it does not prove real financial records changed. Do not approve real invoices, run payment batches, connect banks, change approval rules, or activate schedules to improve a shot. Keep payment execution outside a demo unless separately authorized and handled under the applicable financial-action rules. Avoid submitting free-form agent tasks during rehearsal; they may trigger workflows and external tools.

Across products, sending, paying, publishing, inviting, deleting records, or enabling integrations is not a cosmetic recording step. Prepare a safe preview when it covers the brief. If the requested outcome needs a restricted action, name the exact blocker instead of quietly substituting a different outcome.

## Evidence and handoff

Use [the capture/edit log](../templates/screen-studio-demo.md), or the existing product workspace's manifest with equivalent fields. Keep separate status for staging preflight, recording, project save, editing, export, and review. Use `PASS`, `FINDING`, `FAILURE`, or `BLOCKED` with evidence; leave unrun stages `NOT_RUN`.

For blocked stages, include the actual URL without auth query strings, visible blocker, retained tab, and required human action. Continue independent work such as the script, edit plan, another authorized product, or existing local footage. A blocked Conduitt login does not block editing a saved Eigenn project.

Store raw captures locally outside tracked source paths. Record build/version only if exposed by a trusted source; otherwise write `unknown`. Do not copy credentials, session URLs, private inbox addresses, or customer data into a committed manifest. Deliver local paths and observed outcomes, not a claim that all staging workflows passed.
