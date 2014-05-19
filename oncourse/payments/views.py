from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from oncourse.util.decorators import auth_required

import stripe


@auth_required
def index(request):
    return redirect('payments-create')


@auth_required
def create_payment(request):
    return render_to_response(
        'payments/payment.html',
        {
            'STRIPE_API_SECRET': settings.STRIPE_API_SECRET,
        },
        context_instance=RequestContext(request),
    )


@auth_required
def create_subscription(request):
    return render_to_response(
        'payments/subscription.html',
        {},
        context_instance=RequestContext(request),
    )


@auth_required
def process_payment(request):

    token = request.session.get('token', None)
    user = request.session.get('user', None)

    if request.method == 'POST':

        # TODO: Move this to API
        print request
        stripe.api_key = settings.STRIPE_API_KEY
        token = request.POST['stripeToken']
        next = 'payments-create'

        try:
            # charge = stripe.Charge.create(
            #     amount=10000,
            #     currency="gbp",
            #     card=token,
            #     description="test GBP",
            # )
            customer = stripe.Customer.create(
                card=token,
                plan='premium',
                email=user['email'],
            )
        except stripe.CardError:
            # The card has been declined
            messages.error('Sorry, your card has been declined')
        except stripe.InvalidRequestError:
            return HttpResponse(status=400)
            # messages.error(request, 'You cannot use a token more than once')
        else:
            messages.success(request, 'Your payment was successful')

        return redirect(next)
