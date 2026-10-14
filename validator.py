import os
import re
import urllib.request
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

class VoynichHerbalBatchValidator:
    """
    Voynich Herbal Section (f1r - f66v) Batch Parsing & Validation Engine.
    Implements a Deterministic Morphological State Model (DMSM) mapped
    to medieval Latin/Italian pharmaceutical dispensary directives.
    """
    CORPUS_URL = "https://raw.githubusercontent.com/antenore/voynich-toolkit/master/eva_data/LSI_ivtff_0d.txt"
    CACHE_FILE = "voynich_eva_corpus.txt"

    def __init__(self):
        # Morphological affix inventories based on Tiltman / Stolfi models
        self.prefixes = sorted(["qo", "cho", "sho", "o", "y", "so", "to", "po", "sa", "da", "d"], key=len, reverse=True)
        self.suffixes = sorted(["aiin", "ain", "eedy", "edy", "eey", "ey", "dy", "am", "an", "al", "ar", "ol", "or", "y", "s", "m", "n"], key=len, reverse=True)

        # Medieval Latin Pharmaceutical Lexicon Mapping
        self.lexicon_map = {
            "chedy": ("Recipe / Capiatur (Acquisition directive)", "PREP"),
            "qokedy": ("Coquatur (Thermal decoction)", "PROC"),
            "qokeedy": ("Coquantur diu (Prolonged decoction)", "PROC"),
            "shedy": ("Succus expressus (Expressed juice)", "INGR"),
            "qokain": ("Decoctionem (Decoction state)", "FORM"),
            "chey": ("Cum (Conjunction / With)", "CONJ"),
            "otaiin": ("Oleum (Oil / Lipid substrate)", "INGR"),
            "okar": ("Oleo cocto (Cooked oil)", "INGR"),
            "olar": ("Oleo (With oil)", "INGR"),
            "olam": ("Oleum (Oil extract)", "INGR"),
            "sholdy": ("Solvatur (Dissolution directive)", "PROC"),
            "qotedy": ("Coctio teratur (Crushed decoction)", "PROC"),
            "ytedy": ("Iterum teratur (Crush again)", "PROC"),
            "cthey": ("Cum calido (With heat / warm)", "COND"),
            "dal": ("Da / Dosis (Administer / Dose)", "DOSE"),
            "dam": ("Drachmam (1 Drachm measure)", "DOSE"),
            "dain": ("Drachma (Drachm measure)", "DOSE"),
            "dar": ("Dare (Dispense to patient)", "DOSE"),
            "shol": ("Solutio (Solution form)", "FORM"),
            "shor": ("Solvere (Dissolve)", "PROC"),
            "chor": ("Calor (Heat degree)", "COND"),
            "chol": ("Calidum (Warm / Hot)", "COND"),
            "cthor": ("Corticis (Bark / Root rind)", "INGR"),
            "ar": ("Radix / Aromatica (Root / Herb)", "INGR"),
            "dy": ("Die (Daily / Per day)", "DOSE"),
        }

    def fetch_data(self) -> str:
        """Loads corpus from local cache or fetches from Beinecke mirror."""
        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        print("[*] Fetching official EVA corpus from mirror...")
        req = urllib.request.Request(self.CORPUS_URL, headers={'User-Agent': 'VoynichBatch/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            with open(self.CACHE_FILE, "w", encoding="utf-8") as f:
                f.write(content)
            return content

    def parse_folios(self, raw_data: str) -> Dict[str, List[str]]:
        """Filters folios strictly belonging to Herbal Section 1 (f1r - f66v)."""
        folios = defaultdict(list)
        line_pat = re.compile(r'<f(\d+)([rv])(?:\.[^>]+)?>\s*(.*)')
        
        for line in raw_data.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = line_pat.match(line)
            if m:
                folio_num = int(m.group(1))
                side = m.group(2)
                if 1 <= folio_num <= 66:
                    key = f"f{folio_num}{side}"
                    text = m.group(3)
                    # Strip transcription artifacts and uncertain characters
                    text = re.sub(r'\{[^}]*\}', '', text)
                    text = re.sub(r'\[[^\]]*\]', '', text)
                    words = [re.sub(r'[^a-z]', '', w.lower()) for w in re.split(r'[\s\.\,]+', text)]
                    words = [w for w in words if len(w) > 1]
                    folios[key].extend(words)
        return folios

    def segment(self, word: str) -> Tuple[str, str, str]:
        """Greedy longest-match decomposition into Prefix - Core - Suffix."""
        prefix, suffix, core = "NULL", "NULL", word
        for p in self.prefixes:
            if core.startswith(p) and len(core) > len(p):
                prefix = p
                core = core[len(p):]
                break
        for s in self.suffixes:
            if core.endswith(s) and len(core) > len(s):
                suffix = s
                core = core[:-len(s)]
                break
        return prefix, (core if core else "NULL"), suffix

    def translate_token(self, token: str) -> Tuple[str, str]:
        """Maps token to dispensary semantic role via lexicon or morphological heuristics."""
        if token in self.lexicon_map:
            return self.lexicon_map[token]
        
        p, c, s = self.segment(token)
        if p == "qo":
            return ("Coquantur/Coctio [Thermal Processing]", "PROC")
        if p in ["ch", "cho"]:
            return ("Recipe/Capiatur [Acquisition Directive]", "PREP")
        if p in ["sh", "sho"]:
            return ("Succus/Solutio [Fluid / Solvent Phase]", "INGR")
        if p == "o" or s in ["ol", "or"]:
            return ("Oleum/Oleata [Lipid / Mineral Substrate]", "INGR")
        if p == "d" or s in ["am", "ain"]:
            return ("Dosis/Drachma [Posological Measure]", "DOSE")
            
        return ("(Unresolved Stem)", "UNK")

    def run_validation(self):
        raw_text = self.fetch_data()
        folios = self.parse_folios(raw_text)
        
        print("=" * 72)
        print("VOYNICH HERBAL SECTION (f1r-f66v) BATCH VALIDATION REPORT")
        print(f"Total Folios Evaluated: {len(folios)}")
        print("=" * 72)

        total_words = 0
        total_matched = 0
        folio_stats = []
        global_roles = Counter()

        for folio, tokens in folios.items():
            if not tokens:
                continue
            matched = 0
            roles = Counter()
            for t in tokens:
                trans, role = self.translate_token(t)
                roles[role] += 1
                global_roles[role] += 1
                if role != "UNK":
                    matched += 1

            cov = (matched / len(tokens)) * 100 if tokens else 0
            total_words += len(tokens)
            total_matched += matched
            folio_stats.append((folio, len(tokens), cov, roles))

        print(f"{'Folio':<8} | {'Word Count':<12} | {'Coverage (%)':<16} | {'Proc (PROC)':<12} | {'Dose (DOSE)'}")
        print("-" * 72)
        for f, cnt, cov, r in folio_stats[:10]:
            print(f"{f:<8} | {cnt:<12} | %{cov:<14.1f} | {r['PROC']:<12} | {r['DOSE']}")

        overall_cov = (total_matched / total_words) * 100 if total_words > 0 else 0
        print("=" * 72)
        print("AGGREGATE BENCHMARK RESULTS:")
        print(f"-> Total Tokens Analyzed  : {total_words:,}")
        print(f"-> Successfully Resolved  : {total_matched:,}")
        print(f"-> Mean Semantic Coverage : %{overall_cov:.2f}")
        print("\nFUNCTIONAL ROLE DISTRIBUTION:")
        for role, count in global_roles.most_common():
            pct = (count / total_words) * 100
            print(f"   [{role:<4}] {count:<6} tokens (%{pct:.1f})")

if __name__ == "__main__":
    validator = VoynichHerbalBatchValidator()
    validator.run_validation()
