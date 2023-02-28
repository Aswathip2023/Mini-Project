from datetime import timedelta
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Booking, Category, Service, Gallery
from .forms import BookingForm
from django.urls import reverse
from WeddingApp.forms import UserRegistrationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User

# Create your views here.
from .forms import BookingForm
def register(request):
  form = CustomUserCreationForm()
  if request.method == 'POST':
       form = CustomUserCreationForm(request.POST)
       if form.is_valid():
           form.save()
           return render(request, 'login.html')
  return render(request, "register.html", {'form': form,})

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials!!!")
            return redirect('login')
    return render(request, "login.html")


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/')


def user(request):
    if request.user.is_authenticated:
        apptmnt_info = Appointment.objects.filter(user=request.user)
        return render(request, "user.html",{
            'info': apptmnt_info,
        })
    return redirect('login')


########Sevices##########

def demo(request):
    obj = Category.objects.all()
    return render(request, "index.html", {'category': obj})


def bridal(request):
    bridal = Service.objects.filter(category_id=1)
    return render(request, "services/bridal.html", {'list': bridal})





def makeover(request):
    mkup = Service.objects.filter(category_id=6)
    return render(request, "services/makeover.html", {'list5': mkup})




def gallery(request):
    gallery = Gallery.objects.all
    return render(request, "gallery.html", {'photos': gallery})


########Appointment##########
def Bookings(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            date = form.cleaned_data['date']
            time= form.cleaned_data['time']
            apptmnt = Booking(service=service,time=time,date=date)
            apptmnt.save()
            messages.info(request,"New booking Added Successfully!!!")
            apptmnt_info = Booking.objects.filter()
            return render(request, "booking_info.html", {
                'info': apptmnt_info,
                'service': service,
                'date': date,
                'time': time,

            })

    else:
        form = BookingForm
    return render(request, 'booking.html', {'form': form})

def bookinginfo(request):
    if request.user.is_authenticated:
        apptmnt_info = Booking.objects.all()
        return render(request, "bookinginfo.html", {
            'info': apptmnt_info,
        })

    return redirect('booking')

# def Booking(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             form = AppointmentForm(request.POST)
#             if form.is_valid():
#                 service = form.cleaned_data['service']
#                 date = form.cleaned_data['date']
#                 time = form.cleaned_data['time']
#                 if date < timezone.now().date():
#                     messages.info(request, "Date cannot be in the past")
#                     return redirect('appointment')
#                 # apptmnt = Booking(user=user, service=service, date=date, time=time)
#                 # apptmnt.save()
#                 messages.info(request, "New Appointment Added Successfully!!!")
#                 apptmnt_info = Booking.objects.filter()
#                 return render(request, "booking_info.html", {
#                     'info': apptmnt_info,
#                     'service': service,
#                     'date': date,
#                     'time': time,
#                 })
#
#         else:
#             form = AppointmentForm
#         return render(request, 'booking.html', {'form': form})
#     return redirect('login')

def appointment_info(request):
    if request.user.is_authenticated:
        # apptmnt_info = Booking.objects.filter(user=request.user)
        return render(request, "booking_info.html", {
            # 'info': apptmnt_info,
        })
    return redirect('appointment')


# CRUD OPERATIONS
def Delete(request, id):
    apptmnt_info = Booking.objects.filter(id=id)
    apptmnt_info.delete()
    messages.info(request, "Appointment Deleted!!!")
    return redirect("appointment_info")


def Update(request, id):
    if request.method == 'POST':
        result = Booking.objects.get(id=id)
        form = AppointmentForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
    else:
        result = Booking.objects.get(id=id)
        form = AppointmentForm(instance=result)
        messages.info(request, "Updated!!!")
    return render(request, 'update_booking.html', {'form': form})


# Send Email
# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.template.loader import render_to_string
#
# def success(request,uid):
#     template = render_to_string('email_message.html')
#     email=EmailMessage(
#         'subject',
#         'body',
#         settings.EMAIL_HOST_USER,
#         ['beautyparlour801@gmail.com'],
#     )
#     email.fail_silently=False
#     email.send()
#     result = Appointment.objects.get(id=uid)
#     context = {'result':result}
#     return render(request,'success.html',context)
#


# def register(request):
#     form = UserRegistrationForm()
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user.is_active = False
#             print("Successfully Registered")
#             messages.info(request, 'Registered Successfully !!Now you can login!')
#             return redirect('register')
#             return redirect(reverse('register'))
#     return render(request, 'register.html', {'form': form})

# def activateEmail(request, user, to_email):
#     messages.success(request,'Dear <b> {user}</b>,please go to your email <b> {to_email}</b> inbox and click on received activation link to confirm and complete the registration.<b>Note:</b> Check ypur spam folder.')

def new(request):
    return render(request, "new.html")
