# Power Automate Code Review Agent
You can upload a Power Automate code into the UI and get a review for the code

It outputs:
- code_review_status: True/ False
- Problems_identified: list of problems in code
- Recommendations: Recommended soliuutions by LLM

This agent is powered by Google Gemini model

Get your API Key from Google and place it in .env file


```
|_schemas - input output schemas for app
|_prompts - prompts to be used for code review by Gemini model
|_app     - streamlit app to be run 
```

# Create a python environment
```
conda create -n code_review_env python=3.10 -y
conda activate code_review_env
pip install -r requirements.txt
conda deactivate
```

# Run the app
```
streamlit run app.py
```