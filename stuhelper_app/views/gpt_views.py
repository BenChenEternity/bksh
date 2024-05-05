import random

import django
import requests
from blueapps.account.decorators import login_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

import settings
from stuhelper_app.models import CustomUser


def gpt_page(request):
    return render(request, 'gpt_page.html')
