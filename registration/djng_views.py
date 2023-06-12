from django.http import HttpResponseBadRequest
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.utils import IntegrityError
from django.views.decorators.http import require_http_methods
from knox.models import AuthToken

from registration.business_logic import final_send_mail, final_creation
from registration.forms import RegistrationTryForm, RegisterConfirmForm, password_validation
from registration.models import RegistrationTry, WebMenuUser

from django.shortcuts import render


class DjangoRegisterTryView(CreateView):
    template_name = 'enter_email.html'
    model = RegistrationTry
    fields = ['email']
    success_url = reverse_lazy('djangoform')

    def post(self, request, *args, **kwargs):
        reg_try = RegistrationTry(email=request.POST.get('email'))  # don't save to db
        final_send_mail(reg_try)
        messages.success(request, "The Email was send successfully.")
        return super().post(request, *args, **kwargs)


@require_http_methods(["GET", "POST"])
def django_register_try_function(request):
    form = RegistrationTryForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            try:
                reg_try = RegistrationTry.objects.create(email=form.data['email'])
            except IntegrityError:
                return HttpResponseBadRequest('BadRequest')
            final_send_mail(reg_try)
            messages.success(request, 'The Email was send successfully.')
            return render(request, 'enter_email.html', status=201)
    return render(request, 'enter_email.html', {"form": form})


@require_http_methods(["GET", "POST"])
def django_register_confirm_function(request, code):
    try:
        reg_try = RegistrationTry.objects.get(code=code)
    except RegistrationTry.DoesNotExist:
        return HttpResponseBadRequest('BadRequest')
    form = RegisterConfirmForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            if password_validation(form.data):
                try:
                    final_creation(form.data, reg_try)
                except IntegrityError:
                    return HttpResponseBadRequest('Check the entered data for uniqueness')
                user = WebMenuUser.objects.get(email=reg_try.email)
                token = AuthToken.objects.create(user)[1]
                messages.success(request, 'You create user successful.\n'
                                          f'Token {token}')
                return render(request, 'registration_data.html', status=201)
            else:
                messages.error(request, 'Password fields didn\'t match.')
    return render(request, 'registration_data.html', {"form": form})
