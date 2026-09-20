from django.core.management.base import BaseCommand
from catalog.models import Book


class Command(BaseCommand):
    help = 'Seed the database with sample books'

    def handle(self, *args, **kwargs):
        if Book.objects.exists():
            self.stdout.write('Books already exist, skipping seed.')
            return

        sample_books = [
            ('Clean Code', 'Robert C. Martin', '9780132350884', 'Programming', 3),
            ('The Pragmatic Programmer', 'Andrew Hunt', '9780201616224', 'Programming', 2),
            ('Introduction to Algorithms', 'Thomas H. Cormen', '9780262033848', 'Computer Science', 2),
            ('Atomic Habits', 'James Clear', '9780735211292', 'Self-Help', 4),
            ('The Alchemist', 'Paulo Coelho', '9780062315007', 'Fiction', 3),
        ]
        for title, author, isbn, category, copies in sample_books:
            Book.objects.create(
                title=title, author=author, isbn=isbn, category=category,
                total_copies=copies, available_copies=copies
            )
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(sample_books)} books.'))
