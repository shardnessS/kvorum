# Journal entry format

The journal is a Markdown file, `kvorum/journal.md` by default. The kvorum-retro skill and its script read it, so keep the field names exactly as below.

## New file

Start a new journal with this header:

```markdown
# Журнал решений

Записи добавляет Кворум после каждого заседания. Поля «Итог», «Сбылся», «Кто прав» и «Урок» заполняет ретро.
```

## Entry

Append to the end of the file, after a blank line:

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

## Rules

- The heading is `## <session date> · <topic>`, the date in ISO format.
- «Тип» is one of: цены, люди, запуск, закупка, маркетинг, карьера, другое.
- «Уверенность» is a whole number of percent from 50 to 95, in steps of 5.
- «Дата проверки» is an ISO date after the session date.
- Several exit conditions go on one line, separated by «; ».
- In quick mode there are only two stakes: Скептика and Оппонента.
- The last four fields stay «—». The retro fills them in.
