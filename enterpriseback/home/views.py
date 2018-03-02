from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as dj_login, authenticate, logout as dj_logout


from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import get_template
from django.template import Context

from managers.models import Manager, SuperAdmin

from buildings.forms import BuildingForm, DepartmentForm

from buildings.models import Building, Department, NearbyAtraction, DepartmenGalery

from .forms import MaintenanceForm, ContactForm, MoveOutForm
from django.conf import settings

TO_SEND = settings.TO_SEND
SENDER = settings.SENDER
SENDER_CONTACT = settings.SENDER_CONTACT
SENDER_CONTACT_PASS = settings.SENDER_CONTACT_PASS
EMAIL_HOST = settings.EMAIL_HOST
EMAIL_PORT = settings.EMAIL_PORT
EMAIL_USE_TLS = settings.EMAIL_USE_TLS

# Create your views here.
def index(request):
    successmsg = None
    successmsg = request.GET.get('successmsg', None)
    if successmsg != "True":
        successmsg = None
    departments = Department.objects.all()

    apAndGal=[]
    for apart in departments:
        image=DepartmenGalery.objects.filter(departmen=apart).first()
        apAndGal.append({"depart":apart,"image":image})
    return render(request, 'home/index.html', {'departments': apAndGal, 'successmsg':successmsg})

def rentals(request):
    departments = Department.objects.all()

    apAndGal=[]
    for apart in departments:
        image=DepartmenGalery.objects.filter(departmen=apart).first()
        apAndGal.append({"depart":apart,"image":image})
    return render(request, 'home/rentals.html', {'departments': apAndGal})

def tenants(request):
    return render(request, 'home/tenants.html', {})

def forms(request):
    return render(request, 'home/forms.html', {})

def thanks(request):
    return render(request, 'home/thanks.html', {})

def maintenance(request):
    errors = []
    if request.method=='POST':
        form = MaintenanceForm(request.POST, request.FILES)
        if form.is_valid():
            name= request.POST.get('name', '')
            email= request.POST.get('email', '')
            if 'file' in request.FILES:
                img = request.FILES['file']
                print img
            else:
                img=None
            enviado=maintenance_send_email(name, email, img, form)
            return HttpResponseRedirect('/?successmsg=True')
        else:
            """Errors"""
            errors.append(form.errors)
            print errors
    else:
        form = MaintenanceForm()

    return render(request, 'home/maintenance.html', {'form': form})

def maintenance_send_email(name, email, img, form):
    subject = 'Maintenance Web Form | ' + name
    from_email, to = SENDER, TO_SEND
    text_template = get_template('emailing/maintenance.txt')
    template = get_template('emailing/maintenance.html')
    context = Context({'f': form })
    text_content = text_template.render(context)
    html_content = template.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    if img:
        msg.attach(img.name, img.read(), img.content_type)
    return msg.send()


def move(request):
    errors = []
    if request.method=='POST':
        form = MoveOutForm(request.POST)
        if form.is_valid():
            """Form Valid"""
            name = form.cleaned_data['name']
            adress = form.cleaned_data['adress']
            sender = form.cleaned_data['email']
            phone = form.cleaned_data['phone_number']
            unit_number = form.cleaned_data['unit_number']
            request_move_out_date = form.cleaned_data['request_move_out_date']
            unit_number= form.cleaned_data['unit_number']
            city = form.cleaned_data['city']
            zip_code = form.cleaned_data['zip_code']
            state = form.cleaned_data['state']
            context = {"name": name, "adress": adress, "email": sender, "phone_number": phone,
                        "unit_number": unit_number, "request_move_out_date" : request_move_out_date,
                        "city": city, "zip_code": zip_code, "state": state}
            text_template = get_template('emailing/move_out.txt')
            html_template = get_template('emailing/move_out.html')
            text_content = text_template.render(context)
            html_content = html_template.render(context)
            subject_msg = "The Enterprise Move Out Web Form | " + name
            with get_connection(
                host=EMAIL_HOST,
                port=EMAIL_PORT,
                username=SENDER_CONTACT,
                password=SENDER_CONTACT_PASS,
                user_tls=EMAIL_USE_TLS
            ) as connection:
                msg = EmailMultiAlternatives(subject_msg, text_content, to=[TO_SEND],connection=connection)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            return HttpResponseRedirect('/?successmsg=True')
        else:
            """Errors"""
            errors.append(form.errors)
            print errors
    else:
        form = MoveOutForm()

    return render(request, 'home/move.html', {"form": form})


