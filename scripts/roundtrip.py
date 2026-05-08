"""Round-trip a PRISM-IR file: extract the original English, regenerate
English from the IR alone via an LLM, and present both side-by-side.

The round-trip is the IR's correctness test. If the regenerated English
preserves the intent of the original, the IR is faithful. If not, the
IR is wrong.

This script is a demonstration, not a verifier. It produces output a
human can eyeball. The verifier (Phase 3) adds an LLM-as-judge call to
score semantic equivalence and exit non-zero on divergence.

Usage:
    python scripts/roundtrip.py examples/claims-processing.prism.md

Requires:
    ANTHROPIC_API_KEY environment variable set
    pip install anthropic pyyaml
"""

import os
import re
import sys
from pathlib import Path

import yaml
from anthropic import Anthropic


RECONSTRUCTION_PROMPT = """You are reading a PRISM-IR file. PRISM-IR is a typed intermediate
representation for processes. Your job is to reconstruct the original
plain-English process description from the IR alone.

The IR you receive describes a process: its intention, its entities,
its nodes (steps and decisions), and its edges (the flow between
nodes). Read the IR carefully and write the natural-language process
description it encodes.

Rules:
- Output only the natural-language description. No preamble, no
  commentary, no markdown formatting.
- Match the granularity of a numbered step list, not a paragraph.
- Each numbered step should correspond to a meaningful action or
  decision in the IR.
- Decisions should be expressed as branching language ("if X, then Y;
  otherwise Z").
- Do not invent details that are not in the IR.
- Do not omit details that are in the IR.

PRISM-IR file:

{ir_yaml}

Reconstruct the original natural-language process description:"""


def load_prism_file(path):
    """Read a .prism.md file and return (original_english, ir_yaml_string)."""
    text = Path(path).read_text()

    english_match = re.search(
        r"## Natural Language\s*\n(.+?)(?=\n## )",
        text,
        re.DOTALL,
    )
    if not english_match:
        raise ValueError(f"No '## Natural Language' section found in {path}")
    original_english = english_match.group(1).strip()

    yaml_match = re.search(r"```yaml\s*\n(.+?)\n```", text, re.DOTALL)
    if not yaml_match:
        raise ValueError(f"No ```yaml fenced block found in {path}")
    ir_yaml = yaml_match.group(1).strip()

    yaml.safe_load(ir_yaml)
    return original_english, ir_yaml


def reconstruct_english(ir_yaml, client, model="claude-sonnet-4-6"):
    """Call an LLM to reconstruct the natural-language description from
    the IR alone."""
    prompt = RECONSTRUCTION_PROMPT.format(ir_yaml=ir_yaml)
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def write_roundtrip_report(path, original, reconstructed, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    name = Path(path).stem.replace(".prism", "")
    out_path = out_dir / f"{name}-roundtrip.md"
    out_path.write_text(
        f"# Round-trip: {name}\n\n"
        f"## Original (from file)\n\n{original}\n\n"
        f"## Reconstructed (from IR alone)\n\n{reconstructed}\n"
    )
    return out_path


def main():
    if len(sys.argv) != 2:
        print("usage: python scripts/roundtrip.py <path-to-prism-md>", file=sys.stderr)
        sys.exit(2)

    path = sys.argv[1]
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("error: set ANTHROPIC_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    original, ir_yaml = load_prism_file(path)
    client = Anthropic()

    print(f"Round-tripping: {path}\n")
    print("=" * 72)
    print("ORIGINAL (from file):")
    print("=" * 72)
    print(original)
    print()

    reconstructed = reconstruct_english(ir_yaml, client)

    print("=" * 72)
    print("RECONSTRUCTED (from IR alone, via LLM):")
    print("=" * 72)
    print(reconstructed)
    print()

    out_path = write_roundtrip_report(path, original, reconstructed, "out")
    print(f"Report written to: {out_path}")


if __name__ == "__main__":
    main()
