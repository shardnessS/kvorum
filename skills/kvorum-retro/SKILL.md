---
name: kvorum-retro
description: Retro for decisions recorded by Kvorum. Compares a forecast from the decision journal with what actually happened, marks which directors were right, fills in the journal entry, and shows calibration (whether the user's "70% sure" comes true 70% of the time) and a scoreboard of directors. Use when the user says "ретро по решению ...", "ретро кворума", "что пора проверить", "что в журнале решений", "калибровка", "кто из совета чаще прав", or brings back a past Kvorum forecast together with the facts.
---

# Kvorum retro

Closes the loop of a Kvorum session: forecast, fact, lesson. Over time the journal shows how well the user's confidence matches reality and which director is worth listening to for which kind of decision.

Speak Russian to the user unless they write in another language. No emojis.

## The journal

`kvorum/journal.md` in the project, a path the user names, or entries pasted into the chat. The format and all definitions are in [references/journal-format.md](references/journal-format.md).

| The user asks | Do |
|---|---|
| «ретро по …», or brings facts about a past decision | Retro for one decision |
| «что пора проверить», «что в журнале» | Due list |
| «калибровка», «кто чаще прав», «статистика решений» | Calibration |

## Retro for one decision

1. Find the entry by date or topic. If several fit, ask which one.
2. Get the facts. Ask only for what settles the forecast, the exit conditions and the directors' stakes: one to four numbered questions, numbers preferred. Skip what the user already told you.
3. Judge:
   - **Прогноз**: «да», «нет» or «частично», against the literal wording. Don't reinterpret it after the fact. If the wording can't be checked, mark «нельзя проверить» and make that the lesson.
   - **Условия выхода**: did any trigger, and did the user act on it? A triggered condition that was ignored is the most important finding a retro can make. Say it plainly.
   - **Ставки директоров**: each one «да», «нет», «частично» or «нельзя проверить», with one line of evidence.
   - **Что совет упустил**: what happened that no director predicted.
   - **Урок**: one sentence, a rule for the next decision, for example «Перед решением по ценам проверять даты продления у топ-клиентов».
4. Update the entry: fill in «Итог», «Сбылся», «Кто прав» and «Урок». With file access, edit the journal in place and say so. Without it, show the updated entry in a code block.
5. If the journal has five or more closed entries, finish with a short calibration summary.

Output by [templates/retro.md](templates/retro.md).

## Due list

Run the script from this skill's directory:

```bash
python scripts/journal.py due kvorum/journal.md
```

If you can't run Python, read the journal yourself: entries whose «Дата проверки» is today or earlier and whose «Сбылся» is «—». List them oldest first and offer to start with the first one.

## Calibration

```bash
python scripts/journal.py stats kvorum/journal.md
```

The script prints the hit rate by confidence band, the Brier score, results by decision type and the directors' scoreboard. Explain it in plain words:

- each band: accurate, overconfident or underconfident, for example «Когда ты уверен на 80–95%, сбывается 60%: в таких решениях ты переоцениваешь себя»;
- the Brier score: 0 is perfect, 0.25 is a coin flip;
- the decision type where the user is wrong most often;
- whose stakes came true most often, overall and by decision type;
- with fewer than ten closed entries, say the numbers are early.

Without Python, count by hand using the definitions in journal-format.md.

Before a retro or after editing the journal by hand, `python scripts/journal.py check kvorum/journal.md` finds format errors.

## Rules

- Facts come from the user. Don't fill gaps with guesses: ask, or write «нет данных».
- Judge the forecast, not the person. A good decision can have a bad outcome. When the evidence allows, say which it was: was the information available at the time of the session?
- Never rewrite the original forecast, verdict or stakes. Only fill in the retro fields.
