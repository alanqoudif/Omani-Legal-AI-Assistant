import os
import re
from langchain.schema import Document

class VectorStore:
    """Simple search class for document retrieval using keyword matching"""
    
    def __init__(self, documents, use_huggingface=True):
        """
        Initialize the search engine with documents.
        
        Args:
            documents: List of LangChain Document objects
            use_huggingface: Not used, kept for backward compatibility
        """
        self.documents = documents
        self.use_huggingface = True  # Always use simple search
        
        # Pre-process documents for search
        self.process_documents()
    
    def process_documents(self):
        """Process documents to prepare them for search"""
        # Create a mapping of document content to document objects
        self.doc_contents = {}
        for doc in self.documents:
            # Get content and tokenize into lowercase words
            content = doc.page_content.lower()
            # Create mapping from content to document
            self.doc_contents[content] = doc
    
    def text_similarity(self, query, text):
        """
        Calculate a simple similarity score between query and text.
        
        Args:
            query: The search query
            text: The text to compare against
            
        Returns:
            A similarity score (higher is better)
        """
        query = query.lower()
        text = text.lower()
        
        # Count how many query terms appear in the text
        query_terms = re.findall(r'\b\w+\b', query)
        matches = sum(1 for term in query_terms if term in text)
        
        # Calculate a score between 0 and 1
        if not query_terms:
            return 0
        
        score = matches / len(query_terms)
        
        # Boost score if the exact query appears in the text
        if query in text:
            score += 0.5
            
        # Cap at 1.0
        return min(score, 1.0)
    
    def search(self, query, k=5):
        """
        Search for relevant documents.
        
        Args:
            query: Query string
            k: Number of results to return
            
        Returns:
            List of (Document, score) tuples
        """
        results = []
        
        # Score each document
        for content, doc in self.doc_contents.items():
            score = self.text_similarity(query, content)
            if score > 0:  # Only include results with some match
                results.append((doc, score))
        
        # Sort by score (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k results
        return results[:k]
    
    def search_by_law(self, query, law_name, k=5):
        """
        Search for relevant documents within a specific law.
        
        Args:
            query: Query string
            law_name: Name of the law to search within
            k: Number of results to return
            
        Returns:
            List of (Document, score) tuples
        """
        # Filter documents by law name
        filtered_docs = [doc for doc in self.documents if doc.metadata.get("law_name") == law_name]
        
        if not filtered_docs:
            return []
        
        # Create temporary search instance with filtered documents
        temp_search = VectorStore(filtered_docs)
        
        # Search within the filtered documents
        return temp_search.search(query, k=k)
