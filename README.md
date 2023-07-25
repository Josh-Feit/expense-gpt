# Expense-GPT

Expense-GPT is a Django-based web application used for tracking your recent financial transactions. It utilizes the [OpenAI API](https://openai.com/blog/openai-api) to provide an AI assisstant that you can ask questions to about how to better manage your finances.

![expenseimage](https://github.com/Josh-Feit/expense-gpt/assets/106037593/9ab69bcf-e909-4c0a-8279-c0943b1abb75)

## Installation and Usage

Download Expense-GPT and open with a code editor of your choice. Replace the `.env.template` file with a `.env` file with the same contents as the `.env.template` file. Then get an [OpenAI API Key](https://platform.openai.com/account/api-keys) from the OpenAI website and set `OPENAI_API_KEY` in `.env` to your key. Finally, run the following command in the editor command line and follow http://127.0.0.1:8000/ to the local server.

```python
python manage.py runserver
```
 
