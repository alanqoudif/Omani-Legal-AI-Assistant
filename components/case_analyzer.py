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
    
    # Voice input through file upload
    st.write(upload_text)
    audio_file = st.file_uploader("", type=["wav", "mp3", "ogg"], key="case_audio_upload")
    
    if audio_file is not None and "case_audio_processed" not in st.session_state:
        with st.spinner(transcribing_text):
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
                    
                    st.markdown(f"**Source {i+1}: {law_name}**")
                    st.markdown(f"*File: {source} | Relevance: {score:.2f}*")
                    st.markdown(doc.page_content)
                    st.markdown("---")
