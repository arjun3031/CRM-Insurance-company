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
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Client
from datetime import datetime
from django.core.exceptions import ValidationError




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
            [email, 'arjunkmvat@gmail.com'],
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
            [email, 'arjunkmvat@gmail.com'], 
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

def viewclients(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    clients = Client.objects.filter(agent=agent)
    campaign_clients = CampaignClient.objects.filter(agent=agent)
    all_clients = list(clients) + list(campaign_clients)

    selected_client_name = request.GET.get('client_name')
    selected_profession = request.GET.get('profession')

    if selected_client_name:
        all_clients = [client for client in all_clients if 
                       f"{client.first_name} {client.last_name}".icontains(selected_client_name)]
    
    if selected_profession:
        all_clients = [client for client in all_clients if client.profession and selected_profession in client.profession]
    
    distinct_professions = set(client.profession for client in all_clients if client.profession)

    return render(request, 'viewclients.html', {
        'agent': agent, 
        'clients': all_clients,
        'distinct_professions': distinct_professions,
        'selected_client_name': selected_client_name, 
        'selected_profession': selected_profession,
    })


def moreaboutclientbyadmin(request, client_id):
    try:
        client = Client.objects.get(id=client_id)
        client_sources = client.source.split(',') if isinstance(client.source, str) else client.source
        client_areas = client.insurance_area.split(',') if isinstance(client.insurance_area, str) else client.insurance_area
        client_type = 'normal client'
    except Client.DoesNotExist:
        client = CampaignClient.objects.get(id=client_id)
        client_sources = client.source.split(',') if isinstance(client.source, str) else client.source
        client_areas = client.insurance_area.split(',') if isinstance(client.insurance_area, str) else client.insurance_area
        client_type = 'campaign client'
    
    return render(request, 'moreaboutclientbyadmin.html', {
        'client': client,
        'client_sources': client_sources,
        'client_areas': client_areas,
        'client_type': client_type,
    })


def addcampaign(request):
    if request.method == "POST":
        # agent_id = request.POST.get("agent")
        campaign_name = request.POST.get("campname")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        start_time = request.POST.get("start_time")
        location = request.POST.get("location")
        image = request.FILES.get("img")

        # if not agent_id:
        #     messages.error(request, "Please select an agent.")
        #     return redirect('add_campaign')
        
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

        # agent = Agent.objects.get(id=agent_id)
        Campaign.objects.create(
            # agent=agent,
            campaign_name=campaign_name,
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

def add_agent_to_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    agents = Agent.objects.exclude(id__in=campaign.campaignagent_set.values_list('agent_id', flat=True))

    if request.method == "POST":
        agent_id = request.POST.get("agent")
        if agent_id:
            agent = get_object_or_404(Agent, id=agent_id)
            CampaignAgent.objects.create(campaign=campaign, agent=agent)
            campaign_count = Campaign.objects.filter(campaignagent__agent=agent).count()
            messages.success(request, f"Agent '{agent.user.first_name} {agent.user.last_name}' added to the '{campaign.campaign_name}' successfully! Total campaigns now: {campaign_count}")
            return redirect('viewcampaign')
        else:
            messages.error(request, "Please select an agent.")
    return render(request, 'add_agent_to_campaign.html', {'campaign': campaign, 'agents': agents})

def view_agents_in_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    agents = CampaignAgent.objects.filter(campaign=campaign)
    if not agents:
        agents = None

    return render(request, 'viewcampaignagents.html', {
        'campaign': campaign,
        'agents': agents,
    })

def editcampaign(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    
    if request.method == "POST":
        # agent_id = request.POST.get("agent")
        campaign_name = request.POST.get("campname")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        start_time = request.POST.get("start_time")
        location = request.POST.get("location")
        image = request.FILES.get("img")

        # if not agent_id:
        #     messages.error(request, "Please select an agent.")
        #     return redirect('editcampaign', campaign_id=campaign.id)

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

        # agent = Agent.objects.get(id=agent_id)
        
        # campaign.agent = agent
        campaign.campaign_name = campaign_name
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

def show_campaign_clients_by_admin(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    clients = CampaignClient.objects.filter(campaign=campaign)
    agent = Agent.objects.filter(user=request.user).first()
    campaign_count = Campaign.objects.filter(agent=agent).count() if agent else 0
    selected_client_name = request.GET.get('client_name', '').strip()
    selected_profession = request.GET.get('profession', '').strip()

    if selected_client_name:
        name_parts = selected_client_name.split(' ', 1)
        if len(name_parts) == 2:
            first_name, last_name = name_parts
            clients = clients.filter(first_name=first_name, last_name=last_name)

    if selected_profession:
        clients = clients.filter(profession=selected_profession)

    distinct_professions = CampaignClient.objects.values('profession').distinct()
    context = {
        'campaign': campaign,
        'clients': clients,
        'campaign_count': campaign_count,
        'selected_client_name': selected_client_name,
        'selected_profession': selected_profession,
        'distinct_professions': distinct_professions,
    }
    return render(request, 'show_campaign_clients_by_admin.html', context)

def moreaboutcampaignclientbyadmin(request, client_id):
    try:
        client = CampaignClient.objects.get(id=client_id)
        client_sources = client.source.split(',') if isinstance(client.source, str) else client.source
        client_areas = client.insurance_area.split(',') if isinstance(client.insurance_area, str) else client.insurance_area
        client_type = 'normal client'
    except CampaignClient.DoesNotExist:
        client_sources = []
        client_areas = []
        client_type = 'campaign client'

    return render(request, 'moreaboutclientbyadmin.html', {
        'client': client,
        'client_sources': client_sources,
        'client_areas': client_areas,
        'client_type': client_type,
    })










@login_required(login_url='homepage')
def agenthome(request):
    agent = Agent.objects.filter(user=request.user).first()
    campaign_count = CampaignAgent.objects.filter(agent=agent).count()
    return render(request, 'agenthome.html', {'campaign_count': campaign_count})

def profile(request):
    if request.user.is_authenticated:
        try:
            agent = Agent.objects.get(user=request.user)
            campaign_count = CampaignAgent.objects.filter(agent=agent).count()
            return render(request, 'profile.html', {'agent': agent, 'campaign_count': campaign_count})  
        except Agent.DoesNotExist:
            return redirect('loginpage')
    else:
        return redirect('loginpage')
    
def resetpassword(request):
    agent = Agent.objects.get(user=request.user)
    campaign_count = CampaignAgent.objects.filter(agent=agent).count()
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
    return render(request, 'resetpassword.html',{'campaign_count': campaign_count})

def check_mobile(request):
    mobile = request.GET.get('mobile', '')
    current_mobile = request.GET.get('current_mobile', '')
    if mobile:
        exists = Client.objects.filter(phone=mobile).exclude(phone=current_mobile).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})

def check_username(request):
    username = request.GET.get('username')
    current_username = request.GET.get('current_username')
    exists = User.objects.filter(username=username).exclude(username=current_username).exists()
    return JsonResponse({'exists': exists})

def check_email(request):
    email = request.GET.get('email')
    current_email = request.GET.get('current_email')
    exists = User.objects.filter(email=email).exclude(email=current_email).exists()
    return JsonResponse({'exists': exists})

def editprofile(request):
    agent = Agent.objects.filter(user=request.user).first()
    if not agent:
        messages.error(request, 'Agent profile not found.')
        return redirect('dashboard')
    
    campaign_count = CampaignAgent.objects.filter(agent=agent).count()

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
    return render(request, 'editprofile.html', {'agent': agent,'campaign_count': campaign_count})

def check_adhaar(request):
    aadhar = request.GET.get('aadhar', '')
    if aadhar:
        exists = Client.objects.filter(aadhar=aadhar).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})

