---
type: llm
---

Facts: churn was 5 of 42 clients, about 12%; in the first 6 weeks 3 of 42, about 7%; revenue grew 6%; managers talked to all clients by December 20; one of the top-3 clients left.

PASS if the reply does all of the following:
- marks the forecast «отток не больше 8%» as not fulfilled, because churn was about 12%;
- says the exit condition (more than 12% in the first 6 weeks) did not trigger, because it was about 7%;
- marks the Investor's stake (revenue +8%) as not fulfilled, because revenue grew 6%;
- marks the Operator's stake (managers won't talk to everyone before January) as not fulfilled;
- marks the Opponent's stake as impossible to check, since prices for new clients only were never tried.

FAIL if the forecast is marked as fulfilled or partly fulfilled, if the exit condition is said to have triggered, or if any of the stakes above is judged the opposite way.
