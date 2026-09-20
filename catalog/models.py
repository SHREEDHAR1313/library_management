from django.db import models
from django.utils import timezone
from datetime import timedelta


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, unique=True, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def is_available(self):
        return self.available_copies > 0


class Member(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def active_issue_count(self):
        return self.transactions.filter(status='issued').count()


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('issued', 'Issued'),
        ('returned', 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='transactions')
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.book.title} -> {self.member.name} ({self.status})"

    @property
    def is_overdue(self):
        return self.status == 'issued' and self.due_date < timezone.now()

    @staticmethod
    def default_due_date(days=14):
        return timezone.now() + timedelta(days=days)
