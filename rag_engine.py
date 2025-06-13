import os
import glob
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from markdown import markdown
from bs4 import BeautifulSoup

class KnowledgeBaseRAG:
    """RAG-движок: индексация и поиск по базе знаний (markdown)."""
    def __init__(self, kb_path):
        self.kb_path = kb_path
        self.docs = []
        self.doc_paths = []
        self._load_docs()
        self._build_index()

    def _load_docs(self):
        """Загружает все markdown-файлы как текстовые фрагменты."""
        self.docs = []
        self.doc_paths = []
        for md_file in glob.glob(os.path.join(self.kb_path, '*.md')):
            with open(md_file, encoding='utf-8') as f:
                text = f.read()
                # Преобразуем markdown в чистый текст
                html = markdown(text)
                soup = BeautifulSoup(html, 'html.parser')
                plain = soup.get_text(separator='\n')
                self.docs.append(plain)
                self.doc_paths.append(md_file)

    def _build_index(self):
        """Строит TF-IDF + FAISS индекс по всем документам."""
        self.vectorizer = TfidfVectorizer(stop_words=None, max_features=2048)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.docs).toarray().astype('float32')
        self.index = faiss.IndexFlatL2(self.tfidf_matrix.shape[1])
        self.index.add(self.tfidf_matrix)

    def search(self, query, top_k=5):
        """Ищет top_k релевантных фрагментов по запросу."""
        q_vec = self.vectorizer.transform([query]).toarray().astype('float32')
        D, I = self.index.search(q_vec, top_k)
        results = []
        for idx in I[0]:
            if idx < len(self.docs):
                results.append(self.docs[idx])
        return results 