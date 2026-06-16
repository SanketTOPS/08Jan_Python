import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Transaction
from django.contrib.auth.decorators import login_required
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request):
    try:
        # For simplicity, let's say the premium subscription costs 499 INR
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'Premium Subscription - NotesVault',
                        },
                        'unit_amount': 49900, # 499.00 INR
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payment_success')) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
            customer_email=request.user.email,
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return JsonResponse({'error': str(e)})

@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')
    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            # Update user to premium
            user = request.user
            user.is_premium = True
            user.save()

            # Record transaction
            Transaction.objects.create(
                user=user,
                stripe_checkout_id=session_id,
                amount=499.00,
                status='success'
            )
            return render(request, 'PaymentApp/success.html')
    return redirect('dashboard')

@login_required
def payment_cancel(request):
    return render(request, 'PaymentApp/cancel.html')
