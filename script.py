import sys
import json
import re
from pdf2image import convert_from_path
import pytesseract
from transformers import BartForConditionalGeneration, BartTokenizer





def extract_text_from_pdf(pdf_path):
    # Convert PDF pages to images
    images = convert_from_path(pdf_path)

    # Perform OCR on each image and extract text
    extracted_text = []
    for i, image in enumerate(images):
        # Perform OCR on the image
        text = pytesseract.image_to_string(image, lang='eng')
        extracted_text.append(text)

    return '\n'.join(extracted_text)


def remove_phrases(summary, phrases_to_remove):
    for phrase in phrases_to_remove:
        summary = re.sub(fr'(?m)^{re.escape(phrase)}', '', summary)
    return summary


def join_lines_with_integer(text):
    return re.sub(r'(\d+)\.\n?(\d+)', r'\1\2', text)


def remove_redundant_info(summary):
    redundant_pattern = re.compile(
        r'\b(Exhibits?:|See exhibit)\s\d+\b|/b(for more details?:|For more information)\s\d+\b', re.IGNORECASE)
    summary = re.sub(redundant_pattern, '', summary)
    return summary


def refine_summary(summary, apply_conditions=True):
    summary = summary.replace(' ,', ',').replace(', ,', ',').rstrip(',')
    phrases_to_remove = ['Exhibit 10.3.', 'Exhibit 10.18.18', 'LR1.', '24.']
    summary = remove_phrases(summary, phrases_to_remove)

    if not summary.endswith('.'):
        summary += '.'

    summary = re.sub(r'(?<=[.!?])\s+(?=[A-Z])', '\n', summary)

    lessor_match = re.search(r'Lessor :\s*(.+?)(?=\n)', summary)
    lessee_match = re.search(r'Lessee :\s*(.+?)(?=\n)', summary)
    lessor = lessor_match.group(1) if lessor_match else ''
    lessee = lessee_match.group(1) if lessee_match else ''
    if apply_conditions:
        landlord_match = re.search(r'Landlord:\s*(.+?)(?=\n)', summary)
        tenant_match = re.search(r'Tenant:\s*(.+?)(?=\n)', summary)
        location_match = re.search(r'Location \s*(.+?)(?=\n)', summary)
        Landlord = landlord_match.group(1) if landlord_match else ''
        Tenant = tenant_match.group(1) if tenant_match else ''
        Location = location_match.group(1) if location_match else ''
    else:
        Landlord, Tenant, Location = '', '', ''

    relevant_info = re.findall(
        r'(Lessor|Lessee|Landlord|LANDLORD|Tenant|TENANT|House Owner|Issuer|Servicer|Location)\s*:\s*(.+?)(?=\n)',
        summary)
    extracted_info = {key: value.strip() for key, value in relevant_info}

    summary = re.sub(r'(?<=[A-Z])\.\n\s*(?=[A-Z])', ' ', summary)
    summary = re.sub(r'[“”‚‘’–‑‑‑:;,‛‘‘‛]+', ' ', summary)
    summary = re.sub(r'\(([^)]*)\)\s*', r'(\1) ', summary)
    summary = re.sub(r'Co\.\s*\n', 'Co. ', summary)
    summary = re.sub(r'St\.\s*\n', 'St. ', summary)
    summary = re.sub(r'\b\d{1,2}-\d{3}-\d{3}-\d{4}\b', '', summary)
    summary = re.sub(r'U\.S\.\s*\n\s*(call)', r'U.S. \1', summary)
    summary = re.sub(r'(?<=1521 E\.)\n', ' ', summary)
    summary = re.sub(r'This Lease\.\s*\n', 'This Lease. ', summary)
    summary = re.sub(r'^[A-Z][a-z\']*([A-Z][a-z\']*)*$\.\n', '^[A-Z][a-z\']*([A-Z][a-z\']*)* ', summary)
    summary = re.sub(r'INC\.\s*\n', 'INC. ', summary)
    summary = re.sub(r'NO\.\s*\n', 'NO. ', summary)
    summary = re.sub(r'No\.\s*\n', 'No. ', summary)
    summary = join_lines_with_integer(summary)
    summary = re.sub(r'Exhibits: \d+, ', '', summary)
    summary = re.sub(r'Exhibits: (\d+-\d+, )+\d+-\d+\.', '', summary)
    summary = re.sub(r'Exhibit (\d+\.\d+)', '', summary)
    summary = re.sub(r'\d+, ', '', summary)
    summary = re.sub(r'(\d+-\d+, )+\d+-\d+\.', '', summary)
    summary = re.sub(r'more information \s*www\.[^\s]+\.\s*\n', '', summary, flags=re.IGNORECASE)
    summary = re.sub(r'.*http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F])).*', '',
                     summary, re.IGNORECASE)
    # Remove duplicate lines
    unique_lines = list(set(summary.split('\n')))
    summary = '\n'.join(unique_lines)

    return summary, extracted_info


