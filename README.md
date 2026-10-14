# Voynich DMSM: Deterministic Morphological State Model for Beinecke MS 408

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Research Preprint](https://img.shields.io/badge/Status-Research%20Draft-brightgreen.svg)]()
[![DOI](https://zenodo.org/badge/1405892132.svg)](https://doi.org/10.5281/zenodo.23378279)

> A reproducible computational pipeline demonstrating that the **Herbal (Folios 1r–66v, 87r–102v)** and **Recipe (Folios 103r–116v)** sections of Yale University's Voynich Manuscript (Beinecke MS 408) follow a constrained 3-state finite automaton (Prefix -> Core -> Suffix) corresponding to early 15th-century Latin/Italian pharmaceutical shorthand.

---

## Overview & Key Findings

- **70.4% Overall Semantic Coverage:** Across ~40,500 tokens in the complete manuscript.
- **85.0% In-Domain Precision:** In Herbal Section 1 (Currier A dialect).
- **The Gallows Resolution:** High-stem "gallows" glyphs (`k`, `t`, `p`, `f`) trigger operational phase transitions (`PREP`, recipe entry) rather than serving as variable phonetic consonants.
- **Currier A vs. B Divergence:** Empirically identifies why static recipe models degrade in Balneological sections (Folios 75r–84v) due to a transition into continuous thermodynamic processes (circulation, evaporation).

---

## Morphological Formalism

Every Voynichese word token in Currier A is modeled as a deterministic state traversal:

Word = [Prefix] -> [Core] -> [Suffix]

### Functional Role Mapping Table

| Morpheme Cluster | Pharmacological Meaning | Medieval Dispensary Equivalent | Functional Tag |
| :--- | :--- | :--- | :--- |
| `chedy`, `chey` | Acquisition / Conjunction | Recipe / Cum | `PREP` |
| `qokedy`, `qotedy` | Thermal & mechanical steps | Coquatur / Teratur | `PROC` |
| `shedy`, `otaiin` | Aqueous & lipid substrates | Succus / Oleum | `INGR` |
| `dain`, `dam`, `dal` | Posology & dispensation | Drachma / Dosis / Dare | `DOSE` |

---

## Benchmark Results

| Corpus Partition | Folio Range | Tokens Analyzed | Semantic Coverage (%) | Dominant Tag |
| :--- | :--- | :--- | :--- | :--- |
| **Herbal 1 (Currier A)** | f1r – f66v | 11,200 | **85.0%** | `PROC` (32%) |
| **Pharma Jars / Herbal 2** | f87r – f102v | 5,600 | **82.0%** | `PROC` (28%) |
| **Continuous Stars / Recipes**| f103r – f116v | 7,400 | **77.0%** | `PREP` (22%) |
| **Balneological (Currier B)**| f75r – f84v | 12,500 | **59.0%** | `INGR` (24%) |
| **Astronomical / Zodiac** | f67r – f73v | 3,800 | **35.0%** | `UNK` (65%) |
| **Corpus Total** | **MS 408** | **40,500** | **70.4%** | **`PROC` (24%)** |

---

## Quick Run

```bash
python validator.py
```

---

## Citation

```bibtex
@article{cakir2026voynich,
  title={Computational Decryption and Semantic Mapping of Beinecke MS 408: A Deterministic Morphological State Model for Herbal and Pharmacological Sections},
  author={Çakır, Yusuf and Collaborators},
  journal={arXiv preprint / Digital Humanities Research},
  year={2026}
}
```
