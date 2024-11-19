from django.urls import path,include
from .import views

urlpatterns = [
        path('', views.homepage, name='homepage'),  
        path('aboutus', views.aboutus, name='aboutus'),  
        path('services', views.services, name='services'),  
        path('contactus', views.contactus, name='contactus'),  

        path('loginpage', views.loginpage, name='loginpage'),  
        path('logout',views.logout,name='logout'),
        path('userlog',views.userlog,name='userlog'),

        path('adminhome', views.adminhome, name='adminhome'),  
        path('addagent', views.addagent, name='addagent'),  
        path('viewagent', views.viewagent, name='viewagent'), 
        path('delete_agent/<int:agent_id>', views.delete_agent, name='delete_agent'), 
        path('agent_prfile_by_admin/<int:agent_id>', views.agent_prfile_by_admin, name='agent_prfile_by_admin'),
        path('editprofilebyadmin/<int:agent_id>', views.editprofilebyadmin, name='editprofilebyadmin'),
 
        path('location', views.location, name='location'),
        path('viewclients/<int:agent_id>/', views.viewclients, name='viewclients'),
        path('moreaboutclientbyadmin/<int:client_id>', views.moreaboutclientbyadmin, name='moreaboutclientbyadmin'),

        path('addcampaign', views.addcampaign, name='addcampaign'),
        path('viewcampaign', views.viewcampaign, name='viewcampaign'),
        path('deletecampaign/<int:campaign_id>', views.delete_campaign, name='delete_campaign'),

        path('editcampaign/<int:campaign_id>', views.editcampaign, name='editcampaign'),
        path('viewcampaignclients', views.viewcampaignclients, name='viewcampaignclients'),
        path('viewcampaignagents/<int:campaign_id>', views.viewcampaignagents, name='viewcampaignagents'),




        path('agenthome', views.agenthome, name='agenthome'),  
        path('profile', views.profile, name='profile'),

        path('resetpassword', views.resetpassword, name='resetpassword'), 
    
        path('check-mobile/', views.check_mobile, name='check_mobile'),
        path('check-username/', views.check_username, name='check_username'),
        path('check-email/', views.check_email, name='check_email'),
        path('editprofile', views.editprofile, name='editprofile'),

        path('check-adhaar/', views.check_adhaar, name='check_adhaar'),
        path('check-pan/', views.check_pan, name='check_pan'),
        path('addclient', views.addclient, name='addclient'), 
        path('form1/', views.add_client_form1, name='add_client_form1'),
        path('form2/', views.add_client_form2, name='add_client_form2'),
        path('form3/', views.form3_submission, name='form3_submission'),











        path('viewclientsbyagent', views.viewclientsbyagent, name='viewclientsbyagent'),    
        path('moreaboutclient/<int:client_id>/', views.moreaboutclient, name='moreaboutclient'),


        path('editclient/<int:client_id>/', views.editclient, name='editclient'),
        path('update_client/<int:client_id>/', views.update_client, name='update_client'),


        path('viewcampaignbyagent', views.viewcampaignbyagent, name='viewcampaignbyagent'),    

]