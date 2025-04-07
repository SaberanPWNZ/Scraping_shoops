from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Max, Q
from rest_framework import status
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView

from checker.models import Partner, PartnerItem
from items.models import Item, Brand
from users.forms import UserRegistrationForm, UserChangeProfile
from django import template

register = template.Library()


@login_required(login_url='/users/login/')
def index(request):
    partners = Partner.objects.all()
    return render(request, 'index.html', {'partners': partners})


def dashboard_view(request):
    items = Item.objects.all()
    partners = Partner.objects.all()

    comparison_data = {}
    for item in items:
        partner_prices = PartnerItem.objects.filter(article=item.article)
        prices = {partner_item.partner.id: partner_item.price for partner_item in partner_prices}
        comparison_data[item.article] = prices

    context = {
        'items': items,
        'partners': partners,
        'comparison_data': comparison_data,
    }
    return render(request, 'dashboard.html', context)


def partners(request):
    partners = Partner.objects.all()
    return render(request, 'partners.html', {'partners': partners})


@user_passes_test(lambda u: u.is_staff)
@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()

                user = authenticate(email=user.email, password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Реєстрація пройшла успішно.')
                    return redirect('index')
                else:
                    messages.error(request, 'Помилка автентифікації. Спробуйте ще раз.')
                    return redirect('signup')
            except Exception as e:
                messages.error(request, f'Помилка реєстрації: {e}')
                return redirect('signup')
        else:
            messages.error(request, 'Помилка реєстрації. Перевірте введені дані.')
    else:
        form = UserRegistrationForm()

    return render(request, 'user_register.html', {'form': form})


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserChangeProfile(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Дані успішно збережені.')
            return redirect('profile')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = UserChangeProfile(instance=request.user)

    return render(request, 'profile_edit.html', {'form': form})


def partner_detail(request, slug):
    partner = get_object_or_404(Partner, slug=slug)

    partner_items = PartnerItem.objects.filter(partner=partner)

    last_prices = {}

    for partner_item in partner_items:
        scraped_item_article = partner_item.article
        matching_item = Item.objects.filter(article=scraped_item_article).first()

        if scraped_item_article not in last_prices or last_prices[scraped_item_article][
            'date'] < partner_item.last_updated:
            last_prices[scraped_item_article] = {
                'scraped_item': partner_item,
                'price': partner_item.price,
                'date': partner_item.last_updated,
                'matching_item': matching_item,
            }

    comparison_data = list(last_prices.values())

    last_updated = partner_items.aggregate(max_date=Max('last_updated'))['max_date']

    return render(request, 'partner_detail.html', {
        'partner': partner,
        'comparison_data': comparison_data,
        'last_updated': last_updated,
    })

