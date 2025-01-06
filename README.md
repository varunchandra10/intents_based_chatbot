
# IntelliChat AI Chatbot

```
Demo-Link : 
```

## Overview
IntelliChat AI is a chatbot built using Natural Language Processing (NLP) and Machine Learning techniques. It processes user inputs and responds based on the pre-trained model's understanding of user intents.

## Important Note to inform users that the project is still under development and improvements are planned for the future.

## Project Setup Instructions

### 1. Clone the Repository
To get started, first clone this repository to your local machine:

```bash
git clone https://github.com/varunchandra10/intents_based_chatbot.git
```

### 2. Create a Virtual Environment
Create a virtual environment to manage the dependencies for this project:

On Windows:
```bash
python -m venv .venv
```

On macOS/Linux:
```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment
Activate the virtual environment:

On Windows:
```bash
.\.venv\Scripts\activate
```

On macOS/Linux:
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
Now that your virtual environment is active, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 5. Download Necessary NLTK Data
The project uses the nltk library, which may require additional data to function properly. You can download the required data with the following command in Python:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### 6. Run the Streamlit App
Once all dependencies are installed, you can run the Streamlit app to interact with the chatbot. Use the following command to start the app:

```bash
streamlit run chatbot.py
```

This will launch the chatbot in your default web browser.

### 7. Model Evaluation
If you want to evaluate the model performance, the Streamlit app provides a "Model Evaluation" section where you can see the accuracy and other classification metrics.

## Required Libraries
The following libraries are required to run this project:

- nltk: For natural language processing tasks.
- scikit-learn: For machine learning tasks, including training models and feature extraction.
- streamlit: For creating the interactive web interface.

### 8. Useful Commands

To create a virtual environment:
```bash
python -m venv .venv  # For Windows
python3 -m venv .venv # For macOS/Linux
```

To activate the virtual environment:
```bash
.\.venv\Scripts\ctivate  # For Windows
source .venv/bin/activate # For macOS/Linux
```

To install dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```

To run the Streamlit app:
```bash
streamlit run chatbot.py
```

## File Structure
```bash
/project-folder
    /chatbot_model.py          # Model and training code
    /chatbot.py                # Streamlit app
    /intents.json              # Chatbot training data
    /chat_log.csv              # Saved chat history (generated during usage)
    /requirements.txt          # Python dependencies
    /.venv                     # Virtual environment
    /README.md                 # This file
```

## Additional Notes
- If you encounter any issues with NLTK or other dependencies, make sure that all required packages are installed and up-to-date.
- The chatbot will be hosted locally and can be accessed through http://localhost:8501 once the Streamlit app is running.
