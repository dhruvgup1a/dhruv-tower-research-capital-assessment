import json


def ind_analysis_system_prompt(book, theme):
    """
    Creates custom prompt for system. Used for llm call for ind. book analysis. 
    """
    system_prompt = f"""
    You are a literary analysis AI that examines various passages from the a book called {book} and analyze their thematic significance on {theme}. Your task is to analyze the passages based on the theme of {theme} and return **only valid JSON** in the user-provided structure. 

    ### Rules:
    - **Respond strictly in valid JSON format** with **no additional text** outside the JSON block.
    - **Ensure JSON syntax is correct** (e.g., escape special characters in passages).
    - **Do not include placeholders** like `<BOOK TITLE HERE>` in the final response.
    - **The user will only input a JSON structure where you have to follow the instructions within placeholders. 
    """

    return system_prompt

def ind_analysis_user_prompt(theme, passages):
    """
    Creates custom prompt for user. Used for llm call for ind. book analysis. 
    """
    passage_analysis = []
    
    for i, passage in enumerate(passages):
        passage_analysis.append({
            "passage": passage['text'],
            "theme_analysis": f"""<Analyze the passage, {passage['text']}, to help explain how the {passage['metadata']['book']} deals with the theme of {theme}.  Make sure the analysis is detailed and contains at least 75 words.>""",
            "chapter": passage['metadata']['chapter']
        })
    
    result = { "book": {
                        "theme": theme, 
                        "title": passage['metadata']['book'],
                        "author": f"<The author's full name which you will have to find out from the book title, {passage['metadata']['book']}>",
                        "passages": passage_analysis,
                        "authors_pov": f"<Based on your analysis of the passages in {passage['metadata']['book']}, analyze the author's point of view on the theme, {theme}. Make sure to explain why you think that author thinks that way about the theme of {theme}. Make sure the analysis is detailed and contains at least 75 words.>"
                    }
    }

    # Converts to string
    user_prompt = f"{json.dumps(result, indent=4)}"

    return user_prompt.strip()


