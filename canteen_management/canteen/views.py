from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Sum
from .models import FoodCategory, FoodItem, Order, OrderItem
from .forms import UserRegisterForm, OrderForm, FoodItemForm


def home(request):
    return render(request, 'home.html')


def menu(request):
    categories = FoodCategory.objects.all()
    context = {
        'categories': categories,
        'college_name': 'Asian School of Management and Technology'
    }
    return render(request, 'menu.html', context)


@login_required
def place_order(request, item_id):
    food_item = get_object_or_404(FoodItem, id=item_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_price=food_item.price * int(request.POST.get('quantity', 1)),
                special_instructions=form.cleaned_data['special_instructions']
            )

            # Create order item with quantity
            OrderItem.objects.create(
                order=order,
                food_item=food_item,
                quantity=int(request.POST.get('quantity', 1)),
                price=food_item.price
            )

            messages.success(request, 'Order placed successfully!')
            return redirect('order_success', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'order.html', {
        'food_item': food_item,
        'form': form
    })

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

@staff_member_required
def dashboard(request):
    orders = Order.objects.all().order_by('-created_at')
    total_orders = orders.count()
    total_revenue = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    popular_items = FoodItem.objects.annotate(
        total_ordered=Sum('orderitem__quantity')
    ).order_by('-total_ordered')[:5]

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'popular_items': popular_items
    }
    return render(request, 'dashboard.html', context)


@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, 'Order status updated successfully!')
    return redirect('dashboard')


@staff_member_required
def manage_menu(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food item added successfully!')
            return redirect('manage_menu')
    else:
        form = FoodItemForm()

    food_items = FoodItem.objects.all()
    context = {
        'form': form,
        'food_items': food_items
    }
    return render(request, 'manage_menu.html', context)



def payment_options(request):
    return render(request, 'payment_options.html')