def contact(request):
    errors=[]
    if request.method=='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            """Form Valid"""
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['email']
            phone = form.cleaned_data['phone_number']
            message = form.cleaned_data['description']
            context = {"name": name, "subject": subject, "email": sender, "phone_number": phone, "description": message}
            text_template = get_template('emailing/contact.txt')
            html_template = get_template('emailing/contact.html')
            text_content = text_template.render(context)
            html_content = html_template.render(context)
            subject_msg = "The Enterprise Contact Web Form | " + name
            with get_connection(
                host=EMAIL_HOST,
                port=EMAIL_PORT,
                username=SENDER_CONTACT,
                password=SENDER_CONTACT_PASS,
                user_tls=EMAIL_USE_TLS
            ) as connection:
                msg = EmailMultiAlternatives(subject_msg, text_content, to=[TO_SEND],connection=connection)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            return HttpResponseRedirect('/?successmsg=True')
        else:
            """Errors"""
            errors.append(form.errors)
            print errors

    else:
        form = ContactForm()

    return render(request, 'home/contact.html', {"form": form})


def about(request):
    return render(request, 'home/about.html', {})

def faq(request):
    return render(request, 'home/faq.html', {})

def individual(request):
    id_dep = request.GET.get("id", False)
    if id_dep:
        try:
            depa = Department.objects.get(id=id_dep)
        except:
            depa = None
        if depa:
            try:
                manager = Manager.objects.get(building=depa.building)
            except:
                manager = None
            print depa.building
            galery = DepartmenGalery.objects.filter(departmen=depa)
            atraction = NearbyAtraction.objects.filter(building=depa.building)
            return render(request, 'home/individual.html',
                        {"department": depa, "galery":galery, "atraction":atraction, "manager": manager})
    else:
        try:
            depa = Department.objects.first()
        except:
            depa = None
        if depa:
            try:
                manager = Manager.objects.get(building=depa.building)
            except:
                manager = None
            galery = DepartmenGalery.objects.filter(departmen=depa)
            atraction = NearbyAtraction.objects.filter(building=depa.building)
            return render(request, 'home/individual.html',
                        {"department": depa, "galery":"galery", "atraction":atraction, "manager": manager})

    return render(request, 'home/individual.html', {"error": "There is no department available"})