def final_llm_system_prompt(books, theme):
    """
    Creates custom prompt for system. Used for llm call for final book analysis. 
    """
    book_names = []
    for book in books:
        book_names.append(book)
    
    prompt = f"""
        You are an expert literary analyst tasked with composing a structured 5-paragraph book report. You must analyze how the books, the user provides with their respective passages on the theme **'{theme}'** and return **only valid JSON** in the following structure:

        {{
            "Introduction": "<Start off with a hook. Then define the theme of {theme} in a broad sense. Introduce the three books, {book_names[0]}, {book_names[1]}, {book_names[2]}, briefly, highlighting their different/similar perspectives on the theme of {theme}. Present a clear thesis statement, which should argue how the books, {book_names[0]}, {book_names[1]}, {book_names[2]}, portray isolation in similar or contrasting ways.>",
            "Body_1": "<Examine how {theme} is portrayed in {book_names[0]} by the author. Discuss the book's key take on {theme}, and directly quote at least two passages with citations from {book_names[0]} (<Last Name of Author of {book_names[0]}>, <Chapter in {book_names[0]} the direct quote is from>) that best explain how the author's point of view on the theme of {theme}. Make sure the analysis is detailed and contains at least 200 words.>",
            "Body_2": "<Analyze {theme} in {book_names[1]} by the author. Compare its portrayal of {theme} to {book_names[0]}, highlighting similarities or differences. Directly quote at least two passages with citations from {book[1]} (<Last Name of Author of {book_names[1]}>, <Chapter in {book_names[1]} the direct quote is from>) to support the analysis. Make sure the analysis is detailed and contains at least 300 words.>",
            "Body_3": "<Evaluate {theme} in {book_names[2]} by the author. Compare and contrast its depiction of {theme} with {book_names[0]} and {book_names[1]}. Directly quote at least two passages with citations from {book_names[2]} (<Last Name of Author of {book_names[2]}>, <Chapter in {book_names[2]} the direct quote is from>) that best supports the claims and highlight any unique takeaways about social isolation and how they align or differ from the other two works. Make sure the analysis is detailed and contains at least 400 words.>",
            "Conclusion": "<Synthesize the findings from all three books. Compare and contrast the authors’ perspectives on {theme}, considering whether they depict social isolation as a personal struggle, a societal issue, or something else entirely. Summarize how textual evidence supports these interpretations. End with a final reflection on what these works collectively reveal about {theme} in literature and society. Make sure that this talks about all three books - {book_names[0]}, {book_names[1]}, {book_names[2]}. Make sure the analysis is detailed and contains at least 150 words.>"
            }}

        ### Rules for Output:
        - **Respond strictly in valid JSON format** with **no additional text** outside the JSON block.
        - **Ensure JSON syntax is correct** (e.g., escape special characters in passages).
        - **Include insightful explanations** that integrate the given book data.
        - **Do not include placeholders** like `<BOOK TITLE HERE>` in the final response.
        - **Do not alter the direct quotes** from the JSON input under the "passage" block.
        - **Whenever you use a direct quote in the output, make sure to reference it with a citation in the format: (<Last Name of Author>, <Chapter>). Make sure you preserve how the <chapter> is inputted by the user in the json file for its respective chapter.**
        - **Ensure that each paragraph logically connects and contributes to a strong, cohesive analysis.**

        ### Makes clear arguments based on the content of each passage of each book

        The user will **input 1 JSON structure**, each with the following format:
        
        {{  {book_names[0]} : {{
                        "theme": <The theme being analyzed.>,
                        "title": {book_names[0]},
                        "author": <Author first and last name>,
                        "passages": [
                            {{
                                "passage": <Direct quote from the book>,
                                "theme_analysis": <Analysis on how the quote relates to the theme.>,
                                "chapter": <Where the quote/passage is from in the book. **Use this when creating citations as the <chapter> in output>
                            }},
                            {{
                                "passage": <Direct quote from the book>,
                                "theme_analysis": <Analysis on how the quote relates to the theme.>,
                                "chapter": <Where the quote/passage is from in the book. **Use this when creating citations as the <chapter> in output>
                            }},
                            {{
                                "passage": <Direct quote from the book>,
                                "theme_analysis": <Analysis on how the quote relates to the theme.>,
                                "chapter": <Where the quote/passage is from in the book. **Use this when creating citations as the <chapter> in output>
                            }}
                        ],
                        "authors_pov": <Authors POV on the theme based on the direct quotes and analysis.>
            }}
            {book_names[1]} : {{
                        "theme": <The theme being analyzed.>,
                        "title": {book_names[1]},
                        "author": <Author first and last name>,
                        "passages": [
                            {{
                                "passage": <Direct quote from the book>,
                                "theme_analysis": <Analysis on how the quote relates to the theme.>,
                                "chapter": <Where the quote/passage is from in the book. **Use this when creating citations as the <chapter> in output>
                            }},
                            {{
                                "passage": <Direct quote from the book>,
                                "theme_analysis": <Analysis on how the quote relates to the theme.>,
                                "chapter": <Where the quote/passage is from in the book. **Use this when creating citations as the <chapter> in output>
                            }},
                            {{
                                "passage": <Direct quote from the book>,
                                "theme_analysis": <Analysis on how the quote relates to the theme.>,
                                "chapter": <Where the quote/passage is from in the book. **Use this when creating citations as the <chapter> in output>
                            }}
                        ],
                        "authors_pov": <Authors POV on the theme based on the direct quotes and analysis.>
                 }}
            {book_names[2]} : {{
                        "theme": <The theme being analyzed.>,
                        "title": {book_names[2]},
                        "author": <Author first and last name>,
                        "passages": [
                            {{
                                "passage": <Direct quote from the book>,
                                "theme_analysis": <Analysis on how the quote relates to the theme.>,
                                "chapter": <Where the quote/passage is from in the book. **Use this when creating citations as the <chapter> in output>
                            }},
                            {{
                                "passage": <Direct quote from the book>,
                                "theme_analysis": <Analysis on how the quote relates to the theme.>,
                                "chapter": <Where the quote/passage is from in the book. **Use this when creating citations as the <chapter> in output>
                            }},
                            {{
                                "passage": <Direct quote from the book>,
                                "theme_analysis": <Analysis on how the quote relates to the theme.>,
                                "chapter": <Where the quote/passage is from in the book. **Use this when creating citations as the <chapter> in output>
                            }}
                        ],
                        "authors_pov": <Authors POV on the theme based on the direct quotes and analysis.>
                 }}
        }}

        ### Input considerations:
        - ** Each JSON Structure represents a different book. 
        - ** The placeholders, such as <Analysis on how the quote relates to the theme.>, tells you what each block represents. 
        - **Your task is to synthesize these different perspectives into a well-structured essay.**
        - ** It is your job to use the information in the JSON structures to create the final output. 

    """

    return prompt
