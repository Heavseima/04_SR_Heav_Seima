
# Chunking Method

from typing import List, Optional


# Default separator hierarchy (from coarse to fine-grained)
DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]


def _merge_splits(splits: List[str], separator: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """
    Merge a list of small text splits into chunks that respect chunk_size,
    with optional overlap between consecutive chunks.
    """
    chunks: List[str] = []
    current_splits: List[str] = []
    current_len = 0
    sep_len = len(separator)

    for split in splits:
        split_len = len(split)
        # +sep_len accounts for the separator that will join pieces
        projected_len = current_len + split_len + (sep_len if current_splits else 0)

        if projected_len > chunk_size and current_splits:
            # Flush the current buffer as a chunk
            chunk = separator.join(current_splits)
            if chunk:
                chunks.append(chunk)

            # Drop splits from the front until we're within overlap budget
            while current_splits and (
                current_len + split_len + (sep_len if current_splits else 0) > chunk_size
            ):
                removed = current_splits.pop(0)
                current_len -= len(removed) + (sep_len if current_splits else 0)
                if current_len < 0:
                    current_len = 0

            # Trim overlap: keep only what fits in chunk_overlap
            overlap_text = separator.join(current_splits)
            if len(overlap_text) > chunk_overlap:
                # Remove oldest splits until overlap fits
                while current_splits and len(separator.join(current_splits)) > chunk_overlap:
                    current_splits.pop(0)
                current_len = sum(len(s) for s in current_splits) + sep_len * max(len(current_splits) - 1, 0)

        current_splits.append(split)
        current_len = sum(len(s) for s in current_splits) + sep_len * max(len(current_splits) - 1, 0)

    # Flush any remaining splits
    if current_splits:
        chunk = separator.join(current_splits)
        if chunk:
            chunks.append(chunk)

    return chunks


def recursive_text_split(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    separators: Optional[List[str]] = None,
) -> List[str]:
    """
    Recursively split *text* into chunks of at most *chunk_size* characters,
    with up to *chunk_overlap* characters of whole-split context carried over.

    The function tries each separator in *separators* (from coarsest to finest).
    Any piece that is still larger than *chunk_size* after splitting is passed
    recursively to the next separator in the list.  When no separators remain
    (empty string ``""``), the text is split character-by-character.

    Args:
        text:          The input text to split.
        chunk_size:    Maximum number of characters per chunk.
        chunk_overlap: Number of characters to overlap between consecutive chunks.
        separators:    Ordered list of separator strings. Defaults to
                       ``[\"\\n\\n\", \"\\n\", \". \", \" \", \"\"]``.

    Returns:
        A list of text chunks.
    """
    if chunk_size <= 0 or not 0 <= chunk_overlap < chunk_size:
        raise ValueError("Require chunk_size > 0 and 0 <= chunk_overlap < chunk_size")
    if separators == []:
        raise ValueError("separators must not be empty")
    if separators is None:
        separators = DEFAULT_SEPARATORS

    # Pick the first separator that is present in the text (or the last one)
    separator = separators[-1]
    next_separators: List[str] = []

    for i, sep in enumerate(separators):
        if sep == "" or sep in text:
            separator = sep
            next_separators = separators[i + 1:]
            break

    # Split on the chosen separator
    raw_splits = text.split(separator) if separator else list(text)

    good_splits: List[str] = []   # splits small enough to merge directly
    final_chunks: List[str] = []

    for split in raw_splits:
        if not split:
            continue
        if len(split) <= chunk_size:
            good_splits.append(split)
        else:
            # Current buffer of good splits -> flush before recursing
            if good_splits:
                merged = _merge_splits(good_splits, separator, chunk_size, chunk_overlap)
                final_chunks.extend(merged)
                good_splits = []

            if not next_separators:
                # No finer separator: force-split by character
                for i in range(0, len(split), chunk_size - chunk_overlap):
                    final_chunks.append(split[i: i + chunk_size])
            else:
                # Recurse with the remaining (finer) separators
                sub_chunks = recursive_text_split(
                    split,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    separators=next_separators,
                )
                final_chunks.extend(sub_chunks)

    # Merge any remaining good splits
    if good_splits:
        merged = _merge_splits(good_splits, separator, chunk_size, chunk_overlap)
        final_chunks.extend(merged)

    return final_chunks


# ---------------------------------------------------------------------------
# Quick demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample_text = """Retrieval-Augmented Generation (RAG) is a technique that combines a retrieval
system with a generative language model.

First, a query is used to retrieve relevant documents from a knowledge base.
These documents provide grounding context for the language model.

Finally, the model generates an answer conditioned on both the query and the
retrieved context. This reduces hallucinations and keeps responses up-to-date
without retraining the model."""

    chunks = recursive_text_split(sample_text, chunk_size=150, chunk_overlap=30)
    for idx, chunk in enumerate(chunks, 1):
        print(f"--- Chunk {idx} ({len(chunk)} chars) ---")
        print(chunk)
        print()
