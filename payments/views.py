from django.shortcuts import render, redirect
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


def create_payment(request, recharge):
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    CALLBACK_URL = settings.PAYTM_CALLBACK_URL
    order_id = Checksum.__id_generator__()

    payment_data = recharge.get_payment_info_dict
    payment = Payment.objects.initiate_payment(order_id=order_id,
                                               amount=payment_data.get('amount'),
                                               product_info=payment_data.get('productinfo'),
                                               recharge=recharge,
                                               gateway="PAYTM")

    data_dict = {
                'MID': MERCHANT_ID,
                'ORDER_ID': order_id,
                'TXN_AMOUNT': payment_data.get("amount"),
                'CUST_ID':'print@printmycopy.com',
                'INDUSTRY_TYPE_ID':'Retail',
                'WEBSITE': settings.PAYTM_WEBSITE,
                'CHANNEL_ID':'WEB',
                'CALLBACK_URL':CALLBACK_URL,
            }
    param_dict = data_dict
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
    return render(request,"payments/paytm/payment.html",{'paytmdict':param_dict})


@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            status = data_dict.get("STATUS")
            order_id = data_dict.get("ORDERID")
            amount = float(data_dict.get("TXNAMOUNT"))
            txnid = data_dict.get("TXNID")
            payment = Payment.objects.search_payment_paytm(order_id=order_id, amount=amount)
            payment.txnid = txnid
            payment.save()
            if payment is None:
                raise Http404("Bad Request ")
            else:
                if status == "TXN_SUCCESS":
                    payment.succeed()
                    return recharge_succeed(request, payment)
                else:
                    payment.failed()
                    return recharge_failed(request, payment)
        else:
            return Http404("Bad Request")
    return Http404("Bad Request")


def recharge_succeed(request, payment):
    if not request.user.is_authenticated:
        user = payment.recharge.wallet.user
        login(request, user)
    messages.success(request, alert_messages.RECHARGE_SUCCEED_MESSAGE)
    return redirect("wallets:view")


def recharge_failed(request, payment):
    if not request.user.is_authenticated:
        user = payment.recharge.wallet.user
        login(request, user)
    messages.warning(request, alert_messages.RECHARGE_FAILED_MESSAGE)
    return redirect("wallets:view")