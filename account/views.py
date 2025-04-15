from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import login ,authenticate,logout
from django.views.generic import TemplateView,ListView,DetailView,CreateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import RegisterForm
from django.urls import reverse_lazy

def login_user (request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/")

    return render(request,"account/login_form.html",{})


def logout_user(request):
    logout(request)
    return redirect("/")


def RegisterUserView(request):
    context ={'error':[]}
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        if password1 != password2:
            context['error'].append('password are not same')
            return render(request, "account/register_form.html",context)


        user = User.objects.create_user(username=username,password=password1,email=email)
        login(request,user)
        return redirect('profile/create')

    return render(request,"account/register_form.html",{})



class ProfileUserCreateView (LoginRequiredMixin,CreateView):
    model = Profile
    fields = ["biography","Profile_photo"]
    success_url = "/"
    template_name = "account/profile_form.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if Profile.objects.filter(user=self.request.user).exists():
            return redirect("/")  # به صفحه پروفایل هدایت شود
        return super().dispatch(request, *args, **kwargs)


class ProfileUserDetailView(LoginRequiredMixin,DetailView):
    model = Profile
    pk_url_kwarg = "id"
    template_name = "account/profile_detail.html"
