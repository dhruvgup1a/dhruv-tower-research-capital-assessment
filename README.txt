When setting up the project, follow these steps:
    1. Create a .env file within the src/ directory and store your open ai api key (OPENAI_API_KEY="the_key")
    2. Create VM (in terminal type these commands):
       - python -m venv env
       - source env/bin/activate
       - pip install -r requirements.txt


Before running the project, I would reccomend deleting the contents of the vectorDB directory everytime you try running the program. (I don't remember if it affects anything but I have been doing that while testing and tuning.)

To run, just type in terminal: python main.py 

