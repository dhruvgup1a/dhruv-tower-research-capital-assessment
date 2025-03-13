from src.load_data import *
from src.vector_db import *
from src.report_generator import *
import os
from src.config import *
import shutil

def run_rag_pipeline(theme):

    # Deletes old database of chunks ---------------> Didn't work so not doing
    # print("Deleting Old vectorDB Directory...")
    # # if os.path.exists(VECTOR_DB_PATH):
    # #     shutil.rmtree(VECTOR_DB_PATH)
    # print("Deleted Old vectorDB Directory!")

    # Format for dict --> {book_title: file_path}
    books = {"The Bell Jar": ["data/The-Bell-Jar-1645639705._vanilla.xml", "xml"],
             "Metamorphosis": ["data/franz-kafka_metamorphosis.epub", "epub"],
             "The Stranger": ["data/the_stranger.pdf", "pdf"]}

    # Creates chunks for each book
    print("Processing Books...")
    all_chunks = []
    for book in books:
        all_chunks.extend(process_book(book, books[book][0], books[book][1]))
    print("Processed Books!")

    # Creates embeddings for each chunk 
    print("Storing all book data in DB...")
    create_chroma_index(all_chunks)
    print("Stored all book data in DB!")

    # Retrieves top chunks from each book
    print("Retrieving top chunks from each book...")
    top_chunks = []
    for book in books:
        retrieve_relevant_passages(theme, filter_book=book)
    print("Retrieved top chunks from each book")

    # Analyzes each book against the theme
    print("Analyzing each book against the theme individually...\n")
    for book in books:
        with open(f"{JSON_PATH}/{book}_top_chunks.json", "r") as f:
            json_data = json.load(f)
        generate_individual_analysis(book, json_data, theme)
        print(f"Done analyzing {book}")
    print("\nDone analyzing each book individually!")

    # Creates final report
    print("Generating final report...")
    generate_final_report(books, theme)
    print("Final Report Generated!")

    print("Report saved in /output directory. ")


