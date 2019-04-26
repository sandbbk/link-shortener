from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random


def send_mail(to_email, subject, template, context):
    from_email = 'djangoandrest@gmail.com'
    html_content = render_to_string(template, {'context': context})
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def num(link):
    ha = hash(link)
    if ha < 0:
        ha = ha * -1
    return ha // random.randrange(1, 99999)

BASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"


def encode_index(num, alph_set=BASE):
    if num == 0:
        return alph_set[0]
    list_ = []
    base = len(alph_set)
    while num:
        sta = num % base
        num = num // base
        list_.append(alph_set[sta])
    return ''.join(list_)
