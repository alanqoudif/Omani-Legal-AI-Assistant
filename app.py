import os
import streamlit as st
from pathlib import Path
import glob

# Import components
from components.document_qa import document_qa
from components.article_summarizer import article_summarizer
from components.law_comparison import law_comparison
from components.document_creator import document_creator
from components.case_analyzer import case_analyzer

# Import utilities
from utils.document_processor import process_pdfs, get_available_laws
from utils.vector_store import VectorStore

# Set page config
st.set_page_config(
    page_title="Omani Legal AI Assistant",
    page_icon="⚖️",
    layout="wide",
)

# Initialize session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "processed_docs" not in st.session_state:
    st.session_state.processed_docs = False
if "available_laws" not in st.session_state:
    st.session_state.available_laws = []
if "language" not in st.session_state:
    st.session_state.language = "English"

# Title and description
st.title("Omani Legal AI Assistant")

# Language selection
language_options = ["English", "Arabic"]
language_col1, language_col2 = st.columns([1, 5])
with language_col1:
    selected_language = st.selectbox(
        "Language", 
        language_options, 
        index=language_options.index(st.session_state.language)
    )
    
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()

# Display content based on selected language
if st.session_state.language == "English":
    st.write("Your comprehensive assistant for Omani legal matters.")
    process_btn_text = "Process Legal Documents"
    processing_text = "Processing documents... This may take a few minutes."
    no_docs_text = "No PDF documents found in the current directory. Please add PDF files to continue."
else:  # Arabic
    st.write("مساعدك الشامل للمسائل القانونية العمانية.")
    process_btn_text = "معالجة الوثائق القانونية"
    processing_text = "جاري معالجة المستندات... قد يستغرق ذلك بضع دقائق."
    no_docs_text = "لم يتم العثور على مستندات PDF في الدليل الحالي. يرجى إضافة ملفات PDF للمتابعة."

# Find PDF files in the current directory
pdf_files = glob.glob("*.pdf") + glob.glob("**/*.pdf", recursive=True)

# Create a sample PDF file if none are found
if not pdf_files:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    import io
    
    if st.session_state.language == "English":
        demo_file_text = "Creating a sample PDF file for demonstration..."
        demo_law_text = """
        # Omani Labor Law (Sample)
        
        [Article 1]
        This law shall be called the Labor Law and shall apply to all employers and employees except those excluded by a special provision herein.
        
        [Article 2]
        Employment is a right of every citizen. No person shall be forced to perform work against their will.
        
        [Article 3]
        All citizens are equal in the right to work and in freedom of choice of profession according to rules and conditions set forth by law.
        
        [Article 4]
        It shall be prohibited to violate or evade the provisions of this Law and each condition or agreement to this effect shall be null and void.
        
        [Article 5]
        Arabic shall be the language to be used in all records, contracts, files, statements and other documents provided for in this Law or in any decisions or regulations issued in implementation of this Law.
        """
    else:  # Arabic
        demo_file_text = "إنشاء ملف PDF عينة للعرض التوضيحي..."
        demo_law_text = """
        # قانون العمل العُماني (عينة)
        
        [المادة 1]
        يسمى هذا القانون قانون العمل وينطبق على جميع أصحاب العمل والعاملين باستثناء المستبعدين بحكم خاص في هذا القانون.
        
        [المادة 2]
        العمل حق لكل مواطن. لا يجوز إجبار أي شخص على أداء عمل ضد إرادته.
        
        [المادة 3]
        جميع المواطنين متساوون في حق العمل وحرية اختيار المهنة وفقًا للقواعد والشروط المنصوص عليها في القانون.
        
        [المادة 4]
        يُحظر انتهاك أو التحايل على أحكام هذا القانون ويكون كل شرط أو اتفاق على خلاف ذلك باطلاً وباطلاً.
        
        [المادة 5]
        تكون اللغة العربية هي اللغة المستخدمة في جميع السجلات والعقود والملفات والبيانات وغيرها من الوثائق المنصوص عليها في هذا القانون أو في أي قرارات أو لوائح صادرة تنفيذاً لهذا القانون.
        """
    
    with st.spinner(demo_file_text):
        # Create a PDF
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        
        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, 750, "Omani Labor Law (Sample)")
        
        # Content
        c.setFont("Helvetica", 12)
        y_position = 700
        for line in demo_law_text.split('\n'):
            line = line.strip()
            if not line:
                y_position -= 20  # Add space for empty lines
                continue
                
            if line.startswith('['):
                c.setFont("Helvetica-Bold", 12)
                y_position -= 30  # Add more space before articles
            else:
                c.setFont("Helvetica", 12)
            
            # Check if we need a new page
            if y_position < 72:
                c.showPage()
                y_position = 750
            
            c.drawString(72, y_position, line)
            y_position -= 20
        
        c.save()
        
        # Write the PDF to disk
        pdf_data = pdf_buffer.getvalue()
        with open("oman_labor_law_sample.pdf", "wb") as f:
            f.write(pdf_data)
        
        # Update pdf_files list
        pdf_files = ["oman_labor_law_sample.pdf"]
        st.info("Created a sample PDF file for demonstration purposes.")

# Process PDF files if available
if pdf_files:
    if not st.session_state.processed_docs:
        if st.button(process_btn_text):
            with st.spinner(processing_text):
                # Process PDFs and create vector store
                documents = process_pdfs(pdf_files)
                st.session_state.vector_store = VectorStore(documents)
                st.session_state.available_laws = get_available_laws(documents)
                st.session_state.processed_docs = True
                st.rerun()
else:
    st.warning(no_docs_text)
    st.stop()

# Only show features if documents are processed
if st.session_state.processed_docs:
    # Main navigation tabs
    if st.session_state.language == "English":
        tabs = st.tabs(["Document Q&A", "Article Summarizer", "Law Comparison", "Document Creator", "Case Analyzer"])
    else:  # Arabic
        tabs = st.tabs(["البحث في الوثائق", "ملخص المادة", "مقارنة القوانين", "إنشاء المستندات", "تحليل الحالة"])
    
    # Document Q&A
    with tabs[0]:
        document_qa(st.session_state.vector_store, st.session_state.language)
    
    # Article Summarizer
    with tabs[1]:
        article_summarizer(st.session_state.vector_store, st.session_state.available_laws, st.session_state.language)
    
    # Law Comparison
    with tabs[2]:
        law_comparison(st.session_state.vector_store, st.session_state.available_laws, st.session_state.language)
    
    # Document Creator
    with tabs[3]:
        document_creator(st.session_state.vector_store, st.session_state.language)
    
    # Case Analyzer
    with tabs[4]:
        case_analyzer(st.session_state.vector_store, st.session_state.language)

# Footer
st.markdown("---")
if st.session_state.language == "English":
    st.markdown("Omani Legal AI Assistant © 2023 | Powered by NuqtaAI and LangChain")
else:  # Arabic
    st.markdown("مساعد الذكاء الاصطناعي القانوني العماني © 2023 | مدعوم من NuqtaAI و LangChain")
