<!-- Features -->
## 🌟 Description
- **Streamlit app to take in prompt and generate web page based on the same**

### Prerequisites
- **System**: Set env var "OPENAI_API_KEY" with the openai api key.

### Installation Steps
1. Clone project:
    ```sh
        git clone git@github.com:rajkris-cipherco/page_builder_llm.git
        cd page_builder_llm
    ```
2. Create virtualenv and install requirements:
    ```sh
        virtualenv -p python3.12 env
        source env/bin/activate
        pip install -r requirements.txt
    ```
3. Run the project
    ```sh
        streamlit run app.py
    ```