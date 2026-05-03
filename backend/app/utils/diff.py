"""Diff / Redline utility — produces word-level HTML diff between two texts.

Uses Python's built-in difflib; no extra dependencies needed.
The output is an HTML snippet ready for `dangerouslySetInnerHTML` on the
frontend (deletions in red <del>, insertions in green <ins>).
"""

from __future__ import annotations

import difflib
import html


def compute_diff_html(original: str, revised: str) -> str:
    """Return a word-level HTML diff of `original` → `revised`.

    Words removed from original are wrapped in <del class="diff-del">.
    Words added in revised are wrapped in <ins class="diff-ins">.
    Unchanged words are plain escaped HTML.
    """
    orig_words = original.split()
    rev_words = revised.split()

    matcher = difflib.SequenceMatcher(None, orig_words, rev_words, autojunk=False)
    parts: list[str] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            parts.append(html.escape(" ".join(orig_words[i1:i2])))
        elif tag == "replace":
            parts.append(
                f'<del class="diff-del">{html.escape(" ".join(orig_words[i1:i2]))}</del>'
                f' <ins class="diff-ins">{html.escape(" ".join(rev_words[j1:j2]))}</ins>'
            )
        elif tag == "delete":
            parts.append(
                f'<del class="diff-del">{html.escape(" ".join(orig_words[i1:i2]))}</del>'
            )
        elif tag == "insert":
            parts.append(
                f'<ins class="diff-ins">{html.escape(" ".join(rev_words[j1:j2]))}</ins>'
            )

    return " ".join(parts)


def similarity_ratio(a: str, b: str) -> float:
    """Quick 0-1 similarity score — useful for deciding if a revision is meaningful."""
    return difflib.SequenceMatcher(None, a, b).ratio()
