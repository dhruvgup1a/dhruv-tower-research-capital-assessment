from openai import OpenAI
from fpdf import FPDF

from src.config import *
from src.prompts import *

openai_llm = OpenAI(api_key=OPENAI_API_KEY)

def generate_individual_analysis(book, passages, theme):
    """
    Creates an analysis on a book based on the passages provided based on the theme. 
    """
    # Combine the retrieved passages into a context string with citations.
    response = openai_llm.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": ind_analysis_system_prompt(book, theme)},
            {"role": "user", "content": ind_analysis_user_prompt(theme, passages)}
        ],
        max_tokens=2000, 
        temperature=0.25,
        response_format={"type": "json_object"}
    )

    output_text = response.choices[0].message.content.strip()

    # Creates json file with individual book analysis
    with open(f"{JSON_PATH}/{book}_analysis.json", "w") as f:
        json.dump(json.loads(output_text), f, indent=4)


def generate_final_report(books, theme):
    """
    Creates an analysis on the three books based on the individual analysis of all the books. 
    Creates a .pdf file with the final report. 
    """

    # Opens each .json file for each book's analysis and combines them for llm input
    combined_data = {}
    for book in books:
        with open(f"{JSON_PATH}/{book}_analysis.json", "r") as f:
            data = json.load(f)
            combined_data[book] = data["book"]

    with open(f"{JSON_PATH}/final_report_llm_input.json", 'w') as outfile:
        json.dump(combined_data, outfile, indent=4)

    response = openai_llm.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": final_llm_system_prompt(books, theme)},
            {"role": "user", "content": json.dumps(combined_data, indent=4)}
        ],
        max_tokens=3000, 
        temperature=0.25,
        response_format={"type": "json_object"}
    )

    output_text = response.choices[0].message.content.strip()

    # Creates json file with final report
    with open(f"{JSON_PATH}/final_output.json", "w") as f:
        json.dump(json.loads(output_text), f, indent=4)

    # Calls json to pdf method
    json_to_pdf(f"{JSON_PATH}/final_output.json", f"outputs/final_report.pdf")

def json_to_pdf(json_file, pdf_file, font="Times", font_size=12):
    """
    Converts a JSON file where each key is a paragraph into a PDF with a specified font and font size.
    """
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.add_page()
    pdf.set_font(font, size=font_size)

    for key, paragraph in data.items():
        pdf.set_font("Times", size=font_size)
        pdf.multi_cell(0, 10, paragraph)  # Double-spaced
        pdf.ln(5)  # Space between paragraphs

    pdf.output(pdf_file)
    print(f"PDF saved as {pdf_file}")
