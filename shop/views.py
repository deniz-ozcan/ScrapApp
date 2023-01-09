from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from shop.models import Product, Ram, Storage, Processor, System, Screen, Brand
from django.core.paginator import Paginator
from django.db.models import Q
from django_filters import FilterSet

############################################## FILTER PAGES ################################################
class ListingFilter(FilterSet):

    class Meta:
        model = Product 
        ordering = ('price','rate')
        fields = {
            'ram': ['exact'],
            'storage': ['exact'],
            'processor': ['exact'],
            'system': ['exact'],
            'screen': ['exact'],
            'rate': ['gt'],
            'price': ['gt'],
        }

############################################### GENERAL PAGES ##############################################
def shopproducts(request):
    a=Product.objects.all()
    context={}
    if request.GET.get('order') == 'price':
        context['filtered_products'] = ListingFilter(request.GET, queryset=a.order_by(request.GET.get('order','price')))
        paginated_filtered_products = Paginator(ListingFilter(request.GET, queryset=a.order_by(request.GET.get('order','price'))).qs, 24)
    elif request.GET.get('order') == '-price':
        context['filtered_products'] = ListingFilter(request.GET, queryset=a.order_by(request.GET.get('order','-price')))
        paginated_filtered_products = Paginator( ListingFilter(request.GET, queryset=a.order_by(request.GET.get('order','-price'))).qs, 24)
    elif request.GET.get('order') == 'rate':
        context['filtered_products'] = ListingFilter(request.GET, queryset=a.order_by(request.GET.get('order','rate')))
        paginated_filtered_products = Paginator(ListingFilter(request.GET, queryset=a.order_by(request.GET.get('order','rate'))).qs, 24)
    elif request.GET.get('order') == '-rate':
        context['filtered_products'] = ListingFilter(request.GET, queryset=a.order_by(request.GET.get('order','-rate')))
        paginated_filtered_products = Paginator(ListingFilter(request.GET, queryset=a.order_by(request.GET.get('order','-rate'))).qs, 24)
    else:
        context['filtered_products'] = ListingFilter(request.GET, queryset=a)
        paginated_filtered_products = Paginator(ListingFilter(request.GET, queryset=a).qs, 24)
        
    pagenumber=request.GET.get('page')
    products = paginated_filtered_products.get_page(pagenumber)
    context['products'] = products
    context['pnum'] = products.number - 1
    context['nums'] = products.number
    context['nnum'] = products.number + 1
    return render(request, 'shop/index.html',context)

def shopsearch_products(request):
    if request.method == "POST":
        searched = request.POST['searched']
        products = Product.objects.filter(Q(name__name__icontains=searched) | Q(name__model__icontains=searched) | Q(ram__type__icontains=searched) | Q(storage__type__icontains=searched) | Q(processor__type__icontains=searched) | Q(system__type__icontains=searched) | Q(screen__type__icontains=searched))
        return render(request, 'shop/search.html', {
            'searched':searched,
            'products':products,
        })
    else:
        return render(request, 'shop/search.html', {})

def shopproduct_details(request, slug):
    a = Product.objects.get(slug=slug)
    context={}
    context['products'] = a
    return render(request, "shop/product-details.html",context)

############################################## LOGIN & REGISTER ############################################
def login_request(request):
    if request.user.is_authenticated:
        return redirect("shop")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("shop")
        else:
            return render(request, "shop/login.html", {
                "error": "Kullanıcı adı ya da parola yanlış"
            })

    return render(request, "shop/login.html")

def register_request(request):
    if request.user.is_authenticated:
        return redirect("shop")
        
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "shop/register.html", 
                {
                    "error":"username kullanılıyor.",
                    "username":username,
                    "email":email,
                    "firstname": firstname,
                    "lastname":lastname
                })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "shop/register.html", 
                    {
                        "error":"email kullanılıyor.",
                        "username":username,
                        "email":email,
                        "firstname": firstname,
                        "lastname":lastname
                    })
                else:
                    user = User.objects.create_user(username=username,email=email,first_name=firstname,last_name=lastname,password=password)
                    user.save()
                    return redirect("login")                    
        else:
            return render(request, "shop/register.html", {
                "error":"parola eşleşmiyor.",
                "username":username,
                "email":email,
                "firstname": firstname,
                "lastname":lastname
            })

    return render(request, "shop/register.html")

