### Instructions how to run code are at the bottom

## My Thoughts

Hello Tower Research Capital Team, 

I wanted to say that I had a great time working on this project and enjoyed the technical challenge! 

I hope to use this page to give a quick project overview on my approach:

    1. Parse the book text
        - This required me to use the necessary libraries to acquire text data on each book. While working on this project though, I noticed that it would be useful to save the metadata for the text which would include the chapter the text is from. 
        - Afterwards, I created chunks (initially the chunks were chunks of characters but I later found chunks of sentences are better) for all the text in each book to help the system process the text. 
    2. Embeddings + Vector DB
        - I then created embeddings for each chunk and performed a cosine similarity search on the chunks. I did that individually for each book to ensure I had quotes to work with for each book. 
    3. LLMs use for output
        - After experimenting with various LLMs, I landed on gpt-4-turbo because it was quick and reliable. I did experiment with claude-opus for a bit but I found it to not be too reliable and it didn't an output format of .json. 
        - Also, I chose to first make 3 LLM function calls to have the model create an analysis of each book on the theme of social analysis. After that, I make an LLM call to combine all three analyses. 
        - I did try using different LLM models for each but I just didn't like the output I was getting from the other LLM models. 
    4. Other
        - You will find that my code does store almost every useful function data in JSON files because I was originally hoping to use that to create better prompts, however, I was unable to put enough time into making that work. Also, when I was initially running into hallucinations, my goal was to use the JSON files + PyDantic (for data validation) to ensure the structure and the quotes don't get altered and to ensure that LLM model is outputting everything in the right format with no unnecessary text around the report. 
        - Something I would change to this project if I had more time to work on it would definitely make the prompts more concise and make them work with the JSON files better to reduce the possibility of hallucinations. (Luckily it hasn't been hallucinating too much right now.)


Thank you for taking the time to go over my project and your consideration and I look forward hearing back you the team!

**Please find the generated output from the program in the file called `my_output.pdf`**

## Instructions to run
When setting up the project, follow these steps:

    1. Create a .env file within the src/ directory and store your open ai api key (OPENAI_API_KEY="the_key")
    2. Create VM (in terminal type these commands):
       - python -m venv env
       - source env/bin/activate
       - pip install -r requirements.txt

**Before running the project, I would reccomend deleting the contents of the `vectorDB/` directory everytime you try running the program. (I don't remember if it affects anything but I have been doing that during testing)**

To run, just type in terminal: `python main.py` 

