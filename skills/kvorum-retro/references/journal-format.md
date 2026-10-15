# Journal format

The journal is a Markdown file written by the kvorum skill, `kvorum/journal.md` by default. Every entry starts with a heading and has one field per line.

```markdown
## 2026-10-15 · Поднять цены на 15%
- Тип: цены
- Режим: полный
- Вердикт: делать при условиях
- Прогноз: отток клиентов за квартал не больше 8%
- Уверенность: 70%
- Дата проверки: 2027-01-15
- Условия выхода: отток больше 12% за первые 6 недель → откатываем цены для текущих клиентов
- Сигнал разгона: отток меньше 4% за 6 недель → при продлении поднимаем цены и для топ-3
- Первый шаг: назначить встречи топ-3 клиентам до 2026-10-17
- Ставка Скептика: двое из топ-3 клиентов начнут искать другого подрядчика до февраля
- Ставка Оппонента: повышение только для новых клиентов вернёт маржу к 30% за полгода без оттока
- Ставка Инвестора: выручка за квартал вырастет минимум на 8%
- Ставка Операционщика: менеджеры не успеют поговорить со всеми 42 клиентами до января
- Итог: —
- Сбылся: —
- Кто прав: —
- Урок: —
```

«Тип» is one of: цены, люди, запуск, закупка, маркетинг, карьера, другое. In quick mode only two stakes are present.

## Retro fields

After a retro the last four fields look like this:

```markdown
- Итог: ушли 5 клиентов из 42 (12%), один из них из топ-3; выручка за квартал +6%
- Сбылся: нет
- Кто прав: Скептик: частично; Оппонент: нельзя проверить; Инвестор: нет; Операционщик: нет
- Урок: перед решением по ценам проверять даты продления у топ-клиентов
```

- «Итог»: the facts in one or two sentences, with numbers.
- «Сбылся»: «да», «нет», «частично» or «нельзя проверить».
- «Кто прав»: `<Директор>: <оценка>`, separated by «; ». The same four answers as for «Сбылся».
- «Урок»: one sentence.

## Definitions for calibration

- An entry is **closed** when «Сбылся» is «да», «нет» or «частично». «Нельзя проверить» is counted separately and left out of calibration.
- An entry is **due** when «Дата проверки» is today or earlier and «Сбылся» is «—».
- Outcome: «да» = 1, «частично» = 0.5, «нет» = 0.
- Confidence bands: 50–60%, 65–75%, 80–95%.
- Hit rate of a band: the average outcome of its closed entries.
- A band is accurate when the hit rate is within 10 points of the band's average confidence; below that the user is overconfident, above it underconfident. A band with fewer than three entries has too little data.
- Brier score: the average of (confidence − outcome)², with confidence as a fraction, 0.7 for 70%. 0 is perfect, 0.25 is a coin flip.
- A director's score: (да + 0.5 × частично) / (да + частично + нет) over their stakes.
