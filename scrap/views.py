from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django_filters import FilterSet
from .models import Product, SitesInformation

############################################## FILTER PAGES ################################################
class ListingFilter(FilterSet):

    class Meta:
        model = Product 
        fields = {
            'name__name':['exact'],
            'ram': ['exact'],
            'storage': ['exact'],
            'processor': ['exact'],
            'system': ['exact'],
            'screen': ['exact']
        }


class ListingFilter2(FilterSet):

    class Meta:
        model = SitesInformation 
        ordering = ('price','rate')
        fields = {
            'rate': ['exact'],
            'price': ['exact'],
        }
        
############################################### GENERAL PAGES ##############################################
def scrapproducts(request):
    context={}
    listing_filter = ListingFilter(request.GET, queryset=Product.objects.all())
    context['filtered_products'] = listing_filter
    paginated_filtered_products = Paginator(listing_filter.qs, 24)
    pagenumber=request.GET.get('page')
    products = paginated_filtered_products.get_page(pagenumber)
    context['products'] = products
    context['pnum'] = products.number - 1
    context['nums'] = products.number
    context['nnum'] = products.number + 1
    return render(request, 'scrap/index.html',context)

def scrapsearch_products(request):
    if request.method == "POST":
        context={}
        searched = request.POST['searched']
        context['products']  = Product.objects.filter(Q(name__name__icontains=searched) | Q(name__model__icontains=searched) | Q(ram__type__icontains=searched) | Q(storage__type__icontains=searched) | Q(processor__type__icontains=searched) | Q(system__type__icontains=searched) | Q(screen__type__icontains=searched))
        context['sitenames']  = SitesInformation.objects.filter(Q(sitename__icontains=searched))
        context["searched"] = searched
        return render(request, 'scrap/search.html', context)
    else:
        return render(request, 'scrap/search.html', {})

def scrapproduct_details(request, slug):
    a = Product.objects.get(slug=slug)
    context={}
    po = ListingFilter2(request.GET, queryset=SitesInformation.objects.filter(whichproduct_id=a.id).order_by(request.GET.get('order','price'))[0:3])
    rpo = ListingFilter2(request.GET, queryset=SitesInformation.objects.filter(whichproduct_id=a.id).order_by(request.GET.get('order','-price'))[0:3])
    ro = ListingFilter2(request.GET, queryset=SitesInformation.objects.filter(whichproduct_id=a.id).order_by(request.GET.get('order','rate'))[0:3])
    rro = ListingFilter2(request.GET, queryset=SitesInformation.objects.filter(whichproduct_id=a.id).order_by(request.GET.get('order','-rate'))[0:3])
    if request.GET.get('order') == 'price':
        context['filtered_products'] = po
    elif request.GET.get('order') == '-price':
        context['filtered_products'] = rpo
    elif request.GET.get('order') == 'rate':
        context['filtered_products'] = ro
    elif request.GET.get('order') == '-rate':
        context['filtered_products'] = rro
    else:
        context['filtered_products'] = po
    context['products'] = a
    return render(request, "scrap/product-details.html",context)