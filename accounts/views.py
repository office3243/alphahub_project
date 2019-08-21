from django.shortcuts import render, redirect
from .forms import RegisterForm


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("portal:home")
    return render(request, "accounts/register.html", {"form": form})