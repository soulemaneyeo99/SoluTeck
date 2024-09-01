import stripe
import uuid
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from django.http import JsonResponse

import gopay
from gopay.enums import Recurrence, PaymentInstrument, BankSwiftCode, Currency, Language
from .models import Invoice
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TuitionFee
from .forms import TuitionFeeForm

from django.views.generic import ListView
from django.db.models import Sum
from .models import TuitionFee

class TuitionFeeListView(ListView):
    model = TuitionFee
    template_name = 'payments/tuition_fee.html'
    context_object_name = 'fees'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status == 'paid':
            queryset = queryset.filter(is_paid=True)
        elif status == 'unpaid':
            queryset = queryset.filter(is_paid=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_fees'] = TuitionFee.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_paid'] = TuitionFee.objects.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        context['remaining'] = context['total_fees'] - context['total_paid']
        context['form'] = TuitionFeeForm()
        return context

    def post(self, request, *args, **kwargs):
        form = TuitionFeeForm(request.POST)
        if form.is_valid():
            form.save()
        return self.get(request, *args, **kwargs)



def payment_paypal(request):
    return render(request, "payments/paypal.html", context={})


def payment_stripe(request):
    return render(request, "payments/stripe.html", context={})


def payment_coinbase(request):
    return render(request, "payments/coinbase.html", context={})


def payment_paylike(request):
    return render(request, "payments/paylike.html", context={})


def payment_succeed(request):
    return render(request, "payments/payment_succeed.html", context={})


class PaymentGetwaysView(TemplateView):
    template_name = "payments/payment_gateways.html"

    def get_context_data(self, **kwargs):
        context = super(PaymentGetwaysView, self).get_context_data(**kwargs)
        context["key"] = settings.STRIPE_PUBLISHABLE_KEY
        context["amount"] = 500
        context["description"] = "Stripe Payment"
        context["invoice_session"] = self.request.session["invoice_session"]
        print(context["invoice_session"])
        return context


def stripe_charge(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        charge = stripe.Charge.create(
            amount=500,
            currency="eur",
            description="A Django charge",
            source=request.POST["stripeToken"],
        )
        invoice_code = request.session["invoice_session"]
        invoice = Invoice.objects.get(invoice_code=invoice_code)
        invoice.payment_complete = True
        invoice.save()
        return redirect("completed")
        # return JsonResponse({"invoice_code": invoice.invoice_code}, status=201)
        # return render(request, 'payments/charge.html')


def gopay_charge(request):
    if request.method != "POST":
        return JsonResponse({"message": "GET requested"})
    user = request.user

    payments = gopay.payments(
        {
            "goid": "[PAYMENT_ID]",
            "clientId": "[GOPAY_CLIENT_ID]",
            "clientSecret": "[GOPAY_CLIENT_SECRET]",
            "isProductionMode": False,
            "scope": gopay.TokenScope.ALL,
            "language": gopay.Language.ENGLISH,
            "timeout": 30,
        }
    )

    # recurrent payment must have field ''
    recurrentPayment = {
        "recurrence": {
            "recurrence_cycle": Recurrence.DAILY,
            "recurrence_period": "7",
            "recurrence_date_to": "2015-12-31",
        }
    }

    # pre-authorized payment must have field 'preauthorization'
    preauthorizedPayment = {"preauthorization": True}

    response = payments.create_payment(
        {
            "payer": {
                "default_payment_instrument": PaymentInstrument.BANK_ACCOUNT,
                "allowed_payment_instruments": [PaymentInstrument.BANK_ACCOUNT],
                "default_swift": BankSwiftCode.FIO_BANKA,
                "allowed_swifts": [BankSwiftCode.FIO_BANKA, BankSwiftCode.MBANK],
                "contact": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone_number": user.phone,
                    "city": "example city",
                    "street": "Plana 67",
                    "postal_code": "373 01",
                    "country_code": "CZE",
                },
            },
            "amount": 150,
            "currency": Currency.CZECH_CROWNS,
            "order_number": "001",
            "order_description": "pojisteni01",
            "items": [
                {"name": "item01", "amount": 50},
                {"name": "item02", "amount": 100},
            ],
            "additional_params": [{"name": "invoicenumber", "value": "2015001003"}],
            "callback": {
                "return_url": "http://www.your-url.tld/return",
                "notification_url": "http://www.your-url.tld/notify",
            },
            "lang": Language.CZECH,  # if lang is not specified, then default lang is used
        }
    )

    if response.has_succeed():
        print("\nPayment Succeed\n")
        print(f"hooray, API returned {str(response)}")
    else:
        print("\nPayment Fail\n")
        print(f"oops, API returned {str(response.status_code)}: {str(response)}")
    return JsonResponse({"message": str(response)})


def paymentComplete(request):
    print(request.is_ajax())
    if request.is_ajax() or request.method == "POST":
        invoice_id = request.session["invoice_session"]
        invoice = Invoice.objects.get(id=invoice_id)
        invoice.payment_complete = True
        invoice.save()
        # return redirect('invoice', invoice.invoice_code)
    body = json.loads(request.body)
    print("BODY:", body)
    return JsonResponse("Payment completed!", safe=False)


def create_invoice(request):
    print(request.is_ajax())
    if request.method == "POST":
        invoice = Invoice.objects.create(
            user=request.user,
            amount=request.POST.get("amount"),
            total=26,
            invoice_code=str(uuid.uuid4()),
        )
        request.session["invoice_session"] = invoice.invoice_code
        return redirect("payment_gateways")
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["invoice_session"] = self.request.session.get("invoice_session", None)
    return context


def invoice_detail(request, slug):
    return render(
        request,
        "invoice_detail.html",
        context={"invoice": Invoice.objects.get(invoice_code=slug)},
    )
