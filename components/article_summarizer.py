import streamlit as st
from utils.document_processor import extract_article_by_number
from utils.openai_manager import OpenAIManager
import re

def article_summarizer(vector_store, available_laws, language):
    """
    Component for summarizing specific articles of laws.
    
    Args:
        vector_store: Vector store with document embeddings
        available_laws: List of available law names
        language: Language to use for interface (English or Arabic)
    """
    # Initialize OpenAI manager
    llm_manager = OpenAIManager()
    
    # Set up the UI based on language
    if language == "English":
        st.header("Article Summarizer")
        law_select_label = "Select a Law"
        article_input_label = "Article Number"
        button_text = "Summarize Article"
        loading_text = "Extracting and summarizing article..."
        not_found_text = "Article not found. Please check the article number and law selection."
        example_placeholder = "Example: 5"
    else:  # Arabic
        st.header("ملخص المادة")
        law_select_label = "اختر القانون"
        article_input_label = "رقم المادة"
        button_text = "تلخيص المادة"
        loading_text = "جاري استخراج وتلخيص المادة..."
        not_found_text = "المادة غير موجودة. يرجى التحقق من رقم المادة واختيار القانون."
        example_placeholder = "مثال: ٥"
    
    # Select law
    selected_law = st.selectbox(law_select_label, available_laws)
    
    # Enter article number
    article_number = st.text_input(article_input_label, placeholder=example_placeholder)
    
    # Process article number (handle Arabic numerals if necessary)
    if article_number:
        # Convert Arabic numerals to English if needed
        if any(ord(c) > 128 for c in article_number):
            arabic_to_english = {
                '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
                '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
            }
            for ar, en in arabic_to_english.items():
                article_number = article_number.replace(ar, en)
        
        # Remove non-numeric characters
        article_number = re.sub(r'[^0-9]', '', article_number)
    
    # Process request
    if st.button(button_text):
        if not article_number or not selected_law:
            return
        
        with st.spinner(loading_text):
            # Get the article text
            article_text = extract_article_by_number(vector_store.documents, selected_law, article_number)
            
            if not article_text:
                st.warning(not_found_text)
                return
            
            # Generate summary
            summary = llm_manager.summarize_article(article_text, language)
            
            # Display results
            st.write("### Article")
            st.write(article_text)
            
            st.write("### Summary")
            st.write(summary)
