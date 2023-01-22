from datetime import date
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200,
        help_text='Book genre (e.g. Science Fiction)')

    def __str__(self):
        return self.name


class Language(models.Model):
    """Model representing a Language in which a book is written."""
    name = models.CharField(
        max_length=200,
        help_text="The book's primary language."
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'Author', on_delete=models.SET_NULL,
        null=True)
    summary = models.TextField(
        max_length=200, help_text='Enter a brief description of the book')
    isbn = models.CharField(
        'ISBN', max_length=13, unique=True,
        help_text='13 Character ' +
        '<a href="https//www.isbn-international.org/content/what-isbn">' +
        'ISBN number</a>')
    genre = models.ManyToManyField(
        Genre, help_text='A genre for this book')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for thid book"""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre for the admin pages"""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a specific copy of a book (could be checked out)"""
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        help_text='Unique ID for this copy of the book')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)


class Author(models.Model):
    """Model representing an author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
