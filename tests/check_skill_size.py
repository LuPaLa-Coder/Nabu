"""Misura i token di Nabu/SKILL.md (encoding o200k_base) e fallisce sopra il limite."""

import sys
from pathlib import Path

LIMITE = 600
SKILL = Path(__file__).resolve().parent.parent / "Nabu" / "SKILL.md"

try:
    import tiktoken
except ImportError:
    print("pip install tiktoken")
    sys.exit(2)

enc = tiktoken.get_encoding("o200k_base")
n = len(enc.encode(SKILL.read_text(encoding="utf-8")))
print(f"SKILL.md: {n} token.")
sys.exit(1 if n > LIMITE else 0)
