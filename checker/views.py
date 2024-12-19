from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test

from django.utils.timezone import localtime
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect

from checker.models import Partner, ScrapedItem, ScrapedData
from items.models import Item, Brand
from users.forms import UserRegistrationForm, UserChangeProfile
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, "N/A")


@login_required(login_url='/users/login/')
def index(request):
    partners = Partner.objects.all()
    return render(request, 'index.html', {'partners': partners})



def dashboard_view(request):

    items_from_db = Item.objects.all()
    partners = Partner.objects.all()
    scraped_data = ScrapedData.objects.prefetch_related('items')

    comparison_data = {}
    for item in items_from_db:
        partner_prices = {}
        for partner in partners:
            partner_data = scraped_data.filter(partner=partner).first()
            if partner_data:
                # Поиск ScrapedItem по артикулу
                scraped_item = partner_data.items.filter(article=item.article).first()
                partner_prices[partner.name] = scraped_item.price if scraped_item else None
            else:
                partner_prices[partner.name] = None
        comparison_data[item.article] = partner_prices

    context = {
        'partners': partners,
        'comparison_data': comparison_data,
        'items_from_db': items_from_db,
    }
    return render(request, 'dashboard.html', context)



def partners(request):
    partners = Partner.objects.all()
    return render(request, 'partners.html', {'partners':partners})


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


@login_required
def partner_detail(request, slug):
    partner = get_object_or_404(Partner, slug=slug)
    scraped_data = partner.scraped_data.prefetch_related('items__brand')
    brands_to_include = Brand.objects.all()

    freshest_data = [
        scraped_data.filter(items__brand=brand).order_by('-created_at').first()
        for brand in brands_to_include if scraped_data.filter(items__brand=brand).exists()
    ]

    comparison_data = []
    for data in freshest_data:
        for scraped_item in data.items.filter(brand__in=brands_to_include):
            matching_item = Item.objects.filter(article=scraped_item.article).first()
            comparison_data.append({
                'scraped_item': scraped_item,
                'matching_item': matching_item,
            })

    last_updated = max([data.last_update for data in freshest_data], default=None)

    # Отправляем данные в шаблон
    return render(request, 'partner_detail.html', {
        'partner': partner,
        'comparison_data': comparison_data,
        'last_updated': last_updated,
    })


class DataTableView(TemplateView):
    template_name = "data_table.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        partners_data = []
        for partner in Partner.objects.all():
            partner_data = {
                "partner": partner.name,
                "items": ScrapedData.objects.filter(partner=partner).order_by('-created_at').first()
            }
            partners_data.append(partner_data)
        context['data'] = partners_data
        context['is_summary'] = True
        return context


class PartnerTableView(TemplateView):
    template_name = "data_table.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        partner_slug = self.kwargs.get('slug')
        partner = get_object_or_404(Partner, slug=partner_slug)

        scraped_data = ScrapedData.objects.filter(partner=partner)
        last_updated = scraped_data.order_by('-last_update').first().last_update if scraped_data.exists() else None

        context['data'] = scraped_data
        context['partner'] = partner
        context['last_updated'] = localtime(last_updated) if last_updated else None
        return context
