import streamlit as st
from utils.openai_manager import OpenAIManager

def law_comparison(vector_store, available_laws, language):
    """
    Component for comparing different laws.
    
    Args:
        vector_store: Vector store with document embeddings
        available_laws: List of available law names
        language: Language to use for interface (English or Arabic)
    """
    # Initialize OpenAI manager
    llm_manager = OpenAIManager()
    
    # Set up the UI based on language
    if language == "English":
        st.header("Law Comparison")
        first_law_label = "First Law"
        second_law_label = "Second Law"
        text_input_label = "Comparison Query"
        compare_button_text = "Compare Laws"
        loading_text = "Comparing laws..."
        no_laws_text = "Please select two different laws to compare."
        query_placeholder = "How do these laws differ in their approach to penalties?"
    else:  # Arabic
        st.header("مقارنة القوانين")
        first_law_label = "القانون الأول"
        second_law_label = "القانون الثاني"
        text_input_label = "استعلام المقارنة"
        compare_button_text = "مقارنة القوانين"
        loading_text = "جاري مقارنة القوانين..."
        no_laws_text = "يرجى تحديد قانونين مختلفين للمقارنة."
        query_placeholder = "كيف تختلف هذه القوانين في نهجها تجاه العقوبات؟"
    
    # Select laws to compare
    col1, col2 = st.columns(2)
    with col1:
        first_law = st.selectbox(first_law_label, available_laws, key="first_law")
    with col2:
        # Filter out the first selected law
        second_law_options = [law for law in available_laws if law != first_law]
        second_law = st.selectbox(second_law_label, second_law_options, key="second_law")
    
    # Text input for comparison query
    query = st.text_area(text_input_label, placeholder=query_placeholder, height=100)
    
    # Process comparison
    if st.button(compare_button_text):
        if first_law == second_law:
            st.warning(no_laws_text)
            return
        
        with st.spinner(loading_text):
            # Extract content for the first law
            first_law_docs = [doc for doc in vector_store.documents 
                             if doc.metadata.get("law_name") == first_law]
            first_law_content = "\n".join([doc.page_content for doc in first_law_docs])
            
            # Extract content for the second law
            second_law_docs = [doc for doc in vector_store.documents 
                              if doc.metadata.get("law_name") == second_law]
            second_law_content = "\n".join([doc.page_content for doc in second_law_docs])
            
            # If the content is too long, use a summarized version
            max_content_length = 8000  # Adjust based on LLM context limits
            
            if len(first_law_content) > max_content_length:
                first_law_content = first_law_content[:max_content_length] + "..."
            
            if len(second_law_content) > max_content_length:
                second_law_content = second_law_content[:max_content_length] + "..."
            
            # Generate comparison
            comparison = llm_manager.compare_laws(
                first_law, first_law_content,
                second_law, second_law_content,
                language
            )
            
            # Display comparison with improved formatting
            st.write("### Comparison Results")
            
            # Format the comparison with proper styling for bidirectional text
            comparison_html = f"""
            <div dir="auto" style="background-color: #f9f9f9; padding: 15px; 
                                  border-radius: 5px; margin: 10px 0; 
                                  font-family: 'Arial', sans-serif; line-height: 1.6;
                                  border-left: 4px solid #2c3e50;">
                {comparison}
            </div>
            """
            st.markdown(comparison_html, unsafe_allow_html=True)
