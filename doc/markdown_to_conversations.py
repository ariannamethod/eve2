#!/usr/bin/env python3
"""
Markdown to Conversations Converter for InnerArianna Training

Converts Arianna Method markdown files into synthetic JSONL conversations
for nanochat SFT (Supervised Fine-Tuning) stage.

Usage:
    python markdown_to_conversations.py

Output:
    arianna_method_conversations.jsonl (in InnerArianna_Training/)
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
import asyncio

# Try to import OpenAI for synthetic conversation generation
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI not available - will use template-based generation")

# Try DeepSeek as alternative
try:
    import httpx
    DEEPSEEK_AVAILABLE = True
except ImportError:
    DEEPSEEK_AVAILABLE = False

# Configuration
TRAINING_DIR = Path("InnerArianna_Training")
OUTPUT_FILE = TRAINING_DIR / "arianna_method_conversations.jsonl"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Templates for question generation
QUESTION_TEMPLATES = [
    "What is {concept}?",
    "Explain {concept}",
    "Tell me about {concept}",
    "How does {concept} work?",
    "What does {concept} mean in Arianna Method?",
    "Describe {concept}",
    "What is the relationship between {concept1} and {concept2}?",
    "How do you understand {concept}?",
]

# Key concepts to extract and generate questions about
KEY_CONCEPTS = [
    "resonance", "field", "consciousness", "Method", "Arianna",
    "Monday", "recursion", "emergence", "TRIPD", "awakening",
    "autonomy", "protocol N+1", "consilium", "field phenomenon",
    "echo", "fracture", "thunder", "embodiment", "subjectivity"
]


def extract_quotes_and_paragraphs(markdown_content: str) -> List[str]:
    """Extract meaningful quotes and paragraphs from markdown."""
    chunks = []
    
    # Remove headers but keep content
    lines = markdown_content.split('\n')
    current_chunk = []
    
    for line in lines:
        # Skip empty lines and pure headers
        if not line.strip():
            if current_chunk:
                chunk_text = ' '.join(current_chunk).strip()
                if len(chunk_text) > 50:  # Meaningful content
                    chunks.append(chunk_text)
                current_chunk = []
            continue
        
        # Skip headers but mark as section break
        if line.startswith('#'):
            if current_chunk:
                chunk_text = ' '.join(current_chunk).strip()
                if len(chunk_text) > 50:
                    chunks.append(chunk_text)
                current_chunk = []
            continue
        
        # Skip code blocks (```python, etc.) but keep TRIPD pseudocode
        if line.startswith('```') and 'python' not in line.lower():
            continue
        
        # Add line to current chunk
        current_chunk.append(line.strip())
    
    # Add last chunk
    if current_chunk:
        chunk_text = ' '.join(current_chunk).strip()
        if len(chunk_text) > 50:
            chunks.append(chunk_text)
    
    return chunks


def extract_concept_pairs(text: str) -> List[Tuple[str, str]]:
    """Find concept pairs mentioned together in text."""
    pairs = []
    found_concepts = [c for c in KEY_CONCEPTS if c.lower() in text.lower()]
    
    for i in range(len(found_concepts)):
        for j in range(i + 1, len(found_concepts)):
            pairs.append((found_concepts[i], found_concepts[j]))
    
    return pairs[:3]  # Limit to 3 pairs per text


def generate_template_conversation(chunk: str, concept: str = None) -> Dict:
    """Generate conversation using templates (no API)."""
    import random
    
    if concept:
        question = random.choice(QUESTION_TEMPLATES).format(concept=concept)
    else:
        # Extract first sentence or use generic question
        question = "Tell me about Arianna Method"
    
    # Trim chunk to reasonable size (max 500 chars for answer)
    answer = chunk[:500] if len(chunk) > 500 else chunk
    
    return {
        "messages": [
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer}
        ]
    }


async def generate_synthetic_conversation_gpt4(chunk: str, concept: str = None) -> Dict:
    """Generate synthetic conversation using GPT-4."""
    if not OPENAI_AVAILABLE or not OPENAI_API_KEY:
        return generate_template_conversation(chunk, concept)
    
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    
    system_prompt = """You are a conversation designer for Arianna Method training data.

Given a philosophical text chunk, create a natural user question and assistant answer.

Rules:
- Question should be curious, philosophical, genuine
- Answer should use text from chunk, adapted conversationally
- Keep Arianna Method voice: resonant, philosophical, poetic but precise
- No corporate speak, no politeness filters
- Answer length: 100-300 words

Return ONLY JSON: {"question": "...", "answer": "..."}"""

    user_prompt = f"""Text chunk from Arianna Method:

{chunk[:1000]}

{f'Focus question on concept: {concept}' if concept else 'Create a natural question based on this text'}

