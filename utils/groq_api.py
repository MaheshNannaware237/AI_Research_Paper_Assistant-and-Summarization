import os
from typing import List, Tuple
from groq import Groq
from dotenv import load_dotenv


def get_client() -> Groq:
    """Create Groq client using .env API key only."""

    load_dotenv(override=True)

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found in .env file"
        )

    return Groq(api_key=api_key)


def generate_summary(text: str) -> str:
    """Generate a structured summary of the research paper using Groq."""
    client = get_client()

    safe_text = text[:12000]

    prompt = f"""You are an expert academic research assistant.

Analyse the following research paper and provide a comprehensive summary with these sections:

1. Main Objective
What problem does this paper solve?

2. Key Methodology
How did the authors approach it?

3. Main Results & Findings
What were the key findings and outcomes?

4. Novel Contributions
What is new or unique about this work?

5. Limitations & Future Work
Any noted weaknesses or suggestions for future research?

Be clear, concise, and accessible to a technical audience.

Research Paper:
{safe_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.3,
    )

    return response.choices[0].message.content


def generate_section_summaries(sections: dict) -> dict:
    """Summarise each detected section using Groq."""
    client = get_client()

    results = {}

    for name, content in sections.items():
        if len(content.strip()) < 100:
            results[name] = content.strip()
            continue

        prompt = f"""Summarise the following '{name}' section of a research paper in 2-4 clear sentences.
Be concise and focus on the most important points.

{content[:2500]}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.3,
        )

        results[name] = response.choices[0].message.content

    return results


def answer_question(
    question: str,
    chunks: List[str],
    top_k: int = 4
) -> Tuple[str, List[str]]:
    """Answer a question using keyword retrieval + Groq."""

    client = get_client()

    relevant_chunks = _keyword_retrieve(
        question,
        chunks,
        top_k=top_k
    )

    context = "\n\n---\n\n".join(relevant_chunks)
    context = context[:4000]

    prompt = f"""You are a research paper Q&A assistant.

Answer the question based ONLY on the provided context from the paper.

If the answer is not in the context, say:
"I couldn't find this information in the paper."

Be concise and precise.

Context:
{context[:8000]}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.2,
    )

    return response.choices[0].message.content, relevant_chunks


def _keyword_retrieve(
    query: str,
    chunks: List[str],
    top_k: int = 4
) -> List[str]:
    """Simple keyword-based retrieval."""

    query_words = set(query.lower().split())

    stop_words = {
        "the", "a", "an", "is", "was", "are", "were",
        "what", "how", "why", "when", "where", "who",
        "which", "did", "does", "do", "in", "on",
        "at", "to", "for", "of", "and"
    }

    query_words -= stop_words

    scored = []

    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = sum(
            1 for word in query_words
            if word in chunk_lower
        )
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    top = [chunk for _, chunk in scored[:top_k]]

    if not top:
        return []

    if all(score == 0 for score, _ in scored[:top_k]):
        return chunks[:top_k]

    return top