import os
import requests

API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
headers = {
    "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
}

def split_into_chunks(text, max_words=400):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])

def query(payload, min_length=30, max_length=150):
    response = requests.post(API_URL, headers=headers, json={
        "inputs": payload,
        "parameters": {
            "min_length": min_length,
            "max_length": max_length
        }
    })
    response.raise_for_status()
    result = response.json()

    if isinstance(result, dict) and "error" in result:
        raise Exception(f"Hugging Face error: {result['error']}")

    return result[0]["summary_text"]


def abstractive_summary(text, length="medium"):
    length_map = {
        "short": 0.3,
        "medium": 0.6,
        "detailed": 0.9
    }

    chunks = list(split_into_chunks(text, max_words=200))
    all_summaries = []

    for idx, chunk in enumerate(chunks):
        input_length = len(chunk.split())
        max_length = min(int(input_length * length_map.get(length, 0.6)), 150)
        min_length = max(30, max_length // 2)

        try:
            # print(f"Chunk {idx + 1}/{len(chunks)}: {input_length} words → Summary length {min_length}-{max_length}")
            summary = query(chunk, min_length=min_length, max_length=max_length)
            all_summaries.append(summary)
        except Exception as e:
            print(f"Error summarizing chunk {idx + 1}: {str(e)}")
            continue

    final_summary = " ".join(all_summaries)
    return final_summary if final_summary.strip() else "Summary generation failed."
