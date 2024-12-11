import os
import openai
import streamlit as st
import streamlit.components.v1 as components  # Import the components module

# Configure OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY', 'xxxxxx')

# Function to generate HTML/CSS code using OpenAI
def generate_code_openai(prompt, max_tokens=500, temperature=0.7):
    """
    Generate HTML/CSS code using OpenAI GPT-3.5 or GPT-4 via ChatCompletion.
    The HTML should include embedded CSS and JS and be escaped correctly.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # Use gpt-3.5-turbo or gpt-4
            messages=[
                {"role": "system", "content": "You are an assistant that generates complete HTML code with embedded CSS and JS."},
                {"role": "user", "content": f"""Create a complete and functional webpage based on the following description:\n{prompt}\n
                 The output should follow the below standards/rules:
                 1. Valid HTML structure with a <head> and <body> section.\n
                 2. Embedded CSS for styling, ensuring it is placed within a <style> tag in the <head>.\n 
                 3. Embedded JavaScript, placed inside a <script> tag, for any interactive behavior described.\n 
                 4. Inline assets such as styles or scripts where possible (no external links).\n 
                 5. Follow all the latest design principles/standards. \n 
                 6. Consider all the latest trends and popularity. \n 
                 7. Give weightage to the type of the webpage being generated, if the information is provided. Example: Portfolio, Ecommerce, Feedback forms etc. \n 
                 Ensure that the output is syntactically correct, and return only the HTML code without any explanations, comments, or additional formatting.Do not include any code block formatting like ```html or any additional strings."""}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        st.error(f"Error with OpenAI API: {str(e)}")
        return "Error generating code."


# Streamlit UI components
def main():
    st.set_page_config(layout="wide")  # Set page to use the entire width of the screen
    # Inject custom CSS for scrollable columns
    # st.markdown("""
    #     <style>
    #     html, body, [data-testid="stAppViewContainer"] {
    #         height: 100vh;  /* Full viewport height */
    #         margin: 0;
    #         padding: 0;
    #         overflow: hidden; /* Disable global scrolling */
    #     }
    #     .scrollable {
    #         max-height: 90vh;  /* Set the maximum height to fit within the screen */
    #         overflow-y: auto; /* Enable vertical scrolling */
    #         padding: 10px;
    #         border: 1px solid #ddd;
    #         background-color: #f9f9f9;
    #     }
    #     </style>
    # """, unsafe_allow_html=True)

    # Layout: Divide the screen into 3 columns
    col1, col2, col3 = st.columns([2, 5, 3])  # 20%, 50%, 30%

    # Default prompt
    default_prompt = "Create a landing page with a hero image, three feature sections, and a footer."

    # Column 1: Chat input and token/temperature settings
    with col1:
        st.markdown('<div class="scrollable">', unsafe_allow_html=True)
        st.subheader("Chat with Assistant")
        prompt = st.text_area("Webpage Description", default_prompt, height=150)
        max_tokens = st.slider("Max Tokens", 50, 2000, 500)
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
        st.markdown('</div>', unsafe_allow_html=True)

    # Column 2: Live Preview
    with col2:
        st.markdown('<div class="scrollable">', unsafe_allow_html=True)
        st.subheader("Live Preview")
        preview_html = f"""<iframe style="width:100%; height: 700px" src=""></iframe>"""  # Default message
        preview_placeholder = st.empty()  # Placeholder for live preview area
        preview_placeholder.html(preview_html)
        st.markdown('</div>', unsafe_allow_html=True)

    # Column 3: Code Preview (scrollable)
    with col3:
        st.markdown('<div class="scrollable">', unsafe_allow_html=True)
        st.subheader("Generated Code Preview")
        generated_code = "Nothing to display"  # Default message
        code_placeholder = st.empty()  # Placeholder for code preview area
        code_placeholder.text_area("Generated HTML/CSS", value=generated_code, height=400, max_chars=None)
        st.markdown('</div>', unsafe_allow_html=True)

    with col1:
        # Button to generate code
        if st.button("Generate Code"):
            if prompt:
                with st.spinner("Generating code..."):
                    generated_code = generate_code_openai(prompt, max_tokens, temperature)
                    import base64
                    preview_html = f"""<iframe style="width:100%; height: 700px" src="data:text/html;base64,{base64.b64encode(generated_code.encode('utf-8')).decode('utf-8')}"></iframe>"""  # Set the preview to the generated HTML

                # Update the preview and code in their respective placeholders
                # Use Streamlit's components to render HTML
                preview_placeholder.empty()  # Clear any previous content
                # components.html(preview_html, height=700, scrolling=True)  # Render HTML in Live Preview area
                preview_placeholder.markdown(preview_html, unsafe_allow_html=True)

                # Update the code preview section
                code_placeholder.text_area("Generated HTML/CSS", value=generated_code, height=400, max_chars=None)
            else:
                st.warning("Please enter a description for the webpage.")

    # Error handling - Toast notification
    if generated_code == "Error generating code.":
        st.error("There was an error generating the webpage code.")


# Run the Streamlit app
if __name__ == "__main__":
    main()