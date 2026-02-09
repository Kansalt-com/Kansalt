"""
Skill matching engine with strict word-boundary matching.
"""
import json
import re
from typing import List, Set
from utils.logger import get_logger

logger = get_logger(__name__)

# Acronyms that are valid skills (always allow as whole tokens)
SHORT_OK = {
    "aws", "aks", "eks", "gke", "s3", "ec2", "iam",
    "sql", "api", "sre", "ehr", "emr", "icd", "cpt", "hcc", "rcm",
    "k8s", "k8", "ci/cd", "cicd", "c#", ".net", "bd", "va", "ae", "am", "ea", "deo", "mva"
}

# Common English words that should NEVER match as skills
SHORT_BLOCK = {"go", "ui", "ux", "ml", "r", "c", "is", "are", "on", "in", "to", "a", "the", "be"}


class SkillMatcher:
    """Strict skill matching engine."""

    @staticmethod
    def _normalize(text: str) -> str:
        """Normalize text: unescape HTML, strip tags, collapse whitespace."""
        text = text or ""
        text = re.sub(r"<[^>]+>", " ", text)  # strip HTML tags
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def _normalize_lower(text: str) -> str:
        """Normalize and lowercase."""
        return SkillMatcher._normalize(text).lower()

    @staticmethod
    def _token_set(text: str) -> Set[str]:
        """Extract tokens from text (preserves multi-char symbols like ci/cd, c#)."""
        text_norm = SkillMatcher._normalize_lower(text)
        # Match word-like tokens, allowing +, #, ., /, -
        return set(re.findall(r"[a-z0-9\+\#\./-]+", text_norm))

    @staticmethod
    def contains_term(text: str, term: str) -> bool:
        """
        Check if term exists in text with strict word-boundary matching.
        - Short terms (< 3 chars): must match as exact token, unless in SHORT_OK
        - Multi-word terms: must match phrase with word boundaries
        """
        if not term or not text:
            return False

        text_norm = SkillMatcher._normalize_lower(text)
        term_norm = SkillMatcher._normalize_lower(term)

        # Block risky short tokens
        if term_norm in SHORT_BLOCK:
            return False

        # Short token: only as exact whole token
        if len(term_norm) <= 3 and term_norm not in SHORT_OK:
            return term_norm in SkillMatcher._token_set(text_norm)

        # Allowed short acronyms
        if term_norm in SHORT_OK:
            return term_norm in SkillMatcher._token_set(text_norm)

        # Longer term: match with word boundaries
        # Pattern: not preceded/followed by word chars
        pattern = r"(?<![a-z0-9])" + re.escape(term_norm) + r"(?![a-z0-9])"
        return re.search(pattern, text_norm) is not None

    @staticmethod
    def load_skills(skills_json_path: str = "data/skills.json") -> dict:
        """Load skills database."""
        try:
            with open(skills_json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load skills.json: {e}")
            return {"categories": {}, "all_skills": []}

    @staticmethod
    def infer_skills_strict(text: str, skills_db: dict) -> List[str]:
        """
        Infer skills from text using strict matching across full skill pool.
        """
        found = set()

        # Flatten all skills from categories
        all_skill_entries = []
        for category_name, skills_group in skills_db.get("categories", {}).items():
            for skill_label, skill_info in skills_group.items():
                all_skill_entries.append((skill_label, skill_info.get("aliases", [])))

        # Check each skill against text
        for label, aliases in all_skill_entries:
            candidates = [label] + (aliases if isinstance(aliases, list) else [str(aliases)])
            for candidate in candidates:
                if SkillMatcher.contains_term(text, candidate):
                    found.add(label)
                    break

        return sorted(list(found))

    @staticmethod
    def get_it_skills(skills_db: dict) -> List[str]:
        """Get all IT skills."""
        return [
            label
            for label in skills_db.get("categories", {}).get("IT", {}).keys()
        ]

    @staticmethod
    def get_non_it_skills(skills_db: dict) -> List[str]:
        """Get all non-IT skills."""
        it_keys = set(SkillMatcher.get_it_skills(skills_db))
        all_labels = []
        for category, skills in skills_db.get("categories", {}).items():
            if category != "IT":
                all_labels.extend(skills.keys())
        return sorted(all_labels)
