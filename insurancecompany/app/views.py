from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from app.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from datetime import datetime
import re
from django.contrib.auth import authenticate, update_session_auth_hash
from django.http import JsonResponse
from django.views.decorators.http import require_POST





# Create your views here.


def homepage(request):
    return render(request,'homepage.html')

def aboutus(request):
    return render(request,'aboutus.html')

def services(request):
    return render(request,'services.html')

def contactus(request):
    return render(request,'contactus.html')



def loginpage(request):
    return render(request,'loginpage.html')

def logout(request):
    auth.logout(request)
    return redirect('homepage')

def userlog(request):
    if request.method == 'POST':
        usname = request.POST['username']
        passwrd = request.POST['password']
        
        user = authenticate(username=usname, password=passwrd)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('adminhome')
            try:
                agent = Agent.objects.get(user=user)
                login(request, user) 
                return redirect('agenthome')
            except Agent.DoesNotExist:
                messages.info(request, 'You do not have permission to login as an agent.')
                return redirect('loginpage')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('loginpage')
    else:
        return redirect('loginpage')

@login_required(login_url='homepage')
def adminhome(request):
    return render(request,'adminhome.html')

def addagent(request):
    if request.method == "POST":
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        username = request.POST.get("uname")
        email = request.POST.get("mail")
        mobile = request.POST.get("mobile")
        place = request.POST.get("place")
        image = request.FILES.get("img")
        password = get_random_string(length=6)

        if username == email:
            messages.info(request, 'Username and email cannot be same')
            return redirect('addagent')
    
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('addagent')
        
        if Agent.objects.filter(mobile=mobile).exists():
            messages.info(request, 'Mobile number already exists')
            return redirect('addagent')
        
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists')
            return redirect('addagent')
        
        if '.com' not in email:
            messages.error(request, 'Email format incorrect')
            return redirect('addagent')
        
        user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username)
        user.set_password(password)
        user.save()

        Agent.objects.create(user=user,mobile=mobile,place=place,image=image)

        send_mail(
            'New Account Credentials (Jan suraksha Insurance)',
            f'New user registration details:\n\nUsername: {username}\nPassword: {password}',
            'arjunkmvat@gmail.com',  
            ['arjunkmvat@gmail.com'],
            fail_silently=False,
            )
        messages.success(request, 'Account created successfully!!')
        return redirect('addagent')
    return render(request,'addagent.html')

def viewagent(request):
    agents = Agent.objects.all() 
    return render(request, 'viewagent.html', {'agents': agents})

def delete_agent(request, agent_id):
    agent = Agent.objects.get(id=agent_id)
    user = agent.user
    agent.delete()  
    user.delete()
    messages.error(request, f"Agent '{user.first_name} {user.last_name}' has been deleted")
    return redirect('viewagent')

def agent_prfile_by_admin(request,agent_id):
    agent = Agent.objects.get(id=agent_id)
    return render(request, 'agent_prfile_by_admin.html', {'agent': agent})

def editprofilebyadmin(request, agent_id):
    agent = Agent.objects.get(id=agent_id)
    user = agent.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        old_username = user.username 
        
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = username
        user.email = email
        agent.mobile = mobile
        agent.place = request.POST.get('location')

        if username == email:
            messages.info(request, 'Username and email cannot be the same')
            return redirect('editprofilebyadmin', agent_id=agent_id)

        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.info(request, 'Username already exists')
            return redirect('editprofilebyadmin', agent_id=agent_id)
        
        if Agent.objects.filter(mobile=mobile).exclude(id=agent.id).exists():
            messages.info(request, 'Mobile number already exists')
            return redirect('editprofilebyadmin', agent_id=agent_id)
        
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.info(request, 'Email already exists')
            return redirect('editprofilebyadmin', agent_id=agent_id)
        
        if '.com' not in email:
            messages.error(request, 'Email format incorrect')
            return redirect('editprofilebyadmin', agent_id=agent_id)

        if 'img' in request.FILES:
            agent.image = request.FILES['img']

        user.save()
        agent.save()
        
        send_mail(
            'Profile Updated (Jan Suraksha Insurance)',
            f'Hello {user.first_name},\n\nYour profile has been successfully updated.\n\n'
            f'Updated details:\nUsername: {username}\nEmail: {email}\nMobile: {mobile}\nLocation: {agent.place}',
            'arjunkmvat@gmail.com', 
            ['arjunkmvat@gmail.com'], 
            fail_silently=False,
        )

        if old_username != username:
            send_mail(
                'New Account Credentials (Jan Suraksha Insurance)',
                f'Hello {user.first_name},\n\nYour username has been changed.\n\n'
                f'New Username: {username}\nPlease use this username for future logins.',
                'arjunkmvat@gmail.com',
                ['arjunkmvat@gmail.com'],
                fail_silently=False,
            )
        messages.success(request, 'Agent profile updated')
        return redirect('agent_prfile_by_admin', agent_id=agent_id)

    return render(request, 'editprofilebyadmin.html', {'agent': agent})


def location(request):
    return render(request,'location.html')

def viewclients(request):
    return render(request,'viewclients.html')

def moreaboutclientbyadmin(request):
    return render(request,'moreaboutclientbyadmin.html')

