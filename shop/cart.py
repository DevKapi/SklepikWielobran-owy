from decimal import Decimal

class Cart:
    def __init__(self, request):
        """ Inicjalizacja koszyka w sesji """
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        """ Dodaje produkt do koszyka lub zwiększa jego ilość """
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'id': product.id,  # ✅ Poprawne przechowywanie ID produktu
                'name': product.name,
                'price': float(product.price),  # ✅ Konwersja Decimal na float
                'quantity': quantity
            }
        self.save()

    def remove(self, product_id):
        """ Usuwa produkt z koszyka całkowicie """
        product_id = str(product_id)  # ✅ Konwersja ID na string (dla sesji)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrease(self, product_id):
        """ Zmniejsza ilość produktu w koszyku (jeśli ilość = 1, usuwa produkt) """
        product_id = str(product_id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= 1
            else:
                del self.cart[product_id]
            self.save()

    def save(self):
        """ Zapisuje stan koszyka w sesji """
        self.session.modified = True

    def get_items(self):
        """ Pobiera listę produktów w koszyku """
        return [
            {'id': product_id, **data}
            for product_id, data in self.cart.items()
        ]

    def clear(self):
        """ Usuwa wszystkie produkty z koszyka """
        self.session['cart'] = {}
        self.session.modified = True