def logout_request(request):
    logout(request)
    return redirect("shop")

############################################ GENERAL ADMIN PANEL ###########################################
def admin(request):
    if request.user.is_superuser and request.method == "GET":
        context={}
        context['products'] = Product.objects.all()
        context['rams'] = Ram.objects.all()
        context['storages'] = Storage.objects.all()
        context['processors'] = Processor.objects.all()
        context['systems'] = System.objects.all()
        context['screens'] = Screen.objects.all()
        context['brands'] = Brand.objects.all()
        return render(request, 'admin/admin.html',context)
    else:
        return redirect("shop")
    
############################################ UPDATE & DELETE STUFF #########################################
def admin_products(request,id):
    context={}
    if request.user.is_superuser and request.method == "GET":
        context['product'] = Product.objects.get(id=id)
        context['rams'] = Ram.objects.all()
        context['storages'] = Storage.objects.all()
        context['processors'] = Processor.objects.all()
        context['systems'] = System.objects.all()
        context['screens'] = Screen.objects.all()
        context['brands'] = Brand.objects.all()
        return render(request, 'admin/products.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('_save'):
            product_brand = request.POST.get('product_brand')
            product_ram = request.POST.get('product_ram')
            product_storage = request.POST.get('product_storage')
            product_processor = request.POST.get('product_processor')
            product_system = request.POST.get('product_system')
            product_screen = request.POST.get('product_screen')
            product_image = request.POST.get('product_image')
            product_rate = request.POST.get('product_rate')
            product_price = request.POST.get('product_price')
            brand=Brand.objects.get(id=product_brand)
            ram=Ram.objects.get(id=product_ram)
            storage=Storage.objects.get(id=product_storage)
            processor=Processor.objects.get(id=product_processor)
            system=System.objects.get(id=product_system)
            screen=Screen.objects.get(id=product_screen)
            if Product.objects.filter(name=product_brand).exists() and Product.objects.filter(ram=product_ram).exists() and Product.objects.filter(storage=product_storage).exists() and Product.objects.filter(processor=product_processor).exists() and Product.objects.filter(system=product_system).exists() and Product.objects.filter(screen=product_screen).exists() and Product.objects.filter(image=product_image).exists() and Product.objects.filter(rate=product_rate).exists() and Product.objects.filter(price=product_price).exists() and Product.objects.filter(id=id).exists():
                context["success"]=f"{brand} {processor} {ram} {storage} {system} {screen} değişiklik olmadığı halde güncellenmiştir."
                product = Product.objects.filter(id=id)
                product.update(name=product_brand,ram=product_ram,storage=product_storage,processor=product_processor,system=product_system,screen=product_screen,image=product_image,rate=product_rate,price=product_price)
                context['product'] = Product.objects.get(id=id)
                context['rams'] = Ram.objects.all()
                context['storages'] = Storage.objects.all()
                context['processors'] = Processor.objects.all()
                context['systems'] = System.objects.all()
                context['screens'] = Screen.objects.all()
                context['brands'] = Brand.objects.all()
                return render(request, 'admin/products.html',context)
            else:
                product = Product.objects.filter(id=id)
                product.update(name=product_brand,ram=product_ram,storage=product_storage,processor=product_processor,system=product_system,screen=product_screen,image=product_image,rate=product_rate,price=product_price,is_updated=True)
                context["success"]=f"{brand} {processor} {ram} {storage} {system} {screen}  başarıyla güncellendi."
                context['product'] = Product.objects.get(id=id)
                context['rams'] = Ram.objects.all()
                context['storages'] = Storage.objects.all()
                context['processors'] = Processor.objects.all()
                context['systems'] = System.objects.all()
                context['screens'] = Screen.objects.all()
                context['brands'] = Brand.objects.all()
                return render(request, 'admin/products.html',context)
        elif request.POST.get('_delete'):
            context['product'] = Product.objects.get(id=id)
            context['rams'] = Ram.objects.all()
            context['storages'] = Storage.objects.all()
            context['processors'] = Processor.objects.all()
            context['systems'] = System.objects.all()
            context['screens'] = Screen.objects.all()
            context['brands'] = Brand.objects.all()
            context['productdeleted'] = "Ürün başarıyla silindi."
            return render(request, 'admin/products.html',context)
        elif request.POST.get('_deleteconfirmed'):
            product = Product.objects.filter(id=id).delete()
            return redirect("admin")
        elif request.POST.get('_deletedenied'):
            return redirect("admin")
        else:
            context["error"]="Sistemsel bir arıza yaşandı. Lütfen tekrar deneyiniz."
            return render(request, 'admin/products.html',context)
    else:
        return redirect("shop")

def admin_brands(request,id):
    context={}
    if request.user.is_superuser and request.method == "GET":
        context['brand'] = Brand.objects.get(id=id)
        return render(request, 'admin/brands.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('_save'):
            brand_name = request.POST.get('brand_name')
            brand_model = request.POST.get('brand_model')
            if Brand.objects.filter(name=brand_name).exists() and Brand.objects.filter(model=brand_model).exists() and Brand.objects.filter(id=id).exists():
                context["success"]=f"{brand_name} {brand_model} değişiklik olmadığı halde güncellenmiştir."
                brand = Brand.objects.filter(id=id)
                brand.update(name=brand_name,model=brand_model)
                return render(request, 'admin/brands.html',context)
            else:
                brand = Brand.objects.filter(id=id)
                brand.update(name=brand_name,model=brand_model)
                product = Product.objects.filter(name__id=id).update(is_updated=True, name_id=id)
                context["success"]=f"{brand_name} {brand_model} başarıyla güncellendi."
                return render(request, 'admin/brands.html',context)
        elif request.POST.get('_delete'):
            context['brand_name'] = Brand.objects.get(id=id).name
            context['brand_model'] = Brand.objects.get(id=id).model
            context["effectedproducts"] = Product.objects.filter(name_id=id)
            return render(request, 'admin/brands.html',context)
        elif request.POST.get('_deleteconfirmed'):
            brand = Brand.objects.filter(id=id).delete()
            return redirect("admin")
        elif request.POST.get('_deletedenied'):
            return redirect("admin")
        else:
            context["error"]="Sistemsel bir arıza yaşandı. Lütfen tekrar deneyiniz."
            return render(request, 'admin/brands.html',context)
    else:
        return redirect("shop")

def admin_rams(request,id):
    context={}
    if request.user.is_superuser and request.method == "GET":
        context['ram'] = Ram.objects.get(id=id)
        return render(request, 'admin/rams.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('_save'):
            ram_type = request.POST.get('ram_type')
            if Ram.objects.filter(type=ram_type).exists() and Ram.objects.filter(id=id).exists():
                context["success"]=f"{ram_type} değişiklik olmadığı halde güncellenmiştir."
                ram = Ram.objects.filter(id=id)
                ram.update(type=ram_type)
                return render(request, 'admin/rams.html',context)
            else:
                ram = Ram.objects.filter(id=id)
                ram.update(type=ram_type)
                product = Product.objects.filter(ram__id=id).update(is_updated=True, ram_id=id)
                context["success"]=f"{ram_type} başarıyla güncellendi."
                return render(request, 'admin/rams.html',context)
        elif request.POST.get('_delete'):
            context['ram_type'] = Ram.objects.get(id=id).type
            context["effectedproducts"]=Product.objects.filter(ram_id=id)
            return render(request, 'admin/rams.html',context)
        elif request.POST.get('_deleteconfirmed'):
            ram = Ram.objects.filter(id=id).delete()
            return redirect("admin")
        elif request.POST.get('_deletedenied'):
            return redirect("admin")
        else:
            context["error"]="Sistemsel bir arıza yaşandı. Lütfen tekrar deneyiniz."
            return render(request, 'admin/rams.html',context)
    else:
        return redirect("shop")

def admin_storages(request,id):
    context={}
    if request.user.is_superuser and request.method == "GET":
        context['storage'] = Storage.objects.get(id=id)
        return render(request, 'admin/storages.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('_save'):
            storage_type = request.POST.get('storage_type')
            if Storage.objects.filter(type=storage_type).exists() and Storage.objects.filter(id=id).exists():
                context["success"]=f"{storage_type} değişiklik olmadığı halde güncellenmiştir."
                storage = Storage.objects.filter(id=id)
                storage.update(type=storage_type)
                return render(request, 'admin/storages.html',context)
            else:
                storage = Storage.objects.filter(id=id)
                storage.update(type=storage_type)
                product = Product.objects.filter(storage__id=id).update(is_updated=True,storage_id=id)
                context["success"]=f"{storage_type} başarıyla güncellendi."
                return render(request, 'admin/storages.html',context)
        elif request.POST.get('_delete'):
            context['storage_type'] = Storage.objects.get(id=id).type
            context["effectedproducts"]=Product.objects.filter(storage_id=id)
            return render(request, 'admin/storages.html',context)
        elif request.POST.get('_deleteconfirmed'):
            storage = Storage.objects.filter(id=id).delete()
            return redirect("admin")
        elif request.POST.get('_deletedenied'):
            return redirect("admin")
        else:
            context["error"]="Sistemsel bir arıza yaşandı. Lütfen tekrar deneyiniz."
            return render(request, 'admin/storages.html',context)
    else:
        return redirect("shop")

def admin_processors(request,id):
    context={}
    if request.user.is_superuser and request.method == "GET":
        context['processor'] = Processor.objects.get(id=id)
        return render(request, 'admin/processors.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('_save'):
            processor_type = request.POST.get('processor_type')
            if Processor.objects.filter(type=processor_type).exists() and Processor.objects.filter(id=id).exists():
                context["success"]=f"{processor_type} değişiklik olmadığı halde güncellenmiştir."
                processor = Processor.objects.filter(id=id)
                processor.update(type=processor_type)
                return render(request, 'admin/processors.html',context)
            else:
                processor = Processor.objects.filter(id=id)
                processor.update(type=processor_type)
                product = Product.objects.filter(processor__id=id).update(is_updated=True,processor_id=id)
                context["success"]=f"{processor_type} başarıyla güncellendi."
                return render(request, 'admin/processors.html',context)
        elif request.POST.get('_delete'):
            context['processor_type'] = Processor.objects.get(id=id).type
            context["effectedproducts"]= Product.objects.filter(processor_id=id)
            return render(request, 'admin/processors.html',context)
        elif request.POST.get('_deleteconfirmed'):
            processor = Processor.objects.filter(id=id).delete()
            return redirect("admin")
        elif request.POST.get('_deletedenied'):
            return redirect("admin")
        else:
            context["error"]="Sistemsel bir arıza yaşandı. Lütfen tekrar deneyiniz."
            return render(request, 'admin/processors.html',context)
    else:
        return redirect("shop")

def admin_systems(request,id):
    context={}
    if request.user.is_superuser and request.method == "GET":
        context['system'] = System.objects.get(id=id)
        return render(request, 'admin/systems.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('_save'):
            system_type = request.POST.get('system_type')
            if System.objects.filter(type=system_type).exists() and System.objects.filter(id=id).exists():
                context["success"]=f"{system_type} değişiklik olmadığı halde güncellenmiştir."
                system = System.objects.filter(id=id)
                system.update(type=system_type)
                return render(request, 'admin/systems.html',context)
            else:
                system = System.objects.filter(id=id)
                system.update(type=system_type)
                product = Product.objects.filter(system__id=id).update(is_updated=True, system_id=id)
                context["success"]=f"{system_type} başarıyla güncellendi."
                return render(request, 'admin/systems.html',context)
        elif request.POST.get('_delete'):
            context['system_type'] = System.objects.get(id=id).type
            context["effectedproducts"]=Product.objects.filter(system_id=id)
            return render(request, 'admin/systems.html',context)
        elif request.POST.get('_deleteconfirmed'):
            system = System.objects.filter(id=id).delete()
            return redirect("admin")
        elif request.POST.get('_deletedenied'):
            return redirect("admin")
        else:
            context["error"]="Sistemsel bir arıza yaşandı. Lütfen tekrar deneyiniz."
            return render(request, 'admin/systems.html',context)
    else:
        return redirect("shop")

def admin_screens(request,id):
    context={}
    if request.user.is_superuser and request.method == "GET":
        context['screen'] = Screen.objects.get(id=id)
        return render(request, 'admin/screens.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('_save'):
            screen_type = request.POST.get('screen_type')
            if Screen.objects.filter(type=screen_type).exists() and Screen.objects.filter(id=id).exists():
                context["success"]=f"{screen_type} değişiklik olmadığı halde güncellenmiştir."
                screen = Screen.objects.filter(id=id)
                screen.update(type=screen_type)
                return render(request, 'admin/screens.html',context)
            else:
                screen = Screen.objects.filter(id=id)
                screen.update(type=screen_type)
                product = Product.objects.filter(screen__id=id).update(is_updated=True,screen_id=id)
                context["success"]=f"{screen_type} başarıyla güncellendi."
                return render(request, 'admin/screens.html',context)
        elif request.POST.get('_delete'):
            context['screen_type'] = Screen.objects.get(id=id).type
            context["effectedproducts"]=Product.objects.filter(screen_id=id)
            return render(request, 'admin/screens.html',context)
        elif request.POST.get('_deleteconfirmed'):
            screen = Screen.objects.filter(id=id).delete()
            return redirect("admin")
        elif request.POST.get('_deletedenied'):
            return redirect("admin")
        else:
            context["error"]="Sistemsel bir arıza yaşandı. Lütfen tekrar deneyiniz."
            return render(request, 'admin/screens.html',context)
    else:
        return redirect("shop")

################################################# CREATE STUFF #############################################
def admin_product_add(request):
    context={}
    if request.user.is_superuser and request.method == "GET":
        context['products'] = Product.objects.all()
        context['rams'] = Ram.objects.all()
        context['storages'] = Storage.objects.all()
        context['processors'] = Processor.objects.all()
        context['systems'] = System.objects.all()
        context['screens'] = Screen.objects.all()
        context['brands'] = Brand.objects.all()
        return render(request, 'admin/proedit.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('save_product'):
            product_screen = request.POST.get('product_screen')
            product_system = request.POST.get('product_system')
            product_processor = request.POST.get('product_processor')
            product_storage = request.POST.get('product_storage')
            product_ram = request.POST.get('product_ram')
            product_brand = request.POST.get('product_brand')
            product_image = request.FILES.get('product_image')
            product_price = request.POST.get('product_price')
            product_rate = request.POST.get('product_rate')
            if Product.objects.filter(screen=product_screen,system=product_system,processor=product_processor,storage=product_storage,ram=product_ram,name=product_brand).exists():
                context["error"]="Ürünümüz sistemde mevcuttur. Ürün fotoğrafını, fiyatını ya da oranını güncellemeyi deneyiniz."
                return render(request, 'admin/proedit.html',context)
            else:
                product=Product.objects.create(screen=Screen.objects.get(id=product_screen),system=System.objects.get(id=product_system),processor=Processor.objects.get(id=product_processor),storage=Storage.objects.get(id=product_storage),ram=Ram.objects.get(id=product_ram),name=Brand.objects.get(id=product_brand),image=product_image,price=product_price,rate=product_rate)
                context["success"]="Ürün başarıyla eklendi."
                return render(request, 'admin/proedit.html',context)
        else:
            context['products'] = Product.objects.all()
            context['rams'] = Ram.objects.all()
            context['storages'] = Storage.objects.all()
            context['processors'] = Processor.objects.all()
            context['systems'] = System.objects.all()
            context['screens'] = Screen.objects.all()
            context['brands'] = Brand.objects.all()
            context["error"]="Ürün eklenemedi. Lütfen tekrar deneyiniz."
            return render(request, 'admin/proedit.html',context)
    else:
        return redirect("shop")

def admin_brand_add(request):
    context={}
    if request.user.is_superuser and request.method == "GET":
        return render(request, 'admin/bredit.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('save_brand'):
            brand_name = request.POST.get('brand_name').upper()
            brand_model = request.POST.get('brand_model').upper()
            if Brand.objects.filter(name=brand_name,model=brand_model).exists():
                context["error"]=f"{brand_name} ve {brand_model} sistemde mevcuttur. Güncellemeyi deneyiniz."
                context["brand_name"]=brand_name
                context["brand_model"]=brand_model
                return render(request, 'admin/bredit.html',context)
            else:
                brand = Brand.objects.create(name=brand_name,model=brand_model)
                context["success"]=f"{brand_name} ve {brand_model} başarıyla eklendi."
                return render(request, 'admin/bredit.html',context)
        else:
            context["error"]="Marka ve model eklenemedi. Lütfen tekrar deneyiniz."
            return render(request, 'admin/bredit.html',context)
    else:
        return redirect("shop")

def admin_ram_add(request):
    context={}
    if request.user.is_superuser and request.method == "GET":
        return render(request, 'admin/ramedit.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('save_ram'):
            ram_type = request.POST.get('ram_type').upper()
            if Ram.objects.filter(type=ram_type).exists():
                context["error"]=f"{ram_type} sistemde mevcuttur. Güncellemeyi deneyiniz."
                context["ram_type"]=ram_type
                return render(request, 'admin/ramedit.html',context)
            else:
                ram = Ram.objects.create(type=ram_type)
                context["success"]=f"{ram_type} başarıyla eklendi."
                return render(request, 'admin/ramedit.html',context)
        else:
            context["error"]="Ram tipi eklenemedi. Lütfen tekrar deneyiniz."
            return render(request, 'admin/ramedit.html',context)
    else:
        return redirect("shop")

def admin_storage_add(request):
    context={}
    if request.user.is_superuser and request.method == "GET":
        return render(request, 'admin/stedit.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('save_storage'):
            storage_type = request.POST.get('storage_type').upper()
            if Storage.objects.filter(type=storage_type).exists():
                context["error"]=f"{storage_type} sistemde mevcuttur. Güncellemeyi deneyiniz."
                context["storage_type"]=storage_type
                return render(request, 'admin/stedit.html',context)
            else:
                storage = Storage.objects.create(type=storage_type)
                context["success"]=f"{storage_type}  başarıyla eklendi."
                return render(request, 'admin/stedit.html',context)
        else:
            context["error"]="Depolama alanı eklenemedi. Lütfen tekrar deneyiniz."
            return render(request, 'admin/stedit.html',context)
    else:
        return redirect("shop")

def admin_processor_add(request):
    context={}
    if request.user.is_superuser and request.method == "GET":
        return render(request, 'admin/predit.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('save_processor'):
            processor_type = request.POST.get('processor_type').upper()
            if Processor.objects.filter(type=processor_type).exists():
                context["error"]=f"{processor_type} sistemde mevcuttur. Güncellemeyi deneyiniz."
                context["processor_type"]=processor_type
                return render(request, 'admin/predit.html',context)
            else:
                processor = Processor.objects.create(type=processor_type)
                context["success"]=f"{processor_type} başarıyla eklendi."
                return render(request, 'admin/predit.html',context)
        else:
            context["error"]="İşlemci tipi eklenemedi. Lütfen tekrar deneyiniz."
            return render(request, 'admin/predit.html',context)
    else:
        return redirect("shop")

def admin_system_add(request):
    context={}
    if request.user.is_superuser and request.method == "GET":
        return render(request, 'admin/syedit.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('save_system'):
            system_type = request.POST.get('system_type').upper()
            if System.objects.filter(type=system_type).exists():
                context["error"]=f"{system_type} sistemde mevcuttur. Güncellemeyi deneyiniz."
                context["system_type"]=system_type
                return render(request, 'admin/syedit.html',context)
            else:
                system = System.objects.create(type=system_type)
                context["success"]=f"{system_type} başarıyla eklendi."
                return render(request, 'admin/syedit.html',context)
        else:
            context["error"]="İşletim sistemi eklenemedi. Lütfen tekrar deneyiniz."
            return render(request, 'admin/syedit.html',context)
    else:
        return redirect("shop")

def admin_screen_add(request):
    context={}
    if request.user.is_superuser and request.method == "GET":
        return render(request, 'admin/scedit.html',context)
    elif request.user.is_superuser and request.method == "POST":
        if request.POST.get('save_screen'):
            screen_type = request.POST.get('screen_type').upper()
            if Screen.objects.filter(type=screen_type).exists():
                context["error"]=f"{screen_type} sistemde mevcuttur. Güncellemeyi deneyiniz."
                context["screen_type"]=screen_type
                return render(request, 'admin/scedit.html',context)
            else:
                screen = Screen.objects.create(type=screen_type)
                context["success"]=f"{screen_type} başarıyla eklendi."
                return render(request, 'admin/scedit.html',context)
        else:
            context["error"]="Ekran tipi eklenemedi. Lütfen tekrar deneyiniz."
            return render(request, 'admin/scedit.html',context)
    else:
        return redirect("shop")