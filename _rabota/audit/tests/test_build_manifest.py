import json
import tempfile
import unittest
from pathlib import Path

from _rabota.audit.build_manifest import (
    extract_blocks,
    main,
    validate_control_counts,
    write_jsonl,
)


class ExtractBlocksTests(unittest.TestCase):
    def test_extracts_reader_blocks_in_order_and_excludes_service_navigation(self):
        html = """
        <html><body>
          <nav><p>Служебная навигация</p></nav>
          <main>
            <h1>Тестовая книга</h1>
            <section id="karta">
              <h2>Карта</h2>
              <p>Вводный текст с <button class="t" popovertarget="gp-term">термином</button>.</p>
              <div class="soil" id="soil-sand"><h3>Песок</h3><p>Быстро отводит воду.</p></div>
              <div class="grape"><h3>Прокупац</h3><p>Поздно созревает.</p></div>
              <div class="win"><h3>Вино А</h3><p>Красное вино.</p></div>
              <div class="gl"><p>Тело</p><p>Ощущение веса вина.</p></div>
            </section>
          </main>
          <div class="gpanel" id="gp-term" popover>
            <p class="gp-n">Термин</p><p class="gp-g">Определение термина.</p>
          </div>
          <div class="menju"><p>Содержание</p></div>
        </body></html>
        """

        blocks = extract_blocks(html)

        self.assertEqual(
            [block["block_id"] for block in blocks],
            [f"B{number:04d}" for number in range(1, 9)],
        )
        self.assertEqual(
            [block["kind"] for block in blocks],
            ["heading", "heading", "paragraph", "soil", "grape", "wine", "glossary", "popover"],
        )
        self.assertEqual(blocks[2]["text"], "Вводный текст с термином.")
        self.assertEqual(blocks[3]["text"], "Песок Быстро отводит воду.")
        self.assertEqual(blocks[3]["region_id"], "karta")
        self.assertEqual(blocks[7]["dom_id"], "gp-term")
        self.assertTrue(blocks[7]["interactive"])
        self.assertNotIn("Служебная навигация", " ".join(block["text"] for block in blocks))
        self.assertNotIn("Содержание", " ".join(block["text"] for block in blocks))

    def test_live_book_matches_fixed_interface_control_counts(self):
        html = Path("index.html").read_text(encoding="utf-8")
        blocks = extract_blocks(html)

        self.assertEqual(validate_control_counts(blocks, html), [])

    def test_reports_a_missing_tourism_marker(self):
        html = Path("index.html").read_text(encoding="utf-8").replace(
            'class="tour"', 'class="tour-removed"', 1
        )
        blocks = extract_blocks(html)

        self.assertIn(
            "class tour: expected 17, got 16",
            validate_control_counts(blocks, html),
        )

    def test_writes_one_json_object_per_line_without_ascii_escaping(self):
        blocks = [{"block_id": "B0001", "text": "Песок"}]

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "manifest.jsonl"
            write_jsonl(blocks, output)
            lines = output.read_text(encoding="utf-8").splitlines()

        self.assertEqual(lines, ['{"block_id": "B0001", "text": "Песок"}'])
        self.assertEqual(json.loads(lines[0]), blocks[0])

    def test_void_elements_do_not_swallow_following_reader_blocks(self):
        html = """
        <html><head><meta charset="utf-8"></head><body>
          <main><img src="cover.png" alt=""><p>Перед<br>карточкой.</p>
          <div class="soil"><p>Песок.</p></div></main>
          <div class="gpanel" id="gp-one" popover><p>Определение.</p><button class="gp-x">✕</button></div>
        </body></html>
        """

        blocks = extract_blocks(html)

        self.assertEqual(
            [(block["kind"], block["text"]) for block in blocks],
            [
                ("paragraph", "Перед карточкой."),
                ("soil", "Песок."),
                ("popover", "Определение."),
            ],
        )

    def test_command_line_entrypoint_builds_manifest_file(self):
        html = "<main><h1>Книга</h1><p>Факт.</p></main>"

        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "book.html"
            output = Path(directory) / "manifest.jsonl"
            source.write_text(html, encoding="utf-8")

            exit_code = main([str(source), str(output)])
            records = [
                json.loads(line)
                for line in output.read_text(encoding="utf-8").splitlines()
            ]

        self.assertEqual(exit_code, 0)
        self.assertEqual([record["text"] for record in records], ["Книга", "Факт."])

    def test_preserves_reader_facing_svg_labels_as_one_graphic_block(self):
        html = """
        <main><h1>Книга</h1>
          <svg role="img" aria-label="Карта винодельческих районов Сербии">
            <text>ДУНАЙ</text><a><text>Фрушка гора</text></a>
          </svg>
        </main>
        """

        blocks = extract_blocks(html)

        self.assertEqual(blocks[1]["kind"], "graphic")
        self.assertEqual(
            blocks[1]["text"],
            "Карта винодельческих районов Сербии ДУНАЙ Фрушка гора",
        )

    def test_preserves_collapsible_section_summaries_and_uses_them_as_headings(self):
        html = """
        <main><section id="fruska"><details class="place-det">
          <summary class="place-head"><span>Фрушка гора</span><span>Сремский район</span></summary>
          <div><p>Факт о регионе.</p></div>
        </details></section></main>
        """

        blocks = extract_blocks(html)

        self.assertEqual(
            [(block["kind"], block["text"]) for block in blocks],
            [
                ("summary", "Фрушка гора Сремский район"),
                ("paragraph", "Факт о регионе."),
            ],
        )
        self.assertEqual(blocks[1]["heading_path"], ["Фрушка гора Сремский район"])

    def test_records_tourism_markers_and_linked_popover_targets(self):
        html = """
        <main><div class="win"><p>Хозяйство <span class="tour" title="Стоит приехать">◈</span>
          использует <button class="t" popovertarget="gp-grape">сорт</button>.</p></div></main>
        <div class="gpanel" id="gp-grape" popover><p>Определение.</p></div>
        """

        blocks = extract_blocks(html)

        self.assertEqual(blocks[0]["markers"], ["tour"])
        self.assertEqual(blocks[0]["interactive_targets"], ["gp-grape"])


if __name__ == "__main__":
    unittest.main()
