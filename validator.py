"""
Voynich DMSM (Deterministic Morphological State Model)
Heuristic Pattern & Morphological Structure Validator for Beinecke MS 408.

Author: Yusuf Çakır
License: MIT
"""

import os
import re
import sys
from collections import Counter

# --- 1. MORPHOLOGICAL COMPONENT DEFINITIONS ---
PREFIXES = ["qo", "cho", "sho", "ch", "sh", "da", "sa", "ot"]
SUFFIXES = ["eedy", "edy", "aiin", "iin", "ar", "al", "am", "dy", "y"]

# Positional Gallows Characters
GALLOWS = {"k", "t", "p", "f"}

# Curated Functional Category Mapping (Heuristic Dispensary Framing)
LEXICON_FUNCTION_MAP = {
    # Process / Operational Roots
    "k": "PROC:prep",
    "t": "PROC:extract",
    "p": "PROC:infuse",
    "f": "PROC:filter",
    "ed": "PROC:decoct",
    "eed": "PROC:distill",
    # Substance / Herbal Candidates
    "ar": "INGR:radix",
    "al": "INGR:folia",
    "am": "INGR:semen",
    "aiin": "INGR:herba_ext",
    "iin": "INGR:aqua_sol",
    # Dosage / Measure Markers
    "dy": "DOSE:unit",
    "y": "STATE:terminal",
    "l": "DOSE:part",
    "m": "DOSE:weight",
    # Syntactic / Structural Markers
    "ch": "SYN:conn",
    "sh": "SYN:iter",
    "qo": "SYN:trans",
    "da": "SYN:rel",
    "sa": "SYN:cond",
    "ot": "SYN:init"
}

def clean_ivtff_line(line: str) -> list[str]:
    """
    Strips IVTFF machine tags, uncertain glyph brackets, and metadata.
    Preserves genuine inter-word delimiters.
    """
    line = line.strip()
    if not line or line.startswith("#"):
        return []
    
    # Strip line tags like <f1r.1,@P0> or <f103r.1>
    line = re.sub(r"<[^>]+>", "", line)
    
    # Strip transcription annotations like [m], {?}, $
    line = re.sub(r"\[[^\]]*\]|\{[^\}]*\}|\$", "", line)
    
    # In IVTFF, words are separated by '.' or whitespace
    raw_tokens = re.split(r"[.\s]+", line)
    
    # Normalize: keep valid EVA tokens (letters only)
    cleaned = [t.lower() for t in raw_tokens if re.match(r"^[a-z]+$", t.lower())]
    return cleaned

def segment_token(token: str) -> tuple[str, str, str]:
    """
    Deterministic Tri-state Segmentation: Prefix -> Core -> Suffix.
    Guarantees non-empty core preservation.
    """
    p, c, s = "", token, ""
    
    # Extract longest prefix
    for pref in sorted(PREFIXES, key=len, reverse=True):
        if c.startswith(pref):
            # Avoid consuming the entire token if it leaves core empty
            if len(c) > len(pref):
                p = pref
                c = c[len(pref):]
                break
                
    # Extract longest suffix
    for suff in sorted(SUFFIXES, key=len, reverse=True):
        if c.endswith(suff):
            if len(c) > len(suff):
                s = suff
                c = c[:-len(suff)]
                break
                
    return p, c, s

def evaluate_token(token: str) -> dict:
    """
    Categorizes the morphological components of a token.
    """
    p, c, s = segment_token(token)
    
    # Check if root/core or affixes trigger functional mapping
    matched_features = []
    if p in LEXICON_FUNCTION_MAP:
        matched_features.append(LEXICON_FUNCTION_MAP[p])
    if c in LEXICON_FUNCTION_MAP:
        matched_features.append(LEXICON_FUNCTION_MAP[c])
    if s in LEXICON_FUNCTION_MAP:
        matched_features.append(LEXICON_FUNCTION_MAP[s])
        
    # Gallows presence check in core
    has_gallows = any(g in c for g in GALLOWS)
    
    is_classified = len(matched_features) > 0
    return {
        "token": token,
        "prefix": p,
        "core": c,
        "suffix": s,
        "features": matched_features,
        "has_gallows": has_gallows,
        "status": "CLASSIFIED" if is_classified else "UNK"
    }

def analyze_corpus(corpus_path: str = "voynich_eva_corpus.txt"):
    """
    Executes a structured morphological audit on the corpus.
    """
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file '{corpus_path}' not found.")
        print("Please place the IVTFF corpus file in the working directory.")
        return

    print("Parsing EVA corpus...")
    all_tokens = []
    with open(corpus_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            tokens = clean_ivtff_line(line)
            all_tokens.extend(tokens)
            
    total_tokens = len(all_tokens)
    if total_tokens == 0:
        print("Error: No valid tokens parsed from corpus.")
        return

    print(f"Total valid tokens parsed: {total_tokens:,}")
    print(f"Unique vocabulary size: {len(set(all_tokens)):,}")
    
    classified_count = 0
    gallows_count = 0
    feature_counter = Counter()
    empty_core_guard_count = 0

    for t in all_tokens:
        res = evaluate_token(t)
        if res["status"] == "CLASSIFIED":
            classified_count += 1
            for f in res["features"]:
                feature_counter[f] += 1
        if res["has_gallows"]:
            gallows_count += 1
        if not res["core"]:
            empty_core_guard_count += 1

    heuristic_coverage = (classified_count / total_tokens) * 100
    gallows_pct = (gallows_count / total_tokens) * 100

    print("\n" + "="*50)
    print("VOYNICH DMSM MORPHOLOGICAL AUDIT REPORT")
    print("="*50)
    print(f"Total Evaluated Tokens     : {total_tokens}")
    print(f"Heuristically Tagged Tokens: {classified_count} ({heuristic_coverage:.2f}%)")
    print(f"Unclassified (UNK) Tokens  : {total_tokens - classified_count} ({100 - heuristic_coverage:.2f}%)")
    print(f"Gallows-Bearing Cores      : {gallows_count} ({gallows_pct:.2f}%)")
    print(f"Empty Cores Permitted      : {empty_core_guard_count} (Must be 0)")
    
    print("\nTop Functional Feature Distributions:")
    for feat, count in feature_counter.most_common(8):
        print(f"  - {feat:20}: {count:6,} ({count/total_tokens*100:.2f}%)")
    print("="*50)
    print("NOTE: 'Tagged' rate denotes structural morphological compliance,")
    print("NOT verified linguistic decipherment or semantic accuracy.")

if __name__ == "__main__":
    analyze_corpus()
