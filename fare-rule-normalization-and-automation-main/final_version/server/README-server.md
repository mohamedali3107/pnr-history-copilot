# AI Rules: server

The server part is where you use the APIs to generate fare rules, answers, and where you manage the question and answer chains of the chatbot.

## 1. Run the server in localhost

To run the server you will first need to create a python virtual environment (venv) with the right dependencies. You can create it in `final_version/server`. To do this run the following command lines in a VScode terminal for example:

- <code>cd final_version/server</code>
- <code>python3 -m venv your-venv-name</code>

Then, place yourself in the venv:

- <code>source your-venv-name/bin/activate</code>

(
You are now in your venv, to deactivate it just run:
- <code>deactivate</code>
)

Then, while using your venv, go back in `final_version/server` and install the dependencies:

- <code>cd ..</code>
- <code>pip install -r requirements.txt</code>

It will install the modules present in the `requirements.txt` file with the correct version.

In `final_version/server`, create a file name .env where you can copy paste the following code:
<pre>
OPENAI_API_KEY= "your-openai-api-key"
</pre>
Now that you have done that, you are normally able to run the server (place yourself in final_version/server if it's not already the case):

- <code>unvicorn main:app --reload</code>

And go on the following url: it should be http://127.0.0.1:8000
If you want to see the POST methods go on this one: http://127.0.0.1:8000/docs#

## 2. Architecture of the repository

Here is the detailed architecture of the directory server:

### A. functions

In functions you have the main methods, used to retrieve fare rules using the API amadeus for dev or from the database /db. You also have the methods for scraping the trade portals, or generating responses using GPT-4.

### B. utils

In utils you have more global methods used by other files to extract text from pdf files, split it, embed it or vectorize it.

### C. main.py

This file is where we create the post methods, but also the file used to run the server.

### D. website_list.xlsx / db

Here are the databases.

- `website_list.xlsx` is where we link an Airline IATA Code to a corresponding trade portal. If you want to scrape more websites, here is where you can add them here. Be careful to only have one website per Airline IATA Code, we currently do not handle multiple urls.
- `db/db_flights_par_mad_doh.csv` is a database created with ATPCO data to mimic the behaviour of a professional Amadeus API that returns fare rules from a flight reference. We only had access to Amadeus price-offers API, so we decided to create this database to handle this usecase.

## 3. Roadmap

The nexts steps will be to improve the accuracy score of the answers (some clues are of the document we provided you), to add the possibility to input a webpage url to scrape it. Another step would be to automatically handle inconsistencies by comparing them - currently we are only looking for answers sequentially. Also, it will be important to connect it to the company API instead of the free one to access past flights, and also connect it to the real ATPCO database.
