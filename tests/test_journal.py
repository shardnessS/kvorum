"""Тесты скрипта журнала: python -m unittest discover -s tests -v"""

import contextlib
import datetime
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "kvorum-retro" / "scripts"))

import journal  # noqa: E402

EXAMPLE = ROOT / "examples" / "journal.md"

ENTRY = """\
## 2026-01-10 · Тест
- Тип: цены
- Вердикт: делать
- Прогноз: что-то случится
- Уверенность: {confidence}
- Дата проверки: {check}
- Итог: {result_text}
- Сбылся: {result}
- Кто прав: {directors}
"""


def entry(confidence="70%", check="2026-02-10", result="—", result_text="—", directors="—"):
    return ENTRY.format(confidence=confidence, check=check, result=result,
                        result_text=result_text, directors=directors)


def run(command, text, today="2026-10-15"):
    entries = journal.parse(text)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = journal.COMMANDS[command](entries, datetime.date.fromisoformat(today))
    return code, out.getvalue()


class ParseTest(unittest.TestCase):
    def test_example_journal(self):
        entries = journal.parse(EXAMPLE.read_text(encoding="utf-8"))
        self.assertEqual(len(entries), 13)
        first = entries[0]
        self.assertEqual(first.title, "Нанять второго менеджера по продажам")
        self.assertEqual(first.confidence, 70)
        self.assertEqual(first.outcome, 1.0)
        self.assertEqual(first.directors()["Операционщик"], "да")

    def test_value_with_colons(self):
        [item] = journal.parse(entry(directors="Скептик: да; Оппонент: нет"))
        self.assertEqual(item.directors(), {"Скептик": "да", "Оппонент": "нет"})


class DueTest(unittest.TestCase):
    def test_due_and_not_due(self):
        text = entry(check="2026-10-01") + "\n" + entry(check="2027-01-01").replace("Тест", "Позже")
        code, out = run("due", text)
        self.assertEqual(code, 0)
        self.assertIn("Пора проверить: 1", out)
        self.assertIn("просрочено на 14 дн.", out)
        self.assertNotIn("Позже", out)

    def test_closed_entry_is_not_due(self):
        _, out = run("due", entry(check="2026-10-01", result="да", result_text="сбылось"))
        self.assertIn("ничего", out)


class StatsTest(unittest.TestCase):
    def test_brier_and_bands(self):
        text = "\n".join([
            entry(confidence="80%", result="да", result_text="ok"),
            entry(confidence="80%", result="нет", result_text="ok"),
            entry(confidence="60%", result="частично", result_text="ok"),
        ])
        _, out = run("stats", text)
        # ((0.8-1)^2 + (0.8-0)^2 + (0.6-0.5)^2) / 3 = 0.23
        self.assertIn("Brier: 0.23", out)
        self.assertIn("Закрыто: 3", out)

    def test_overconfidence(self):
        text = "\n".join(entry(confidence="90%", result=r, result_text="ok") for r in ("да", "нет", "нет"))
        _, out = run("stats", text)
        self.assertIn("переоцениваешь себя", out)

    def test_uncheckable_left_out(self):
        text = entry(result="нельзя проверить", result_text="ok")
        _, out = run("stats", text)
        self.assertIn("Нельзя проверить: 1", out)
        self.assertIn("Закрытых решений пока нет", out)


class CheckTest(unittest.TestCase):
    def test_example_is_valid(self):
        code, _ = run("check", EXAMPLE.read_text(encoding="utf-8"))
        self.assertEqual(code, 0)

    def test_bad_confidence_and_dates(self):
        code, out = run("check", entry(confidence="72%", check="2025-12-01", result="может быть"))
        self.assertEqual(code, 1)
        self.assertIn("уверенность", out)
        self.assertIn("позже даты решения", out)
        self.assertIn("«Сбылся»", out)


if __name__ == "__main__":
    unittest.main()
