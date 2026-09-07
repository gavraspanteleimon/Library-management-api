# Library Management API — Σημειώσεις

Django REST API με σχέσεις μεταξύ πινάκων (ForeignKey, ManyToMany, OneToOne).

---

## 📁 Δομή Project

```
library_service/
    manage.py
    library_service/       ← settings package
        settings.py
        urls.py             ← κεντρικό urls.py
    library/                ← το app μας
        models.py
        admin.py
        serializers.py
        views.py
        urls.py              ← urls του app
        migrations/
```

---

## 🗂️ models.py — Οι πίνακες και οι σχέσεις τους

```python
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    loan_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book} loaned by {self.member}"
```

### Τύποι σχέσεων που χρησιμοποιήσαμε

| Τύπος | Παράδειγμα | Τι σημαίνει |
|---|---|---|
| **ForeignKey** | `Book.author` | Many-to-One: πολλά βιβλία → έναν συγγραφέα |
| **ManyToManyField** | `Book.categories` | Many-to-Many: ένα βιβλίο πολλές κατηγορίες, μια κατηγορία πολλά βιβλία |
| **OneToOneField** | `Member.user` | One-to-One: κάθε member συνδέεται με ακριβώς έναν user |
| **Δύο ForeignKeys μαζί** | `Loan.book` + `Loan.member` | Σύνθετος πίνακας που συνδέει δύο άλλους πίνακες με επιπλέον δεδομένα (loan_date κλπ) |

### Βασικοί κανόνες
- Κάθε `ForeignKey`/`OneToOneField` χρειάζεται **υποχρεωτικά** `on_delete` (π.χ. `models.CASCADE` = διαγραφή "παιδιών" όταν διαγραφεί ο "γονιός").
- Το πρώτο argument σε ForeignKey/ManyToMany/OneToOne είναι πάντα το **model class**, όχι string.
- `__str__` πρέπει να κάνει **`return`**, ποτέ `print()` — αλλιώς σκάει η Django.
- `null=True` = επιτρέπει NULL στη **βάση**. `blank=True` = επιτρέπει κενό σε **forms/admin**. Συνήθως πάνε μαζί.

---

## 🛠️ admin.py — Εμφάνιση στο admin panel

```python
from django.contrib import admin
from .models import Author, Category, Book, Loan, Member

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio', 'birth_date')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'author__name')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'loan_date', 'return_date')
    search_fields = ('book__title', 'member__user__username')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'phone')
```

### Βασικοί κανόνες
- `search_fields`/`list_display` με **ένα** στοιχείο πρέπει να έχουν κόμμα: `('name',)` — χωρίς το κόμμα δεν είναι tuple.
- Στο `search_fields`, όταν το field είναι ForeignKey, χρησιμοποιείς **διπλή κάτω παύλα** (`__`) για να μπεις μέσα στο σχετιζόμενο model: `author__name` = "πήγαινε στο author, βρες το name του".
- **ManyToMany fields δεν επιτρέπονται** στο `list_display` απευθείας (π.χ. `categories`) — χρειάζεται custom method.
- `search_fields` δεν δουλεύει πάνω σε `DateField` (μόνο κειμενική αναζήτηση).

---

## 🔄 serializers.py — Μετατροπή σε JSON

```python
from rest_framework import serializers
from .models import Author, Book, Member, Loan, Category

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'birth_date']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'categories']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['user', 'phone', 'address']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['book', 'member', 'loan_date', 'return_date', 'is_returned']
```

- Το `serializers.ModelSerializer` παίρνει τα fields ενός model και τα μετατρέπει αυτόματα σε JSON (και αντίστροφα).
- Στο `Meta`, ορίζεις `model` (ποιο model) και `fields` (ποια πεδία να συμπεριλάβει).
- Προσοχή στο **case-sensitivity**: `rest_framework` (όχι `rest_Framework`), `serializers` (όχι `Serializers`).

---

## 🌐 views.py — Τα endpoints

```python
from rest_framework import viewsets
from .models import Author, Category, Book, Member, Loan
from .serializers import (
    AuthorSerializer, CategorySerializer, BookSerializer,
    MemberSerializer, LoanSerializer
)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
```

- `viewsets.ModelViewSet` δίνει **δωρεάν** GET (list + detail), POST, PUT, DELETE — χωρίς να γράψεις τίποτα άλλο.
- `queryset` = ποια δεδομένα επιστρέφει.
- `serializer_class` = πώς μετατρέπονται σε JSON.

---

## 🔗 urls.py

**Μέσα στο app (`library/urls.py`):**
```python
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet, CategoryViewSet, BookViewSet,
    MemberViewSet, LoanViewSet
)

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'books', BookViewSet)
router.register(r'members', MemberViewSet)
router.register(r'loans', LoanViewSet)

urlpatterns = router.urls
```

**Στο κεντρικό (`library_service/urls.py`):**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('library/', include('library.urls')),
]
```

- `DefaultRouter()` δημιουργεί αυτόματα όλα τα standard URLs (list, detail, create, update, delete) για κάθε ViewSet.
- Τελικά endpoints: `/library/authors/`, `/library/books/`, `/library/loans/` κλπ.
- **Πάντα trailing slash** στο τέλος του URL (π.χ. `/library/authors/`, όχι `/library/authors`).

---

## 💻 Χρήσιμες εντολές

### Django
```bash
python manage.py makemigrations   # δημιουργεί migration αρχεία από αλλαγές στα models
python manage.py migrate          # εφαρμόζει τα migrations στη βάση
python manage.py createsuperuser  # φτιάχνει admin χρήστη
python manage.py runserver        # ξεκινάει τον development server
```

### Git / GitHub
```bash
git init                          # αρχικοποίηση repo
git add .                         # προσθήκη όλων των αρχείων
git commit -m "μήνυμα"            # αποθήκευση snapshot
git remote add origin <URL>       # σύνδεση με GitHub repo
git branch -M main                # ονομασία branch σε main
git push -u origin main           # ανέβασμα στο GitHub
git remote -v                     # έλεγχος ποιο remote URL έχει συνδεθεί
git remote remove origin          # αφαίρεση remote (αν έγινε λάθος URL)
```

### `.gitignore` — τι ΔΕΝ ανεβαίνει στο GitHub
```
__pycache__/
*.pyc
venv/
env/
db.sqlite3
*.log
.env
```

---

## 📚 Πηγές για περαιτέρω μελέτη

- [Django Models & Relationships (επίσημη τεκμηρίωση)](https://docs.djangoproject.com/en/5.0/topics/db/models/)
- [Django Model Field Reference](https://docs.djangoproject.com/en/5.0/ref/models/fields/#field-types)
- [Foreign Key σε Django (freeCodeCamp)](https://www.freecodecamp.org/news/what-is-one-to-many-relationship-in-django/)

---

## 🎯 Επόμενα βήματα (για άλλη φορά)

- **Authentication/permissions** στο API (ποιος μπορεί να κάνει τι)
- **Filtering** π.χ. `/loans/?is_returned=false`
- **Nested serializers** — να βλέπεις πλήρη στοιχεία του author μέσα στο book, αντί για μόνο ID
- **README.md** για το repo (τι κάνει το project, πώς το τρέχει κάποιος άλλος)
