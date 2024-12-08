from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
from django.views.generic import TemplateView

from checker.models import ScrapedData, Partner, ScrapedItem
from django.shortcuts import render, get_object_or_404, redirect

from items.models import Item, Brand
from users.forms import UserRegistrationForm


def index(request):
    partners = Partner.objects.all()
    return render(request, 'index.html', {'partners': partners})


def about(request):
    return render(request, 'about.html')


def partners(request):
    return render(request, 'partners.html')


def contact(request):
    return render(request, 'contact.html')


@login_required
def profile_view(request):
    return render(request, 'profile.html')



def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user = authenticate(username=user.username, password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                messages.success(request, 'Реєстрація пройшла успішно')
                return redirect('home')
            else:
                messages.error(request, 'Помилка аутентифікації. Спробуйте ще раз.')
                return redirect('register')
        else:
            messages.error(request, 'Помилка реєстрації. Перевірте введені дані.')
    else:
        form = UserRegistrationForm()

    return render(request, 'user_register.html', {'form': form})



@login_required
def profile_edit_view(request):
    # Логика для редактирования профиля
    return render(request, 'profile_edit.html')


def partner_detail(request, slug):
    partner = get_object_or_404(Partner, slug=slug)
    scraped_data = partner.scraped_data.prefetch_related('items__brand')
    print(f'{request.user.is_authenticated}')

    freshest_data = []
    brands_to_include = Brand.objects.all()

    for brand in brands_to_include:
        latest_entry = scraped_data.filter(items__brand=brand).order_by('-created_at').first()
        if latest_entry:
            freshest_data.append(latest_entry)

    comparison_data = []
    for data in freshest_data:
        for scraped_item in data.items.filter(brand__in=brands_to_include):
            try:
                matching_item = Item.objects.get(article=scraped_item.article)
            except Item.DoesNotExist:
                matching_item = None

            comparison_data.append({
                'scraped_item': scraped_item,
                'matching_item': matching_item,
            })

    return render(request, 'partner_detail.html', {
        'partner': partner,
        'comparison_data': comparison_data,
        'last_updated': max([data.last_update for data in freshest_data], default=None),
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
