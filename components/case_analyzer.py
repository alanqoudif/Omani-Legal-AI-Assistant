import streamlit as st
from utils.openai_manager import OpenAIManager
from utils.pdf_generator import PDFGenerator
from utils.speech_to_text import SpeechToText, preprocess_audio
import datetime

def case_analyzer(vector_store, language):
    """
    Component for analyzing legal cases.
    
    Args:
        vector_store: Vector store with document embeddings
        language: Language to use for interface (English or Arabic)
    """
    # Initialize OpenAI manager, PDF generator, and speech-to-text
    llm_manager = OpenAIManager()
    pdf_gen = PDFGenerator(language)
    stt = SpeechToText("en" if language == "English" else "ar")
    
    # Set up the UI based on language
    if language == "English":
        st.header("Legal Case Analysis")
        case_input_label = "Describe the Legal Situation or Case"
        analyze_button_text = "Analyze Case"
        loading_text = "Analyzing the legal case..."
        download_text = "Download Analysis Report (PDF)"
        upload_text = "Or upload an audio file with your case description"
        transcribing_text = "Transcribing audio..."
        case_placeholder = """
        Please describe the legal situation or case in detail. Include relevant facts, dates, and circumstances.
        
        Example: "A person invested outside Oman without a permit from the Central Bank. The investment was 50,000 OMR in a foreign real estate project. What are the legal consequences according to Omani law?"
        """
    else:  # Arabic
        st.header("تحليل الحالة القانونية")
        case_input_label = "وصف الحالة أو القضية القانونية"
        analyze_button_text = "تحليل القضية"
        loading_text = "جاري تحليل القضية القانونية..."
        download_text = "تحميل تقرير التحليل (PDF)"
        upload_text = "أو قم بتحميل ملف صوتي يحتوي على وصف القضية"
        transcribing_text = "جاري نسخ الصوت..."
        case_placeholder = """
        يرجى وصف الحالة أو القضية القانونية بالتفصيل. قم بتضمين الحقائق والتواريخ والظروف ذات الصلة.
        
        مثال: "قام شخص بالاستثمار خارج عمان بدون تصريح من البنك المركزي. كان الاستثمار 50,000 ريال عماني في مشروع عقاري أجنبي. ما هي العواقب القانونية وفقاً للقانون العماني؟"
        """
    
    # Initialize session state for voice input
    if "case_voice_input" not in st.session_state:
        st.session_state.case_voice_input = ""
    
    # Case description input
    case_description = st.text_area(case_input_label, value=st.session_state.case_voice_input, placeholder=case_placeholder, height=200)
    
    # Voice input through file upload with improved styling
    if language == "English":
        record_button_text = "🎤 Upload Voice Case Description"
        processing_text = "Processing audio..."
    else:  # Arabic
        record_button_text = "🎤 تحميل وصف القضية صوتياً"
        processing_text = "جارٍ معالجة الصوت..."
    
    # Create a styled container for audio upload
    audio_container = st.container()
    with audio_container:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(f"**{record_button_text}**")
        with col2:
            audio_file = st.file_uploader("", type=["wav", "mp3", "ogg"], key="case_audio_upload",
                                        label_visibility="collapsed")
    
    # Process the audio file if uploaded
    if audio_file is not None and "case_audio_processed" not in st.session_state:
        with st.spinner(processing_text):
            # Read the audio file
            audio_bytes = audio_file.read()
            
            # Process the audio
            processed_audio = preprocess_audio(audio_bytes)
            
            # Transcribe the audio
            transcription = stt.transcribe_audio(processed_audio)
            
            # Update the case description
            st.session_state.case_voice_input = transcription
            st.session_state.case_audio_processed = True
            
            # Rerun to update the text area with the transcription
            st.rerun()
    
    # Clear the processed flag if there's no audio file
    if audio_file is None and "case_audio_processed" in st.session_state:
        st.session_state.pop("case_audio_processed")
    
    # Additional help text
    st.write(upload_text)
    
    # Process analysis
    if st.button(analyze_button_text):
        if not case_description:
            return
        
        with st.spinner(loading_text):
            # Search for relevant legal context
            search_results = vector_store.search(case_description, k=7)
            
            # Gather context from search results
            legal_context = ""
            for doc, score in search_results:
                # Only include relevant results
                if score > 0.2:
                    # Add metadata about the source
                    law_name = doc.metadata.get("law_name", "Unknown Law")
                    
                    # Add to context
                    legal_context += f"\nFrom {law_name}:\n{doc.page_content}\n"
            
            # Generate analysis
            analysis = llm_manager.analyze_legal_case(case_description, legal_context, language)
            
            # Display analysis
            st.write("### Legal Analysis")
            st.write(analysis)
            
            # Prepare PDF sections
            if language == "English":
                report_title = "Legal Case Analysis Report"
                sections = {
                    "Case Description": case_description,
                    "Legal Analysis": analysis,
                    "Relevant Laws": legal_context,
                    "Date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "Disclaimer": "This analysis is provided for informational purposes only and does not constitute legal advice. Consult with a qualified attorney for professional advice."
                }
            else:  # Arabic
                report_title = "تقرير تحليل الحالة القانونية"
                sections = {
                    "وصف القضية": case_description,
                    "التحليل القانوني": analysis,
                    "القوانين ذات الصلة": legal_context,
                    "التاريخ": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "إخلاء المسؤولية": "يتم تقديم هذا التحليل لأغراض إعلامية فقط ولا يشكل استشارة قانونية. استشر محاميًا مؤهلًا للحصول على مشورة مهنية."
                }
            
            # Generate PDF report
            pdf_buffer = pdf_gen.generate_legal_report(report_title, sections)
            
            # Download option
            st.download_button(
                label=download_text,
                data=pdf_buffer,
                file_name=f"legal_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
            
            # Show sources
            with st.expander("Relevant Legal Sources" if language == "English" else "المصادر القانونية ذات الصلة"):
                for i, (doc, score) in enumerate(search_results[:5]):  # Show top 5 sources
                    law_name = doc.metadata.get("law_name", "Unknown Law")
                    source = doc.metadata.get("source", "Unknown Source")
                    page_num = doc.metadata.get("page", "Unknown")
                    
                    # Create styled header for source
                    if language == "English":
                        header = f"**Source {i+1}: {law_name}**"
                        file_info = f"*File: {source} | Page: {page_num} | Relevance: {score:.2f}*"
                    else:
                        header = f"**المصدر {i+1}: {law_name}**"
                        file_info = f"*الملف: {source} | الصفحة: {page_num} | الصلة: {score:.2f}*"
                    
                    st.markdown(header)
                    st.markdown(file_info)
                    
                    # Display content in a more readable format
                    st.markdown("---")
                    st.markdown("##### Content:")
                    
                    # Improve the readability of the text using OpenAI
                    original_content = doc.page_content
                    
                    # Show loading spinner while improving text
                    with st.spinner("Improving text readability..." if language == "English" else "تحسين قراءة النص..."):
                        improved_content = llm_manager.improve_legal_text_readability(original_content, language)
                    
                    # Format the original content with proper styling
                    original_html = f"""
                    <details>
                        <summary style="cursor: pointer; color: #555; font-weight: bold; margin-bottom: 5px;">
                            {"Show Original Text" if language == "English" else "عرض النص الأصلي"}
                        </summary>
                        <div dir="auto" style="background-color: #f0f0f0; padding: 10px; 
                                              border-radius: 5px; margin: 10px 0; 
                                              font-family: 'Arial', sans-serif; line-height: 1.5;">
                            {original_content}
                        </div>
                    </details>
                    """
                    
                    # Format the improved content with proper styling
                    improved_html = f"""
                    <div dir="auto" style="background-color: #f0f0f0; padding: 10px; 
                                          border-radius: 5px; margin: 10px 0; 
                                          font-family: 'Arial', sans-serif; line-height: 1.5;
                                          border-left: 4px solid #2c3e50;">
                        {improved_content}
                    </div>
                    """
                    
                    # Show the improved text by default with option to view original
                    st.markdown(f"<h6>{'Improved Text:' if language == 'English' else 'النص المحسن:'}</h6>", unsafe_allow_html=True)
                    st.markdown(improved_html, unsafe_allow_html=True)
                    st.markdown(original_html, unsafe_allow_html=True)
                    st.markdown("---")
