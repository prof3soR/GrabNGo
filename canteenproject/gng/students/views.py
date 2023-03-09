from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views import View
from .forms import MenuItemForm
from .models import *
# Create your views here.
class menu(View):
    def get(self, request):
        query = request.GET.get('query')
        category = request.GET.get('category')
        items = MenuItem.objects.all()

        if category:
            items = items.filter(category__name=category)

        if query:
            items = items.filter(name__icontains=query)

        categories = Category.objects.all()

        return render(request, 'menu.html', {'items': items, 'categories': categories, 'category': category, 'query': query})



class add_menu_item(View):
    def get(self, request):
        form = MenuItemForm()
        return render(request, 'add_menu_item.html', {'form': form})

    def post(self, request):
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu')
        else:
            form = MenuItemForm()
        return render(request, 'add_menu_item.html', {'form': form})

        
class index(View):
    def get(self,request):
        return render(request,'index.html')
    





from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User

def register(request):
    if request.method == 'POST':
        # Get form data from POST request
        username = request.POST.get('username')
        registration_number = request.POST.get('registration_number')
        password = request.POST.get('password')
        mobile_number = request.POST.get('mobile_number')

        # Check if user with same registration number already exists
        if User.objects.filter(registration_number=registration_number).exists():
            messages.error(request, 'User with this registration number already exists')
            return redirect('login')

        # Create new user object and save to database
        user = User.objects.create_user(username=username, registration_number=registration_number, password=password, mobile_number=mobile_number)
        user.is_active = False
        user.save()

        # Send confirmation email to activate account (implementation not shown)
        # ...

        messages.success(request, 'Registration successful. Please check your email to activate your account.')
        return redirect('login')
    else:
        return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        # Get form data from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user based on username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if user account is active
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Your account is not active. Please check your email to activate your account.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


class login(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        if request.method == 'POST':
            registration_number = request.POST.get('registration_number')
            password = request.POST.get('password')
            User = authenticate(request, registration_number=registration_number, password=password)
            if User is not None:
                login(request, User)
                return redirect('menu')
            else:
                return redirect('signup')
        return render(request, 'signup')
        




class signup(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        if request.method == 'POST':
            # Get form data from POST request
            username = request.POST.get('username')
            registration_number = request.POST.get('registration_number')
            password = request.POST.get('password')
            mobile_number = request.POST.get('mobile_number')

            # Check if user with same registration number already exists
            if User.objects.filter(registration_number=registration_number).exists():
                messages.error(request, 'User with this registration number already exists')
                return redirect('login')

            # Create new user object and save to database
            user = User.objects.create_user(username=username, registration_number=registration_number, password=password, mobile_number=mobile_number)
            user.is_active = False
            user.save()

            # Send confirmation email to activate account (implementation not shown)
            # ...

            messages.success(request, 'Registration successful. Please check your email to activate your account.')
            return redirect('login')
        else:
            return render(request, 'signup')
class cart(View):
    def get(self,request):
        return render(request,"cart.html")
from django.shortcuts import render
from .models import MenuItem

def menu_item_update(request):
    if request.method == 'POST':
        # Handle form submission
        for item_id, data in request.POST.items():
            if item_id.startswith('item-'):
                item_id = item_id.replace('item-', '')
                try:
                    item = MenuItem.objects.get(pk=item_id)
                    item.available_plates = int(data)
                    item.price = float(request.POST.get(f'price-{item_id}'))
                    item.description = request.POST.get(f'description-{item_id}')
                    item.save()
                except MenuItem.DoesNotExist:
                    pass
    menu_items = MenuItem.objects.all()
    context = {
        'menu_items': menu_items,
    }
    return render(request, 'menu_item_update.html', context)
