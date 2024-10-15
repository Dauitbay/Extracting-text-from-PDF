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
    for item in toc:
        level, title, page_num = item

        add_to_structure(structure, title, level)
        # print(level, title,  item)
    doc.close()
    print(structure)
    return structure


def add_to_structure(structure: str, title: str,  level: int):

    if level == 1:
        numbers = list(filter(lambda x: x.isdigit(), title.split()))
        chapter = ''.join(numbers)
        if level == 1 and 'Глава' not in title:
            chapter_title = title

        structure[chapter] = {'title': title, 'sections': {}}
    elif level == 2:
        numbers = re.findall(r'\d+\.\d+', title)
        chapter = ''.join(numbers)
        string_part = re.sub(r'^\d+(\.\d+)*\s+', '', title)
        last_chapter = list(structure.keys())[-1]
        section_key = chapter
        counter = 1

        while section_key in structure[last_chapter]['sections']:
            section_key = f"{chapter}_{counter}"
            counter += 1
        structure[last_chapter]['sections'][section_key] = {'title': string_part, 'subsections': {}}
    elif level == 3:
        numbers = re.findall(r'\d+\.\d+.\d+', title)
        chapter = ''.join(numbers)
        if chapter:
            string_part = re.sub(r'^\d+(\.\d+)*\s+', '', title)
            last_chapter = list(structure.keys())[-1]
            last_section = list(structure[last_chapter]['sections'].keys())[-1]
            structure[last_chapter]['sections'][last_section]['subsections'][chapter] = {'title': string_part, 'subsections': {}}

def save_to_json(data):
    with open("structure_result.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    pdf_path = "Руководство_Бухгалтерия_для_Узбекистана_ред_3_0.pdf"

    pdf_structure = extract_pdf_structure(pdf_path)

    if pdf_structure:
        save_to_json(pdf_structure)
        print(f"PDF structure saved ")
