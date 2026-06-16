import requests
import logging
from django.shortcuts import render, redirect
from django.contrib import messages

logger = logging.getLogger(__name__)

# Fast2SMS API Key provided by user
FAST2SMS_API_KEY = "KEodGZf5czOn3eCxJPkWAFHQUYtS86Rbmrv1MyuViag4hs7N2DujvzKSw5MN9mRryb3LC4DsIHiWph78"
FAST2SMS_URL = "https://www.fast2sms.com/dev/bulkV2"

def send_quick_sms(phone_number, message_text):
    """
    Sends a custom message to the mobile number using Fast2SMS Quick SMS API.
    Returns (success_boolean, response_message_string)
    """
    # Clean phone number (must be 10 digits)
    phone_number = "".join(filter(str.isdigit, str(phone_number)))
    if len(phone_number) != 10:
        return False, "Invalid mobile number format. Please enter a 10-digit number."

    if not message_text.strip():
        return False, "Message content cannot be empty."

    headers = {
        'authorization': FAST2SMS_API_KEY,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }
    
    payload = {
        'route': 'q',
        'message': message_text,
        'language': 'english',
        'sender_id': 'FSTSMS',
        'numbers': phone_number,
    }

    try:
        # Fast2SMS bulkV2 POST request for Quick SMS
        response = requests.post(FAST2SMS_URL, data=payload, headers=headers, timeout=10)
        response_json = response.json()
        
        # Fast2SMS returns success boolean in key 'return'
        if response_json.get('return') is True:
            return True, "Your message was sent successfully."
        else:
            # API returned error
            error_msg = response_json.get('message', ['An error occurred with the SMS service.'])[0]
            logger.error(f"Fast2SMS API Error: {response_json}")
            return False, error_msg
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Fast2SMS Connection Error: {e}")
        return False, "Failed to connect to the SMS provider. Please check your internet connection."
    except Exception as e:
        logger.error(f"Unexpected error sending SMS: {e}")
        return False, "An unexpected error occurred while sending the message."

def sms_home_view(request):
    """
    Page 1: SMS Home View.
    Enables user to submit a mobile number and a custom message.
    On form submission, attempts to send via Fast2SMS.
    """
    # If already sent, allow redirection to success view
    if request.session.get('sms_sent') is True:
        return redirect('success')

    phone_number = ""
    message_text = ""

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '').strip()
        message_text = request.POST.get('message_text', '').strip()
        
        # Clean mobile number
        clean_phone = "".join(filter(str.isdigit, phone_number))
        if not clean_phone or len(clean_phone) != 10:
            messages.error(request, "Please enter a valid 10-digit mobile number.")
            return render(request, 'otp_verification/index.html', {
                'phone_number': phone_number,
                'message_text': message_text
            })

        if not message_text:
            messages.error(request, "Please enter a message to send.")
            return render(request, 'otp_verification/index.html', {
                'phone_number': phone_number,
                'message_text': message_text
            })

        # Attempt to dispatch the SMS
        success, api_msg = send_quick_sms(clean_phone, message_text)

        # Store delivery details in session
        request.session['sms_phone'] = clean_phone
        request.session['sms_message'] = message_text
        request.session['sms_sent'] = True

        if success:
            request.session['sms_demo_mode'] = False
            messages.success(request, "SMS dispatched successfully via Fast2SMS!")
        else:
            # Enable Demo Mode Fallback for testing since Fast2SMS keys can be dry/inactive
            request.session['sms_demo_mode'] = True
            request.session['sms_api_error'] = api_msg
            messages.warning(request, f"Fast2SMS API reported: {api_msg}. Message saved in Demo Mode!")

        return redirect('success')

    return render(request, 'otp_verification/index.html', {
        'phone_number': phone_number,
        'message_text': message_text
    })

def success_view(request):
    """
    Page 2: Success Landing Page.
    Only accessible if a message was dispatched in the current session.
    """
    if not request.session.get('sms_sent') is True:
        messages.error(request, "Please send a message first.")
        return redirect('sms_home')

    phone_number = request.session.get('sms_phone', '')
    message_text = request.session.get('sms_message', '')
    demo_mode = request.session.get('sms_demo_mode', False)
    api_error = request.session.get('sms_api_error', '')

    return render(request, 'otp_verification/welcome.html', {
        'phone_number': phone_number,
        'message_text': message_text,
        'demo_mode': demo_mode,
        'api_error': api_error
    })

def reset_view(request):
    """
    Resets the session state to send another SMS.
    """
    keys_to_delete = ['sms_phone', 'sms_message', 'sms_sent', 'sms_demo_mode', 'sms_api_error']
    for key in keys_to_delete:
        if key in request.session:
            del request.session[key]
            
    messages.info(request, "Ready to send another message.")
    return redirect('sms_home')
