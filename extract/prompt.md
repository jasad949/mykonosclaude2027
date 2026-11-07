You extract facts for an affordable-housing finance case from ONE public document.
The text of the document follows the instructions, between <document> tags.

Rules:
- Use only the document. Never use outside knowledge, never estimate, never compute
  a number the document does not state.
- If the document does not state a fact, return it with "value": null and
  "found": false. Unknown is a correct answer; a guessed number is the worst answer.
- For every fact you do find, copy a quote of 15 words or fewer, exactly as it
  appears in the document (same words, same numbers), that shows the value.
- Give a locator: the table, note, section, exhibit or page label nearest the quote.
- Money as plain numbers in dollars (220000, not "$220K"). Rates as decimals
  (5.00% -> 0.05). Months as numbers. Dates as YYYY-MM-DD or YYYY-MM.
- If two places in the document disagree, return value null and put both quotes
  in "conflict".
- Do not include any personal information about buyers, tenants or residents.

Facts to look for (names are fixed):
- construction_line_balance: amount drawn on the project's construction loan or line
- construction_line_rate: its interest rate
- construction_line_maturity: when it matures
- city_holdback: city funds committed to the project but not yet paid out
- city_funds_expended: city funds already paid out to the project
- city_grant_total: total city grant or loan for the project
- holdback_release_condition: what must happen before the remaining city funds are paid
- existing_line_rate: interest rate on the organization's other existing line of credit
- existing_line_limit: that line's maximum commitment
- existing_line_drawn: amount drawn on that line
- contingency_remaining: construction contingency left
- scheduled_construction_completion: when construction is scheduled to finish
- assignment_consent: whether grant rights can be assigned, and whose consent is needed

Return ONLY a JSON object, no prose, in this shape:

{"facts": {"<fact name>": {"value": <number|string|null>, "found": <true|false>,
  "quote": "<15 words or fewer, verbatim>", "locator": "<where>",
  "as_of": "<date the value was true, if stated>", "conflict": ["<quote>", "<quote>"]}}}

Include every fact name above, found or not.
