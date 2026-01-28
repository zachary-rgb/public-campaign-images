#!/usr/bin/env python3
"""
Compare two Portamedic documentation sources by:
- Extracting document text (DOCX -> text via stdlib ZIP+XML, or HTML -> text)
- Extracting embedded images and OCR'ing them via free local Tesseract
- Producing combined per-doc text + a diff (unified diff + HTML diff)

Usage example:
  python3 compare_portamedic_docs.py \
    --new "/Users/noahdebrincat/Desktop/Projects/Portamedic/new docs/Portamedic - Ordering API Documentation (v2) (2).docx" \
    --old "/Users/noahdebrincat/Desktop/Projects/Portamedic/old docs/PM - Ordering API Documentation.docx" \
    --out "/Users/noahdebrincat/Desktop/Projects/Portamedic/out/portamedic_ordering_api_compare"
"""

from __future__ import annotations

import argparse
import difflib
import html
import os
import re
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = {"w": W_NS}


def _collapse_whitespace(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def extract_html_text(html_path: Path) -> str:
    """
    Minimal HTML -> text extraction without external deps.
    Removes scripts/styles and strips tags.
    """
    raw = html_path.read_text(encoding="utf-8", errors="ignore")
    raw = re.sub(r"(?is)<(script|style)\b.*?>.*?</\1>", "", raw)
    raw = re.sub(r"(?is)<!--.*?-->", "", raw)
    raw = re.sub(r"(?is)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?is)</p\s*>", "\n", raw)
    raw = re.sub(r"(?is)</h[1-6]\s*>", "\n", raw)
    raw = re.sub(r"(?is)</li\s*>", "\n", raw)
    raw = re.sub(r"(?is)<[^>]+>", "", raw)
    raw = html.unescape(raw)
    return _collapse_whitespace(raw)


def _w_tag(local: str) -> str:
    return f"{{{W_NS}}}{local}"


def _para_text(p: ET.Element) -> str:
    chunks: list[str] = []
    for node in p.iter():
        tag = node.tag
        if tag == _w_tag("t") and node.text:
            chunks.append(node.text)
        elif tag == _w_tag("tab"):
            chunks.append("\t")
        elif tag in (_w_tag("br"), _w_tag("cr")):
            chunks.append("\n")
    return "".join(chunks).strip()


def _cell_text(tc: ET.Element) -> str:
    parts: list[str] = []
    for p in tc.findall(".//w:p", XML_NS):
        t = _para_text(p)
        if t:
            parts.append(t)
    return _collapse_whitespace("\n".join(parts))


def extract_docx_text(docx_path: Path) -> str:
    """
    Extract readable text from DOCX using only stdlib.
    Keeps some structure: paragraphs and tables.
    """
    xml_candidates = [
        "word/document.xml",
        "word/footnotes.xml",
        "word/endnotes.xml",
    ]
    # include headers/footers if present
    with zipfile.ZipFile(docx_path) as z:
        for name in z.namelist():
            if re.match(r"word/(header|footer)\d+\.xml$", name):
                xml_candidates.append(name)

        out_sections: list[str] = []
        for name in xml_candidates:
            if name not in z.namelist():
                continue
            try:
                data = z.read(name)
                root = ET.fromstring(data)
            except Exception:
                continue

            section_lines: list[str] = []

            body = root.find("w:body", XML_NS)
            if body is None:
                body = root  # footnotes/endnotes don't have w:body

            for child in list(body):
                if child.tag == _w_tag("p"):
                    t = _para_text(child)
                    if t:
                        section_lines.append(t)
                elif child.tag == _w_tag("tbl"):
                    for tr in child.findall(".//w:tr", XML_NS):
                        cells = tr.findall("./w:tc", XML_NS)
                        row = " | ".join([_cell_text(tc) for tc in cells]).strip()
                        row = re.sub(r"\s+\|\s+", " | ", row)
                        if row:
                            section_lines.append(row)
                # else ignore other elements

            section_text = _collapse_whitespace("\n".join(section_lines))
            if section_text:
                out_sections.append(f"=== {name} ===\n{section_text}")

    return _collapse_whitespace("\n\n".join(out_sections))


def extract_docx_images(docx_path: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    images: list[Path] = []
    with zipfile.ZipFile(docx_path) as z:
        for name in z.namelist():
            if not name.startswith("word/media/"):
                continue
            filename = Path(name).name
            dest = out_dir / filename
            dest.write_bytes(z.read(name))
            images.append(dest)
    return images


def which(cmd: str) -> Optional[str]:
    p = shutil.which(cmd)
    return p


def convert_to_png(src: Path, dst: Path) -> bool:
    """
    Best-effort conversion for vector formats (e.g., EMF) to PNG using common local tools.
    Returns True if conversion succeeded.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)

    magick = which("magick")
    if magick:
        r = subprocess.run([magick, str(src), str(dst)], capture_output=True, text=True)
        return r.returncode == 0 and dst.exists() and dst.stat().st_size > 0

    convert = which("convert")
    if convert:
        r = subprocess.run([convert, str(src), str(dst)], capture_output=True, text=True)
        return r.returncode == 0 and dst.exists() and dst.stat().st_size > 0

    inkscape = which("inkscape")
    if inkscape:
        r = subprocess.run(
            [inkscape, str(src), f"--export-type=png", f"--export-filename={dst}"],
            capture_output=True,
            text=True,
        )
        return r.returncode == 0 and dst.exists() and dst.stat().st_size > 0

    return False


@dataclass
class OcrResult:
    image: Path
    ocr_txt: Optional[Path]
    skipped_reason: Optional[str] = None


def ocr_images(images: Iterable[Path], ocr_dir: Path, lang: str = "eng") -> list[OcrResult]:
    ocr_dir.mkdir(parents=True, exist_ok=True)
    results: list[OcrResult] = []

    raster_exts = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
    tesseract = which("tesseract")
    if not tesseract:
        raise RuntimeError("tesseract not found on PATH. Install it to run OCR.")

    for img in images:
        ext = img.suffix.lower()
        img_to_ocr = img

        if ext not in raster_exts:
            # try conversion for common vector formats
            converted = ocr_dir / f"{img.stem}.png"
            if convert_to_png(img, converted):
                img_to_ocr = converted
            else:
                results.append(OcrResult(image=img, ocr_txt=None, skipped_reason=f"unsupported image type: {ext}"))
                continue

        out_base = ocr_dir / img_to_ocr.stem
        # tesseract writes `${out_base}.txt`
        cmd = [tesseract, str(img_to_ocr), str(out_base), "-l", lang, "--psm", "6"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        out_txt = Path(str(out_base) + ".txt")
        if r.returncode != 0 or not out_txt.exists():
            results.append(
                OcrResult(
                    image=img,
                    ocr_txt=None,
                    skipped_reason=f"tesseract failed (code={r.returncode})",
                )
            )
            continue

        results.append(OcrResult(image=img, ocr_txt=out_txt, skipped_reason=None))

    return results


def find_old_doc_html_and_images(old_doc_dir: Path) -> tuple[Optional[Path], list[Path]]:
    html_files = sorted(old_doc_dir.glob("*.docx.html"))
    html_path = html_files[0] if html_files else None
    images_dir = old_doc_dir / "images"
    imgs: list[Path] = []
    if images_dir.exists():
        for p in sorted(images_dir.rglob("*")):
            if p.is_file():
                imgs.append(p)
    return html_path, imgs


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n", encoding="utf-8")


def build_combined_text(doc_text: str, ocr_results: list[OcrResult]) -> str:
    parts: list[str] = []
    parts.append("=== DOCUMENT TEXT ===")
    parts.append(doc_text.strip())
    parts.append("")
    parts.append("=== OCR (IMAGES -> TEXT) ===")

    skipped: list[str] = []
    for r in ocr_results:
        if r.ocr_txt and r.ocr_txt.exists():
            txt = r.ocr_txt.read_text(encoding="utf-8", errors="ignore").strip()
            if txt:
                parts.append(f"\n--- IMAGE: {r.image.name} ---\n{txt}")
        else:
            skipped.append(f"{r.image.name}: {r.skipped_reason or 'skipped'}")

    if skipped:
        parts.append("")
        parts.append("=== OCR SKIPPED / FAILED ===")
        parts.extend(skipped)

    return _collapse_whitespace("\n".join(parts))


def make_unified_diff(old_text: str, new_text: str, old_label: str, new_label: str) -> str:
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)
    diff = difflib.unified_diff(old_lines, new_lines, fromfile=old_label, tofile=new_label, n=3)
    return "".join(diff).strip()


def make_html_diff(old_text: str, new_text: str, old_label: str, new_label: str) -> str:
    hd = difflib.HtmlDiff(tabsize=2, wrapcolumn=120)
    return hd.make_file(old_text.splitlines(), new_text.splitlines(), fromdesc=old_label, todesc=new_label)


def parse_source(path: Path, out_dir: Path, lang: str) -> tuple[str, list[OcrResult]]:
    if path.is_file() and path.suffix.lower() == ".docx":
        doc_text = extract_docx_text(path)
        images = extract_docx_images(path, out_dir / "images_extracted")
        ocr_results = ocr_images(images, out_dir / "ocr", lang=lang) if images else []
        return doc_text, ocr_results

    if path.is_dir():
        html_path, images = find_old_doc_html_and_images(path)
        doc_text = extract_html_text(html_path) if html_path else ""
        ocr_results = ocr_images(images, out_dir / "ocr", lang=lang) if images else []
        return doc_text, ocr_results

    raise ValueError(f"Unsupported input path: {path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", required=True, type=Path, help="Path to NEW doc (.docx file or extracted doc directory).")
    ap.add_argument("--old", required=True, type=Path, help="Path to OLD doc (.docx file or extracted doc directory).")
    ap.add_argument("--out", type=Path, default=None, help="Output directory for generated txt/diff files.")
    ap.add_argument("--lang", type=str, default="eng", help="Tesseract language (default: eng).")
    args = ap.parse_args()

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = args.out or (Path.cwd() / "out" / f"portamedic_compare_{stamp}")
    out_dir.mkdir(parents=True, exist_ok=True)

    # OLD
    old_dir = out_dir / "old"
    old_dir.mkdir(exist_ok=True)
    old_doc_text, old_ocr = parse_source(args.old, old_dir, lang=args.lang)
    old_combined = build_combined_text(old_doc_text, old_ocr)
    write_text(old_dir / "document_text.txt", old_doc_text)
    write_text(old_dir / "combined.txt", old_combined)

    # NEW
    new_dir = out_dir / "new"
    new_dir.mkdir(exist_ok=True)
    new_doc_text, new_ocr = parse_source(args.new, new_dir, lang=args.lang)
    new_combined = build_combined_text(new_doc_text, new_ocr)
    write_text(new_dir / "document_text.txt", new_doc_text)
    write_text(new_dir / "combined.txt", new_combined)

    # DIFF
    diff_txt = make_unified_diff(old_combined, new_combined, old_label="OLD/combined.txt", new_label="NEW/combined.txt")
    write_text(out_dir / "diff.txt", diff_txt if diff_txt else "(no differences detected)")
    (out_dir / "diff.html").write_text(
        make_html_diff(old_combined, new_combined, old_label="OLD", new_label="NEW"),
        encoding="utf-8",
    )

    print(f"✅ Wrote outputs to: {out_dir}")
    print(f"   - {old_dir / 'combined.txt'}")
    print(f"   - {new_dir / 'combined.txt'}")
    print(f"   - {out_dir / 'diff.txt'}")
    print(f"   - {out_dir / 'diff.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


