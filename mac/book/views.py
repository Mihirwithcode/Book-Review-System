from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from django.db import models

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets

from .models import Book, Review
from .forms import BookForm, ReviewForm
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib.auth import get_user_model
User = get_user_model()

# Book list view
def book_list(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(ISBN__icontains=query)
        )
    else:
        books = Book.objects.all().order_by('title')
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'book/book_list.html', {'page_obj': page_obj})

# Book detail view
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    return render(request, 'book/book_detail.html', {'book': book, 'reviews': reviews})

# CREATE a new book
@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book/book_form.html', {'form': form})

# UPDATE an existing book
@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'book/book_form.html', {'form': form})

# DELETE an existing book
@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'book/book_confirm_delete.html', {'book': book})

# Submit review
@login_required
def submit_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', pk=book_id)
    else:
        form = ReviewForm()
    return render(request, 'book/review_form.html', {'form': form, 'book': book})


# user registration

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_profile(request):
    user = request.user
    reviews = Review.objects.filter(user=user)
    return render(request, 'registration/profile.html', {'user': user, 'reviews': reviews})

