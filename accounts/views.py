from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("portal:home")
    return render(request, "accounts/register.html", {"form": form})