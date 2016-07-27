from django.shortcuts import render
from django.shortcuts import render_to_response
from classviews import *
import datetime
from django.db.models import Max
import smtplib
from django.template import loader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import os
import django
from django.conf import settings
from django.views.decorators.csrf import csrf_protect

#https://accounts.google.com/DisplayUnlockCaptcha

sys.path.append("C:/Users/NIcky Koganti/PycharmProjects/online_acuction_system")
os.environ["DJANGO_SETTINGS_MODULE"]="online_auction_system.settings"
django.setup()

def mailing(bidder, seller):
    template = loader.get_template("auction_system/college_mail.html")
    if (bidder == 0):
        result = template.render(context={'status': "Your product bid end has been completed. "
                                                    "No auction customers for you product. Please register once again."})
        friend = seller[0]['email']
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = seller[0]['email']
        msg['Subject'] = "Product auction date ended"
        msg.attach(MIMEText(result, 'html'))
        server = smtplib.SMTP(settings.EMAIL_HOST, 587)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.EMAIL_HOST_USER, friend, text)
        server.close()
    else:
        result = template.render(context={'status': "You won the product in auction please contact "+seller[0]['email']})
        friend = bidder[0]['email']
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = bidder[0]['email']
        msg['Subject'] = "Product auction date ended"
        msg.attach(MIMEText(result, 'html'))
        server = smtplib.SMTP(settings.EMAIL_HOST, 587)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.EMAIL_HOST_USER, friend, text)
        server.close()

        result = template.render(context={'status': "Your product bid"
                                                    " end date has been completed. please contact " + bidder[0]['email'] +" bid the product for highest amount"})
        friend = seller[0]['email']
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = seller[0]['email']
        msg['Subject'] = "Product auction date ended"
        msg.attach(MIMEText(result, 'html'))
        server = smtplib.SMTP(settings.EMAIL_HOST, 587)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.EMAIL_HOST_USER, friend, text)
        server.close()

        if(len(bidder)>1):
            result = template.render(context={'status':"your bid amount did not win the product! Come explore for more products and bid them!"})
            friend = ",".join(person['email'] for person in bidder[1:])
            msg = MIMEMultipart()
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = friend
            msg['Subject'] = "college report using onlinedb.py"
            msg.attach(MIMEText(result, 'html'))
            server = smtplib.SMTP(settings.EMAIL_HOST, 587)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            text = msg.as_string()
            server.sendmail(settings.EMAIL_HOST_USER, friend, text)
            server.close()


def send_email():
    product = Product.objects.all()
    for item in product:
        if(item.bid_end_date <= datetime.date.today()):
            bidder = User.objects.filter(bidder__product_id=item.id).annotate(max = Max('bidder__bid_amount')).values('email').order_by('-max')
            seller = User.objects.filter(seller__product_id=item.id).values('email')
            if(bidder):
                mailing(bidder, seller)
            else:
                mailing(0, seller)
            Bidder.objects.filter(product_id=item.id).delete()
            Seller.objects.filter(product_id=item.id).delete()
            Product.objects.get(id=item.id).delete()

def index(request):
    send_email()
    return render(request, 'auction_system/index.html')


def save_bid(request):
    context = dict()
    context['product_list'] = Product.objects.get(id=request.POST.get('product_id'))
    context['seller'] = Seller.objects.get(product_id_id=request.POST.get('product_id'))
    if request.method == 'POST':
        if int(request.POST.get('minimum_price')) > int(request.POST.get('bid_amount')):
            context['error'] = "bid price should be more than minimum price"
            return render(request, 'auction_system/product_detail.html', context)
        else:
            x = Bidder.objects.filter(product_id=Product.objects.get(id=request.POST.get('product_id'))).values('user_name')
            a = 0
            for item in x:
                if item['user_name'] == request.user.id:
                    y = Bidder.objects.get(user_name=request.user.id, product_id=Product.objects.get(id=request.POST.get('product_id')))
                    y.bid_amount = int(request.POST.get('bid_amount'))
                    y.save()
                    a = 1
            if not a:
                obj = Bidder(user_name=request.user, product_id=Product.objects.get(id=request.POST.get('product_id')), bid_amount=int(request.POST.get('bid_amount')))
                obj.save()
            return HttpResponseRedirect(reverse('view_product'))
    return render(request, 'auction_system/product_detail.html', context)