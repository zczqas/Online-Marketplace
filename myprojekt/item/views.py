import stripe

from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .models import Category, Item
from .forms import AccountForm, NewItemForm, EditItemForm

stripe.api_key = settings.STRIPE_SECRET_KEY

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

def thanks(request):
    return render(request, 'item/thanks.html')

@login_required
def account(request):
    item_id = request.GET.get('item_id')
    if not item_id:
        messages.error(request, 'Item not found')
        return redirect('item:items')
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        messages.error(request, 'Item not found')
        return redirect('item:account')

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            stripeToken = request.POST['stripeToken']
            payment_intent = stripe.PaymentIntent.create(
                amount=int(item.price * 100),
                currency='usd',
                payment_method_types=['card'],
                description='Example charge',
                confirm=True,
                payment_method_data={
                    'type': 'card',
                    'card': {'token': stripeToken},
                },
            )
            print(f"hello {payment_intent.status}")
            if payment_intent.status == 'succeeded' or payment_intent.status == 'requires_action':
                item.is_sold = True
                item.save()
                return render(request, 'item/thanks.html')
    else:
        form = AccountForm(instance=request.user)
    context = {
        'form': form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'item/account_form.html', context)