def addcampaign(request):
    if request.method == "POST":
        agent_id = request.POST.get("agent")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        start_time = request.POST.get("start_time")
        location = request.POST.get("location")
        image = request.FILES.get("img")

        if not agent_id:
            messages.error(request, "Please select an agent.")
            return redirect('add_campaign')
        
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        
        if start_date_obj and end_date_obj and start_date_obj > end_date_obj:
            messages.error(request, "Date selected wrongly")
            return redirect('addcampaign')

        if start_time:
            start_time_obj = datetime.strptime(start_time, '%H:%M').time()
            if start_time_obj >= datetime.strptime("20:00", '%H:%M').time():
                messages.error(request, "Please select a time b/w 8 AM and 8 PM.")
                return redirect('addcampaign')

        agent = Agent.objects.get(id=agent_id)
        Campaign.objects.create(
            agent=agent,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            location=location,
            image=image,
        )
        messages.success(request, "Campaign added successfully!")
        return redirect('addcampaign')

    agents = Agent.objects.all()
    return render(request, 'addcampaign.html', {'agents': agents})

def viewcampaign(request):
    campaigns = Campaign.objects.all()  
    return render(request, 'viewcampaign.html', {'campaigns': campaigns})

def editcampaign(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    
    if request.method == "POST":
        agent_id = request.POST.get("agent")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        start_time = request.POST.get("start_time")
        location = request.POST.get("location")
        image = request.FILES.get("img")

        if not agent_id:
            messages.error(request, "Please select an agent.")
            return redirect('editcampaign', campaign_id=campaign.id)

        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        
        if start_date_obj and end_date_obj and start_date_obj > end_date_obj:
            messages.error(request, "Start date cannot be greater than end date.")
            return redirect('editcampaign', campaign_id=campaign.id)

        if start_time:
            start_time_obj = datetime.strptime(start_time, '%H:%M').time()
    
        if start_time_obj < datetime.strptime("08:00", '%H:%M').time() or start_time_obj >= datetime.strptime("20:00", '%H:%M').time():
            messages.error(request, "Please select a time between 8 AM and 8 PM.")
            return redirect('editcampaign', campaign_id=campaign.id)

        agent = Agent.objects.get(id=agent_id)
        
        campaign.agent = agent
        campaign.start_date = start_date
        campaign.end_date = end_date
        campaign.start_time = start_time
        campaign.location = location
        if image:
            campaign.image = image
        campaign.save()

        messages.success(request, "Campaign details updated successfully!")
        return redirect('viewcampaign')

    agents = Agent.objects.all()
    return render(request, 'editcampaign.html', {'campaign': campaign, 'agents': agents})

def viewcampaignclients(request):
    return render(request,'viewcampaignclients.html')

def viewcampaignagents(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    agent = campaign.agent
    return render(request, 'viewcampaignagents.html', {'campaign': campaign, 'agent': agent})

def delete_campaign(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    location = campaign.location
    campaign.delete()
    messages.success(request, f'Campaign at {location} has been successfully deleted.')
    return redirect('viewcampaign')  


def agenthome(request):
    return render(request,'agenthome.html')

def profile(request):
    if request.user.is_authenticated:
        try:
            agent = Agent.objects.get(user=request.user)
            return render(request, 'profile.html', {'agent': agent})
        except Agent.DoesNotExist:
            return redirect('loginpage') 
    else:
        return redirect('loginpage')

def resetpassword(request):
    if request.method == 'POST':
        current_password = request.POST.get('cpassword')
        new_password = request.POST.get('npassword')
        confirm_password = request.POST.get('confirm')

        user = User.objects.get(id=request.user.id)

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('resetpassword')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('resetpassword')

        if len(new_password) < 8 or not re.search(r'\d', new_password) or not re.search(r'[@$!%*?&]', new_password):
            messages.error(request, 'Password must have at least 8 characters, one digit, and one special character.')
            return redirect('resetpassword')

        user.set_password(new_password)
        user.save()

        auth.login(request, user)
        update_session_auth_hash(request, user) 

        messages.success(request, "Password reset successfully.")
        return redirect('resetpassword')
    return render(request, 'resetpassword.html')

def check_phone(request):
    phone = request.GET.get('phone')
    exists = Agent.objects.filter(mobile=phone).exists()
    return JsonResponse({'exists': exists})

def editprofile(request):
    agent = Agent.objects.filter(user=request.user).first()
    if not agent:
        messages.error(request, 'Agent profile not found.')
        return redirect('dashboard')

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email')
        agent.mobile = request.POST.get('mobile')
        agent.place = request.POST.get('location')

        if request.user.username == request.user.email:
            messages.info(request, 'Username and email cannot be the same')
            return redirect('editprofile')

        if User.objects.filter(username=request.user.username).exclude(id=request.user.id).exists():
            messages.info(request, 'Username already exists')
            return redirect('editprofile')

        if Agent.objects.filter(mobile=agent.mobile).exclude(id=agent.id).exists():
            messages.info(request, 'Mobile number already exists')
            return redirect('editprofile')

        if User.objects.filter(email=request.user.email).exclude(id=request.user.id).exists():
            messages.info(request, 'Email already exists')
            return redirect('editprofile')

        if '.com' not in request.user.email:
            messages.error(request, 'Email format incorrect')
            return redirect('editprofile')

        if 'img' in request.FILES:
            agent.image = request.FILES['img']

        request.user.save()
        agent.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('profile')

    return render(request, 'editprofile.html', {'agent': agent})

def addclient(request):
    return render(request,'addclient.html')

def viewclientsbyagent(request):
    return render(request,'viewclientsbyagent.html')

def moreaboutclient(request):
    return render(request,'moreaboutclient.html')

def editclient(request):
    return render(request,'editclient.html')


def viewcampaignbyagent(request):
    agent = Agent.objects.filter(user=request.user).first()
    if not agent:
        return render(request, 'viewcampaignbyagent.html', {'error': "Agent not found"})
    campaigns = Campaign.objects.filter(agent=agent)
    return render(request, 'viewcampaignbyagent.html', {'campaigns': campaigns})