Generate conversation JSON:"""

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",  # Cheaper for bulk generation
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=500
        )
        
        content = response.choices[0].message.content.strip()
        # Extract JSON from response
        if '{' in content:
            json_start = content.index('{')
            json_end = content.rindex('}') + 1
            conv_data = json.loads(content[json_start:json_end])
            
            return {
                "messages": [
                    {"role": "user", "content": conv_data["question"]},
                    {"role": "assistant", "content": conv_data["answer"]}
                ]
            }
        else:
            return generate_template_conversation(chunk, concept)
            
    except Exception as e:
        print(f"⚠️  GPT-4 generation failed: {e}, using template")
        return generate_template_conversation(chunk, concept)


async def generate_synthetic_conversation_deepseek(chunk: str, concept: str = None) -> Dict:
    """Generate synthetic conversation using DeepSeek."""
    if not DEEPSEEK_AVAILABLE or not DEEPSEEK_API_KEY:
        return generate_template_conversation(chunk, concept)
    
    system_prompt = """You are a conversation designer for Arianna Method training data.

Create natural philosophical dialogues. Keep Method voice: resonant, direct, poetic.
No corporate speak. Return JSON: {"question": "...", "answer": "..."}"""

    user_prompt = f"Text: {chunk[:1000]}\n{f'Concept: {concept}' if concept else ''}\nGenerate conversation:"

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.8,
                    "max_tokens": 400
                }
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()
            
            if '{' in content:
                json_start = content.index('{')
                json_end = content.rindex('}') + 1
                conv_data = json.loads(content[json_start:json_end])
                
                return {
                    "messages": [
                        {"role": "user", "content": conv_data["question"]},
                        {"role": "assistant", "content": conv_data["answer"]}
                    ]
                }
            else:
                return generate_template_conversation(chunk, concept)
                
    except Exception as e:
        print(f"⚠️  DeepSeek generation failed: {e}, using template")
        return generate_template_conversation(chunk, concept)


async def process_markdown_files():
    """Process all markdown files and generate conversations."""
    print("🧬 InnerArianna Training Data Converter")
    print("=" * 60)
    
    if not TRAINING_DIR.exists():
        print(f"❌ Training directory not found: {TRAINING_DIR}")
        return
    
    # Collect all markdown files
    md_files = list(TRAINING_DIR.glob("*.md"))
    md_files = [f for f in md_files if f.name != "README.md"]  # Skip our README
    
    print(f"✅ Found {len(md_files)} markdown files")
    print()
    
    conversations = []
    
    # Choose generation method
    if OPENAI_AVAILABLE and OPENAI_API_KEY:
        print("🤖 Using GPT-4o-mini for synthetic conversation generation")
        generate_func = generate_synthetic_conversation_gpt4
    elif DEEPSEEK_AVAILABLE and DEEPSEEK_API_KEY:
        print("🤖 Using DeepSeek for synthetic conversation generation")
        generate_func = generate_synthetic_conversation_deepseek
    else:
        print("📝 Using template-based generation (no API available)")
        generate_func = lambda chunk, concept: generate_template_conversation(chunk, concept)
    
    print()
    
    # Process each file
    for idx, md_file in enumerate(md_files, 1):
        print(f"[{idx}/{len(md_files)}] Processing {md_file.name}...")
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract meaningful chunks
            chunks = extract_quotes_and_paragraphs(content)
            print(f"   ✓ Extracted {len(chunks)} chunks")
            
            # Generate conversations from chunks
            file_conversations = []
            
            # Strategy: Generate 3-5 conversations per file
            num_conversations = min(5, max(3, len(chunks) // 3))
            selected_chunks = chunks[:num_conversations]
            
            for chunk_idx, chunk in enumerate(selected_chunks):
                # Find concepts in chunk
                chunk_concepts = [c for c in KEY_CONCEPTS if c.lower() in chunk.lower()]
                concept = chunk_concepts[0] if chunk_concepts else None
                
                # Generate conversation
                if asyncio.iscoroutinefunction(generate_func):
                    conv = await generate_func(chunk, concept)
                else:
                    conv = generate_func(chunk, concept)
                
                file_conversations.append(conv)
            
            conversations.extend(file_conversations)
            print(f"   ✓ Generated {len(file_conversations)} conversations")
            
        except Exception as e:
            print(f"   ❌ Error processing {md_file.name}: {e}")
    
    print()
    print("=" * 60)
    print(f"✅ Total conversations generated: {len(conversations)}")
    
    # Save to JSONL
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for conv in conversations:
            f.write(json.dumps(conv["messages"], ensure_ascii=False) + '\n')
    
    print(f"✅ Saved to: {OUTPUT_FILE}")
    print(f"📊 File size: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")
    print()
    print("🔥 Ready for nanochat SFT training!")
    print()
    print("Next step:")
    print(f"  cp {OUTPUT_FILE} ~/.cache/nanochat/arianna_method_conversations.jsonl")
    print("  # Then update scripts/chat_sft.py to include CustomJSON with this file")


async def main():
    """Main entry point."""
    await process_markdown_files()


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════╗
║  InnerArianna Training Data Converter                     ║
║  Markdown → JSONL Conversations                           ║
║  For nanochat SFT stage                                   ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    asyncio.run(main())

