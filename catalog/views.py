from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction as db_transaction
from django.db.models import Q
from django.utils import timezone
from .models import Book, Member, Transaction


def dashboard(request):
    total_books = Book.objects.count()
    available_copies = sum(b.available_copies for b in Book.objects.all())
    total_copies = sum(b.total_copies for b in Book.objects.all())
    total_members = Member.objects.count()
    active_issues = Transaction.objects.filter(status='issued').count()
    overdue_count = Transaction.objects.filter(status='issued', due_date__lt=timezone.now()).count()

    context = {
        'total_books': total_books,
        'available_copies': available_copies,
        'total_copies': total_copies,
        'total_members': total_members,
        'active_issues': active_issues,
        'overdue_count': overdue_count,
    }
    return render(request, 'catalog/dashboard.html', context)


# ---------- Books ----------

def book_list(request):
    query = request.GET.get('q', '')
    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(category__icontains=query)
        )
    return render(request, 'catalog/books.html', {'books': books, 'query': query})


def book_add(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        isbn = request.POST.get('isbn', '').strip() or None
        category = request.POST.get('category', '').strip() or None
        copies = int(request.POST.get('total_copies') or 1)

        if not title or not author:
            messages.error(request, 'Title and author are required.')
            return redirect('book_list')

        if isbn and Book.objects.filter(isbn=isbn).exists():
            messages.error(request, 'A book with this ISBN already exists.')
            return redirect('book_list')

        Book.objects.create(
            title=title, author=author, isbn=isbn, category=category,
            total_copies=copies, available_copies=copies
        )
        messages.success(request, f'"{title}" added successfully.')
    return redirect('book_list')


def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.transactions.filter(status='issued').exists():
        messages.error(request, 'Cannot delete a book that is currently issued.')
    else:
        book.delete()
        messages.success(request, 'Book deleted.')
    return redirect('book_list')


# ---------- Members ----------

def member_list(request):
    members = Member.objects.all()
    return render(request, 'catalog/members.html', {'members': members})


def member_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip() or None

        if not name or not email:
            messages.error(request, 'Name and email are required.')
            return redirect('member_list')

        if Member.objects.filter(email=email).exists():
            messages.error(request, 'A member with this email already exists.')
            return redirect('member_list')

        Member.objects.create(name=name, email=email, phone=phone)
        messages.success(request, f'{name} added successfully.')
    return redirect('member_list')


def member_delete(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if member.transactions.filter(status='issued').exists():
        messages.error(request, 'Cannot delete a member with an active book issue.')
    else:
        member.delete()
        messages.success(request, 'Member deleted.')
    return redirect('member_list')


# ---------- Issue / Return ----------

def issue_view(request):
    available_books = Book.objects.filter(available_copies__gt=0)
    members = Member.objects.all()
    active_transactions = Transaction.objects.filter(status='issued').select_related('book', 'member')

    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        member_id = request.POST.get('member_id')
        days = int(request.POST.get('days_allowed') or 14)

        book = get_object_or_404(Book, id=book_id)
        member = get_object_or_404(Member, id=member_id)

        if book.available_copies < 1:
            messages.error(request, 'No available copies of this book.')
            return redirect('issue_view')

        with db_transaction.atomic():
            Transaction.objects.create(
                book=book, member=member,
                due_date=Transaction.default_due_date(days),
                status='issued'
            )
            book.available_copies -= 1
            book.save()

        messages.success(request, f'"{book.title}" issued to {member.name}.')
        return redirect('issue_view')

    context = {
        'available_books': available_books,
        'members': members,
        'active_transactions': active_transactions,
    }
    return render(request, 'catalog/issue.html', context)


def return_book(request, transaction_id):
    txn = get_object_or_404(Transaction, id=transaction_id)
    if txn.status == 'returned':
        messages.error(request, 'This book has already been returned.')
        return redirect('issue_view')

    with db_transaction.atomic():
        txn.status = 'returned'
        txn.return_date = timezone.now()
        txn.save()

        book = txn.book
        book.available_copies += 1
        book.save()

    messages.success(request, f'"{txn.book.title}" returned successfully.')
    return redirect('issue_view')


# ---------- Transactions history ----------

def transaction_list(request):
    transactions = Transaction.objects.select_related('book', 'member').all()
    return render(request, 'catalog/transactions.html', {'transactions': transactions})
