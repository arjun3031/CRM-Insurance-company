from django.shortcuts import render

# Create your views here.


def homepage(request):
    return render(request,'homepage.html')

def loginpage(request):
    return render(request,'loginpage.html')

def aboutus(request):
    return render(request,'aboutus.html')

def services(request):
    return render(request,'services.html')

def contactus(request):
    return render(request,'contactus.html')

def adminhome(request):
    return render(request,'adminhome.html')

def addagent(request):
    return render(request,'addagent.html')

def viewagent(request):
    return render(request,'viewagent.html')

def agent1(request):
    return render(request,'agent1.html')

def editprofilebyadmin(request):
    return render(request,'editprofilebyadmin.html')

def agent2(request):
    return render(request,'agent2.html')

def location(request):
    return render(request,'location.html')

def viewclients(request):
    return render(request,'viewclients.html')

def moreaboutclientbyadmin(request):
    return render(request,'moreaboutclientbyadmin.html')

def addcampaign(request):
    return render(request,'addcampaign.html')

def viewcampaign(request):
    return render(request,'viewcampaign.html')

def editcampaign(request):
    return render(request,'editcampaign.html')

def viewcampaignclients(request):
    return render(request,'viewcampaignclients.html')

def viewcampaignagents(request):
    return render(request,'viewcampaignagents.html')

def agenthome(request):
    return render(request,'agenthome.html')

def profile(request):
    return render(request,'profile.html')

def resetpassword(request):
    return render(request,'resetpassword.html')

def editprofile(request):
    return render(request,'editprofile.html')

def addclient(request):
    return render(request,'addclient.html')

def viewclientsbyagent(request):
    return render(request,'viewclientsbyagent.html')

def moreaboutclient(request):
    return render(request,'moreaboutclient.html')

def editclient(request):
    return render(request,'editclient.html')

def viewcampaignbyagent(request):
    return render(request,'viewcampaignbyagent.html')