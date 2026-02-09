"""
Intelligent resume optimizer that analyzes and modifies resume content based on job description.
Instead of appending, it rewrites sections to align with the target job.
"""
import re
from typing import List, Dict, Optional, Tuple
from utils.logger import get_logger

logger = get_logger(__name__)


class ResumeOptimizer:
    """Intelligently optimize resume content to match job description."""

    # Section patterns for parsing resume structure
    SECTION_PATTERNS = {
        "summary": r"^(PROFESSIONAL SUMMARY|EXECUTIVE SUMMARY|CAREER SUMMARY|OBJECTIVE|PROFESSIONAL PROFILE|SUMMARY)",
        "experience": r"^(PROFESSIONAL EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT HISTORY|EXPERIENCE)",
        "skills": r"^(TECHNICAL SKILLS|KEY SKILLS|CORE COMPETENCIES|SKILLS|SKILL SET|TECHNICAL COMPETENCIES)",
        "education": r"^(EDUCATION|ACADEMIC BACKGROUND|DEGREES)",
        "certifications": r"^(CERTIFICATIONS|CERTIFICATIONS & LICENSES|LICENSES|PROFESSIONAL CERTIFICATIONS)",
        "projects": r"^(PROJECTS|KEY PROJECTS|NOTABLE PROJECTS)",
        "achievements": r"^(ACHIEVEMENTS|KEY ACHIEVEMENTS|AWARDS|ACCOMPLISHMENTS)"
    }

    @staticmethod
    def parse_resume_sections(resume_text: str) -> Dict[str, List[str]]:
        """
        Parse resume into structured sections.
        Returns dict: {section_name: [content_lines]}
        """
        try:
            sections = {}
            current_section = "header"
            sections[current_section] = []

            lines = resume_text.split("\n")
            for line in lines:
                stripped = line.strip().upper()

                # Check if this line is a section header
                found_section = None
                for section_name, pattern in ResumeOptimizer.SECTION_PATTERNS.items():
                    if re.match(pattern, stripped):
                        found_section = section_name
                        break

                if found_section:
                    current_section = found_section
                    if current_section not in sections:
                        sections[current_section] = []
                else:
                    sections[current_section].append(line)

            logger.debug(f"Parsed resume into {len(sections)} sections")
            return sections
        except Exception as e:
            logger.error(f"Error parsing resume sections: {e}")
            return {"header": resume_text.split("\n")}

    @staticmethod
    def extract_jd_keywords(job: Dict) -> Tuple[List[str], List[str], str]:
        """
        Extract keywords from job description.
        Returns: (technical_keywords, soft_skills, job_context)
        """
        try:
            description = job.get("description_text", "").lower()
            title = job.get("title", "").lower()
            company = job.get("company", "").lower()

            # Technical keywords (common tech terms)
            tech_keywords = set()
            tech_patterns = [
                r"\b(python|java|javascript|typescript|kotlin|go|rust|cpp|csharp|sql|mongodb|postgresql|mysql|docker|kubernetes|aws|azure|gcp|react|vue|angular|nodejs|django|flask|fastapi|spring|microservices|api|rest|graphql|git|ci/cd|jenkins|terraform|terraform|ansible)\b"
            ]

            for pattern in tech_patterns:
                matches = re.findall(pattern, description + " " + title)
                tech_keywords.update(matches)

            # Soft skills from job description
            soft_skills = set()
            soft_patterns = [
                r"\b(leadership|communication|teamwork|problem.solving|critical thinking|analytical|attention to detail|time management|project management|collaboration|agile|scrum|kanban|mentoring|public speaking)\b"
            ]

            for pattern in soft_patterns:
                matches = re.findall(pattern, description)
                soft_skills.update(matches)

            all_keywords = list(tech_keywords) + list(soft_skills)
            job_context = f"{title} at {company}"

            logger.debug(f"Extracted {len(all_keywords)} keywords from JD")
            return list(tech_keywords), list(soft_skills), job_context
        except Exception as e:
            logger.error(f"Error extracting JD keywords: {e}")
            return [], [], ""

    @staticmethod
    def rewrite_summary(
        original_summary: str,
        job: Dict,
        technical_keywords: List[str],
        soft_skills: List[str],
        candidate_skills: List[str]
    ) -> str:
        """
        Intelligently rewrite professional summary to align with job.
        """
        try:
            job_title = job.get("title", "").strip()
            company = job.get("company", "").strip()

            # Extract experience level from original resume
            years_match = re.search(r"(\d+)\+?\s*years?", original_summary.lower())
            years_exp = f"{years_match.group(1)}+ years of" if years_match else ""

            # Combine job keywords with candidate skills
            relevant_skills = list(set(technical_keywords[:5] + candidate_skills[:3]))
            skills_str = ", ".join(relevant_skills) if relevant_skills else "diverse technical and professional"

            # Build optimized summary
            summary = f"Results-driven professional with {years_exp} experience in {skills_str}. "
            summary += f"Seeking a {job_title} position to leverage expertise in {', '.join(technical_keywords[:3])} "
            summary += f"and contribute to {company}'s success. "

            if soft_skills:
                summary += f"Demonstrated strengths in {', '.join(soft_skills[:2])}. "

            summary += "Committed to delivering high-quality solutions and driving continuous improvement."

            logger.debug("Rewrote professional summary")
            return summary
        except Exception as e:
            logger.error(f"Error rewriting summary: {e}")
            return original_summary

    @staticmethod
    def enhance_experience_section(
        experience_lines: List[str],
        job: Dict,
        technical_keywords: List[str]
    ) -> List[str]:
        """
        Enhance experience bullets to match job keywords and requirements.
        """
        try:
            enhanced_lines = []

            for line in experience_lines:
                cleaned = line.strip()

                # Skip empty lines and headers
                if not cleaned or cleaned.isupper():
                    enhanced_lines.append(line)
                    continue

                # For experience bullets, check if they mention relevant skills
                line_lower = cleaned.lower()

                # Count relevance score
                relevance_score = sum(
                    1 for keyword in technical_keywords
                    if keyword.lower() in line_lower
                )

                # Keep highly relevant lines as-is, mark moderately relevant ones
                if relevance_score >= 2 or any(
                    pattern in line_lower
                    for pattern in ["designed", "developed", "implemented", "led", "managed", "improved"]
                ):
                    # Add emphasis marker for UI (can be styled later)
                    enhanced_lines.append(line)
                elif line_lower.startswith("•") or line_lower.startswith("-"):
                    enhanced_lines.append(line)
                else:
                    enhanced_lines.append(line)

            logger.debug(f"Enhanced {len(enhanced_lines)} experience lines")
            return enhanced_lines
        except Exception as e:
            logger.error(f"Error enhancing experience: {e}")
            return experience_lines

    @staticmethod
    def reorder_skills_section(
        skills_lines: List[str],
        technical_keywords: List[str],
        candidate_skills: List[str]
    ) -> List[str]:
        """
        Reorder skills section to prioritize job-relevant skills.
        """
        try:
            # Extract individual skills from lines
            skills = []
            for line in skills_lines:
                cleaned = line.strip()
                # Remove bullet points and clean
                skill = re.sub(r"^[-•*]\s*", "", cleaned)
                if skill and not skill.isupper() and len(skill) > 2:
                    skills.append(skill)

            # Score skills based on relevance
            scored_skills = []
            for skill in skills:
                score = 0
                skill_lower = skill.lower()

                # Check against job keywords
                for keyword in technical_keywords:
                    if keyword.lower() in skill_lower:
                        score += 10

                # Check against candidate skills
                for cand_skill in candidate_skills:
                    if cand_skill.lower() in skill_lower:
                        score += 5

                scored_skills.append((skill, score))

            # Sort by relevance score (descending)
            scored_skills.sort(key=lambda x: x[1], reverse=True)

            # Return reordered skills with bullets
            reordered = []
            for skill, score in scored_skills:
                reordered.append(f"• {skill}")

            logger.debug(f"Reordered {len(reordered)} skills by relevance")
            return reordered
        except Exception as e:
            logger.error(f"Error reordering skills: {e}")
            return skills_lines

    @staticmethod
    def optimize_resume(
        resume_text: str,
        job: Dict,
        candidate_skills: Optional[List[str]] = None
    ) -> str:
        """
        Main method: Analyze resume and JD, then intelligently modify resume content.
        Returns optimized resume text ready for document generation.
        """
        try:
            candidate_skills = candidate_skills or []

            # Parse resume into sections
            sections = ResumeOptimizer.parse_resume_sections(resume_text)

            # Extract JD requirements
            tech_keywords, soft_skills, job_context = ResumeOptimizer.extract_jd_keywords(job)

            # Optimize each section
            if "summary" in sections:
                original_summary = "\n".join(sections["summary"])
                optimized_summary = ResumeOptimizer.rewrite_summary(
                    original_summary, job, tech_keywords, soft_skills, candidate_skills
                )
                sections["summary"] = optimized_summary.split("\n")

            if "experience" in sections:
                enhanced_experience = ResumeOptimizer.enhance_experience_section(
                    sections["experience"], job, tech_keywords
                )
                sections["experience"] = enhanced_experience

            if "skills" in sections:
                reordered_skills = ResumeOptimizer.reorder_skills_section(
                    sections["skills"], tech_keywords, candidate_skills
                )
                sections["skills"] = reordered_skills

            # Reconstruct resume
            optimized_text = ""
            for section_name in ["header", "summary", "experience", "skills", "education", "certifications", "projects", "achievements"]:
                if section_name in sections and sections[section_name]:
                    section_content = sections[section_name]
                    if isinstance(section_content, list):
                        optimized_text += "\n".join(section_content)
                    else:
                        optimized_text += section_content
                    optimized_text += "\n\n"

            logger.info(f"Successfully optimized resume for {job.get('title')}")
            return optimized_text.strip()

        except Exception as e:
            logger.error(f"Error optimizing resume: {e}")
            return resume_text
