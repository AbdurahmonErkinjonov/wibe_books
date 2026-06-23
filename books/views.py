from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Book, Category, Order, OrderItem


def home(request):
    books = Book.objects.select_related('category').all()
    categories = Category.objects.all()
    selected_cat = request.GET.get('category', '')
    if selected_cat:
        books = books.filter(category__id=selected_cat)
    return render(request, 'books/home.html', {
        'books': books,
        'categories': categories,
        'selected_cat': selected_cat,
    })


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})


def admin_dashboard(request):
    books = Book.objects.select_related('category').all().order_by('-created_at')
    categories = Category.objects.all().order_by('-created_at')
    return render(request, 'books/admin_dashboard.html', {
        'books': books,
        'categories': categories,
    })


def admin_login(request):
    if request.session.get('admin_authenticated'):
        return admin_dashboard(request)

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username == 'Abdurahmon2011' and password == '201123':
            request.session['admin_authenticated'] = True
            return admin_dashboard(request)
        error = "Login yoki parol noto'g'ri."

    return render(request, 'books/admin_login.html', {'error': error})


def admin_logout(request):
    request.session.pop('admin_authenticated', None)
    return redirect('home')


@csrf_exempt
@require_http_methods(["POST"])
def add_book(request):
    try:
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        description = request.POST.get('description')
        pages = request.POST.get('pages', 0)
        language = request.POST.get('language', "O'zbek")
        published_year = request.POST.get('published_year', 2024)
        isbn = request.POST.get('isbn', '')
        category_id = request.POST.get('category')
        cover = request.FILES.get('cover_image')

        book = Book(
            title=title, author=author, price=price,
            description=description, pages=pages,
            language=language, published_year=published_year, isbn=isbn
        )
        if category_id:
            book.category = Category.objects.get(id=category_id)
        if cover:
            book.cover_image = cover
        book.save()
        return JsonResponse({'success': True, 'id': book.id, 'message': 'Kitob muvaffaqiyatli qo\'shildi!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    try:
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.price = request.POST.get('price', book.price)
        book.description = request.POST.get('description', book.description)
        book.pages = request.POST.get('pages', book.pages)
        book.language = request.POST.get('language', book.language)
        book.published_year = request.POST.get('published_year', book.published_year)
        book.isbn = request.POST.get('isbn', book.isbn)
        cat_id = request.POST.get('category')
        if cat_id:
            book.category = Category.objects.get(id=cat_id)
        cover = request.FILES.get('cover_image')
        if cover:
            book.cover_image = cover
        book.save()
        return JsonResponse({'success': True, 'message': 'Kitob yangilandi!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return JsonResponse({'success': True, 'message': 'Kitob o\'chirildi!'})


@csrf_exempt
@require_http_methods(["POST"])
def add_category(request):
    try:
        data = json.loads(request.body)
        cat = Category.objects.create(name=data['name'], description=data.get('description', ''))
        return JsonResponse({'success': True, 'id': cat.id, 'name': cat.name})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def edit_category(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    try:
        data = json.loads(request.body)
        cat.name = data.get('name', cat.name)
        cat.description = data.get('description', cat.description)
        cat.save()
        return JsonResponse({'success': True, 'message': 'Kategoriya yangilandi!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def delete_category(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    cat.delete()
    return JsonResponse({'success': True, 'message': 'Kategoriya o\'chirildi!'})


def get_book_data(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return JsonResponse({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'price': str(book.price),
        'description': book.description,
        'pages': book.pages,
        'language': book.language,
        'published_year': book.published_year,
        'isbn': book.isbn,
        'category': book.category.id if book.category else '',
    })


def get_category_data(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    return JsonResponse({'id': cat.id, 'name': cat.name, 'description': cat.description})


# ========== SAVATCHA (CART) ==========

def _get_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


@csrf_exempt
@require_http_methods(["POST"])
def cart_add(request):
    try:
        data = json.loads(request.body)
        book_id = str(data.get('book_id'))
        cart = _get_cart(request)
        if book_id in cart:
            cart[book_id]['quantity'] += 1
        else:
            book = get_object_or_404(Book, pk=int(book_id))
            cart[book_id] = {
                'book_id': int(book_id),
                'title': book.title,
                'author': book.author,
                'price': str(book.price),
                'quantity': 1,
                'cover_image': book.cover_image.url if book.cover_image else '',
            }
        _save_cart(request, cart)
        return JsonResponse({'success': True, 'message': 'Savatga qo\'shildi!', 'cart_count': sum(i['quantity'] for i in cart.values())})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def cart_remove(request):
    try:
        data = json.loads(request.body)
        book_id = str(data.get('book_id'))
        cart = _get_cart(request)
        if book_id in cart:
            del cart[book_id]
            _save_cart(request, cart)
        return JsonResponse({'success': True, 'message': 'O\'chirildi!', 'cart_count': sum(i['quantity'] for i in cart.values())})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def cart_get(request):
    cart = _get_cart(request)
    items = []
    total = 0
    for item in cart.values():
        price = float(item['price'])
        qty = item['quantity']
        items.append({
            'book_id': item['book_id'],
            'title': item['title'],
            'author': item['author'],
            'price': price,
            'quantity': qty,
            'subtotal': price * qty,
            'cover_image': item.get('cover_image', ''),
        })
        total += price * qty
    return JsonResponse({'items': items, 'total': total, 'cart_count': sum(i['quantity'] for i in cart.values())})


# ========== BUYURTMA (ORDER) ==========

@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    try:
        data = json.loads(request.body)
        cart = _get_cart(request)
        if not cart:
            return JsonResponse({'success': False, 'error': 'Savatcha bo\'sh!'})

        total = 0
        for item in cart.values():
            total += float(item['price']) * item['quantity']

        order = Order.objects.create(
            customer_name=data.get('customer_name', ''),
            phone=data.get('phone', ''),
            extra_phone=data.get('extra_phone', ''),
            telegram_username=data.get('telegram_username', ''),
            payment_method=data.get('payment_method', 'naqt'),
            delivery_method=data.get('delivery_method', 'yetkazish'),
            delivery_address=data.get('delivery_address', ''),
            total_price=total,
            status='pending',
        )

        for item in cart.values():
            book = get_object_or_404(Book, pk=item['book_id'])
            OrderItem.objects.create(
                order=order,
                book=book,
                quantity=item['quantity'],
                price=item['price'],
            )

        request.session['cart'] = {}
        request.session.modified = True

        return JsonResponse({'success': True, 'message': 'Buyurtma muvaffaqiyatli yuborildi!', 'order_id': order.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ========== ADMIN - BUYURTMALAR ==========

def admin_orders(request):
    if not request.session.get('admin_authenticated'):
        return admin_login(request)
    orders = Order.objects.prefetch_related('items__book').all()
    return render(request, 'books/admin_orders.html', {
        'orders': orders,
    })


@csrf_exempt
@require_http_methods(["POST"])
def admin_accept_order(request, pk):
    if not request.session.get('admin_authenticated'):
        return JsonResponse({'success': False, 'error': 'Auth required'})
    try:
        order = get_object_or_404(Order, pk=pk)
        order.status = 'accepted'
        order.save()
        return JsonResponse({'success': True, 'message': f'Buyurtma #{order.id} qabul qilindi!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def admin_reject_order(request, pk):
    if not request.session.get('admin_authenticated'):
        return JsonResponse({'success': False, 'error': 'Auth required'})
    try:
        order = get_object_or_404(Order, pk=pk)
        order.status = 'rejected'
        order.save()
        return JsonResponse({'success': True, 'message': f'Buyurtma #{order.id} rad etildi!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
