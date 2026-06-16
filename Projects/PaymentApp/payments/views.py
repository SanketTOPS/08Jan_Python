import razorpay
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import Transaction

# Initialize Razorpay Client
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

def homepage(request):
    currency = 'INR'
    amount = 50000  # Rs. 500

    # Create Razorpay Order
    # amount is in paise (100 paise = 1 INR)
    razorpay_order = razorpay_client.order.create({
        'amount': amount,
        'currency': currency,
        'payment_capture': '1'
    })

    # Order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    # Pass details to template
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'index.html', context=context)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # Verify the payment signature
            # This will raise SignatureVerificationError if verification fails
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # If no error, payment is successful
            amount = 50000  # Rs. 500
            Transaction.objects.create(
                payment_id=payment_id,
                order_id=razorpay_order_id,
                signature=signature,
                amount=amount
            )
            return render(request, 'paymentsuccess.html')
            
        except Exception as e:
            print(f"Payment verification failed: {e}")
            return render(request, 'paymentfail.html')
    else:
        return HttpResponseBadRequest()