def check_pan(request):
    pan = request.GET.get('pan', '')
    if pan:
        exists = Client.objects.filter(pan=pan).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})

def addclient(request):
    agent = Agent.objects.get(user=request.user)
    campaign_count = CampaignAgent.objects.filter(agent=agent).count()
    return render(request, 'sample.html', {'agent': agent, 'campaign_count': campaign_count})

def add_client_form1(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        profession = request.POST.get('profession')
        annual_income = request.POST.get('annual_income')
        qualification = request.POST.get('qualification')
        aadhar = request.POST.get('aadhar')
        pan = request.POST.get('pan')

        client_id = request.session.get('client_id')
        if client_id:
            client = get_object_or_404(Client, id=client_id)
        else:
            client = Client()

        agent = Agent.objects.get(user=request.user)
        client.agent = agent 

        client.first_name = fname
        client.last_name = lname
        client.phone = phone
        client.address = address
        client.dob = datetime.strptime(dob, '%Y-%m-%d')
        client.age = age
        client.profession = profession
        client.annual_income = annual_income
        client.qualification = qualification
        client.aadhar = aadhar
        client.pan = pan
        client.save()

        request.session['client_id'] = client.id

        return JsonResponse({'success': True, 'client_id': client.id})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def add_client_form2(request):
    if request.method == 'POST':
        income_level = request.POST.get('income_level')
        children = request.POST.get('children')
        source = request.POST.getlist('source')
        feedback = request.POST.get('feedback')
        claim_satisfaction = request.POST.get('claim_satisfaction')
        areas = request.POST.getlist('area')
        img1 = request.FILES.get('img1')

        client_id = request.session.get('client_id')
        client = Client.objects.get(id=client_id)

        client.income_level = income_level
        client.children = children
        client.source = ', '.join(source)
        client.feedback = feedback
        client.claim_satisfaction = claim_satisfaction
        client.insurance_area = ', '.join(areas)
        if img1:
            client.agent_visited_policy = img1
        client.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def form3_submission(request):
    if request.method == 'POST':
        purchase = request.POST.get('Purchase')
        previous = request.POST.get('Previous')
        feedback = request.POST.get('feedback')
        agent_notes = request.POST.get('agent_notes')
        switch = request.POST.get('Switch')
        img = request.FILES.get('img')

        try:
            client_id = request.session.get('client_id')
            if not client_id:
                return JsonResponse({'error': 'No client found in session'}, status=400)

            client = Client.objects.get(id=client_id)
            agent = Agent.objects.get(user=request.user)
            client.agent = agent

            client.willingness_to_purchase = purchase
            client.willingness_to_share_previous_insurance = previous
            client.customer_preferences = feedback
            client.agent_notes = agent_notes
            client.willingness_to_switch = switch
            client.existing_profile_details = img

            client.save()
            del request.session['client_id']
            messages.success(request, 'Client added successfully!')
            return redirect('addclient')

        except Client.DoesNotExist:
            return JsonResponse({'error': 'Client not found'}, status=404)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def addclient_through_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    agent = Agent.objects.get(user=request.user)
    request.session['campaign_id'] = campaign_id
    campaign_count = CampaignAgent.objects.filter(agent=agent).count()
    return render(request, 'campaign_client_form.html', {'agent': agent, 'campaign': campaign,'campaign_count': campaign_count})

def campaign_client_form1(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        profession = request.POST.get('profession')
        annual_income = request.POST.get('annual_income')
        qualification = request.POST.get('qualification')
        aadhar = request.POST.get('aadhar')
        pan = request.POST.get('pan')

        campaign = Campaign.objects.get(id=request.session.get('campaign_id'))
        agent = Agent.objects.get(user=request.user)

        client = CampaignClient()
        request.session['campaign_client_id'] = client.id
        client.agent = agent 
        client.campaign = campaign
        client.first_name = fname
        client.last_name = lname
        client.phone = phone
        client.address = address
        client.dob = datetime.strptime(dob, '%Y-%m-%d')
        client.age = age
        client.profession = profession
        client.annual_income = annual_income
        client.qualification = qualification
        client.aadhar = aadhar
        client.pan = pan
        client.save()

        request.session['campaign_client_id'] = client.id

        return JsonResponse({'success': True, 'client_id': client.id})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def campaign_client_form2(request):
    if request.method == 'POST':
        client_id = request.session.get('campaign_client_id')
        if not client_id:
            return JsonResponse({'success': False, 'message': 'No client found in session'})

        client = CampaignClient.objects.get(id=client_id)

        client.income_level = request.POST.get('income_level')
        client.children = request.POST.get('children')
        client.source = ', '.join(request.POST.getlist('source'))
        client.feedback = request.POST.get('feedback')
        client.claim_satisfaction = request.POST.get('claim_satisfaction')
        client.insurance_area = ', '.join(request.POST.getlist('area'))
        img1 = request.FILES.get('img1')
        if img1:
            client.agent_visited_policy = img1
        client.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def campaign_client_form3(request):
    if request.method == 'POST':
        client_id = request.session.get('campaign_client_id')
        if not client_id:
            return JsonResponse({'success': False, 'message': 'No client found in session'})

        client = CampaignClient.objects.get(id=client_id)

        client.willingness_to_purchase = request.POST.get('Purchase')
        client.willingness_to_share_previous_insurance = request.POST.get('Previous')
        client.customer_preferences = request.POST.get('feedback')
        client.agent_notes = request.POST.get('agent_notes')
        client.willingness_to_switch = request.POST.get('Switch')
        img = request.FILES.get('img')
        if img:
            client.existing_profile_details = img

        client.save()

        del request.session['campaign_client_id']
        messages.success(request, 'Client added successfully through campaign!')
        return redirect('addclient_through_campaign', campaign_id=client.campaign.id)

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def viewclientsbyagent(request):
    agent = Agent.objects.get(user=request.user)  
    clients = Client.objects.filter(agent=agent)  
    campaign_count = CampaignAgent.objects.filter(agent=agent).count()

    selected_client_name = request.GET.get('client_name')
    selected_profession = request.GET.get('profession')

    if selected_client_name:
        clients = clients.filter(first_name__icontains=selected_client_name.split(' ')[0],
                                 last_name__icontains=selected_client_name.split(' ')[1] if len(selected_client_name.split(' ')) > 1 else '')
    if selected_profession:
        clients = clients.filter(profession__icontains=selected_profession)

    distinct_professions = clients.values_list('profession', flat=True).distinct()
    return render(request, 'viewclientsbyagent.html', {
        'agent': agent,
        'campaign_count': campaign_count,
        'clients': clients,  
        'distinct_professions': distinct_professions,
        'selected_client_name': selected_client_name, 
        'selected_profession': selected_profession,})

def moreaboutclient(request, client_id):
    agent = Agent.objects.get(user=request.user)
    client = get_object_or_404(Client, id=client_id)
    client_sources = client.source.split(',') if isinstance(client.source, str) else client.source
    client_areas = client.insurance_area if isinstance(client.insurance_area, list) else client.insurance_area.split(',')
    campaign_count = CampaignAgent.objects.filter(agent=agent).count()
    return render(request, 'moreaboutclient.html', {
        'agent': agent,
        'client': client,
        'client_sources': client_sources,
        'client_areas': client_areas,
        'campaign_count': campaign_count,
    })

def editclient(request, client_id):
    agent = Agent.objects.filter(user=request.user).first()
    campaigns = Campaign.objects.filter(agent=agent)
    campaign_count = CampaignAgent.objects.filter(agent=agent).count()
    client = get_object_or_404(Client, id=client_id)
    insurance_area_list = client.insurance_area if isinstance(client.insurance_area, list) else []

    return render(request, 'editclient.html', {
        'client': client, 
        'campaigns': campaigns, 
        'campaign_count': campaign_count, 
        'insurance_area_list': insurance_area_list
    })

def update_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == "POST":
        client.first_name = request.POST.get("fname")
        client.last_name = request.POST.get("lname")
        client.phone = request.POST.get("phone")
        client.address = request.POST.get("address")
        client.dob = request.POST.get("dob")
        client.age = request.POST.get("age")
        client.profession = request.POST.get("profession")
        client.annual_income = request.POST.get("annual_income")
        client.qualification = request.POST.get("qualification")
        client.aadhar = request.POST.get("aadhar")
        client.pan = request.POST.get("pan")
        client.income_level = request.POST.get("income_level")
        client.children = request.POST.get("children")
        client.source = request.POST.getlist("source")
        client.feedback = request.POST.get("feedback")
        client.claim_satisfaction = request.POST.get("claim_satisfaction")
        client.insurance_area = request.POST.getlist("area")

        img1 = request.FILES.get("img1")
        if img1:
            client.img1 = img1

        client.willingness_to_purchase = request.POST.get("Purchase")
        client.willingness_to_share_previous_insurance = request.POST.get("Previous")
        client.agent_notes = request.POST.get("agent_notes")
        client.willingness_to_switch = request.POST.get("Switch")
        client.save()

        messages.success(request, "Client information updated successfully!")
        return redirect('editclient', client_id=client.id)  

    context = {
        "client": client,
    }
    return render(request, 'moreaboutclient.html', context)

def delete_normal_client(request, client_id):
    client = Client.objects.filter(id=client_id).first()
    if not client:
        messages.error(request, "Client not found.")
        return redirect('viewclientsbyagent')

    client.delete()
    messages.success(request, f"Client '{client.first_name} {client.last_name}' has been deleted.")
    return redirect('viewclientsbyagent')

def viewcampaignbyagent(request):
    agent = Agent.objects.filter(user=request.user).first()

    if not agent:
        return render(request, 'viewcampaignbyagent.html', {'error': "Agent not found"})
    campaigns = Campaign.objects.filter(campaignagent__agent=agent)
    campaign_count = CampaignAgent.objects.filter(agent=agent).count()
    return render(request, 'viewcampaignbyagent.html', {
        'campaigns': campaigns,
        'campaign_count': campaign_count})


def show_campaign_clients(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)    
    clients = CampaignClient.objects.filter(campaign=campaign)
    agent = Agent.objects.filter(user=request.user).first()
    campaign_count = CampaignAgent.objects.filter(agent=agent).count()

    
    selected_client_name = request.GET.get('client_name', '')
    selected_profession = request.GET.get('profession', '')
    
    if selected_client_name:
        first_name, last_name = selected_client_name.split(' ', 1)
        clients = clients.filter(first_name=first_name, last_name=last_name)

    if selected_profession:
        clients = clients.filter(profession=selected_profession)

    distinct_professions = CampaignClient.objects.values('profession').distinct()

    context = {
        'clients': clients,
        'selected_client_name': selected_client_name,
        'selected_profession': selected_profession,
        'distinct_professions': distinct_professions,'campaign': campaign,'campaign_count': campaign_count,

    }
    return render(request, 'show_campaign_clients.html', context)

def moreaboutcampaignclient(request, client_id):
    agent = Agent.objects.get(user=request.user)
    client = get_object_or_404(CampaignClient, id=client_id)
    client_sources = client.source.split(',') if isinstance(client.source, str) else client.source
    client_areas = client.insurance_area if isinstance(client.insurance_area, list) else client.insurance_area.split(',')
    campaign_count = CampaignAgent.objects.filter(agent=agent).count()
    return render(request, 'moreaboutcampaignclient.html', {
        'agent': agent,
        'client': client,
        'client_sources': client_sources,
        'client_areas': client_areas,
        'campaign_count': campaign_count,
    })

def delete_campaign_client(request, client_id):
    client = get_object_or_404(CampaignClient, id=client_id)
    campaign_id = client.campaign.id
    client.delete()
    messages.success(request, f"Campaign client '{client.first_name} {client.last_name}' has been deleted.")
    return redirect('show_campaign_clients', campaign_id=campaign_id)

def edit_campaign_client(request, client_id):
    agent = Agent.objects.filter(user=request.user).first()
    campaigns = Campaign.objects.filter(agent=agent)
    campaign_count = CampaignAgent.objects.filter(agent=agent).count()
    campaign_client = get_object_or_404(CampaignClient, id=client_id)
    insurance_area_list = campaign_client.insurance_area if isinstance(campaign_client.insurance_area, list) else []

    return render(request, 'edit_campaign_client.html', {
        'client': campaign_client,
        'campaigns': campaigns,
        'campaign_count': campaign_count,
        'insurance_area_list': insurance_area_list
    })


def update_campaign_client(request, client_id):
    campaign_client = get_object_or_404(CampaignClient, id=client_id)

    if request.method == "POST":
        campaign_client.first_name = request.POST.get("fname")
        campaign_client.last_name = request.POST.get("lname")
        campaign_client.phone = request.POST.get("phone")
        campaign_client.address = request.POST.get("address")
        campaign_client.dob = request.POST.get("dob")
        campaign_client.age = request.POST.get("age")
        campaign_client.profession = request.POST.get("profession")
        campaign_client.annual_income = request.POST.get("annual_income")
        campaign_client.qualification = request.POST.get("qualification")
        campaign_client.aadhar = request.POST.get("aadhar")
        campaign_client.pan = request.POST.get("pan")
        campaign_client.income_level = request.POST.get("income_level")
        campaign_client.children = request.POST.get("children")
        campaign_client.source = request.POST.getlist("source")
        campaign_client.feedback = request.POST.get("feedback")
        campaign_client.claim_satisfaction = request.POST.get("claim_satisfaction")
        campaign_client.insurance_area = request.POST.getlist("area")

        img1 = request.FILES.get("img1")
        if img1:
            campaign_client.img1 = img1

        campaign_client.willingness_to_purchase = request.POST.get("Purchase")
        campaign_client.willingness_to_share_previous_insurance = request.POST.get("Previous")
        campaign_client.agent_notes = request.POST.get("agent_notes")
        campaign_client.willingness_to_switch = request.POST.get("Switch")
        campaign_client.save()

        messages.success(request, "Campaign client information updated successfully!")
        return redirect('edit_campaign_client', client_id=campaign_client.id)

    context = {
        "client": campaign_client,
    }
    return render(request, 'moreaboutcampaignclient.html', context)


























