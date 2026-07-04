import os
import re
from collections import defaultdict

class OfflineSearchEngine:
    def __init__(self):
        self.index = defaultdict(list)
        self.documents = {}
        self.document_id_counter = 0

    def add_document(self, text, doc_name="Untitled"):
        """Adds a document to the search engine and builds its index."""
        doc_id = self.document_id_counter
        self.documents[doc_id] = {"name": doc_name, "text": text}
        self.document_id_counter += 1

        # Simple tokenization: split by non-alphanumeric characters
        words = re.findall(r'\w+', text.lower())

        # Build the index: word -> list of (doc_id, position)
        for i, word in enumerate(words):
            self.index[word].append((doc_id, i))

    def search(self, query):
        """Searches for documents containing the query terms."""
        query_words = re.findall(r'\w+', query.lower())
        if not query_words:
            return []

        # Get all documents that contain the first query word
        results = set()
        if query_words[0] in self.index:
            for doc_id, _ in self.index[query_words[0]]:
                results.add(doc_id)

        # Intersect with documents containing subsequent query words
        for word in query_words[1:]:
            if word not in self.index:
                return [] # If any word is not found, no results
            current_word_docs = set()
            for doc_id, _ in self.index[word]:
                current_word_docs.add(doc_id)
            results.intersection_update(current_word_docs)

        # Return document names for the matching document IDs
        return [self.documents[doc_id]['name'] for doc_id in results]

if __name__ == "__main__":
    # Example Usage:
    engine = OfflineSearchEngine()

    # Simulate adding documents (e.g., from local files)
    doc1_text = "Bu ders notu, makine öğrenmesi algoritmalarını anlatır. Yapay zeka temelleri içerir."
    engine.add_document(doc1_text, "Makine Öğrenmesi Temelleri.txt")

    doc2_text = "Araştırma makalesi, derin öğrenme modellerinin performansını inceler. Büyük veri setleri kullanılır."
    engine.add_document(doc2_text, "Derin Öğrenme Performans Analizi.pdf")

    doc3_text = "Kampüs duyurusu: Kütüphane çalışma saatleri uzatıldı. Öğrenci etkinlikleri hakkında bilgi."
    engine.add_document(doc3_text, "Kampüs Duyuruları.docx")

    print("--- Çevrimdışı Arama Motoru Örneği ---")

    # Perform searches
    query1 = "makine öğrenmesi"
    print(f"\nAranan: '{query1}'")
    results1 = engine.search(query1)
    if results1:
        print("Bulunan Belgeler:", results1)
    else:
        print("Belge bulunamadı.")

    query2 = "derin öğrenme büyük veri"
    print(f"\nAranan: '{query2}'")
    results2 = engine.search(query2)
    if results2:
        print("Bulunan Belgeler:", results2)
    else:
        print("Belge bulunamadı.")

    query3 = "kütüphane"
    print(f"\nAranan: '{query3}'")
    results3 = engine.search(query3)
    if results3:
        print("Bulunan Belgeler:", results3)
    else:
        print("Belge bulunamadı.")

    query4 = "yapay zeka"
    print(f"\nAranan: '{query4}'")
    results4 = engine.search(query4)
    if results4:
        print("Bulunan Belgeler:", results4)
    else:
        print("Belge bulunamadı.")
