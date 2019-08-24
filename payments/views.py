from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from . import paytm_checksum as Checksum
from django.http import Http404
import decimal
from django.contrib import messages
from django.contrib.auth import login
from .models import Payment
from . import alert_messages
from orders.models import Order


def create_payment(request, order_id):
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    CALLBACK_URL = settings.PAYTM_CALLBACK_URL
    order = get_object_or_404(Order, order_id=order_id)

    data_dict = {
                'MID': MERCHANT_ID,
                'ORDER_ID': order.order_id,
                'TXN_AMOUNT': order['amount'],
                'CUST_ID':'cust@alphahub.in',
                'INDUSTRY_TYPE_ID':'Retail',
                'WEBSITE': settings.PAYTM_WEBSITE,
                'CHANNEL_ID':'WEB',
                'CALLBACK_URL':CALLBACK_URL,
            }
    param_dict = data_dict
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
    return render(request, "payments/paytm/payment.html", {'paytmdict':param_dict})


@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            pt_status = data_dict.get("STATUS")
            status = "SC" if pt_status == "TXN_SUCCESS" else "FL"
            order_id = data_dict.get("ORDERID")
            amount = float(data_dict.get("TXNAMOUNT"))
            txnid = data_dict.get("TXNID")
            payment = Payment.objects.create(order_id=order_id, amount=amount, user=request.user, status=status,
                                             txnid=txnid)
            if status == "TXN_SUCCESS":
                orders = Order.objects.filter(order_id=order_id, amount=amount, user=request.user)
                if orders.exists():
                    order = orders.first()
                    payment.order = order
                    payment.save()
                    order.is_payed = True
                    order.save()
                    messages.success(request, alert_messages.ORDER_PLACED_MESSAGE)
                else:
                    messages.warning(request, "Payment Successfull but Order not Found. Amount will be refunded")
            else:
                messages.warning(request, "Payment Failed. Try again.")
            return redirect("orders:list")
        else:
            return Http404("Payment not verified")
    return Http404("Bad Request")

