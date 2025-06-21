from django.shortcuts import render
from .models import Book

# Create your views here.

def home(request):
    # Fetch 5 books to be featured on the home page.
    # We can later add a specific flag for "featured" books.
    featured_books = Book.objects.all().order_by('?')[:5]
    
    context = {
        'featured_books': featured_books,
        'store_name': 'المكتبة الجيرمانية',
        'hero_title': 'اكتشف كتابك القادم المثالي',
        'hero_subtitle': 'مجموعة منتقاة من أفضل الكتب لتعلم اللغة الألمانية وتطوير مهارات القراءة',
        'store_description': 'بسبب الإقبال الكبير على تعلم اللغة الألمانية، وصعوبة إيجاد كتاب ملائم لتنمية مهارة القراءة وزيادة الحصيلة اللغوية، قررنا إنشاء هذه المكتبة لترشيح الكتب وتحديد مستواها، كما نوفر كتباً بالإنجليزية في مجالات مختلفة بأسعار جيدة.',
        'opening_hours': 'يومياً من ١٠ صباحاً إلى ١٢ مساءً - كتاب جديد كل يوم'
    }
    return render(request, 'bookstore/home.html', context)

def book_list(request):
    all_books = Book.objects.all()
    context = {
        'books': all_books,
        'store_name': 'المكتبة الجيرمانية',
        'opening_hours': 'يومياً من ١٠ صباحاً إلى ١٢ مساءً - كتاب جديد كل يوم'
    }
    return render(request, 'bookstore/book_list.html', context)
