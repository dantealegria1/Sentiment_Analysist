# Sentiment Analyst

## Description
Sentiment Analyst is a tool designed to identify the emotions in a text. Whether it's a message from your girlfriend, 
a review left on your website, or any other text, Sentiment Analyst can help you understand the underlying sentiments.

## Installation

It is highly recommended to create and use a virtual environment on your own machine to manage dependencies.

- Instal Virtualenv
```bash
pip install virtualenv
```
- Create a Virtual Environment:
Navigate to your project directory and create a virtual environment:
```bash
virtualenv env
```
- Activate the Virtual Environment:
  - On windows 
  ```bash
  source venv/bin/activate
  ```

  - On macOs or Linux
  ```bash
  source venv/bin/activate
  ```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the requiered libraries.

```bash
pip install nltk transformers collections spacy requests
```
## Usage

After installing all the requirements, run the following command. Make sure you are in the correct folder where the application is located:
```bash
python app.py
```
*IMPORTANT*: Remember youi have to get your on PRIVATE KEY for the [Thesaurus API](https://api-ninjas.com/api/thesaurus) 

```python
def Get_Synonyms(word):
    api_url = 'https://api.api-ninjas.com/v1/thesaurus?word={}'.format(word)
    response = requests.get(api_url, headers={'X-Api-Key': 'PRIVATE KEY'})
    try:
        if response.status_code == requests.codes.ok:
            data = response.json()
            synonyms = data.get('synonyms', [])
            return synonyms
    except Exception as e:
        print(f"Error getting synonyms: {e}")
```
Replace 'YOUR_PRIVATE_KEY' with your actual API key to use the Thesaurus API.

With these steps, you should be able to set up and run the Sentiment Analyst tool successfully. Enjoy analyzing sentiments!

