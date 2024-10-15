import fitz
import json
import re

def extract_pdf_structure(pdf_file_path: str):
    try:
        doc = fitz.open(pdf_file_path)
    except Exception as e:
        print(f"Failed to open the PDF: {e}")
        return None

    toc = doc.get_toc()
    structure = {}
    count_chapters = 0

    for item in toc:
        level, title, page_num = item
        if "Глава" in title:
            count_chapters += 1
            continue
        else:
            add_to_structure(structure, level, title, count_chapters)
    doc.close()
    return structure


def extract_text_after_number(title: str):
    parts = title.split(' ', 1)
    if len(parts) > 1:
        return parts[1]
    return title


def extract_number(title: str):
    parts = title.split(' ', 1)
    if len(parts) > 0:
        return parts[0].rstrip('.')
    return ""


def is_valid_section_number(number: str):
    return bool(re.match(r'^\d+(\.\d+)*$', number))


def add_to_structure(structure: dict, level: int, title: str, count_chapter: int):

    if level == 1:
        structure[count_chapter] = {'title': title, 'sections': {}}
    elif level == 2:
        numbers = extract_number(title)
        if is_valid_section_number(numbers):
            chapter_key = numbers
            string_part = extract_text_after_number(title)
            last_chapter = list(structure.keys())[-1]
            if chapter_key in structure[last_chapter]['sections']:
                chapter_key = f"{numbers}."
            structure[last_chapter]['sections'][chapter_key] = {'title': string_part, 'subsections': {}}

    elif level == 3:
        numbers = extract_number(title)
        if is_valid_section_number(numbers):
            chapter_key = numbers
            if chapter_key:
                string_part = extract_text_after_number(title)
                last_chapter = list(structure.keys())[-1]
                last_section = list(structure[last_chapter]['sections'].keys())[-1]
                if chapter_key in structure[last_chapter]['sections'][last_section]['subsections']:
                    chapter_key = f"{numbers}."
                structure[last_chapter]['sections'][last_section]['subsections'][chapter_key] = {'title': string_part, 'subsections': {}}
    return structure


def save_to_json(data):
    with open("structure_result.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    pdf_path = "Руководство_Бухгалтерия_для_Узбекистана_ред_3_0.pdf"

    pdf_structure = extract_pdf_structure(pdf_path)

    if pdf_structure:
        save_to_json(pdf_structure)
        print(f"PDF structure saved")
