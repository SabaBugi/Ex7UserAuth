from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def home(request):
    return render(request, 'productshop/home.html')

@login_required
def product_page(request):
    user = request.user
    print("User:", user)
    print("Authenticated:", user.is_authenticated)
    print("Add Permission:", user.has_perm('productshop.add_product'))
    print("Change Permission:", user.has_perm('productshop.change_product'))
    print("Delete Permission:", user.has_perm('productshop.delete_product'))
    
    # Print all permissions for this user:
    print("All Permissions:", user.get_all_permissions())
    products = Product.objects.all()
    context = {'products': products, 'request': request}

    if request.method == 'POST':
        if 'add_product' in request.POST:
            if not request.user.has_perm('ProductShop.add_product'):
                return HttpResponseForbidden("You do not have permission to add products.")
            name = request.POST['name']
            price = request.POST['price']
            description = request.POST['description']
            Product.objects.create(name=name, price=price, description=description)

        elif 'edit_product' in request.POST:
            if not request.user.has_perm('ProductShop.change_product'):
                return HttpResponseForbidden("You do not have permission to edit products.")
            product_id = request.POST['product_id_edit']
            try:
                product = Product.objects.get(id=product_id)
                product.name = request.POST['name_edit']
                product.price = request.POST['price_edit']
                product.description = request.POST['description_edit']
                product.save()
            except Product.DoesNotExist:
                pass

        elif 'delete_product' in request.POST:
            if not request.user.has_perm('ProductShop.delete_product'):
                return HttpResponseForbidden("You do not have permission to delete products.")
            product_id = request.POST['product_id_delete']
            try:
                product = Product.objects.get(id=product_id)
                product.delete()
            except Product.DoesNotExist:
                pass

        return redirect('product_shop:product_page')

    return render(request, 'productshop/product_page.html', context)
