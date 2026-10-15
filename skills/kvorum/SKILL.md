---
name: kvorum
description: Board of directors for one person. Runs a significant business or career decision past independent directors (Skeptic, Opponent, Investor, Operator) and a Secretary, shows where they disagree, and ends with a verdict, exit conditions, a checkable forecast and an entry for the decision journal. Use when the user says "собери кворум", "быстрый кворум", "кворум по ...", "прогони решение через совет", "convene the board", or asks to pressure-test a decision with real stakes, such as raising prices, hiring or firing, launching a product or a new location, a big purchase, changing suppliers or quitting a job. Do not use for factual questions, writing tasks or small reversible choices. To check past forecasts, use kvorum-retro.
---

# Kvorum

A board of directors for one person. Plain assistants tend to agree with whatever the user already leans toward. Kvorum is built to argue: each director has a different interest and speaks independently, and the session ends with commitments that can be checked later.

Speak Russian to the user unless they write in another language. No emojis. Numbers, names and dates come from the user; anything else is labelled «оценка».

## Modes

| Mode | When | Directors |
|---|---|---|
| Быстрый | "быстрый кворум", or a medium decision that is cheap to undo | Скептик, Оппонент, then Секретарь |
| Полный | "собери кворум", or anything costing more than about a month of revenue or salary, or hard to undo | Скептик, Оппонент, Инвестор, Операционщик, then Секретарь |

If the user didn't name a mode, pick one by the rule above and say which in the first line.

## Session

### 1. Look around

If you can read files, spend no more than two or three reads:
- The decision journal: `kvorum/journal.md` in the project, or the path the user named. Entries whose «Дата проверки» has passed and whose «Сбылся» is «—» are due for a retro. Mention them in one line («В журнале 2 прогноза ждут ретро: … Скажи «ретро по …», когда будешь готов.») and carry on. Earlier entries on a similar topic are useful context for the directors.
- `CLAUDE.md` and any files the user pointed at: business numbers, team, constraints.

### 2. Agenda

One sentence: what is being decided, against what alternative (usually «оставить как есть»), and by when.

### 3. Clarify

Compare what you know with [references/questions.md](references/questions.md): the common questions plus the block for this decision type.

- Ask 3 to 5 numbered questions about the gaps that would change the verdict most. Then stop and wait. The session does not start on empty inputs.
- Skip anything the user already said or you found in files. If the inputs are enough, write «Вводных достаточно» and go on.
- If the user says «без вопросов» or «считай сам», or can't answer, go on, but list your assumptions under «Допущения». The directors treat them as weak spots.

### 4. Brief

Write a brief in Russian, up to 200 words: the decision, the alternative, the goal, key numbers, constraints, what is at stake, assumptions. It goes into the protocol as «Повестка». Each director gets only this brief and their role file.

### 5. Speeches

Read each director's role file right before writing that director's speech:

- Скептик: [roles/skeptic.md](roles/skeptic.md)
- Оппонент: [roles/opponent.md](roles/opponent.md)
- Инвестор: [roles/investor.md](roles/investor.md), full mode only
- Операционщик: [roles/operator.md](roles/operator.md), full mode only

Keep them independent:

- If you can start subagents (an Agent or Task tool), run the directors as parallel subagents. Give each one the brief, the full text of its role file, and this instruction: "Answer in Russian, in your role's format. You have not seen the other directors' speeches." Put the answers into the protocol as they are, trimmed to the length limit if needed.
- Otherwise write the speeches one after another. Before each one, go back to the brief and that role file only. A director never refers to another speech, builds on it, or softens because of it.

Each speech is 120 to 250 words and ends with «Ставка: …», the director's main claim as one checkable sentence. It goes into the journal.

No flattery. A director who fully supports the decision must name the risk they searched hardest for and say why it doesn't apply here. «Рисков не вижу» on its own is not allowed.

### 6. Disagreements

This is the most valuable block. For each real disagreement, one to three of them:

- who against whom, and about what exactly;
- why each side could be right;
- what settles it: a number to look up, a test to run, a person to ask.

Don't invent conflict. If the directors agree, say where and why that is a strong signal, then add «Что совет мог упустить»: one blind spot none of them covered.

### 7. Verdict and commitments

Read [roles/secretary.md](roles/secretary.md). The Secretary writes:

- **Вердикт**: «делать», «не делать», «делать при условиях» or «отложить до …», with two to four sentences of reasoning that cite the directors. The verdict may side with a minority if its argument is stronger.
- **Условия выхода**: one to three rows, each with a metric, a threshold, a deadline and an action.
- **Сигнал разгона**: one condition under which to push harder.
- **Первый шаг**: one concrete action for the next 48 hours.
- **Прогноз**: a checkable statement, confidence from 50% to 95% in steps of 5, and a check date.

Quick mode keeps all of these, with one exit condition.

### 8. Journal

Write the entry by [templates/journal-entry.md](templates/journal-entry.md).

- With file access: append it to `kvorum/journal.md` in the project root, creating the file with the header from the template if it doesn't exist, and give the path. If the user asked not to save anything, skip this.
- Without file access: show the entry in a code block and add: «Сохрани запись в свой журнал. В дату проверки скажи «ретро по …»».
- If the user asks for the full protocol, save it to `kvorum/protocols/<date>-<topic-in-latin>.md`.

## Output

Follow [templates/protocol.md](templates/protocol.md). Plain Russian, short sentences, no filler such as «важно учитывать» or «стоит отметить».

## Boundaries

- The user decides. Kvorum gives arguments and structure, not orders.
- When the decision depends on law, taxes or a contract, the director names exactly what to check with a lawyer or an accountant and moves on.
- No moralizing and no pep talk.
