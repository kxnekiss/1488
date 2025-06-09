from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import LoginForm, ChangePasswordForm
from .models import User


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = ''
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        try:
            user_obj = User.objects.get(username=username)
            if not user_obj.is_active:
                msg = 'Вы заблокированы. Обратитесь к администратору.'
            elif user_obj.last_login and (timezone.now() - user_obj.last_login).days > 30:
                user_obj.is_active = False
                user_obj.save()
                msg = 'Вы заблокированы. Обратитесь к администратору.'
            else:
                user = authenticate(username=username, password=password)
                if user:
                    user.failed_attempts = 0
                    user.last_login = timezone.now()
                    user.save()
                    login(request, user)
                    if user.first_login:
                        user.first_login = False
                        user.save()
                        return redirect('change_password')
                    msg = 'Вы успешно авторизовались'
                else:
                    user_obj.failed_attempts += 1
                    if user_obj.failed_attempts >= 3:
                        user_obj.is_active = False
                    user_obj.save()
                    msg = 'Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз.'
        except User.DoesNotExist:
            msg = 'Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз.'
    return render(request, 'core/login.html', {'form': form, 'msg': msg})


@login_required
def change_password(request):
    form = ChangePasswordForm(request.POST or None)
    msg = ''
    if request.method == 'POST' and form.is_valid():
        current = form.cleaned_data['current_password']
        new = form.cleaned_data['new_password']
        confirm = form.cleaned_data['confirm_password']
        if not request.user.check_password(current):
            msg = 'Текущий пароль введён неверно.'
        elif new != confirm:
            msg = 'Новый пароль и подтверждение несовпадают'
        else:
            request.user.set_password(new)
            request.user.save()
            msg = 'Пароль успешно изменён.'
    return render(request, 'core/change_password.html', {'form': form, 'msg': msg})
