from transformers import pipeline


# Load model once
summarization_pipeline = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# -------------------------------
# Helper to split text safely (word-level)
# -------------------------------
def split_into_chunks(text, max_words=400):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])

# -------------------------------
# Abstractive Summary with Safe Chunks
# -------------------------------
def abstractive_summary(text, length="medium"):
    length_map = {
        "short": 0.3,
        "medium": 0.6,
        "detailed": 0.9
    }

    chunks = list(split_into_chunks(text, max_words=400))  # Keep chunks small
    all_summaries = []

    for idx, chunk in enumerate(chunks):
        input_length = len(chunk.split())
        max_length = min(int(input_length * length_map.get(length, 0.6)), 150)
        min_length = max(30, max_length // 2)

        try:
            print(f"Summarizing chunk {idx + 1}/{len(chunks)} → Words: {input_length} | Target: {min_length}-{max_length}")
            summary = summarization_pipeline(
                chunk,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )[0]['summary_text']
            all_summaries.append(summary)
        except Exception as e:
            print(f"Chunk {idx + 1} summarization error:", str(e))
            continue

    final_summary = " ".join(all_summaries)
    return final_summary if final_summary.strip() else "Summary generation failed."
