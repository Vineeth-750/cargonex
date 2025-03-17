import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
from django.db.models import Avg
from django.shortcuts import render,redirect,HttpResponse
from myapp.models import *

# Create your views here.

ststic_path = r"C:\Users\vineeth\Desktop\cargonex\myapp\static\\"
def admin_home(request):
    return render(request,'admin/index.html')


def logins(request):
    return render(request,'index.html')


def login_post(request):
    name=request.POST['textfield']
    paswrd=request.POST['textfield2']
    log=login.objects.filter(Username=name,password=paswrd)
    if log.exists():
        logid=log[0].id
        request.session['lid']=logid
        if log[0].User_type == 'admin':
             return redirect('/adminhome')
        if log[0].User_type == 'user':
             return redirect('/user_home')
        if log[0].User_type == 'logistics_team':
             return redirect('/logistics_home')
        else:
            return HttpResponse("<script>alert('invalid user');window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('check your entries');window.location='/'</script>")

def change_password(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        return render (request,'admin/change password.html')


def change_password1(request):
    old_passwrd=request.POST['textfield']
    new_passwrd=request.POST['textfield2']
    confrm_pswd=request.POST['textfield3']
    res = login.objects.filter(id=request.session['lid'], password=old_passwrd)
    if res.exists():
        if new_passwrd==confrm_pswd:
            login.objects.filter(id=request.session['lid']).update(password=new_passwrd)
            return redirect('/')
        else:
            return HttpResponse("<script>incorrect password('check your entries');window.location='/change_password'</script>")


    return HttpResponse("<script>alert('Password Changed Successfully');window.location='/admin_home'</script>")


def feedback(request):
    feedback=feedback_rating.objects.all()

    feedback_avg = feedback_rating.objects.aggregate(avg_rating=Avg('rating'))
    average_rating = feedback_avg['avg_rating']
    print(average_rating, "oooooooooooo")
    fs = "/static/star/full.jpg"
    hs = "/static/star/half.jpg"
    es = "/static/star/empty.jpg"
    arr = []
    ar = []

    for rt in feedback:
        # print(rt)
        a = float(rt.rating)

        if a >= 0.0 and a < 0.4:
            ar = [es, es, es, es, es]

        elif a >= 0.4 and a < 0.8:
            ar = [hs, es, es, es, es]

        elif a >= 0.8 and a < 1.4:
            ar = [fs, es, es, es, es]

        elif a >= 1.4 and a < 1.8:
            ar = [fs, hs, es, es, es]

        elif a >= 1.8 and a < 2.4:
            ar = [fs, fs, es, es, es]

        elif a >= 2.4 and a < 2.8:
            ar = [fs, fs, hs, es, es]

        elif a >= 2.8 and a < 3.4:
            ar = [fs, fs, fs, es, es]

        elif a >= 3.4 and a < 3.8:
            ar = [fs, fs, fs, hs, es]

        elif a >= 3.8 and a < 4.4:
            ar = [fs, fs, fs, fs, es]

        elif a >= 4.4 and a < 4.8:
            ar = [fs, fs, fs, fs, hs]

        elif a >= 4.8 and a <= 5.0:
            ar = [fs, fs, fs, fs, fs]
        arr.append({'USER': rt.USER, 'feedback': rt.feedback, 'date': rt.date, 'rating': ar,'LOGISTICS':rt.LOGISTICS,'avg_rating':average_rating})
        # print(arr)

    return render(request,'admin/feedback and rating.html',{'data':arr})

#average feedback
def average_feedback(request):
    feedback = feedback_rating.objects.filter(LOGISTICS__LOGIN=request.session['lid'])

    # Initialize variables to calculate the sum and count of ratings
    total_rating = 0
    rating_count = 0

    # Iterate through each feedback item and accumulate the ratings
    for rt in feedback:
        total_rating += float(rt.rating)
        rating_count += 1

    # Calculate the average rating
    if rating_count > 0:
        average_rating = total_rating / rating_count
        print("Average Rating:", average_rating)
    else:
        print("No ratings available.")


def user(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        return render(request,'admin/user.html')

def complaints(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        complaint=complaints_replies.objects.all()
        return render(request,'admin/complaints.html',{'data':complaint})

def reply(request, id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        return render(request,'admin/reply.html',{'id':id})

def reply_post(request, id):
    reply=request.POST['textarea']
    complaints_replies.objects.filter(id=id).update(
        reply=reply,
        reply_date=datetime.datetime.now().date()
    )
    return HttpResponse(("<script>alert('Replied Successfully');window.location='/complaints'</script>"))



def view_verify_logistics_team(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        res = logistics_team.objects.filter(LOGIN__User_type='pending')
        return render(request,'admin/view&verify Logistics team.html', {'data': res})

def verify_logistics(request, id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        login.objects.filter(id=id).update(User_type='logistics_team')
        return HttpResponse(("<script>alert('Approved');window.location='/view_verify_logistics_team'</script>"))

def reject_logistics(request, id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        login.objects.get(id=id).delete()
        return HttpResponse(("<script>alert('Rejected');window.location='/view_verify_logistics_team'</script>"))

def view_logistics_team(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        res = logistics_team.objects.filter(LOGIN__User_type='logistics_team')
        l = []

        fs = "/static/star/full.jpg"
        hs = "/static/star/half.jpg"
        es = "/static/star/empty.jpg"

        for i in res:
            feedback_avg = feedback_rating.objects.aggregate(avg_rating=Avg('rating'))
            average_rating = feedback_avg['avg_rating'] or 0  # If no rating, set average_rating to 0

            print("Average rating for", i.company_name, ":",
                  average_rating)  # Print average rating for each logistics team

            # Logic to determine rating categories
            if average_rating >= 0.0 and average_rating < 0.4:
                ar = [es, es, es, es, es]
            elif average_rating >= 0.4 and average_rating < 0.8:
                ar = [hs, es, es, es, es]
            elif average_rating >= 0.8 and average_rating < 1.4:
                ar = [fs, es, es, es, es]
            elif average_rating >= 1.4 and average_rating < 1.8:
                ar = [fs, hs, es, es, es]
            elif average_rating >= 1.8 and average_rating < 2.4:
                ar = [fs, fs, es, es, es]
            elif average_rating >= 2.4 and average_rating < 2.8:
                ar = [fs, fs, hs, es, es]
            elif average_rating >= 2.8 and average_rating < 3.4:
                ar = [fs, fs, fs, es, es]
            elif average_rating >= 3.4 and average_rating < 3.8:
                ar = [fs, fs, fs, hs, es]
            elif average_rating >= 3.8 and average_rating < 4.4:
                ar = [fs, fs, fs, fs, es]
            elif average_rating >= 4.4 and average_rating < 4.8:
                ar = [fs, fs, fs, fs, hs]
            elif average_rating >= 4.8 and average_rating <= 5.0:
                ar = [fs, fs, fs, fs, fs]
            else:
                ar = ['N/A', 'N/A', 'N/A', 'N/A', 'N/A']  # Handle any other cases

            l.append({
                "reg_id": i.reg_id,
                "company_name": i.company_name,
                "post_address": i.post_address,
                "contact": i.contact,
                "pincode": i.pincode,
                "website": i.website,
                "email": i.email,
                "contact_name": i.contact_name,
                "freigt_forwarder_license_image": i.freigt_forwarder_license_image,
                "Transportation_Permits": i.Transportation_Permits,
                "other_license_and_permits": i.other_license_and_permits,
                "latitude": i.latitude,
                "longitude": i.longitude,
                "country": i.country,
                "id": i.id,
                "average_rating": average_rating,
                "rating": ar,  # Add rating category list to the dictionary
            })

        print(l)
        return render(request, 'admin/view Logistics team.html', {'data': l})


def view_logistics_team_kick(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        res=logistics_team.objects.get(id=id)
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("cargonex9@gmail.com", "ieyc jkrg xsyx gtrt")
        msg = MIMEMultipart()  # create a message.........."
        msg['From'] = "cargonex9@gmail.com"
        msg['To'] = res.email
        msg['Subject'] = "Notice of Termination of Service Contract"
        body ="I hope this message finds you well.After careful consideration and numerous discussions, we regret to inform you that we have decided to terminate our service contract with "+str(res.company_name)+" effective immediately. This decision has been made due to consistent issues with the quality of service provided, which have not met our expectations despite multiple attempts to resolve these concerns.We appreciate your understanding in this matter."
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)
        login.objects.filter(id=res.LOGIN.id).update(User_type='blocked')
        return HttpResponse("<script>alert('kicked Successfull');window.location='/view_logistics_team'</script>")
def view_users(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        res = User.objects.all()
        return render(request, 'admin/view_users.html', {'data': res})

def update_regisister_logistics(request):
    res=logistics_team.objects.get(LOGIN=request.session['lid'])
    return render(request,'Logistics_team/update_Logistics team.html',{'data':res})

def update_regisister_logistics_post(request):
    try:
        reg_id=request.POST['textfield9']
        company_name=request.POST['textfield2']
        post_address=request.POST['textfield10']
        contact=request.POST['textfield6']
        pincode=request.POST['textfield7']
        website=request.POST['textfield3']
        email=request.POST['textfield4']
        contact_pearson=request.POST['textfield5']
        freight_forwarder_image=request.FILES['fileField']
        d = datetime.datetime.now().strftime('%d%m%Y-%H%M%S')
        FileSystemStorage().save(ststic_path+"logistics_image\\"+d+'.jpg', freight_forwarder_image)
        country=request.POST['textfield9']
        logistics_team.objects.filter(LOGIN=request.session['lid']).update(reg_id=reg_id,company_name=company_name,
        contact_name = contact_pearson,email=email,freigt_forwarder_license_image="/static/logistics_image/"+d+'.jpg',
                                                                           country=country,pincode=pincode,post_address=post_address,website=website,contact=contact)
        return HttpResponse("<script>alert('U');window.location='/update_regisister_logistics'</script>")
    except Exception as e:
        reg_id = request.POST['textfield9']
        company_name = request.POST['textfield2']
        post_address = request.POST['textfield10']
        contact = request.POST['textfield6']
        pincode = request.POST['textfield7']
        website = request.POST['textfield3']
        email = request.POST['textfield4']
        contact_pearson = request.POST['textfield5']
        country = request.POST['textfield9']
        logistics_team.objects.filter(LOGIN=request.session['lid']).update(reg_id=reg_id, company_name=company_name,
                                                                           contact_name=contact_pearson, email=email,
                                                                           country=country, pincode=pincode,
                                                                           post_address=post_address, website=website,
                                                                           contact=contact)
        return HttpResponse("<script>alert('U');window.location='/update_regisister_logistics'</script>")

def regisister_logistics(request):
    return render(request,'signin.html')

def regisister_logistics_post(request):
    print(request.POST)
    reg_id=request.POST['textfield9']
    company_name=request.POST['textfield2']
    post_address=request.POST['textfield10']
    contact=request.POST['textfield6']
    pincode=request.POST['textfield7']
    website=request.POST['textfield3']
    email=request.POST['textfield4']
    contact_pearson=request.POST['textfield5']

    freight_forwarder_image=request.FILES['fileField']
    d = datetime.datetime.now().strftime('%d%m%Y-%H%M%S')
    FileSystemStorage().save(ststic_path+"logistics_image\\"+d+'.jpg', freight_forwarder_image)
    transport_permit=request.POST.getlist('CheckboxGroup1')
    permits_and_certifications=request.POST.getlist('CheckboxGroup2')
    print()
    country=request.POST['textfield9']
    latitude=request.POST['textfield11']
    longitude=request.POST['textfield12']
    password=request.POST['textfield8']
    if login.objects.filter(Username=email).exists():
        return HttpResponse("<script>alert('User already Exist');window.location='/'</script>")
    log = login()
    log.Username=email
    log.User_type='pending'
    log.password=password
    log.save()
    obj = logistics_team()
    obj.LOGIN=log
    obj.reg_id=reg_id
    obj.company_name=company_name
    obj.contact_name=contact_pearson
    obj.email=email
    obj.freigt_forwarder_license_image="/static/logistics_image/"+d+'.jpg'
    obj.pincode=pincode
    obj. post_address=post_address
    obj.website=website
    obj.Transportation_Permits=transport_permit
    obj.contact=contact
    obj.other_license_and_permits=permits_and_certifications
    obj.latitude=latitude
    obj.longitude=longitude
    obj.country=country
    obj.save()
    return HttpResponse("<script>alert('Registation Successfull');window.location='/'</script>")



#logistics module

def logistics_home(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        return render(request,'Logistics_team/index.html')




def change_password2(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        return render (request,'logistics_team/logistics_confirmpassword.html')

def change_password3(request):
    old_passwrd=request.POST['textfield']
    new_passwrd=request.POST['textfield2']
    confrm_pswd=request.POST['textfield3']
    res = login.objects.filter(id=request.session['lid'], password=old_passwrd)
    if res.exists():
        if new_passwrd==confrm_pswd:
            login.objects.filter(id=request.session['lid']).update(password=new_passwrd)
            return HttpResponse("<script>alert('Password Changed Successfully');window.location='/logistics_home'</script>")
        else:
            return HttpResponse("<script>alert('check your entries');window.location='/change_password'</script>")
    return HttpResponse("<script>alert('Password Changed Successfully');window.location='/logistics_home'</script>")




def feedback1(request):
    feedback=feedback_rating.objects.filter(LOGISTICS__LOGIN=request.session['lid'])
    fs = "/static/star/full.jpg"
    hs = "/static/star/half.jpg"
    es = "/static/star/empty.jpg"
    arr = []
    ar = []

    for rt in feedback:
        print(rt)
        a = float(rt.rating)

        if a >= 0.0 and a < 0.4:
            ar = [es, es, es, es, es]

        elif a >= 0.4 and a < 0.8:
            ar = [hs, es, es, es, es]

        elif a >= 0.8 and a < 1.4:
            ar = [fs, es, es, es, es]

        elif a >= 1.4 and a < 1.8:
            ar = [fs, hs, es, es, es]

        elif a >= 1.8 and a < 2.4:
            ar = [fs, fs, es, es, es]

        elif a >= 2.4 and a < 2.8:
            ar = [fs, fs, hs, es, es]

        elif a >= 2.8 and a < 3.4:
            ar = [fs, fs, fs, es, es]

        elif a >= 3.4 and a < 3.8:
            ar = [fs, fs, fs, hs, es]

        elif a >= 3.8 and a < 4.4:
            ar = [fs, fs, fs, fs, es]

        elif a >= 4.4 and a < 4.8:
            ar = [fs, fs, fs, fs, hs]

        elif a >= 4.8 and a <= 5.0:
            ar = [fs, fs, fs, fs, fs]
        arr.append({'USER':rt.USER,'feedback':rt.feedback,'date':rt.date,'rating':ar})
        # print(arr)
    #     ================
    feedback_avg = feedback_rating.objects.filter(LOGISTICS__LOGIN=request.session['lid']).aggregate(avg_rating=Avg('rating'))
    average_rating = feedback_avg['avg_rating'] or 0  # If no rating, set average_rating to 0
    ar1=[]
    # Logic to determine rating categories
    if average_rating >= 0.0 and average_rating < 0.4:
        ar1 = [es, es, es, es, es]
    elif average_rating >= 0.4 and average_rating < 0.8:
        ar1 = [hs, es, es, es, es]
    elif average_rating >= 0.8 and average_rating < 1.4:
        ar1 = [fs, es, es, es, es]
    elif average_rating >= 1.4 and average_rating < 1.8:
        ar1 = [fs, hs, es, es, es]
    elif average_rating >= 1.8 and average_rating < 2.4:
        ar1 = [fs, fs, es, es, es]
    elif average_rating >= 2.4 and average_rating < 2.8:
        ar1 = [fs, fs, hs, es, es]
    elif average_rating >= 2.8 and average_rating < 3.4:
        ar1 = [fs, fs, fs, es, es]
    elif average_rating >= 3.4 and average_rating < 3.8:
        ar1 = [fs, fs, fs, hs, es]
    elif average_rating >= 3.8 and average_rating < 4.4:
        ar1 = [fs, fs, fs, fs, es]
    elif average_rating >= 4.4 and average_rating < 4.8:
        ar1 = [fs, fs, fs, fs, hs]
    elif average_rating >= 4.8 and average_rating <= 5.0:
        ar1 = [fs, fs, fs, fs, fs]
    else:
        ar1 = ['N/A', 'N/A', 'N/A', 'N/A', 'N/A']  # Handle any other cases
    print(ar1,"--------")
    print(average_rating,"=avg=")
    # ==================
    # return render_template('admin/adm_view_apprating.html',data=re33,r1=ar,ln=len(ar55))
    # return render_template('vew app raiting.html', resu=res, r1=arr, ln=len(arr))
    return render(request,'logistics_team/feedback and rating.html',{'data':arr,'ar1':ar1,'average_rating':average_rating})

def verify_logistic_request(request):
    res = logistics_request.objects.filter(status='pending', LOGISTICS_TEAM__LOGIN=request.session['lid'])
    li = []
    for i in res:
        li.append({
            'seller_name': i.ORDER.RECUSER.Username,
            'Place':i.ORDER.RECUSER.country,
            'Pincode':i.ORDER.RECUSER.pincode,
            'lati':i.ORDER.latitude,
            'longi':i.ORDER.latitude,
            'Email':i.ORDER.RECUSER.email,
            'Contact':i.ORDER.RECUSER.phone,
            'buyer_name': i.ORDER.REQUSER.Username,
            'buyer_Place':i.ORDER.REQUSER.country,
            'buyer_Pincode':i.ORDER.REQUSER.pincode,
            'buyer_lati':i.ORDER.latitude,
            'buyer_longi':i.ORDER.longitude,
            'buyer_email':i.ORDER.REQUSER.email,
            'buyer_contact':i.ORDER.REQUSER.phone,
            'date':i.ORDER.date,
            'id':i.id


        })
    return render(request,'Logistics_team/verify_request.html', {'data': li})


def aprove_logistic_request(request, id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfully');window.location='/'</script>")
    else:
        return render(request, 'Logistics_team/set_del_charge.html', {"id": id})


def aprove_logistic_request_post(request, id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        am = request.POST['amount']
        logistics_request.objects.filter(id=id).update(status='approved', amount=am)
        return HttpResponse(("<script>alert('Approved');window.location='/verify_logistic_request'</script>"))

def reject_logistic_request(request, id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        logistics_request.objects.get(id=id).delete(status='rejected')
        return HttpResponse(("<script>alert('Rejected');window.location='/verify_logistic_request'</script>"))

def verified_logistic_request(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        print(request.session['lid'],"aaa")
        res = logistics_request.objects.filter(status='Approved', LOGISTICS_TEAM__LOGIN=request.session['lid'])
        print(res)
        li = []
        for i in res:
            isDelivered = False
            obj = tracker.objects.filter(LOGISTIC_REQUEST=i).order_by('-id')
            if obj.exists():
                if obj[0].status == "delivered":
                    isDelivered = True
            li.append({
                'seller_name': i.ORDER.RECUSER.Username,
                'Place': i.ORDER.RECUSER.country,
                'Pincode': i.ORDER.RECUSER.pincode,
                'lati': i.ORDER.latitude,
                'longi': i.ORDER.latitude,
                'Email': i.ORDER.RECUSER.email,
                'Contact': i.ORDER.RECUSER.phone,
                'buyer_name': i.ORDER.REQUSER.Username,
                'buyer_Place': i.ORDER.REQUSER.country,
                'buyer_Pincode': i.ORDER.REQUSER.pincode,
                'buyer_lati': i.ORDER.latitude,
                'buyer_longi': i.ORDER.longitude,
                'buyer_email': i.ORDER.REQUSER.email,
                'buyer_contact': i.ORDER.REQUSER.phone,
                'date': i.ORDER.date,
                'id': i.id,
                'amount': i.amount,
                'isDelivered': isDelivered
            })
        return render(request,'Logistics_team/verified_request.html', {'data': li})



#user

def register_User(request):
    return render(request,'sign_in_user.html')

def register_User_Post(request):
    first_name=request.POST['textfield']
    lastname=request.POST['textfield2']
    email=request.POST['textfield3']
    contact=request.POST['textfield4']
    post_address=request.POST['textfield5']
    pincode=request.POST['textfield6']
    home_town=request.POST['textfield7']
    country=request.POST['textfield8']
    state=request.POST['textfield9']
    impot_expot_license=request.POST['textfield10']
    industrial_type=request.POST['jumpMenu']
    passwrd=request.POST['textfield11']
    latitude = request.POST['textfield11']
    longitude = request.POST['textfield12']
    log = login()
    log.Username=email
    log.User_type='user'
    log.password=passwrd
    log.save()
    obj=User()
    obj.LOGIN=log
    obj.Username= first_name+" "+lastname
    obj.email=email
    obj.phone=contact
    obj.near_by_town=home_town
    obj.country=country
    obj.pincode=pincode
    obj.address=post_address
    obj.Expt_Impt_license_no=impot_expot_license
    obj.industry=industrial_type
    obj.state=state
    obj.latitude = latitude
    obj.longitude = longitude
    obj.save()
    return HttpResponse("<script>alert('Registation Successfull');window.location='/'</script>")


def update_user(request):
    res=User.objects.get(LOGIN=request.session['lid'])
    return render(request,'User/view_ and_update_profile.html',{'data':res})

def update_User_Post(request):
    Name=request.POST['textfield']
    email=request.POST['textfield3']
    contact=request.POST['textfield4']
    post_address=request.POST['textfield5']
    pincode=request.POST['textfield6']
    home_town=request.POST['textfield7']
    country=request.POST['textfield8']
    state=request.POST['textfield9']
    impot_expot_license=request.POST['textfield10']
    industrial_type=request.POST['jumpMenu']
    User.objects.filter(LOGIN=request.session['lid']).update(Username=Name,email=email,phone=contact,near_by_town= home_town,country=country,pincode=pincode,address=post_address,state=state,Expt_Impt_license_no=impot_expot_license,industry=industrial_type)
    return HttpResponse("<script>alert('Updated Successfull');window.location='/update_user'</script>")


def user_home(request):
    obj = tracker.objects.filter(status="delivered", LOGISTIC_REQUEST__ORDER__REQUSER__LOGIN=request.session['lid'])
    arr = []
    for i in obj:
        am = 0
        am += float(i.LOGISTIC_REQUEST.amount)
        am+= float(i.LOGISTIC_REQUEST.ORDER.amount)
        arr.append({"LOGISTIC_REQUEST": i.LOGISTIC_REQUEST,
                    "amount": am,
                    "date": i.date,})
    return render(request,'User/index.html', {"data": arr})

def add_product(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/add_product'</script>")
    else:
        return render(request,'User/product_reg.html')
def add_product_post(request):
    product_name=request.POST['textfield']
    price=request.POST['textfield2']
    q=request.POST['q']
    image=request.FILES['fileField']
    d = datetime.datetime.now().strftime('%d%m%Y-%H%M%S')
    FileSystemStorage().save(ststic_path+"product\\"+d+'.jpg', image)
    description=request.POST['textarea']

    obj=products()
    obj.USER = User.objects.get(LOGIN=request.session['lid'])
    obj.productname=product_name
    obj.price=price
    obj.quntity=q
    obj.image="/static/product/"+d+'.jpg'
    obj.description=description
    obj.save()
    return HttpResponse("<script>alert('Product Added Successfully');window.location='/add_product'</script>")

def view_my_product(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/view_my_product'</script>")
    else:
        res = products.objects.filter(USER__LOGIN=request.session['lid'])
        return render(request,'User/view my product.html',{'data':res})

def delete_product(request, id):
    products.objects.filter(id=id).delete()
    return HttpResponse("<script>alert('Deleted Successfull');window.location='/view_my_product'</script>")


def product_update(request, id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/view_my_product'</script>")
    else:
        res = products.objects.get(id=id)

        return render(request,'User/product_update.html',{'data':res})

def product_update_post(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('update Successfull');window.location='/view_my_product'</script>")
    else:
      try:
            product_name=request.POST['textfield']
            price=request.POST['textfield2']
            q=request.POST['q']
            image=request.FILES['fileField']
            d = datetime.datetime.now().strftime('%d%m%Y-%H%M%S')
            FileSystemStorage().save(ststic_path + "product\\" + d + '.jpg', image)
            description=request.POST['textarea']
            products.objects.filter(id=id).update(
                productname=product_name,
                price=price,
                quntity=q,
                image="/static/product/"+d+'.jpg',
                description=description
            )
            return HttpResponse("<script>alert('Updated Successfully');window.location='/view_my_product'</script>")
      except Exception as e:
          product_name = request.POST['textfield']
          price = request.POST['textfield2']
          q = request.POST['q']
          description = request.POST['textarea']
          products.objects.filter(id=id).update(
              productname=product_name,
              price=price,
              quntity=q,
              description=description
          )
          return HttpResponse("<script>alert('Updated Successfully');window.location='/view_my_product'</script>")

def view_product(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        res = products.objects.all().exclude(USER__LOGIN=request.session['lid'])
        return render(request,'User/view_product.html',{'data':res})

def request_product(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('request Successfull');window.location='/view_product'</script>")
    else:
        cart(
            PRODUCTS_id=request.POST['id'],
            USER=User.objects.get(LOGIN=request.session['lid']),
            quantity=request.POST['qty']
        ).save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/view_product'</script>")

def view_request(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        return render(request,'User/view_request.html')

def view_cart(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        res=cart.objects.filter(USER__LOGIN=request.session['lid'])
        sum=0
        for i in res:
            print(i.quantity,"quty")
            print(i.PRODUCTS.price,"pricee")
            amnt=int(i.PRODUCTS.price)*int(i.quantity)

            sum=amnt+sum

        return render(request,'User/view_cart.html',{'data':res,'sum':sum})

def add_order(request, id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        res = cart.objects.get(id=id)
        a = float(res.quantity) * float(res.PRODUCTS.price)
        oo = order(
            USER=User.objects.get(LOGIN=request.session['lid']),
            amount=a,
            date=datetime.datetime.now().date(),
            payment_date='pending',
            payment_status='pending',

        )
        oo.save()
        order_Sub(
            ORDER=oo,
            PRODUCTS_id=res.PRODUCTS.id,
            quantity=res.quantity

        ).save()
        cart.objects.get(id=id).delete()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/view_cart'</script>")
def order_status(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        arr = []
        res = order.objects.filter(REQUSER__LOGIN=request.session['lid'])
        for i in res:
            can_pay = False
            rr=logistics_request.objects.filter(ORDER=i)
            if rr.exists():
                rr=rr[0]
                if rr.amount != "pending":
                    can_pay = True


            arr.append({"RECUSER": i.RECUSER,
                        "status": i.status,
                        "date": i.date,
                        "amount": i.amount,
                        "payment_date": i.payment_date,
                        "payment_status": i.payment_status,
                        "id": i.id,
                        "can_pay": can_pay})
        print(arr)
        return render(request,'User/order.html',{'data':arr})


def view_products(request, id):
    obj = order_Sub.objects.filter(ORDER=id)
    arr = []
    for i in obj:
        t = float(i.PRODUCTS.price)*float(i.quantity)
        arr.append({"productname": i.PRODUCTS.productname,
                    "quantity": i.quantity,
                    "total": t})
    return render(request, 'User/view_products.html', {"data": arr})


def view_orders(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        res = order.objects.filter(RECUSER__LOGIN=request.session['lid']).order_by('-id')
        arr = []
        for i in res:
            isAllocated = "false"
            ob = logistics_request.objects.filter(ORDER=i)
            if ob.exists():
                isAllocated = ob[0].LOGISTICS_TEAM.company_name
            arr.append({"date": i.date,
                        "amount": i.amount,
                        "username": i.REQUSER.Username,
                        "id": i.id,
                        "payment_date": i.payment_date,
                        "payment_status": i.payment_status,
                        "isAllocated": isAllocated})
        return render(request,'User/view_order.html',{'data':arr})

def aprove_order(request, id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        order.objects.filter(id=id).update(status='Approved')
        return HttpResponse(("<script>alert('Approved');window.location='/view_order'</script>"))

def reject_order(request, id):
    order.objects.filter(id=id).update(status='rejected')
    return HttpResponse(("<script>alert('Rejected');window.location='/view_order'</script>"))

def logistics_team_request(request, id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        res = logistics_team.objects.all()
        return render(request,'User/view Logistics team.html',{'data':res, 'id': id})


def send_request(request, loid, rid):
    logistics_request(
        LOGISTICS_TEAM_id=loid,
        ORDER_id=rid,
        date=datetime.datetime.now().strftime('%d-%m-%Y, %H:%M:%S'),
        payment_date='pending',
        payment_status='pending',
        amount='pending',
        status='pending'
    ).save()
    order.objects.filter(id=rid).update(status='Approved')
    # ==================
    res=order.objects.filter(id=rid)
    for i in res:
        es = order_Sub.objects.filter(ORDER_id=i.id)
        for j in es:
            products.objects.filter(id=j.PRODUCTS.id).update(quntity=int(j.PRODUCTS.quntity)-int(j.quantity))
    return HttpResponse("<script>alert('Requested');window.location='/user_home'</script>")



def change_password4(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        return render (request,'User/change password.html')


def change_password5(request):
    old_passwrd=request.POST['textfield']
    new_passwrd=request.POST['textfield2']
    confrm_pswd=request.POST['textfield3']
    res = login.objects.filter(id=request.session['lid'], password=old_passwrd)
    if res.exists():
        if new_passwrd==confrm_pswd:
            login.objects.filter(id=request.session['lid']).update(password=new_passwrd)
            return HttpResponse("<script>alert('Password Changed Successfully');window.location='/user_home'</script>")
        else:
            return HttpResponse("<script>alert('check your entries');window.location='/change_password'</script>")


    return HttpResponse("<script>alert('Password Changed Successfully');window.location='/user_home'</script>")

def complaint(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
         return render(request,'User/Complaints.html')

def complaint_post(request):
    complaint=request.POST['textarea']
    complaint_date = datetime.datetime.now().strftime('%d%m%Y-%H%M%S')
    complaints_replies(
    USER=User.objects.get(LOGIN=request.session['lid']),
    complaint=complaint,
    complaint_date=complaint_date,
    reply='pending'
    ).save()
    return HttpResponse("<script>alert('Complainte Added Successfully');window.location='/'</script>")

def view_reply(request):
    res=complaints_replies.objects.filter(USER=User.objects.get(LOGIN=request.session['lid']))
    return render(request,'User/reply.html', {'data': res})

def view_logistic_team_status(request):
    res=order_Sub.objects.filter(PRODUCTS__USER__LOGIN=request.session['lid'])
    li = []
    for i in res:
        log = logistics_request.objects.filter(ORDER=i.ORDER.id)
        if log.exists():
            log = log[0]
            li.append({
                'product': i.PRODUCTS.productname,
                'Buyer':log.ORDER.REQUSER.Username,
                'Request_Date':log.date,
                'Logistic_Team':log.LOGISTICS_TEAM.company_name,
                'request_status':log.status,
                'liid':log.LOGISTICS_TEAM_id,
                'oid':log.ORDER_id,
            })
    return render(request,'User/logistic_request_status.html',{'data':li})

def user_feedback(request,id):
    request.session['logid'] = id
    return render(request,'User/feedback.html')

def user_feedback_post(request):
    feedback=request.POST['textarea']
    rating=request.POST['star']
    date= datetime.datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    feedback_rating(
    USER = User.objects.get(LOGIN=request.session['lid']),
    feedback=feedback,
    rating=rating,
    date=date,
    LOGISTICS_id=request.session['logid']
     ).save()
    return HttpResponse("<script>alert('Feedback Added Successfully');window.location='/'</script>")

def delete_order(request,id):
    cart.objects.get(id=id).delete()
    return HttpResponse("<script>alert('deleted');window.location='/'</script>")

def estimation(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('logout Successfull');window.location='/'</script>")
    else:
        return render(request,'User/estimation.html')

def estimation_post(request):
    lat=request.POST['textfield']
    lon=request.POST['textfield2']
    res = cart.objects.filter(USER__LOGIN=request.session['lid'])
    ar = []
    for i in res:
        if i.PRODUCTS.USER.id not in ar:
            ar.append(i.PRODUCTS.USER_id)
    for i in ar:
        q = cart.objects.filter(PRODUCTS__USER=i)
        sum = 0
        for p in q:
            sum+=float(p.PRODUCTS.price)*float(p.quantity)

        obj = order()
        obj.date = datetime.datetime.now().strftime("%Y-%m-%d")
        obj.REQUSER = User.objects.get(LOGIN=request.session['lid'])
        obj.RECUSER_id = i
        obj.amount = sum
        obj.latitude = lat
        obj.longitude = lon
        obj.status = "pending"
        obj.save()

        for j in q:
            ob = order_Sub()
            ob.quantity = j.quantity
            ob.PRODUCTS = j.PRODUCTS
            ob.ORDER = obj
            ob.save()
    cart.objects.filter(USER__LOGIN=request.session['lid']).delete()
    return HttpResponse("<script>alert('updated');window.location='/view_cart'</script>")



def logout(request):
    request.session['lid']=''
    return HttpResponse("<script>alert('Logout Successfully');window.location='/'</script>")


def logoistic_view_products(request, id):
    obj = order_Sub.objects.filter(ORDER=id)
    arr = []
    for i in obj:
        t = float(i.PRODUCTS.price) * float(i.quantity)
        arr.append({"productname": i.PRODUCTS.productname,
                    "quantity": i.quantity,
                    "total": t})
    return render(request, 'Logistics_team/view_products.html', {"data": arr})


def view_invoice(request, id):
    obj = order_Sub.objects.filter(ORDER=id)
    arr = []
    total = 0
    delamt = float(logistics_request.objects.get(ORDER=id).amount)
    for i in obj:
        am = float(i.quantity)*float(i.PRODUCTS.price)
        total+=am
        arr.append({"product": i.PRODUCTS.productname,
                    "quantity": i.quantity,
                    "amount": am})

    return render(request, 'User/view_invoice.html', {"data": arr, "total": total, "delamount": delamt, "id": id, "gt": total+delamt})


def pay(request, id):
    import razorpay

    razorpay_api_key = "rzp_test_MJOAVy77oMVaYv"
    razorpay_secret_key = "MvUZ03MPzLq3lkvMneYECQsk"

    razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))
    obj = order_Sub.objects.filter(ORDER=id)
    delamt = float(logistics_request.objects.get(ORDER=id).amount)
    total = 0
    for i in obj:
        am = float(i.quantity)*float(i.PRODUCTS.price)
        total+=am
    total += delamt
    amount = total*100
    # amount = float(amount)

    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',  # Auto-capture payment
    }

    # Create an order
    order = razorpay_client.order.create(data=order_data)

    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id'],
        'id': id
    }

    return render(request, 'User/payment.html', context)


def complete_payment(request, id):
    order.objects.filter(id=id).update(payment_status="paid", payment_date=datetime.datetime.now().strftime("%Y-%m-%d"))
    return redirect('/order_status#oo')


def track_product(request, id):
    obj = tracker.objects.filter(LOGISTIC_REQUEST__ORDER=id)
    isDelivered = "false"
    for i in obj:
        if i.status == "delivered":
            isDelivered = i.date +" "+i.time
    return render(request, 'User/track_order.html', {"data": obj, "isDelivered": isDelivered})


def update_tracking(request, id):
    obj = tracker.objects.filter(LOGISTIC_REQUEST=id)
    isDelivered = False
    if obj.exists():
        ob = obj.order_by('-id')
        if ob[0].status == "delivered":
            isDelivered = True

    return render(request, 'Logistics_team/track_updates.html', {"data": obj, "id": id, "isDelivered": isDelivered})


def update_tracking_post(request, id):
    status = request.POST['status']
    place = request.POST['place']
    obj = tracker()
    obj.LOGISTIC_REQUEST_id = id
    obj.date = datetime.datetime.now().strftime("%Y-%m-%d")
    obj.time = datetime.datetime.now().strftime("%H:%M")
    obj.status = status
    obj.location = place
    obj.save()
    return redirect('/update_tracking/'+id+"#oo")