def generate_summary_bart_from_pdf(pdf_path):
    pdf_text = extract_text_from_pdf(pdf_path)
    model_name = 'facebook/bart-large-cnn'
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)
    lines = pdf_text.split('\n')
    part1 = '\n'.join(lines[:8])
    part2 = '\n'.join(lines[8:30])
    part3 = '\n'.join(lines[30:])

    # Generate summary for part 1
    inputs_part1 = tokenizer.encode(part1, return_tensors="pt", max_length=1024, truncation=True)
    summary_part1_ids = model.generate(inputs_part1, max_length=800, min_length=60, length_penalty=2.0, num_beams=4,
                                       early_stopping=True)
    summary_part1 = tokenizer.decode(summary_part1_ids[0], skip_special_tokens=True)
    refined_summary_part1, extracted_info1 = refine_summary(summary_part1)

    # Generate summary for part 2
    inputs_part2 = tokenizer.encode(part2, return_tensors="pt", max_length=1024, truncation=True)
    summary_part2_ids = model.generate(inputs_part2, max_length=800, min_length=80, length_penalty=2.0, num_beams=4,
                                       early_stopping=True)
    summary_part2 = tokenizer.decode(summary_part2_ids[0], skip_special_tokens=True)
    refined_summary_part2, extracted_info2 = refine_summary(summary_part2)

    # Join the refined summaries of part 1 and part 2
    refined_summary_part1 += "\n\n" + refined_summary_part2

    # Generate summary for part 3
    inputs_part3 = tokenizer.encode(part3, return_tensors="pt", max_length=1024, truncation=True)
    summary_part3_ids = model.generate(inputs_part3, max_length=2500, min_length=150, length_penalty=2.0, num_beams=4,
                                       early_stopping=True)
    summary_part3 = tokenizer.decode(summary_part3_ids[0], skip_special_tokens=True)
    refined_summary_part3, _ = refine_summary(summary_part3, apply_conditions=False)

    paragraph_summary_part3 = ' '.join([line.strip() for line in refined_summary_part3.split("\n") if line.strip()])

    # Construct the final summary
    final_summary = {
        "Parties_Detail_and_Address": [line.strip() for line in refined_summary_part1.split("\n") if
                                       line.strip() and not line.startswith("Lessor:") and not line.startswith(
                                           "Lessee:")],
        "Contract_Detail(Agreement)": paragraph_summary_part3
    }

    # Convert the dictionary to a JSON-formatted string
    json_summary = json.dumps(final_summary, indent=2, ensure_ascii=False)

    return json_summary

def generate_summary_for_pdf(pdf_path):
    try:
        json_summary_bart_pdf = generate_summary_bart_from_pdf(pdf_path)
        print(json_summary_bart_pdf)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    generate_summary_for_pdf(pdf_path)


# Example usage

