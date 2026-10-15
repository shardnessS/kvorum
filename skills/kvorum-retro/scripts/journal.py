"""Журнал решений Кворума: что пора проверить, калибровка, проверка формата.

    python journal.py due   kvorum/journal.md [--today 2026-10-15]
    python journal.py stats kvorum/journal.md
    python journal.py check kvorum/journal.md

Формат журнала и определения — references/journal-format.md.
Только стандартная библиотека Python 3.8+.
"""

import argparse
import datetime
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean

HEADING = re.compile(r"^##\s+(\S+)\s*[·|—–-]\s*(.+?)\s*$")
FIELD = re.compile(r"^\s*[-*]\s+([^:]+?)\s*:\s*(.*?)\s*$")
DIRECTORS = ("Скептик", "Оппонент", "Инвестор", "Операционщик")
OUTCOMES = {"да": 1.0, "частично": 0.5, "нет": 0.0}
UNCHECKABLE = "нельзя проверить"
EMPTY = {"", "—", "–", "-"}
BANDS = ((50, 60), (65, 75), (80, 95))
TYPES = ("цены", "люди", "запуск", "закупка", "маркетинг", "карьера", "другое")
REQUIRED = ("Тип", "Вердикт", "Прогноз", "Уверенность", "Дата проверки")


def parse_date(value):
    try:
        return datetime.date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


@dataclass
class Entry:
    date: str
    title: str
    line: int
    fields: dict = field(default_factory=dict)

    def get(self, key):
        value = self.fields.get(key, "").strip()
        return "" if value in EMPTY else value

    @property
    def decided(self):
        return parse_date(self.date)

    @property
    def check_date(self):
        return parse_date(self.get("Дата проверки"))

    @property
    def confidence(self):
        match = re.fullmatch(r"(\d{1,3})\s*%?", self.get("Уверенность"))
        return int(match.group(1)) if match else None

    @property
    def result(self):
        return self.get("Сбылся").lower()

    @property
    def outcome(self):
        return OUTCOMES.get(self.result)

    @property
    def is_open(self):
        return not self.result

    @property
    def kind(self):
        return self.get("Тип").lower() or "другое"

    def directors(self):
        marks = {}
        for part in self.get("Кто прав").split(";"):
            match = re.match(r"\s*([^:—–-]+?)\s*[:—–-]\s*(.+?)\s*$", part)
            if match:
                marks[match.group(1)] = match.group(2).lower()
        return marks


def parse(text):
    entries, current = [], None
    for number, line in enumerate(text.splitlines(), 1):
        heading = HEADING.match(line)
        if heading:
            current = Entry(heading.group(1), heading.group(2), number)
            entries.append(current)
        elif line.startswith("#"):
            current = None
        elif current is not None:
            match = FIELD.match(line)
            if match:
                current.fields[match.group(1)] = match.group(2)
    return entries


def print_table(rows):
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    for row in rows:
        print("  " + "  ".join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip())


def percent(value):
    return f"{value * 100:.0f}%"


def band_verdict(count, confidence, hit):
    if count < 3:
        return "мало данных"
    if hit < confidence - 10:
        return "переоцениваешь себя"
    if hit > confidence + 10:
        return "недооцениваешь себя"
    return "точно"


def director_score(marks):
    yes = marks.count("да")
    part = marks.count("частично")
    no = marks.count("нет")
    total = yes + part + no
    return yes, part, no, ((yes + 0.5 * part) / total if total else None)


def cmd_due(entries, today):
    waiting = sorted((e for e in entries if e.is_open and e.check_date), key=lambda e: e.check_date)
    due = [e for e in waiting if e.check_date <= today]
    if not due:
        print("Пора проверить: ничего.")
        if waiting:
            print(f"Ближайшая проверка: {waiting[0].check_date} — {waiting[0].title}")
        return 0
    print(f"Пора проверить: {len(due)}")
    for entry in due:
        late = (today - entry.check_date).days
        note = "сегодня" if late == 0 else f"просрочено на {late} дн."
        print(f"  {entry.date} · {entry.title} — проверка {entry.check_date}, {note}")
    return 0


