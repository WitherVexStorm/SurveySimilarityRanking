from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ExtendedUserCreationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('list-surveys')
    else:
        form = ExtendedUserCreationForm()

    return render(request, 'users/register.html', { 'form': form })