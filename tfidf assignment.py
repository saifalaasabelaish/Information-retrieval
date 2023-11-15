from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import os

def open_folder(folder_path):
    documents = []
    file_paths = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        file = open(file_path, 'r')
        document = file.read()
        documents.append(document)
        file_paths.append(file_path)
        file.close()

    return documents, file_paths


def cos_ranked_docs(query, documents, file_paths, top_k=5):
    tfidf_transformer = TfidfTransformer()
    query_vector = vectorizer.transform([query])
    query_tfidf = tfidf_transformer.transform(query_vector)
    vectorizer = CountVectorizer(lowercase=True, stop_words='english',min_df=1, max_features=500)
    X = vectorizer.fit_transform(documents)
    X_tfidf = tfidf_transformer.fit_transform(X)
    cosine_similarities = cosine_similarity(query_tfidf, X_tfidf).flatten()
    top_similar_docs = cosine_similarities.argsort()[:-top_k-1:-1]

    top_documents = [(file_paths[i], cosine_similarities[i]) for i in top_similar_docs]
    return top_documents

folder_path = "C:/Users/SAIF/Desktop/test"  
query = ""

documents, file_paths = open_folder(folder_path)
top_documents = cos_ranked_docs(query, documents, file_paths)

print('top 5 files along with their cosine similarities :')
for i in range(5):
    file_path, similarity = top_documents[i]
    print(f"{i + 1}. Path: {file_path}, Similarity: {similarity}")
