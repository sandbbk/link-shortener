from django.shortcuts import (redirect, render, get_object_or_404)
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.forms import AuthenticationForm
from .forms import User_Creation_Form
import hashlib
from django.http import Http404
from django.http import JsonResponse
from short.extentions import (send_mail, encode_index, num)
from datetime import timedelta
from .models import (Key, Link, NativeLink)
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from short.exceptions import (RequestMethodError, UserAuthError)
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)
from django.contrib.sites.shortcuts import get_current_site


def main(request):
    context = {'user': request.user}
    return render(request, 'short/main.html', context)


def auth_login(request):
    data = request.POST
    username = data['username']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
    return user


def signin(request):
    msg = None
    if request.method == 'POST':
        user = auth_login(request)
        if user:
            return redirect('main')
        msg = "Invalid username or password"
    form = AuthenticationForm()
    return render(request, 'short/login.html', {'form': form, 'msg': msg})


def signout(request):
    logout(request)
    return redirect('main')


def check_user_exists(user):
    try:
        User.objects.get(email=user.email)
        return f'User with email "{user.email}" already exists!'
    except ObjectDoesNotExist:
        return False


@transaction.atomic
def signup(request):
    msg = None
    if request.method == "GET":
        form = User_Creation_Form()
        return render(request, 'short/register.html', {'form': form})
    else:
        form = User_Creation_Form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            msg = check_user_exists(user)
            if msg:
                return render(request, 'short/register.html', {'form': form, 'msg': msg})
            user.save()
            key = (hashlib.sha256(user.email.encode('utf-8'))).hexdigest()
            key = Key.objects.create(user=user, data=key, expire_time=(timezone.now() + timedelta(hours=3)))
            subject = 'Activation of account on sandbbk.pythonanywhere.com'
            protocol = 'https' if request.is_secure() else 'http'
            data = f'{protocol}://{get_current_site(request)}/activate/{key.data}'
            send_mail(user.email, subject, 'short/activate.html', data)
            msg = 'We just sent an email to Your mailbox. For finishing the registration, please follow it.'
            return render(request, 'short/message.html', {'msg': msg})
        msg = "Invalid form!"
        return render(request, 'short/register.html', {'form': form, 'msg': msg})


def activate(request, link):
    try:
        if request.method != 'GET':
            raise RequestMethodError('Invalid request method')
        key = Key.objects.get(data=link)
        if key.expire_time <= timezone.now():
            key.user.delete()
            raise UserAuthError('Time for activation expired!')
        key.user.is_active = True
        key.user.save()
        key.delete()
    except (UserAuthError, RequestMethodError) as e:
        return render(request, 'short/message.html', {'msg': e.message})
    return redirect('signin')


def process(request):
    if request.method == "POST" and request.is_ajax():
        user = request.user
        user = None if user.is_anonymous else user
        link = request.POST['link']
        if not link.startswith(('http://', 'https://')):
            return JsonResponse({'response': 'Link is not valid!', 'result': 'success'})
        native, created = NativeLink.objects.get_or_create(nativelink=link)
        x = True
        while x:
            short_link = encode_index(num(link))
            try:
                Link.objects.get(short_link=short_link)
            except ObjectDoesNotExist:
                x = False
        Link.objects.create(short_link=short_link, nativelink=native, user=user)
        protocol = 'https' if request.is_secure() else 'http'
        temp = f'{protocol}://{get_current_site(request)}/{short_link}'
        return JsonResponse({'response': temp, 'result': 'success'})
    return JsonResponse({'response': 'Invalid request method!', 'result': 'error'})


def follow(request, link):
    try:
        link = Link.objects.select_related('nativelink').get(short_link=link)
        link.follow += 1
        link.save()
        return redirect(link.nativelink.nativelink)
    except ObjectDoesNotExist:
        raise Http404("Not found")


def p_range(pages, num_page):   # returns  convenient list of page-numbers;
    p_set = {1, pages.num_pages}
    try:
        num_page = int(num_page)
    except (ValueError, TypeError):
        num_page = 1
    base_set = set(pages.page_range)
    p_set.update(range(num_page - 5, num_page + 6))
    p_set.update(range(0, pages.num_pages, 50))
    p_set.intersection_update(base_set)
    return sorted(list(p_set))


def stat(request):
    user = request.user
    if user.is_anonymous:
        return render(request, 'short/message.html', {'msg': 'Please, sign in!'})
    links = Link.objects.all().select_related('nativelink').order_by('short_link')
    pages = Paginator(links, 30)
    num_page = request.GET.get('page')
    try:
        page_content = pages.page(num_page)
    except PageNotAnInteger:
        page_content = pages.page(1)
    except EmptyPage:
        page_content = pages.page(pages.num_pages)
    p_list = p_range(pages, num_page)
    return render(request, 'short/stat.html', {'links': page_content, 'p_list': p_list})
