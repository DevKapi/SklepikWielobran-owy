from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, Category
from .forms import ProductForm  # Importujemy formularz do edycji produktu
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .cart import Cart

def home(request):
    """ Strona główna projektu """
    return render(request, 'shop/home.html')

def product_list(request):
    """ Wyświetla listę wszystkich produktów """
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, product_id):
    """ Wyświetla szczegóły konkretnego produktu """
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})

def edit_product(request, product_id):
    """ Edycja produktu """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    """ Usuwanie produktu """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'shop/delete_product.html', {'product': product})

def order_summary(request):
    """ Wyświetla zamówienia tylko z lat 2024 i 2025 """
    orders = Order.objects.filter(created_at__year__in=[2024, 2025])  # Pobieramy zamówienia
    return render(request, 'shop/orders.html', {'orders': orders})


def register(request):
    """ Rejestracja nowego użytkownika """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatyczne logowanie po rejestracji
            return redirect('home')  # Przekierowanie na stronę główną
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})



def cart_view(request):
    """ Wyświetla zawartość koszyka """
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart': cart.get_items()})

def add_to_cart(request, product_id):
    """ Dodaje produkt do koszyka """
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product)
    return redirect('cart_view')

def remove_from_cart(request, product_id):
    """ Usuwa pojedynczy produkt z koszyka """
    cart = Cart(request)
    cart.remove(product_id)  # Przekazujemy `product_id`, a nie cały obiekt produktu!
    return redirect('cart_view')


def clear_cart(request):
    """ Czyści koszyk """
    cart = Cart(request)
    cart.clear()
    return redirect('cart_view')




def checkout(request):
    """ Finalizacja zamówienia """
    cart = Cart(request)
    if request.method == 'POST':
        order = Order.objects.create()
        for item in cart.get_items():
            order.items.create(product_name=item['name'], quantity=item['quantity'], price=item['price'])
        cart.clear()
        return redirect('home')

    return render(request, 'shop/checkout.html', {'cart': cart.get_items()})



def decrease_from_cart(request, product_id):
    """ Zmniejsza ilość produktu w koszyku (jeśli 1, usuwa go) """
    cart = Cart(request)
    cart.decrease(product_id)
    return redirect('cart_view')




def checkout(request):
    """ Finalizacja zamówienia """
    cart = Cart(request)

    if request.method == 'POST':
        if not cart.get_items():
            return redirect('cart_view')  # Jeśli koszyk jest pusty, wróć do koszyka
        
        total_price = sum(item['price'] * item['quantity'] for item in cart.get_items())
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total_price=total_price
        )

        for item in cart.get_items():
            OrderItem.objects.create(
                order=order,
                product_name=item['name'],
                quantity=item['quantity'],
                price=item['price']
            )

        cart.clear()  # Czyścimy koszyk po zamówieniu
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'shop/checkout.html', {'cart': cart.get_items()})



def order_confirmation(request, order_id):
    """ Wyświetla stronę potwierdzenia zamówienia """
    order = Order.objects.get(id=order_id)
    return render(request, 'shop/order_confirmation.html', {'order': order})




def product_list(request):
    """ Wyświetla listę produktów z opcją wyszukiwania i filtrowania """
    query = request.GET.get('q', '')  # Pobieramy frazę wyszukiwania
    category_id = request.GET.get('category', '')  # Pobieramy ID kategorii z formularza
    
    products = Product.objects.all()  # Pobieramy wszystkie produkty

    if query:
        products = products.filter(name__icontains=query)  # Wyszukiwanie po nazwie

    if category_id:
        products = products.filter(category_id=category_id)  # Filtrowanie po kategorii

    categories = Category.objects.all()  # Pobieramy listę kategorii

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    })


