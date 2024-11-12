from django.urls import path,include
from .import views

urlpatterns = [
        path('', views.homepage, name='homepage'),  
        path('loginpage', views.loginpage, name='loginpage'),  
        path('aboutus', views.aboutus, name='aboutus'),  
        path('services', views.services, name='services'),  
        path('contactus', views.contactus, name='contactus'),  
        path('adminhome', views.adminhome, name='adminhome'),  
        path('addagent', views.addagent, name='addagent'),  
        path('viewagent', views.viewagent, name='viewagent'),  
        path('agent1', views.agent1, name='agent1'), 
        path('editprofilebyadmin', views.editprofilebyadmin, name='editprofilebyadmin'), 
        path('agent2', views.agent2, name='agent2'),
        path('location', views.location, name='location'),
        path('viewclients', views.viewclients, name='viewclients'),
        path('moreaboutclientbyadmin', views.moreaboutclientbyadmin, name='moreaboutclientbyadmin'),
        path('addcampaign', views.addcampaign, name='addcampaign'),
        path('viewcampaign', views.viewcampaign, name='viewcampaign'),
        path('editcampaign', views.editcampaign, name='editcampaign'),
        path('viewcampaignclients', views.viewcampaignclients, name='viewcampaignclients'),
        path('viewcampaignagents', views.viewcampaignagents, name='viewcampaignagents'),
        path('agenthome', views.agenthome, name='agenthome'),  
        path('profile', views.profile, name='profile'),  
        path('resetpassword', views.resetpassword, name='resetpassword'), 
        path('editprofile', views.editprofile, name='editprofile'),
        path('addclient', views.addclient, name='addclient'),    
        path('viewclientsbyagent', views.viewclientsbyagent, name='viewclientsbyagent'),    
        path('moreaboutclient', views.moreaboutclient, name='moreaboutclient'),    
        path('editclient', views.editclient, name='editclient'),    
        path('viewcampaignbyagent', views.viewcampaignbyagent, name='viewcampaignbyagent'),    

]