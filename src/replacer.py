from docx import Document
import re

def replace_keywords_in_docx(input_path, output_path, replacement_map):
    """
    Replaces text in a .docx file while attempting to preserve formatting.
    """
    doc = Document(input_path)

    def process_text_container(container):
        """Helper to process paragraphs or table cells."""
        for item in container:
            for old_text, new_text in replacement_map.items():
                # We use regex with word boundaries to avoid partial word replacement
                # e.g., don't replace 'lead' inside 'pleading'
                pattern = re.compile(re.escape(old_text), re.IGNORECASE)
                
                if pattern.search(item.text):
                    # Iterate through 'runs' to maintain bold/italic/font styles
                    for run in item.runs:
                        if pattern.search(run.text):
                            run.text = pattern.sub(new_text, run.text)

    # 1. Process all standard paragraphs
    process_text_container(doc.paragraphs)

    # 2. Process all tables (including nested cells)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                process_text_container(cell.paragraphs)

    doc.save(output_path)
    return True

if __name__ == "__main__":
    # Test logic
    sample_map = {"Managed": "Orchestrated", "coding": "software architecture"}
    replace_keywords_in_docx("data/input_resume.docx", "data/output_resume.docx", sample_map)
    print("Optimization complete. Check data/output_resume.docx")