def login(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/admin')

    if request.method=='POST':
        Aform=AuthenticationForm(request.POST)
        if Aform.is_valid:

            user=request.POST['username']
            passw=request.POST['password']


            access=authenticate(username=user,password=passw)

            if access is not None:
                if access.is_active:
                    dj_login(request,access)
                    #Pantalla del Perfil
                    return HttpResponseRedirect('/admin')
                else:
                    error="Possibly your user is disabled, contact your administrator"
            else:
                error="Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive."
        else:
            error="Invalid data"
        ctx={'Aform':Aform, 'error':error, "username":user}
        return render(request, 'admin/admin-sesion.html', ctx)

    else:
        Aform=AuthenticationForm()

    return render(request, 'admin/admin-sesion.html', {'Aform':Aform})



@login_required(login_url="/login/")
def log_out(request):
    dj_logout(request)
    return HttpResponseRedirect('/login')

#Admins


@login_required(login_url="/login/")
def admin(request):
    if SuperAdmin.objects.filter(user = request.user).exists():
        #dash superusuario
        error=None
        activem = None
        if 'removeApart' in request.POST:
            idA=request.POST.get("id","")
            try:
                apart=Department.objects.get(id=idA)
                apart.delete()
            except :
                error="Could not delete"

        if 'removeBuild' in request.POST:
            idA=request.POST.get("id","")
            try:
                build=Building.objects.get(id=idA)
            except :
                error="Could not delete"
                build=None
            if build:
                try:
                    manager=Manager.objects.get(building=build)
                    user=manager.user
                    manager.delete()
                    user.delete()
                except :
                    pass
                build.delete()


        if 'removeManager' in request.POST:
            activem=True
            idM=request.POST.get("id","")
            try:
                manag=Manager.objects.get(id=idM)
                user=manag.user
                manag.delete()
                user.delete()
            except :
                error="Could not delete"

        if 'editManager' in request.POST:
            activem=True
            name =request.POST.get("name","")
            username=request.POST.get("username","")
            email=request.POST.get("email","")
            passw=request.POST.get("password","")
            build=request.POST.get("building","")
            idM=request.POST.get("id","")
            try:
                manag=Manager.objects.get(id=idM)
            except :
                manag=None



            if manag:
                manag.user.first_name=name
                manag.user.username=username
                manag.user.email=email
                manag.user.save()
                if passw:
                    manag.user.set_password(passw)
                    manag.user.save()
                #asignation
                try:
                    building=Building.objects.get(id=build)
                except:
                    building=None
                #x=1/0
                if building:
                    if building:
                        revManager=Manager.objects.filter(building=building)
                        for mang in revManager:
                            mang.building=None
                            mang.save()
                manag.building=building
                manag.save()

            else:
                error="Manager not found"

        if 'newManager' in request.POST:
            activem=True
            name =request.POST.get("name","")
            username=request.POST.get("username","")
            email=request.POST.get("email","")
            passw=request.POST.get("password","")
            build=request.POST.get("building","")

            try:
                building=Building.objects.get(id=build)
            except:
                building=None


            try:
                user = User.objects.create_user(username, email, passw)
                user.first_name=name
                user.save()
                if building:
                    try:
                        revManager=Manager.objects.filter(building=building)
                        for mang in revManager:
                            mang.building=None
                            mang.save()
                    except:
                        pass
                newManager=Manager()
                newManager.user=user
                newManager.building=building
                newManager.save()
            except :
                error="Error creating account Manager, verify that the data are correct or that the username '%s' is not being occupied"%username

        managers=Manager.objects.all()
        buildings=Building.objects.all()
        apartments=Department.objects.all()
        apAndGal=[]
        for apart in apartments:
            image=DepartmenGalery.objects.filter(departmen=apart).first()
            apAndGal.append({"depart":apart,"image":image})


        ctx={'managers':managers, 'buildings':buildings, "apartments":apAndGal, "activem": activem, "error":error}
        return render(request, 'admin/super-admin-home-dash.html',ctx)
    elif Manager.objects.filter(user = request.user).exists():
        if 'removeApart' in request.POST:
            idA=request.POST.get("id","")
            try:
                apart=Department.objects.get(id=idA)
                apart.delete()
            except :
                error="Could not delete"
        #dash Manager
        manag=Manager.objects.get(user = request.user)
        apartments=Department.objects.filter(building=manag.building)

        apAndGal=[]
        for apart in apartments:
            image=DepartmenGalery.objects.filter(departmen=apart).first()
            apAndGal.append({"depart":apart,"image":image})

        return render(request, 'admin/admin-home.html', {"departments":apAndGal, "manager":manag})
    elif request.user.is_staff:
        return HttpResponseRedirect('/djangoadmin')

    else:
        return HttpResponseRedirect('/Doesnthavepermission')

@login_required(login_url="/login/")
def adminBuilding(request):
    if SuperAdmin.objects.filter(user = request.user).exists():
        error=None
        if request.method=='POST':
            idB = request.POST.get("id",False)
            if 'saveBuild' in request.POST:
                idB = request.POST.get("id",False)
                if idB:
                    try:
                        build=Building.objects.get(id=idB)
                    except :
                        build=None
                    if build:
                        Bform =BuildingForm(request.POST, request.FILES, instance=build)
                    else:
                        Bform =BuildingForm(request.POST, request.FILES)
                else:

                    Bform =BuildingForm(request.POST, request.FILES)
                if Bform.is_valid():
                    build=Bform.save()
                    picturesName=request.POST.getlist('pictureAmeniName')
                    atractionsPictures=request.FILES.getlist('pictureAmeni')
                    if atractionsPictures:
                        x=0
                        for pictureA in atractionsPictures:
                            atraction=NearbyAtraction()
                            if picturesName[x]:
                                atraction.titulo_img=picturesName[x]
                            else:
                                atraction.titulo_img="NearbyAtraction"
                            atraction.picture=pictureA
                            atraction.building=build
                            atraction.save()
                            x=x+1


                    return HttpResponseRedirect('/admin')
                error="Error with Data, Try Again"
                return render(request, 'admin/super-admin-edit-building.html', {'Bform':Bform, 'error':error, "id":idB})
            elif 'removeApart' in request.POST:
                idA=request.POST.get("idA","")
                try:
                    apart=Department.objects.get(id=idA)
                    apart.delete()
                except :
                    error="Could not delete"
            elif 'removeAtraction' in request.POST:
                idA=request.POST.get("idA","")
                try:
                    atrac=NearbyAtraction.objects.get(id=idA)
                    atrac.delete()
                except :
                    error="Could not delete"
        else:
            idB = request.GET.get("id","")
        if idB:
            try:
                build=Building.objects.get(id=idB)
            except :
                build=None
            if build:
                #render de datos
                departments=Department.objects.filter(building=build)
                apAndGal=[]
                for apart in departments:
                    image=DepartmenGalery.objects.filter(departmen=apart).first()
                    apAndGal.append({"depart":apart,"image":image})
                atractions=NearbyAtraction.objects.filter(building=build)
                Bform =BuildingForm(instance=build)
                ctx={'Bform':Bform, "id":idB, "apartments":apAndGal, "atractions":atractions}
                return render(request, 'admin/super-admin-edit-building.html',ctx)
            else:
                error="id Not found"
                Bform =BuildingForm()
                return render(request, 'admin/super-admin-edit-building.html',{'Bform':Bform, "error":error})
        else:
            Bform =BuildingForm()
            return render(request, 'admin/super-admin-edit-building.html',{'Bform':Bform})
    else:
        return HttpResponseRedirect('/Doesnthavepermission')


@login_required(login_url="/login/")
def adminDepartment(request):
    editD=False
    manager=None
    superusuario=False
    Dform=DepartmentForm()
    ctx={}
    if SuperAdmin.objects.filter(user = request.user).exists():
        superusuario=True
    elif Manager.objects.filter(user = request.user).exists():
        manager=Manager.objects.get(user = request.user)
        ctx.update({"manager":manager})
        if not manager.building:
           return HttpResponseRedirect('/admin')
    else:
        return HttpResponseRedirect('/Doesnthavepermission')


    if request.method=='POST' and (manager or superusuario):
        idD=request.POST.get("id","")
        if 'removePicture' in request.POST:
            idP=request.POST.get("idP","")
            try:
                picture=DepartmenGalery.objects.get(id=idP)
                picture.delete()
            except :
                pass
        elif 'saveD' in request.POST:
            if not idD:
                Dform=DepartmentForm(request.POST)
                if Dform.is_valid:
                    department=Dform.save()
                    saveGalery(department, request.FILES.getlist('galeria') )
                    return HttpResponseRedirect('/admin')
            else:
                editD=True

    else:
        idD=request.GET.get("id","")
    if idD:
        try:
            depa=Department.objects.get(id=idD)
        except :
            return HttpResponseRedirect('/admin')
        if manager:
            if not manager.building == depa.building:
                return HttpResponseRedirect('/admin')

        if editD:
            Dform=DepartmentForm(request.POST, instance=depa)
            if Dform.is_valid:
                department=Dform.save()
                saveGalery(department, request.FILES.getlist('galeria') )
                return HttpResponseRedirect('/admin')
        else:
            Dform=DepartmentForm(instance=depa)
            galeryD=DepartmenGalery.objects.filter(departmen=depa)
        ctx.update({"Dform":Dform, "idD":idD, "BuildName":depa.building, "galeryD":galeryD})
        try:
            manag=Manager.objects.get(building=depa.building)
            if manag.user.first_name:
                ctx.update({"managerB":manag.user.first_name})
            else:
                ctx.update({"managerB":manag.user.username})
        except :
            pass


    ctx.update({"Dform":Dform})

    return render(request, 'admin/admin-edit-department.html', ctx)

def saveGalery(department, galeryList):
    for image in galeryList:
        tipo=image.content_type
        if tipo == "image/png" or tipo == "image/jpeg":
            galery=DepartmenGalery()
            galery.titulo_img=image.name
            galery.picture=image
            galery.departmen=department
            galery.save()

