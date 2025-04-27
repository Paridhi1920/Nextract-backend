from file_handler import extract_text_from_pdf, extract_text_from_docx, extract_text_from_pptx

print("📂 PDF Text:")
print(extract_text_from_pdf("data/syllabus 6th sem.pdf"))

print("\n📂 DOCX Text:")
print(extract_text_from_docx("data/exp1.docx"))

print("\n📂 PPTX Text:")
# print(extract_text_from_pptx("data/sample.pptx"))