def cmd_stats(entries, today):
    closed = [e for e in entries if e.outcome is not None and e.confidence]
    uncheckable = [e for e in entries if e.result == UNCHECKABLE]
    waiting = [e for e in entries if e.is_open]
    due = [e for e in waiting if e.check_date and e.check_date <= today]
    print(
        f"Решений: {len(entries)}. Закрыто: {len(closed)}. Нельзя проверить: {len(uncheckable)}. "
        f"Ждут проверки: {len(waiting)}, из них пора: {len(due)}."
    )
    if not closed:
        print("Закрытых решений пока нет, калибровку считать не по чему.")
        return 0

    print("\nКалибровка")
    rows = [("Уверенность", "Решений", "Средняя", "Сбылось", "Вывод")]
    for low, high in BANDS:
        band = [e for e in closed if low <= e.confidence <= high]
        if not band:
            rows.append((f"{low}–{high}%", "0", "—", "—", "нет данных"))
            continue
        confidence = mean(e.confidence for e in band)
        hit = mean(e.outcome for e in band) * 100
        rows.append((f"{low}–{high}%", str(len(band)), f"{confidence:.0f}%", f"{hit:.0f}%",
                     band_verdict(len(band), confidence, hit)))
    print_table(rows)
    brier = mean((e.confidence / 100 - e.outcome) ** 2 for e in closed)
    print(f"\nBrier: {brier:.2f} (0 — идеально, 0.25 — как монетка)")

    print("\nПо типам решений")
    rows = [("Тип", "Решений", "Средняя уверенность", "Сбылось")]
    for kind in sorted({e.kind for e in closed}):
        group = [e for e in closed if e.kind == kind]
        rows.append((kind, str(len(group)), f"{mean(e.confidence for e in group):.0f}%",
                     percent(mean(e.outcome for e in group))))
    print_table(rows)

    print("\nСовет директоров")
    rows = [("Директор", "Ставок", "да", "частично", "нет", "Счёт")]
    for name in DIRECTORS:
        yes, part, no, score = director_score([e.directors().get(name, "") for e in entries])
        rows.append((name, str(yes + part + no), str(yes), str(part), str(no),
                     percent(score) if score is not None else "—"))
    print_table(rows)

    best = []
    for kind in sorted({e.kind for e in entries}):
        group = [e for e in entries if e.kind == kind]
        scored = []
        for name in DIRECTORS:
            yes, part, no, score = director_score([e.directors().get(name, "") for e in group])
            if score is not None and yes + part + no >= 2:
                scored.append((score, name, yes + part + no))
        if scored:
            top = max(score for score, _, _ in scored)
            leaders = ", ".join(f"{name} ({total})" for score, name, total in scored if score == top)
            best.append(f"  {kind}: {percent(top)} — {leaders}")
    if best:
        print("\nЧаще всех прав по типам")
        print("\n".join(best))

    if len(closed) < 10:
        print("\nЗакрытых решений меньше 10, выводы предварительные.")
    return 0


def cmd_check(entries, today):
    problems = []
    if not entries:
        problems.append("нет ни одной записи вида «## ГГГГ-ММ-ДД · тема»")
    for entry in entries:
        where = f"строка {entry.line}, «{entry.title}»"
        if entry.decided is None:
            problems.append(f"{where}: дата в заголовке не в формате ГГГГ-ММ-ДД")
        for key in REQUIRED:
            if not entry.get(key):
                problems.append(f"{where}: нет поля «{key}»")
        raw = entry.get("Уверенность")
        confidence = entry.confidence
        if raw and (confidence is None or not 50 <= confidence <= 95 or confidence % 5):
            problems.append(f"{where}: уверенность «{raw}» — целое число от 50 до 95 с шагом 5")
        if entry.get("Дата проверки"):
            if entry.check_date is None:
                problems.append(f"{where}: дата проверки не в формате ГГГГ-ММ-ДД")
            elif entry.decided and entry.check_date <= entry.decided:
                problems.append(f"{where}: дата проверки должна быть позже даты решения")
        if entry.get("Тип") and entry.kind not in TYPES:
            problems.append(f"{where}: тип «{entry.get('Тип')}» — один из: {', '.join(TYPES)}")
        if entry.result and entry.result not in OUTCOMES and entry.result != UNCHECKABLE:
            problems.append(f"{where}: «Сбылся» — да, нет, частично или нельзя проверить")
        if entry.result and not entry.get("Итог"):
            problems.append(f"{where}: есть «Сбылся», но пустой «Итог»")
        for name, mark in entry.directors().items():
            if name not in DIRECTORS:
                problems.append(f"{where}: в «Кто прав» неизвестный директор «{name}»")
            elif mark not in OUTCOMES and mark != UNCHECKABLE:
                problems.append(f"{where}: оценка «{mark}» у директора {name}")
    if problems:
        print(f"Проблем: {len(problems)}")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print(f"Журнал в порядке: записей {len(entries)}.")
    return 0


COMMANDS = {"due": cmd_due, "stats": cmd_stats, "check": cmd_check}


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Журнал решений Кворума")
    parser.add_argument("command", choices=COMMANDS, help="due — что пора проверить, stats — калибровка, check — формат")
    parser.add_argument("journal", type=Path, nargs="?", default=Path("kvorum/journal.md"))
    parser.add_argument("--today", type=datetime.date.fromisoformat, default=datetime.date.today(),
                        help="дата отсчёта, ГГГГ-ММ-ДД")
    args = parser.parse_args(argv)
    if not args.journal.is_file():
        print(f"Журнал не найден: {args.journal}")
        return 1
    entries = parse(args.journal.read_text(encoding="utf-8"))
    return COMMANDS[args.command](entries, args.today)


if __name__ == "__main__":
    sys.exit(main())
