from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse
from django.views import View 
from django.http import HttpResponseRedirect

# Create your views here. 
class HomePageView(TemplateView): 
    template_name = 'pages/home.html'

class AboutPageView(TemplateView): 
    template_name = 'pages/about.html' 
 
     
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "About us - Online Store", 
            "subtitle": "About us", 
            "description": "This is an about page ...", 
            "author": "Developed by: Your Name", 
        }) 
 
        return context 
    
class ContactPageView(TemplateView): 
    template_name = 'pages/contact.html' 
 
     
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "email": "gabriela@gmail.com", 
            "address": "cra 13 cl 35 #43-101", 
            "phone": "3188745287", 
        }) 
 
        return context 
    
 
class Product: 
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": 799.99},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 999.00},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 49.99},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 129.50}
    ]
 
class ProductIndexView(View): 
    template_name = 'products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.products 
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            # Try to convert ID to int and find the product
            product_id = int(id)
            product = Product.products[product_id - 1]
        except (ValueError, IndexError):
            # If the ID is not a number or out of range → redirect to home
            return HttpResponseRedirect(reverse('home'))

        # If product exists, render normally
        viewData = {
            "title": f"{product['name']} - Online Store",
            "subtitle": f"{product['name']} - Product information",
            "product": product,
        }
        return render(request, self.template_name, viewData)


from django import forms 
from django.shortcuts import render, redirect 
 
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            raise forms.ValidationError("Price is required.")
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price
 
 
class ProductCreateView(View): 
    template_name = 'products/create.html' 
 
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 
 

class ProductCreateView(View): 
    template_name = 'products/create.html' 
    success_template = 'products/success.html' 

    def get(self, request): 
        form = ProductForm() 
        viewData = { 
            "title": "Create product", 
            "form": form 
        } 
        return render(request, self.template_name, viewData) 

    def post(self, request): 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
            viewData = { 
                "title": "Product created", 
                "message": "Product created successfully!" 
            } 
            return render(request, self.success_template, viewData)
        else: 
            viewData = { 
                "title": "Create product", 
                "form": form 
            } 
            return render(request, self.template_name, viewData)
