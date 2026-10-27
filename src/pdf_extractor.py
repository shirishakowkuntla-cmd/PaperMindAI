"""
PDF Extractor and Section Parser Module for PaperMind AI.
Extracts clean text and structural sections (Title, Abstract, Methods, Results, Conclusion)
using PyMuPDF (fitz) with automatic fallback to pypdf.
"""

import io
import re
from typing import Dict, List, Optional, Union, Tuple


class PDFExtractor:
    """Extracts and structures scientific paper content from PDF documents."""

    # Common section header patterns in academic papers
    SECTION_PATTERNS = {
        "abstract": [
            r"\babstract\b",
            r"\bsummary\b"
        ],
        "introduction": [
            r"(?:^|\n)(?:\d+[\.\s]+)?(?:i[\.\s]+)?introduction\b",
            r"(?:^|\n)background\b"
        ],
        "related_work": [
            r"(?:^|\n)(?:\d+[\.\s]+)?related\s+work\b",
            r"(?:^|\n)(?:\d+[\.\s]+)?literature\s+review\b",
            r"(?:^|\n)(?:\d+[\.\s]+)?prior\s+work\b"
        ],
        "methodology": [
            r"(?:^|\n)(?:\d+[\.\s]+)?methodology\b",
            r"(?:^|\n)(?:\d+[\.\s]+)?methods\b",
            r"(?:^|\n)(?:\d+[\.\s]+)?proposed\s+(?:method|approach|framework|system|architecture)\b",
            r"(?:^|\n)(?:\d+[\.\s]+)?model\s+architecture\b",
            r"(?:^|\n)(?:\d+[\.\s]+)?system\s+design\b"
        ],
        "results": [
            r"(?:^|\n)(?:\d+[\.\s]+)?results\b",
            r"(?:^|\n)(?:\d+[\.\s]+)?experiments\b",
            r"(?:^|\n)(?:\d+[\.\s]+)?evaluation\b",
            r"(?:^|\n)(?:\d+[\.\s]+)?experimental\s+(?:setup|results|evaluation)\b",
            r"(?:^|\n)(?:\d+[\.\s]+)?performance\s+analysis\b"
        ],
        "discussion": [
            r"(?:^|\n)(?:\d+[\.\s]+)?discussion\b",
            r"(?:^|\n)(?:\d+[\.\s]+)?analysis\b"
        ],
        "conclusion": [
            r"(?:^|\n)(?:\d+[\.\s]+)?conclusion\b",
            r"(?:^|\n)(?:\d+[\.\s]+)?conclusions\s+and\s+future\s+work\b",
            r"(?:^|\n)(?:\d+[\.\s]+)?concluding\s+remarks\b"
        ],
        "references": [
            r"(?:^|\n)references\b",
            r"(?:^|\n)bibliography\b"
        ]
    }

    def __init__(self):
        self._fitz_available = self._check_fitz()

    @staticmethod
    def _check_fitz() -> bool:
        try:
            import fitz
            return True
        except ImportError:
            return False

    def extract_from_file(self, file_source: Union[str, bytes, io.BytesIO]) -> Dict:
        """
        Extract text, metadata, and sections from a PDF file path or stream.

        Args:
            file_source: Path string, bytes, or BytesIO buffer of the PDF file.

        Returns:
            Dict containing metadata, full_text, pages, and parsed sections.
        """
        if self._fitz_available:
            try:
                return self._extract_with_fitz(file_source)
            except Exception as e:
                # Fallback to pypdf if fitz fails on this file
                return self._extract_with_pypdf(file_source, fallback_reason=str(e))
        else:
            return self._extract_with_pypdf(file_source)

    def _extract_with_fitz(self, file_source: Union[str, bytes, io.BytesIO]) -> Dict:
        """Primary extractor using PyMuPDF (fitz) for high accuracy."""
        import fitz

        if isinstance(file_source, (bytes, bytearray)):
            doc = fitz.open(stream=file_source, filetype="pdf")
        elif isinstance(file_source, io.BytesIO):
            doc = fitz.open(stream=file_source.getvalue(), filetype="pdf")
        else:
            doc = fitz.open(file_source)

        page_texts = []
        num_pages = len(doc)

        for page_num in range(num_pages):
            page = doc[page_num]
            text = page.get_text("text")
            cleaned = self._clean_text(text)
            if cleaned:
                page_texts.append({"page_number": page_num + 1, "text": cleaned})

        doc.close()

        full_text = "\n\n".join([p["text"] for p in page_texts])
        metadata = self._compute_metadata(full_text, num_pages, engine="PyMuPDF")
        sections = self._parse_sections(full_text, page_texts)

        return {
            "metadata": metadata,
            "full_text": full_text,
            "page_count": num_pages,
            "pages": page_texts,
            "sections": sections,
            "title": self._detect_title(page_texts, full_text)
        }

    def _extract_with_pypdf(self, file_source: Union[str, bytes, io.BytesIO], fallback_reason: Optional[str] = None) -> Dict:
        """Fallback extractor using pypdf."""
        import pypdf

        if isinstance(file_source, (bytes, bytearray)):
            stream = io.BytesIO(file_source)
        elif isinstance(file_source, io.BytesIO):
            stream = file_source
        else:
            stream = open(file_source, "rb")

        reader = pypdf.PdfReader(stream)
        num_pages = len(reader.pages)
        page_texts = []

        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            cleaned = self._clean_text(text)
            if cleaned:
                page_texts.append({"page_number": idx + 1, "text": cleaned})

        if isinstance(file_source, str) and hasattr(stream, "close"):
            stream.close()

        full_text = "\n\n".join([p["text"] for p in page_texts])
        metadata = self._compute_metadata(full_text, num_pages, engine="pypdf", fallback_reason=fallback_reason)
        sections = self._parse_sections(full_text, page_texts)

        return {
            "metadata": metadata,
            "full_text": full_text,
            "page_count": num_pages,
            "pages": page_texts,
            "sections": sections,
            "title": self._detect_title(page_texts, full_text)
        }

    def _clean_text(self, text: str) -> str:
        """Clean extracted text from common PDF artifacts."""
        if not text:
            return ""

        # Normalize line breaks and tabs
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Fix hyphenated line breaks (e.g. "com-\nputer" -> "computer")
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

        # Replace excessive whitespace while preserving paragraph breaks
        lines = [line.strip() for line in text.split("\n")]
        cleaned_lines = []
        for line in lines:
            if line:
                cleaned_lines.append(line)
            elif cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")

        text = "\n".join(cleaned_lines)

        # Remove standalone page numbers or headers
        text = re.sub(r"\n\s*\d+\s*\n", "\n\n", text)
        return text.strip()

    def _compute_metadata(self, full_text: str, num_pages: int, engine: str, fallback_reason: Optional[str] = None) -> Dict:
        """Compute document metrics like word count, character count, and reading time."""
        words = full_text.split()
        word_count = len(words)
        char_count = len(full_text)
        # Average academic reading speed is ~180-220 wpm
        reading_time_mins = max(1, round(word_count / 200))

        return {
            "page_count": num_pages,
            "word_count": word_count,
            "char_count": char_count,
            "estimated_reading_time_mins": reading_time_mins,
            "extractor_engine": engine,
            "fallback_reason": fallback_reason,
            "is_scanned_suspicion": word_count < (num_pages * 30)
        }

    def _detect_title(self, pages: List[Dict], full_text: str) -> str:
        """Extract a plausible paper title from the first page."""
        if not pages:
            return "Untitled Document"

        first_page = pages[0]["text"]
        lines = [l.strip() for l in first_page.split("\n") if l.strip()]

        title_candidates = []
        for line in lines[:8]:
            # Stop if we hit abstract or common intro tokens
            if re.match(r"(?i)^(abstract|keywords|introduction|arxiv:)", line):
                break
            # Skip emails, URLs, dates, or very short tokens
            if "@" in line or "http" in line or len(line) < 4:
                continue
            title_candidates.append(line)
            if len(" ".join(title_candidates).split()) >= 15:
                break

        if title_candidates:
            raw_title = " ".join(title_candidates[:3])
            # Truncate if unreasonably long
            return raw_title[:200]
        return "Untitled Document"

    def _parse_sections(self, full_text: str, pages: List[Dict]) -> Dict[str, str]:
        """
        Segment the paper text into core academic sections.
        Returns a dict with: abstract, introduction, methodology, results, conclusion, references.
        """
        sections: Dict[str, str] = {
            "abstract": "",
            "introduction": "",
            "methodology": "",
            "results": "",
            "conclusion": "",
            "other": ""
        }

        # Try to locate the Abstract explicitly
        abstract_match = re.search(r"(?i)\babstract\b[\s:\-–—\n]+(.*?)(?=\n(?:\d+[\.\s]+)?(?:i[\.\s]+)?(?:introduction|1\.\s+intro)|$)", full_text, re.DOTALL)
        if abstract_match:
            abstract_text = abstract_match.group(1).strip()
            # Safety check: if abstract is > 3000 chars, it probably ran past the intro boundary
            if len(abstract_text) > 3000:
                abstract_text = abstract_text[:3000]
            sections["abstract"] = abstract_text

        # Try to locate Introduction
        intro_match = re.search(r"(?i)(?:\n(?:\d+[\.\s]+)?(?:i[\.\s]+)?introduction\b[\s:\-–—\n]+)(.*?)(?=\n(?:\d+[\.\s]+)?(?:related\s+work|methodology|methods|proposed|system|background)|$)", full_text, re.DOTALL)
        if intro_match:
            intro_text = intro_match.group(1).strip()
            if len(intro_text) > 5000:
                intro_text = intro_text[:5000]
            sections["introduction"] = intro_text

        # Methodology / Methods / Architecture / Approach
        method_match = re.search(
            r"(?i)(?:^|\n)(?:\d+[\.\s]+)?(?:(?:proposed|system|model)\s+)?(?:methodology|methods?|approach|architecture|system\s+design|framework)\b.*?\n+(.*?)(?=\n+(?:\d+[\.\s]+)?(?:experiments?|results?|evaluation|performance)|$)",
            full_text,
            re.DOTALL
        )
        if method_match:
            sections["methodology"] = method_match.group(1).strip()[:6000]

        # Results / Experiments / Evaluation
        results_match = re.search(
            r"(?i)(?:^|\n)(?:\d+[\.\s]+)?(?:experimental\s+)?(?:results?|experiments?|evaluations?|performance(?:\s+analysis)?)\b.*?\n+(.*?)(?=\n+(?:\d+[\.\s]+)?(?:discussion|conclusions?|future\s+work)|$)",
            full_text,
            re.DOTALL
        )
        if results_match:
            sections["results"] = results_match.group(1).strip()[:6000]

        # Conclusion / Concluding Remarks
        conclusion_match = re.search(
            r"(?i)(?:^|\n)(?:\d+[\.\s]+)?(?:conclusions?(?:\s+and\s+future\s+work)?|concluding\s+remarks)\b.*?\n+(.*?)(?=\n+(?:\d+[\.\s]+)?(?:references?|bibliography|acknowledgements?)|$)",
            full_text,
            re.DOTALL
        )
        if conclusion_match:
            sections["conclusion"] = conclusion_match.group(1).strip()[:4000]

        # If abstract couldn't be extracted via regex, use heuristic from first page
        if not sections["abstract"] and pages:
            first_text = pages[0]["text"]
            # Look for lines right after title before introduction
            lines = first_text.split("\n")
            candidate_lines = []
            capturing = False
            for l in lines:
                if re.search(r"(?i)\babstract\b", l):
                    capturing = True
                    continue
                if capturing:
                    if re.search(r"(?i)\b(introduction|1\.\s*intro|keywords)\b", l):
                        break
                    candidate_lines.append(l)
            if candidate_lines:
                sections["abstract"] = " ".join(candidate_lines).strip()
            elif len(lines) > 5:
                # Fallback: take lines 3-10
                sections["abstract"] = " ".join(lines[3:12]).strip()

        # If sections are mostly empty (e.g. non-standard format), segment by text slices
        if not sections["introduction"] and len(full_text) > 500:
            words = full_text.split()
            total_w = len(words)
            if not sections["abstract"]:
                sections["abstract"] = " ".join(words[:min(250, total_w)])
            sections["introduction"] = " ".join(words[min(250, total_w):min(800, total_w)])
            sections["methodology"] = " ".join(words[min(800, total_w):min(1600, total_w)])
            sections["results"] = " ".join(words[min(1600, total_w):min(2400, total_w)])
            sections["conclusion"] = " ".join(words[max(0, total_w - 400):])

        return sections
