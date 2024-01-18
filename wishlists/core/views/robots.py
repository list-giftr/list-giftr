from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def robots_txt(request: HttpRequest) -> HttpResponse:
    return render(request, "core/robots.txt", {}, content_type="text/plain")
