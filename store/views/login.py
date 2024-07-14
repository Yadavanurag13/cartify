from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import  View
from store.forms import CustomerProfileForm


class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'login.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')

@login_required
def view_profile(request):
    customer = Customer.objects.get(email=request.user.email)
    return render(request, 'view_profile.html', {'customer': customer})

@login_required
def edit_profile(request):
    customer = Customer.objects.get(email=request.user.email)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = CustomerProfileForm(instance=customer)
    return render(request, 'edit_profile.html', {'form': form})