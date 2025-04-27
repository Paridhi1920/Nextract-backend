from summarizer import abstractive_summary, extractive_summary

sample_text = """
Artificial Intelligence (AI) is revolutionizing industries by enabling machines to perform tasks that 
typically require human intelligence. From healthcare to finance, AI is driving innovation. 
Deep Learning, a subset of AI, uses neural networks to analyze vast amounts of data and make predictions.
"""

print("🔹 Abstractive Summary (BART):")
print(abstractive_summary(sample_text, max_length=50))

print("\n🔹 Extractive Summary (TextRank):")
print(extractive_summary(sample_text, num_sentences=2))
