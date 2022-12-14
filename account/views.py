from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from store.models import Order
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View


from django.contrib.auth import get_user_model
User = get_user_model()

def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)

    return render(request, 'account/vendor_detail.html', {
        'user': user
    })

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
            username=cd['username'],
            password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def landingPage(request):
    return render(request, "landingPage.html")

@login_required
def dashboard(request):
    # order = Order.objects.filter(user=request.user)
    order =  Order.objects.filter(user=request.user, ordered=True)
    context = {
        'profile' : Profile,
        'order': order
    }
    # print(request.user.profile)
    return render(request, 'account/dashboard.html', context)

class DashboardView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order =  Order.objects.filter(user=self.request.user, ordered=True)
        context = {
            'profile' : Profile,
            'order' : order
        }
        print(order)
        return render(self.request, 'test.html', context)
        

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password'])
            # Save the User object
            new_user.save() 
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
        data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',{'user_form': user_form, 
                    'profile_form': profile_form})        