from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


CARD_KINDS = {
    "soil": "soil",
    "grape": "grape",
    "win": "wine",
    "gl": "glossary",
    "gpanel": "popover",
}

PLAIN_BLOCK_TAGS = {"p", "li", "figcaption", "caption", "th", "td"}
HEADING_TAGS = {f"h{level}" for level in range(1, 7)}
SERVICE_CLASSES = {"ctl", "menju"}
VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
CONTROL_COUNTS = {
    "place-det": 10,
    "soil": 11,
    "grape": 30,
    "win": 55,
    "gpanel": 64,
    "gl": 18,
    "tour": 17,
}


def _classes(attributes: dict[str, str]) -> set[str]:
    return set(attributes.get("class", "").split())


def _normalise_text(parts: list[str]) -> str:
    text = " ".join(part.strip() for part in parts if part.strip())
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub(r"\s+([,.;:!?…])", r"\1", text)


class _ReaderBlockParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[dict[str, object]] = []
        self.stack: list[dict[str, object]] = []
        self.capture: dict[str, object] | None = None
        self.skip_depth = 0
        self.current_region_id: str | None = None
        self.heading_levels: dict[int, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._open_tag(tag, attrs)
        if tag in VOID_TAGS:
            self.handle_endtag(tag)

    def _open_tag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: value or "" for name, value in attrs}
        classes = _classes(attributes)
        frame = {
            "tag": tag,
            "region_before": self.current_region_id,
            "skip_started": False,
        }
        self.stack.append(frame)

        if self.skip_depth:
            self.skip_depth += 1
            return

        if tag in {"style", "script", "nav"} or classes & SERVICE_CLASSES or "gp-x" in classes:
            self.skip_depth = 1
            frame["skip_started"] = True
            return

        if tag in {"section", "details"} and attributes.get("id"):
            self.current_region_id = attributes["id"]

        if self.capture is not None:
            if "tour" in classes and "tour" not in self.capture["markers"]:
                self.capture["markers"].append("tour")
            target = attributes.get("popovertarget")
            if target and target not in self.capture["interactive_targets"]:
                self.capture["interactive_targets"].append(target)
            return

        in_main = any(item["tag"] == "main" for item in self.stack)
        kind = next((CARD_KINDS[name] for name in CARD_KINDS if name in classes), None)
        if kind == "popover" or in_main:
            if kind is not None:
                self._start_capture(tag, attributes, kind, interactive=kind == "popover")
            elif tag == "svg" and attributes.get("aria-label"):
                self._start_capture(tag, attributes, "graphic", interactive=False)
                assert self.capture is not None
                self.capture["parts"].append(attributes["aria-label"])
            elif tag == "summary":
                heading_level = 2 if classes & {"place-head", "part-head"} else 3
                self._start_capture(
                    tag,
                    attributes,
                    "summary",
                    interactive=True,
                    heading_level=heading_level,
                )
            elif tag in HEADING_TAGS:
                self._start_capture(
                    tag,
                    attributes,
                    "heading",
                    interactive=False,
                    heading_level=int(tag[1]),
                )
            elif tag in PLAIN_BLOCK_TAGS:
                self._start_capture(tag, attributes, "paragraph", interactive=False)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._open_tag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self.capture is not None and not self.skip_depth:
            self.capture["parts"].append(data)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            return

        frame = self.stack[-1]
        if self.skip_depth:
            self.skip_depth -= 1
        elif self.capture is not None and self.capture["depth"] == len(self.stack):
            self._finish_capture()

        self.current_region_id = frame["region_before"]
        self.stack.pop()

    def _start_capture(
        self,
        tag: str,
        attributes: dict[str, str],
        kind: str,
        *,
        interactive: bool,
        heading_level: int | None = None,
    ) -> None:
        self.capture = {
            "tag": tag,
            "depth": len(self.stack),
            "kind": kind,
            "dom_id": attributes.get("id") or None,
            "region_id": self.current_region_id,
            "interactive": interactive,
            "heading_level": heading_level,
            "parts": [],
            "markers": [],
            "interactive_targets": [],
        }

    def _finish_capture(self) -> None:
        assert self.capture is not None
        text = _normalise_text(self.capture["parts"])
        if text:
            kind = str(self.capture["kind"])
            if self.capture["heading_level"] is not None:
                level = int(self.capture["heading_level"])
                self.heading_levels[level] = text
                for deeper_level in range(level + 1, 7):
                    self.heading_levels.pop(deeper_level, None)

            heading_path = [
                self.heading_levels[level]
                for level in sorted(self.heading_levels)
            ]
            number = len(self.blocks) + 1
            self.blocks.append(
                {
                    "block_id": f"B{number:04d}",
                    "order": number,
                    "dom_id": self.capture["dom_id"],
                    "kind": kind,
                    "heading_path": heading_path,
                    "region_id": self.capture["region_id"],
                    "text": text,
                    "interactive": bool(self.capture["interactive"]),
                    "markers": self.capture["markers"],
                    "interactive_targets": self.capture["interactive_targets"],
                }
            )
        self.capture = None


def extract_blocks(html: str) -> list[dict[str, object]]:
    parser = _ReaderBlockParser()
    parser.feed(html)
    parser.close()
    return parser.blocks


class _ClassCounter(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.counts: Counter[str] = Counter()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: value or "" for name, value in attrs}
        self.counts.update(_classes(attributes))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def validate_control_counts(blocks: list[dict[str, object]], html: str) -> list[str]:
    counter = _ClassCounter()
    counter.feed(html)
    counter.close()

    errors = []
    for class_name, expected in CONTROL_COUNTS.items():
        actual = counter.counts[class_name]
        if actual != expected:
            errors.append(f"class {class_name}: expected {expected}, got {actual}")

    extracted_counts = Counter(str(block["kind"]) for block in blocks)
    for kind, expected in {
        "soil": 11,
        "grape": 30,
        "wine": 55,
        "glossary": 18,
        "popover": 64,
    }.items():
        actual = extracted_counts[kind]
        if actual != expected:
            errors.append(f"manifest kind {kind}: expected {expected}, got {actual}")
    return errors


def write_jsonl(blocks: list[dict[str, object]], path: Path) -> None:
    content = "".join(
        json.dumps(block, ensure_ascii=False) + "\n"
        for block in blocks
    )
    path.write_text(content, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the reader-facing audit manifest")
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args(argv)

    html = arguments.source.read_text(encoding="utf-8")
    write_jsonl(extract_blocks(html), arguments.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
