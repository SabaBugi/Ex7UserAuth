import csv
from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductUploadForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages


def home(request):
    return render(request, 'productshop/home.html')

@login_required
def product_page(request):
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

        elif 'import_csv' in request.POST:
            form = ProductUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                try:
                    decoded_file = csv_file.read().decode('utf-8').splitlines()
                    reader = csv.DictReader(decoded_file)
                    for row in reader:
                        Product.objects.create(
                            name=row['name'],
                            price=row['price'],
                            description=row['description']
                        )
                    messages.success(request, "Products imported successfully.")
                except Exception as e:
                    messages.error(request, f"Failed to import products: {e}")
            return redirect('product_shop:product_page')

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
        
        elif 'bulk_delete' in request.POST:
            if not request.user.has_perm('ProductShop.delete_product'):
                return HttpResponseForbidden("You do not have permission to delete products.")
            
            selected_ids = request.POST.getlist('selected_products')
            
            if selected_ids:
                Product.objects.filter(id__in=selected_ids).delete()
                messages.success(request, f"{len(selected_ids)} product(s) deleted successfully.")
            else:
                messages.error(request, "No products were selected for deletion.")
            
            return redirect('product_shop:product_page')


    return render(request, 'productshop/product_page.html', context)