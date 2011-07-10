from utils.decorators import render_to
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

@render_to('accounts/create.html')
def create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'Account created success!')
            return redirect('accounts:login')
        messages.error(request, u'Please correct the error below.')
    else:
        form = UserCreationForm()
    return {
        'form': form
    }