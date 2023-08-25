from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required #import the login_required to restrict user to some pages if not login
from django.db.models import Q # import Q for search queries
from django.contrib.auth import authenticate, login, logout # import django built-in authenticate and login method
from .models import Room, Topic, Message, User # import the tables created from the model module
from .forms import RoomForm, UserRegistration, UpdateForm

#sendig email imports
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django .utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, BadHeaderError
from. token import GenerateToken
#import time, datetime






#from django.conf import settings

# Create your views here.


#homepage method
def index(request):
    search = request.GET.get('search') if request.GET.get('search') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=search) |
        Q(name__icontains=search) |
        Q(description__icontains=search)  
        
    )
    allGroupMessages = Message.objects.filter(Q(room__topic__name__icontains=search)) 

    total_group = rooms.count()
    topics = Topic.objects.all()[0:4]
    context = {'rooms':rooms, 'topics':topics, 'total_group':total_group, 'allGroupMessages':allGroupMessages}
    return render(request, 'base/index.html', context)





def sendActivationLink(request, user, receipient_email):
    mail_subject = "Activate your account."
    token_generator = GenerateToken()  # Create an instance of GenerateToken
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)  # Generate the token using the instance

    msg = render_to_string("base/activate_account_template.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': uid,
        'token': token,
        'protocol': 'https' if request.is_secure() else 'http'             
    })
    #messages.success(request, f"Activate Your Account by clicking the link in your gmail {msg}")
    try:
        sendMail = EmailMessage(mail_subject, msg, to=[receipient_email])
        if sendMail.send():
            messages.success(request, f"An email with activation link has been sent to {receipient_email}. Please check your inbox and follow the link to activate your account.")
        else:
            messages.error(request, f"Problem sending email to {receipient_email}. Check that your email is correct.")

    except BadHeaderError:
        return HttpResponse("Invalid header found.")
 
    
    



# Registration method
def registerUser(request):
   regForm = UserRegistration()
   if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if User.objects.filter(email=email).exists():
                messages.error(request, "An account has been registered with the provided email address.")
            elif password1 != password2:
                messages.error(request, "Passwords do not match.")
            else:
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.is_active = False
                user.save()
    
                # Assuming you pass the user instance to sendActivationLink function
                sendActivationLink(request, user, email)
                #messages.success(request, f"Registration successful! An activation link has been sent {email}.")
                return redirect('register')
               

               
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

   context = {'regForm': regForm}
   return render(request, 'base/user-page.html', context)






#Successful Account Activation    
def accountActivation(request, uidb64, token):
    token_generator = GenerateToken()
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, f"Thank you for activating your account. You can login!")
        return redirect('login')
    else:
        messages.error(request, f"Dear {user}, an error has occured while activating your account. check your network!")


#login method
def UserLogin(request):
    page = 'login'
    #if user is loggedin redirect them back to home page
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            None
           # messages.error(request, 'Your account is not activated. Please check your email for the activation link.')  
           # return redirect('login') 
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #Check if there's a stored URL in the session
                redirect_to = request.session.pop('redirect_to', None)
                if redirect_to:
                    return redirect(redirect_to)
                messages.success(request, f'Welcome, {user}')
                return redirect('index')  # Default redirection if no stored URL
            else:
                 messages.error(request, 'Your account is not activated. Please check your email for the activation link')
        else:
            messages.error(request, 'Invalid login details')

    messages.error(request, "")
    context = {'page':page}
    return render(request, 'base/user-page.html', context)



#User Profile
#@login_required(login_url='login')
def userProfile(request, username):
    user = User.objects.get(username=username) #(field_name=variable_passed_into_url)
    print(user)
    rooms = user.room_set.all()
    allGroupMessages= user.message_set.all()
    topics = Topic.objects.all()
    
    context = {'user': user,
               'rooms': rooms, 
               'allGroupMessages':allGroupMessages,
               'topics':topics,
               }
    return render(request, 'base/profile.html')

@login_required(login_url='login')
def updateUserProfile(request, username):
    user = User.objects.get(username=username)
    form = UpdateForm(instance=user)


    if request.method == 'POST':
       pass
       form = UpdateForm(request.POST, request.FILES, instance=user)

        #Validate data
       if form.is_valid():
            user.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile', username=user.username)  
       else:
            messages.error(request, 'All fields are required')
        

    context = {'form': form}
    return render(request, 'base/update-profile.html', context)

