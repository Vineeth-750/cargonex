from django.db import models

# Create your models here.

class login(models.Model):
    Username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    User_type=models.CharField(max_length=50)

class User(models.Model):
    LOGIN=models.ForeignKey(login,on_delete=models.CASCADE)
    Username=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    near_by_town=models.CharField(max_length=50,default=1)
    country=models.CharField(max_length=50)
    pincode=models.CharField(max_length=50)
    address=models.CharField(max_length=50,default=1)
    Expt_Impt_license_no=models.CharField(max_length=50,default=1)
    industry=models.CharField(max_length=50,default=1)
    state=models.CharField(max_length=50,default=1)
    latitude=models.CharField(max_length=50,default=1)
    longitude=models.CharField(max_length=50,default=1)


class complaints_replies(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    complaint=models.CharField(max_length=100)
    complaint_date=models.CharField(max_length=20)
    reply=models.CharField(max_length=100)
    reply_date=models.CharField(max_length=20)

class logistics_team(models.Model):
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE)
    reg_id=models.CharField(max_length=50,default=1)
    company_name=models.CharField(max_length=50,default=1)
    contact_name=models.CharField(max_length=50,default=1)
    email=models.CharField(max_length=50,default=1)
    post_address=models.CharField(max_length=50)
    Transportation_Permits=models.CharField(max_length=100,default=1)
    freigt_forwarder_license_image=models.CharField(max_length=50)
    website=models.CharField(max_length=50,default=1)
    country=models.CharField(max_length=50,default=1)
    pincode=models.CharField(max_length=50,default=1)
    latitude=models.CharField(max_length=50,default=1)
    longitude=models.CharField(max_length=50,default=1)
    other_license_and_permits=models.CharField(max_length=100,default=1)
    contact=models.CharField(max_length=50,default=1)

class feedback_rating(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    LOGISTICS=models.ForeignKey(logistics_team,on_delete=models.CASCADE,default=1)
    date=models.CharField(max_length=50)
    feedback=models.CharField(max_length=50)
    rating=models.CharField(max_length=50)
    avgrating=models.CharField(max_length=50,default=1)

class products(models.Model):
    USER= models.ForeignKey(User,on_delete=models.CASCADE)
    productname=models.CharField(max_length=50)
    image=models.CharField(max_length=50)
    quntity=models.CharField(max_length=50)
    date=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    price=models.CharField(max_length=50,default=1)

class order(models.Model):
    date=models.CharField(max_length=50)
    REQUSER=models.ForeignKey(User,on_delete=models.CASCADE, related_name="requesteduser")
    RECUSER=models.ForeignKey(User,on_delete=models.CASCADE, related_name="recieveduser")
    amount=models.CharField(max_length=50)
    payment_date=models.CharField(max_length=50,default="pending")
    payment_status=models.CharField(max_length=50,default="pending")
    latitude=models.CharField(max_length=50,default=1)
    longitude=models.CharField(max_length=50,default=1)
    status=models.CharField(max_length=50,default=1)


class order_Sub(models.Model):
    ORDER =models.ForeignKey(order,on_delete=models.CASCADE)
    PRODUCTS=models.ForeignKey(products,on_delete=models.CASCADE)
    quantity=models.CharField(max_length=100)

class logistics_request(models.Model):
    ORDER=models.ForeignKey(order,on_delete=models.CASCADE,default=1)
    LOGISTICS_TEAM=models.ForeignKey(logistics_team,on_delete=models.CASCADE)
    date=models.CharField(max_length=50)
    payment_date=models.CharField(max_length=50,default=1)
    payment_status=models.CharField(max_length=50,default=1)
    status=models.CharField(max_length=50)
    amount=models.CharField(max_length=50,default=1)

class payment(models.Model):
    ORDER=models.ForeignKey(order,on_delete=models.CASCADE,default=1)
    date=models.CharField(max_length=50)
    amount=models.CharField(max_length=50)
    payment_status=models.CharField(max_length=50)



class cart(models.Model):
    PRODUCTS=models.ForeignKey(products,on_delete=models.CASCADE)
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity=models.CharField(max_length=50,default=1)

class tracker(models.Model):
    LOGISTIC_REQUEST = models.ForeignKey(logistics_request, on_delete=models.CASCADE)
    time=models.CharField(max_length=50)
    date=models.CharField(max_length=50)
    status=models.CharField(max_length=50,default=1)
    location=models.CharField(max_length=50,default=1)