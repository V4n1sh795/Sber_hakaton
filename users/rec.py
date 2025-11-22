from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from books.models import Book
# Данные книг с жанрами и авторами


books= list(
    Book.objects.values('title', 'author', 'genre')
)
# Объединяем жанр и автора для создания признаков
def combine_features(book):
    return f"{book['genre']} {book['author']}"

book_features = [combine_features(book) for book in books]

# Векторизация признаков (Bag of Words)
vectorizer = CountVectorizer()
feature_matrix = vectorizer.fit_transform(book_features)

# Вычисляем косинусное сходство между книгами
similarity_matrix = cosine_similarity(feature_matrix)
def get_books_by_titles(titles):
    """
    Генератор: принимает список названий книг,
    возвращает соответствующие объекты Book (если найдены).
    
    Для каждого названия возвращает:
    - первый найденный объект Book, если есть;
    - пропускает, если книги нет.
    """
    for title in titles:
        book = Book.objects.filter(title=title).first()
        if book:
            yield book
# Функция для получение рекомендаций по названию книги
def recommend(book_title):
    book_index = next((i for i, book in enumerate(books) if book["title"] == book_title), None)
    if book_index is None:
        return "Книга не найдена"
    
    sim_scores = list(enumerate(similarity_matrix[book_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [score for score in sim_scores if score[0] != book_index]
    
    top_books = sim_scores[:3]
    recommendations = [books[i]["title"] for i, score in top_books]
    res = []
    for book in get_books_by_titles(recommendations):
        res.append(book)
    return res

# Пример вывода рекомендаций