#logout method
def logUserOut(request):
    logout(request)
    messages.success(request, 'logout success')
    return redirect('index')




#Create New Group
@login_required(login_url='login')
def createGroup(request): 
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        topic_name= request.POST.get('topic')
        group_descrip = request.POST.get('description')

        if group_name and topic_name and group_descrip:
            topic, created = Topic.objects.get_or_create(name=topic_name)
            room = Room.objects.create(
            host=request.user,
            topic=topic,
            name=group_name,
            description=group_descrip
            )
            room.members.add(request.user)
            return redirect('index')
        else:
            print('Invalid form')
        
    else:
        print("request != post")

    context = {}
    return render(request, 'base/create-group.html', context)



#View Group
def viewGroup(request, pk):
    # The code below redirect to each room once clicked  
    try:
        #Getting each room based on primary key
        room = Room.objects.get(id=pk)
        # Get related messages (i.e message to a specic room)
        room_messages = room.message_set.all().order_by('-date_created') 
        #accessing the users who are members of the specific room
        members = room.members.all()

        if request.method == 'POST':
            body = request.POST.get('body')
            
            # Check if the user is authenticated
            if request.user.is_authenticated:
                # Check if the user is a member of the group
                if request.user in members:
                    message = Message.objects.create(
                        user=request.user,
                        room=room,
                        body=body
                    )
                    return redirect('group', pk=room.id)
                else:
                    # User is logged in but not a member of the group
                    return redirect('join-group', pk=room.id)
            else:
                # Store the current URL in the session
                request.session['redirect_to'] = request.path
                return redirect('login')  # Redirect to login view
        else:
            pass
            # ... Do something ...
        
    except Room.DoesNotExist:
        room = None
        return HttpResponse('Ooops! It seems the room you are trying to access is Forbidden')
    context = {'room': room, 
               'room_messages':room_messages, 
               'members':members}
    return render(request, 'base/group.html', context)



#Join Group
@login_required(login_url='login')
def joinGroup(request, pk):
    room = get_object_or_404(Room, id=pk)
    members = room.members.all()
    
    if request.user.is_authenticated and request.user not in members:
        room.members.add(request.user)
        
    # Redirect the user back to the room's page after joining
    return redirect('group', pk=room.id)




#Update Group
@login_required(login_url='login')
def updateGroup(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("Your are not authorized")
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        topic_name= request.POST.get('topic')
        group_descrip = request.POST.get('description')
        
        if group_name and topic_name and group_descrip:
            # Get or create the topic
            topic, created = Topic.objects.get_or_create(name=topic_name)

            # Update the room's attributes
            room.name = group_name
            room.topic = topic
            room.description = group_descrip
            room.save()

            return redirect('group', pk=room.id)
        

    context = {'room':room}
    return render(request, 'base/update-group.html', context)


#Delete Group
@login_required(login_url='login')
def deleteGroup(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("Your are not authorized")
    if request.method == 'POST':
        room.delete()
        return redirect('index')
    context = {'room': room}
    return render(request, 'base/delete-group.html', context)


#Update comment
@login_required(login_url='login')
def updateComment(request, pk):
    comment = get_object_or_404(Message, id=pk)

    if request.user == comment.user:
        if request.method == "POST":
            updatedComment = request.POST.get('update')
            comment.body = updatedComment
            comment.save()
            return redirect('group', pk=comment.room.id)
        
        context = {'comment': comment}
        return render(request, 'base/edit-comment.html',context)
    else:
        return HttpResponse("You are not authorized to edit this comment")



#Delete Comment
@login_required(login_url='login')
def deleteComment(request, pk):
    comment = get_object_or_404(Message, id=pk)

    if request.user == comment.user:
        if request.method == "POST":
            comment.delete()
            return redirect('index')

        context = {'comment':comment}
        return render(request, 'base/delete-comment.html',context)
    else:
        return HttpResponse("You are not authorized to delete this message!")




def browseTopics(request):
    search = request.GET.get('search') if request.GET.get('search') != None else ''
    topics = Topic.objects.filter(name__icontains=search) 
        
    
    context = {'topics': topics}
    return render(request, 'base/browse-topics.html', context)



def browseActivity(request):
    allGroupMessages = Message.objects.all()
        
    
    context = {'allGroupMessages': allGroupMessages}
    return render(request, 'base/browse-activity.html', context)











 # elif User.objects.filter(username__iexact=username).exists():
        #     print('This username is already taken.')