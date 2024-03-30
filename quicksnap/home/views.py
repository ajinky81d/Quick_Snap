from django.shortcuts import render
from .models import Data
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from django.views.generic import DeleteView
from django.contrib.auth.models import User
from quicksnap.settings import EMAIL_HOST_USER,EMAIL_ADMIN
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.mail import send_mail 
from home.tokens import generate_token
from django.shortcuts import get_object_or_404
from  quicksnap import settings
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request,'index.html')

def contact(request):

    if request.method=='POST':
        name = request.POST.get('name')
        query = request.POST.get('query')
        detail = request.POST.get('detail')
        datetime = timezone.now().strftime("%d-%m-%Y %H:%M:%S")
        email= request.POST.get('email')
        messages.success(request, f"Hi {name} ! Your Query is recived, We contact you as soon as possible.Stay updated on mail. ")
        send_mail(
                'New Query Submited',
                f'A new query has been submitted.\nName:{name}\nQuery:{query}\nDetail: {detail}\nEmail: {email}\nDate: {datetime}\n',
                EMAIL_HOST_USER,[EMAIL_ADMIN],fail_silently=True,)   
        return render(request,'contact.html')


    return render (request,'contact.html')

def feature(request):
    return render(request,'feature.html')

class CustomLoginView(LoginView):
    template_name='login.html'
    fields='__all__'
    redirect_authenticated_user=True
    def get_success_url(self):
        return reverse_lazy('data')

class DataList(LoginRequiredMixin,ListView):
    model=Data
    template_name = 'data.html'
    context_object_name = 'images'
    def get_context_data(self, **kwargs) :
        context=super().get_context_data(**kwargs)
        context['images']=context['images'].filter(user=self.request.user)
         
        return  context


class CreateData(LoginRequiredMixin,CreateView):
    model=Data
    fields= ['img','detail'] 
    template_name='add_data.html'
    success_url=reverse_lazy('data')
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
         
        
        return response


class UpdateData(LoginRequiredMixin, UpdateView):
    model = Data
    fields =  fields= ['img','detail' ]
    template_name = 'update_data.html'
    success_url = reverse_lazy('data')

    #def get_object(self, queryset=None):
    #   data_id = self.kwargs.get('data_id')
    #   return get_object_or_404(Data, pk=data_id)
    def get_object(self, queryset=None):
        data_id = self.kwargs.get('data_id')
        data = get_object_or_404(Data, pk=data_id)
        return data
        
 
class DeleteData(LoginRequiredMixin, DeleteView):
    model = Data
    success_url = reverse_lazy('data')
    template_name = 'delete_data.html'
     
    def get_object(self, queryset=None):
        data_id = self.kwargs.get('data_id')
        obj=get_object_or_404(Data, pk=data_id)
        try: 
           path=os.path.join(settings.MEDIA_ROOT,  obj.img.name)
           os.remove(path)
        except:
            pass
        return obj

       
@login_required
def get_image(request, data_id):
    try:
        # Get the Data instance based on data_id
        data_instance = get_object_or_404(Data, pk=data_id)
        
        # Check if the logged-in user owns the image
        if data_instance.user == request.user:
            image_name = data_instance.img.name
            return render(request, 'image_detail.html', {'image_name': image_name, 'image_id': data_id})
        else:
            # If the user doesn't own the image, render an appropriate error page
            return render(request, 'data.html')
    except Data.DoesNotExist:
        # If the Data instance doesn't exist, render an appropriate error page
        return render(request, 'data.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('userid')
      
        name = request.POST.get('name')
         
        
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        datetime = timezone.now().strftime("%d-%m-%Y %H:%M:%S")


        if len(username) > 20:
            messages.error(request, "Username should be less than 12 characters")  # Added 'request' argument
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return redirect('signup')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")  # Added 'request' argument
            return redirect('signup')
        if not username.isalnum():
            messages.error(request, "Username should be alphanumeric")  # Added 'request' argument
            return redirect('signup')

        myuser = User.objects.create_user(username,  pass1)
        
        myuser.name = name
        myuser.datetime=datetime
        
        myuser.is_active = True
        myuser.save()
        messages.success(request, f"Awesome {username} ! Your Account has been created succesfully, Login and add your snaps! ")
        send_mail(
                'New User Signup',
                f'A new user has been submitted.\nUsername:{username}\nName: {name}\nDate: {datetime}',
                EMAIL_HOST_USER,[EMAIL_ADMIN],fail_silently=True,)       
      
        '''current_site = get_current_site(request)
        email_subject = "Confirm your Email "
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()'''
        
        return redirect('login')
        

    return render(request, 'signup.html')  


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        
        messages.success(request, "Your Account has been activated!!")
        return redirect('login')
    else:
        messages.error(request,"Activation Failed")
        return render(request,'signup.html')
 
 

from django.http import HttpResponseServerError    
def error_page(request, unknown_path):
 
    return render(request, 'error_page.html', {'unknown_path': unknown_path})
def handle_dns_error(request):
    return  render(request,'error_page.html',{'unknown_path':"DNS Resolution Error"})
