from django.shortcuts import render

from coolboards.models import Item, ItemCategory, Manufacturer, Order
import json
from urllib.parse import unquote

from coolboards.models.order import DeliveryMethodChoices, PaymentMethodChoices
from coolboards.models.orderitem import OrderItem


def home(request):
    # Get 4 latest items from database
    items = Item.objects.all().order_by("-id")[:4]
    # Get main photo for each item
    for item in items:
        item.main_photo = item.get_main_photo()
    # Pass items to template
    return render(request, "home.html", {"items": items})


# Products page
def products(request, category=None):
    if category:
        # Get all items with category slug
        items = Item.objects.filter(category__slug=category)
    else:
        # Get all items from database
        items = Item.objects.all()
    cat = None
    if category:
        cat = ItemCategory.objects.get(slug=category)
    # Get main photo for each item and build compatibility
    for item in items:
        item.main_photo = item.get_main_photo()
        item.compatibility = item.get_build_compatibility()
    # Pass items to template
    return render(request, "products.html", {"items": items, "category": cat})


# Brand page
def brand(request, brand):
    manufacturer = Manufacturer.objects.get(slug=brand)
    # Get all items from manufacturer
    items = manufacturer.item_set.all()
    # Get main photo for each item
    for item in items:
        item.main_photo = item.get_main_photo()
        item.compatibility = item.get_build_compatibility()
    # Pass items from manufacturer to template
    return render(
        request,
        "brand.html",
        {"items": items, "manufacturer": manufacturer},
    )


# Product page
def product(request, item_id):
    # Get item from database
    item = Item.objects.get(id=item_id)
    item.compatibility = item.get_build_compatibility()
    # Get all photos for item except main photo
    photos = item.photos.filter(main=False)
    # Get main photo
    main_photo = item.get_main_photo()

    # Get reviews for item
    reviews = item.review_set.all()

    # Pass item to template
    return render(
        request,
        "product.html",
        {
            "product": item,
            "photos": photos,
            "main_photo": main_photo,
            "reviews": reviews,
        },
    )


# Cart page
def cart(request):
    # Get cart from cookies (url encoded as JSON)
    cart_json = request.COOKIES.get("cart", "{}")
    cart_json = unquote(cart_json)
    cart = json.loads(cart_json)
    # Get all items from cart
    items = Item.objects.filter(id__in=cart.keys())
    # Attach quantity, photo and sum to each item
    for item in items:
        item.quantity = cart[str(item.id)]
        item.main_photo = item.get_main_photo()
        item.sum = item.quantity * item.price

    # Reduce items to total price
    total = 0
    for item in items:
        total += item.sum
    # Pass items to template
    return render(
        request,
        "cart.html",
        {"items": items, "total": total, "cart_empty": len(items) == 0},
    )


# Brands page
def brands(request):
    # Get all manufacturers from database
    manufacturers = Manufacturer.objects.all()
    # Pass manufacturers to template
    return render(request, "brands.html", {"manufacturers": manufacturers})


# Categories page
def categories(request):
    # Get all categories from database
    categories = ItemCategory.objects.all()
    # Pass categories to template
    return render(request, "categories.html", {"categories": categories})


# Order page
def order(request):
    # Get cart from cookies (url encoded as JSON)
    cart_json = request.COOKIES.get("cart", "{}")
    cart_json = unquote(cart_json)
    cart = json.loads(cart_json)
    # Get all items from cart
    items = Item.objects.filter(id__in=cart.keys())
    # Attach quantity, photo and sum to each item
    for item in items:
        item.quantity = cart[str(item.id)]
        item.main_photo = item.get_main_photo()
        item.sum = item.quantity * item.price

    # Reduce items to total price
    total = 0
    for item in items:
        total += item.sum
    # Pass items to template
    return render(
        request,
        "order.html",
        {"items": items, "total": total, "cart_empty": len(items) == 0},
    )


def ordercomplete(request):
    # handle order form submission and put the order in the database
    if request.method == "POST":
        # Get cart from cookies (url encoded as JSON)
        cart_json = request.COOKIES.get("cart", "{}")
        cart_json = unquote(cart_json)
        cart = json.loads(cart_json)
        # Get all items from cart
        items = Item.objects.filter(id__in=cart.keys())
        # Attach quantity, photo and sum to each item
        for item in items:
            item.quantity = cart[str(item.id)]
            item.main_photo = item.get_main_photo()
            item.sum = item.quantity * item.price

        # Reduce items to total price
        total = 0
        for item in items:
            total += item.sum

        # get the form data
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        delivery_address = request.POST.get("delivery_address")
        notes = request.POST.get("notes")
        payment_method = request.POST.get("payment_method")
        delivery_method = request.POST.get("delivery_method")

        # save the order in the database
        order = Order(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            delivery_address=delivery_address,
            notes=notes,
            payment_method=PaymentMethodChoices[payment_method.upper()],
            delivery_method=DeliveryMethodChoices[delivery_method.upper()],
            payment_amount=total,
            payment_complete=False,
        )
        order.save()
        # Save the order items with quantities
        for item in items:
            order_item = OrderItem(
                item=item,
                quantity=cart[str(item.id)],
                order=order,
            )
            order_item.save()

        return render(request, "ordercomplete.html", {"order": order, "success": True})
    return render(request, "ordercomplete.html", {"success": False})


def post_review(request, item_id):
    if request.method == "POST":
        # get the form data
        user_name = request.POST.get("user_name")
        rating = min(int(request.POST.get("rating")), 5)
        text = request.POST.get("text")
        # save the review in the database
        item = Item.objects.get(id=item_id)
        review = item.review_set.create(user_name=user_name, rating=rating, text=text)
        review.save()
        return render(
            request, "post_review.html", {"success": True, "item_id": item_id}
        )
    return render(request, "post_review.html", {"success": False})
