# Voynich DMSM: Deterministic Morphological State Model for Beinecke MS 408

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/1405892132.svg)](https://doi.org/10.5281/zenodo.23378279)

A reproducible computational framework for evaluating positional morphology and structural regularities in the Voynich Manuscript (Beinecke MS 408), benchmarked against medieval dispensary operational patterns.

---

## Abstract & Research Scope

Rather than proposing a speculative phonetic decipherment or treating MS 408 as natural language orthography, this project models the manuscript's token regularities via a **Deterministic Morphological State Model (DMSM)**. 

The framework systematically segments tokens into a tri-state positional automaton:
$$\text{Prefix} \rightarrow \text{Core} \rightarrow \text{Suffix}$$

The goal is to test whether the morphological structure reflects functional shorthand conventions analogous to late medieval Salernitan recipe and dispensary records (e.g., *Antidotarium Nicolai*).

---

## Key Methodological Principles

1. **Non-Empty Core Preservation:** Tokens are strictly partitioned so that affixes do not consume the semantic carrier (core root).
2. **Structural Coverage vs. Decipherment:** We explicitly distinguish between **heuristic structural matching rate** (the frequency with which tokens conform to defined affix rules) and **semantic decipherment** (which requires external verified bilingual evidence).
3. **Reproducible Pipeline:** Designed to run offline directly against the standard IVTFF corpus (`voynich_eva_corpus.txt`).

---

## Quick Start

### Prerequisites
- Python 3.10 or higher (Standard library only; no external dependencies required).

### Execution
Ensure `voynich_eva_corpus.txt` is present in the repository root, then execute:

```bash
python validator.py

@software{cakir_2026_voynich_dmsm,
  author       = {Çakır, Yusuf},
  title        = {Voynich DMSM: Deterministic Morphological State Model for Beinecke MS 408},
  year         = {2026},
  publisher    = {Zenodo},
  version      = {v1.0.3},
  doi          = {10.5281/zenodo.23378280},
  url          = {[https://doi.org/10.5281/zenodo.23378279](https://doi.org/10.5281/zenodo.23378279)}
}
