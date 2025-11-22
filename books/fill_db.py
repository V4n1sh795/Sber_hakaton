from .models import Book
import csv

def create_db():
    filepath='books/archive/data.csv'
    
    with open(file=filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            book = Book.objects.get_or_create(
                title=row['title'],
                genre=row['categories'],
                author=row['authors'],
                description=['description'],
                cover_photo=None,
                cover_thumbnail=None,
            )
    print('database created')