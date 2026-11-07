# Event brief (provisional): Claude Impact Lab, UC Irvine, Nov 7, 2026

> **Superseded on Nov 7.** This was written before the event, from the Luma and Merage pages.
> The real rules, schedule, judging and lanes are in [`docs/event/`](../event/README.md), the lane
> pages in `lanes/` and `docs/judging.md` / `docs/submission.md`. Several "not stated anywhere"
> items below are now answered there (deadline 2:30 PM, judging criteria, team size up to 5,
> public repo required, data rules). The product is about affordable homes in OC generally, not a
> Habitat for Humanity tool. Still useful here: the housing-data risks and the product selection
> criteria.

Context for the team and for Claude. It chooses no product. Organizer instructions given at the
event override everything here. Checked against the two official pages on 2026-11-05.

## Verified facts (both pages read on 2026-11-05)

Sources: [Luma event page](https://luma.com/uci-impact-lab) (L) and
[UCI Merage event page](https://merage.uci.edu/events/2026/11/AI-Hackathon-110726.html) (M).

- **When:** Saturday, November 7, 2026, 09:00 AM – 05:00 PM (M). Neither page states a time zone.
  Pacific is inferred from the location.
- **Where:** Paul Merage School of Business, UC Irvine, 4293 Pereira Dr, Irvine, CA (L).
- **Hosts:** Claude Community, UCI Paul Merage School of Business Center for Real Estate, and
  Habitat for Humanity of Orange County (L, M).
- **Challenge, as published:** working in teams, "prototype a scalable, repeatable solution that
  makes owning a home financially sustainable" (L). Explore "how Claude and AI can help Habitat
  for Humanity create more affordable homeownership opportunities" (M).
- **Participants:** students from across UC Irvine "regardless of major" (M). "No coding experience
  needed" (L, M). Teams "work alongside industry professionals and technical developers" (M).
- **Resources:** "$100 in Claude API credits per participant" (L, M).
- **Prizes:** 1st, 2nd and 3rd place. Top winners receive additional Claude credits and other
  prizes. No amounts are stated (M).

## Discrepancies and unconfirmed items (do not treat as rules)

- **Room:** L says Eric Li Classroom, SB1 1128. M says Merage Auditorium. Confirm on arrival.
- **Event name:** L is titled "Claude Impact Lab: UCI × SoCal Affordable Housing". M says "AI Hackathon".
- **Habitat OC's goal of 100 homeownership opportunities** does not appear on either official page.
  Ask Habitat staff before citing it.
- **Not stated anywhere:**
  - agenda, check-in time and presentation time
  - team size or formation rules
  - judging criteria
  - submission deadline, format and where to submit
  - whether the product must call the Claude API, or only be built with Claude
  - any data provided, and whether real Habitat data may be used
  - IP and ownership terms
  - whether the repo must be public
  - demo length, and whether demos are live or recorded

## Questions to ask on arrival

**Organizers (first 15 minutes):**
1. When exactly are submissions due, in what form, and where? When do presentations start, and how long are they?
2. What are the judging criteria and weights? Who are the judges?
3. Must the product use the Claude API, or is building with Claude Code enough?
4. Team size limits? May we use templates, libraries or code written before today?
5. Is any Habitat data provided? May any real data be used, and under what conditions?
6. How do we redeem the API credits, can we do it before building starts, and do they expire?
   Repository visibility and IP terms?
7. How long are Habitat staff and mentors available, and when?
8. Whose laptop presents? Is there a projector or adapter, and reliable Wi-Fi for a live demo?

**Habitat staff and domain experts (ask about real cases, not features):**
1. Walk us through a recent case that took too long or went wrong. Where did the time go?
2. Who would use this tool: staff, volunteers, applicants, homeowners, partners? What do they use today?
3. Which step most limits how many families you can serve? What has already been tried?
4. What would a good result look like next month, and how would you measure it?
5. What must a tool never do (decide eligibility, give financial advice, store certain data)?
6. Which languages, devices and accessibility needs do your users have?
7. What would you actually use on Monday if we built it today?

Record answers under five headings: *heard*, *agreed*, *asked to return with*, *unraised risks*,
*next actions*. Note who said what.

## Product selection criteria (score each candidate idea 0–2)

| Criterion | Question |
|---|---|
| Real pain | Did a stakeholder describe this problem from a real case today? |
| AI adds value | Does the model do something a form, a spreadsheet or a rule couldn't do as well? |
| Repeatable and scalable | Does it help with every case of this kind, not one family or one event? (published challenge wording) |
| Observable improvement | Can the demo show a before/after: time per case, errors caught, steps removed? |
| Demoable today | Can one end-to-end path work on synthetic data within the build window? |
| Safe by design | Does it work without real personal data, with a human confirming consequential outputs? |
| Team fit | Can this team's actual skills build and present it? |

Prefer the idea with the best total that has **no zero** in Real pain, Demoable today or Safe by
design. If no stakeholder is reachable, Real pain may score 1 for a problem documented in a
credible public source. Label it as an assumption in the demo. The team decides. These notes don't
pick.

## Risks specific to housing and financial information

- **Sensitive data.** Income, credit, debts, bank details, government IDs, household composition,
  immigration, disability and health details are highly sensitive. Use synthetic or de-identified
  data. Don't put real records into prompts, logs, screenshots, slides or the repository unless the
  data owner (for example, Habitat staff with authority) explicitly permits it for this purpose.
- **Consequential decisions.** Eligibility, affordability, approvals and prioritization affect
  families. The AI drafts, summarizes or flags. A named person reviews and decides. Show which
  inputs were missing or assumed.
- **Fairness and law.** Housing and lending decisions may be subject to fair-housing,
  fair-lending and privacy rules. Don't claim compliance. Ask Habitat staff what applies, avoid
  criteria that could act as proxies for protected characteristics, and say "not legal advice".
- **Financial figures.** Don't hardcode income limits, rates, costs or program rules from memory.
  Use figures staff provide, label their source and date, and make them editable.
- **Advice framing.** Outputs are drafts for staff, not financial or legal advice to families.
- **Third-party processing.** Anything sent to an AI API is processed by that provider under its
  terms. Mention this in the demo when relevant.

## Time plan for a fixed window

Measure against the **submission deadline (D)**, once known, not 5 PM. Use the playbook's shares:
discover ~10%, spike and skeleton ~15%, build ~35%, harden ~20% (freeze at the end), demo prep
~20%. Subtract lunch and talks first.

*Example only:* work starts 9:30 and D is 3:30 (about 6 h, before subtracting breaks). That gives
scope by ~10:05, spike and skeleton by ~11:00, slice working by ~1:05, freeze by ~2:20, then
rehearse and submit by 3:30. A lunch break pushes every later time back by its length unless people
eat while working. Merge to `main` at each checkpoint.

## Demo and submission checklist (adapt to the announced rules)

- [ ] The problem stated in a stakeholder's words, and who the user is
- [ ] One live end-to-end path on synthetic data, rehearsed twice from a cold start
- [ ] A before/after measure, labelled as estimated or measured
- [ ] What the AI does, where a human reviews, what happens when the AI is unsure or offline
- [ ] Limitations and what wasn't verified, stated plainly
- [ ] How it scales or repeats beyond today's example
- [ ] A labelled fallback (recording or cached real result) for the live step
- [ ] Repo, README (what's real, stubbed or sample) and submission in the required format,
      before the deadline, with no secrets or real personal data anywhere
