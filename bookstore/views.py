from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Book, Category, SiteSettings
from .cart import Cart

# Create your views here.

@require_POST
def add_to_cart(request, book_id):
    '''
    
    '''
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    
    # Check for quantity in POST for cart updates
    if 'quantity' in request.POST:
        quantity = int(request.POST.get('quantity'))
        override = request.POST.get('override') == 'True'
        cart.add(book=book, quantity=quantity, override_quantity=override)
    else:
        # Default action from product pages
        cart.add(book=book)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # AJAX request, return updated totals
        book_id_str = str(book.id)
        if book_id_str in cart.cart:
            item_data = cart.cart[book_id_str]
            item_total_price = float(item_data['quantity']) * float(item_data['price'])
        else:
            # Should not happen if adding, but for safety
            item_total_price = 0

        return JsonResponse({
            'status': 'ok',
            'quantity': cart.cart.get(book_id_str, {}).get('quantity', 0),
            'total_items': len(cart),
            'item_total_price': item_total_price,
            'cart_total_price': float(cart.get_total_price())
        })

    return redirect('bookstore:cart_detail')

@require_POST
def remove_from_cart(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'removed': True,
            'total_items': len(cart),
            'cart_total_price': float(cart.get_total_price()),
        })

    return redirect('bookstore:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'bookstore/cart_detail.html', {
        'cart': cart,
        'store_name': 'المكتبة الجيرمانية'
    })

def contact_to_order(request):
    cart = Cart(request)
    if not cart:
        return redirect('bookstore:home')

    # --- Construct the pre-filled message ---
    message_lines = ["Hello! I'd like to order the following books from your store:", ""]
    for item in cart:
        line = f"- {item['book'].title} (Quantity: {item['quantity']})"
        message_lines.append(line)
    message_lines.append("")
    message_lines.append(f"Total Price: EGP {cart.get_total_price():.2f}")
    
    prefilled_message = "\n".join(message_lines)

    # --- TODO: Replace with your actual WhatsApp number and Messenger username ---
    whatsapp_number = "201149482404"  # Example: "201234567890" (Country code without +)
    messenger_username = "61560901176029" # From facebook.com/profile.php?id=61560901176029

    context = {
        'cart': cart,
        'whatsapp_url': f"https://wa.me/{whatsapp_number}?text={prefilled_message}",
        'messenger_url': f"https://m.me/{messenger_username}?text={prefilled_message}",
        'prefilled_message': prefilled_message,
        'store_name': 'المكتبة الجيرمانية',
    }
    return render(request, 'bookstore/contact_to_order.html', context)

def home(request):
    # Fetch 5 books to be featured on the home page.
    # We can later add a specific flag for "featured" books.
    featured_books = Book.objects.all().order_by('?')[:5]
    
    # Get site settings (creates defaults if none exist)
    site_settings = SiteSettings.get_settings()
    
    context = {
        'featured_books': featured_books,
        'site_settings': site_settings,
        'store_name': site_settings.site_title,
        'hero_title': site_settings.hero_title,
        'hero_subtitle': site_settings.hero_subtitle,
        'store_description': 'بسبب الإقبال الكبير على تعلم اللغة الألمانية، وصعوبة إيجاد كتاب ملائم لتنمية مهارة القراءة وزيادة الحصيلة اللغوية، قررنا إنشاء هذه المكتبة لترشيح الكتب وتحديد مستواها، كما نوفر كتباً بالإنجليزية في مجالات مختلفة بأسعار جيدة.',
        'opening_hours': 'يومياً من ١٠ صباحاً إلى ١٢ مساءً - كتاب جديد كل يوم'
    }
    return render(request, 'bookstore/home.html', context)

def book_list(request):
    all_books = Book.objects.all().order_by('-id')

    # Pagination
    page_number = request.GET.get('page')
    paginator = Paginator(all_books, 12)  # 12 books per page
    page_obj = paginator.get_page(page_number)

    context = {
        'books': page_obj,  # iterable of books on the current page
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'store_name': 'المكتبة الجيرمانية',
        'opening_hours': 'يومياً من ١٠ صباحاً إلى ١٢ مساءً - كتاب جديد كل يوم'
    }
    return render(request, 'bookstore/book_list.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # The 'images' related_name comes from the BookImage model
    # This gets all BookImage objects related to this book
    other_images = book.images.all()

    context = {
        'book': book,
        'other_images': other_images,
        'store_name': 'المكتبة الجيرمانية',
    }
    return render(request, 'bookstore/book_detail.html', context)
