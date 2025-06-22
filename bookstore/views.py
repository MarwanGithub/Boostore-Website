from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Book
from .cart import Cart

# Create your views here.

@require_POST
def add_to_cart(request, book_id):
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
    return render(request, 'bookstore/cart_detail.html', {'cart': cart})

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
    whatsapp_number = "201234567890"  # Example: "201234567890" (Country code without +)
    messenger_username = "61560901176029" # From facebook.com/profile.php?id=61560901176029

    context = {
        'cart': cart,
        'whatsapp_url': f"https://wa.me/{whatsapp_number}?text={prefilled_message}",
        'messenger_url': f"https://m.me/{messenger_username}?text={prefilled_message}",
        'prefilled_message': prefilled_message,
    }
    return render(request, 'bookstore/contact_to_order.html', context)

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
