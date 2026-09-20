from django.contrib import admin
from .models import Book, Member, Transaction


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'total_copies', 'available_copies', 'is_available')
    search_fields = ('title', 'author', 'isbn', 'category')
    list_filter = ('category',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'joined_at', 'active_issue_count')
    search_fields = ('name', 'email')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'issue_date', 'due_date', 'return_date', 'status', 'is_overdue')
    list_filter = ('status',)
    search_fields = ('book__title', 'member__name')
