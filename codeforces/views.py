from django.shortcuts import render
import requests
from django.http import HttpResponse, JsonResponse
import json
import string
import random
from codeforces.models import CodeforcesVerification
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone

# Create your views here.


def codeforcesapi(request,handle):
    codeforces_url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.post(url=codeforces_url)
    return response



# Verify Codeforces Profile

# 1. Request to get steps to verify 
@login_required(login_url='')
def AddProfile(request):
    # Prevent Too Much Requests
    curr_time = timezone.now()
    range_time = curr_time - timedelta(hours=1)
    prev_reqs = CodeforcesVerification.objects.filter(user=request.user,req_time__range=(range_time,curr_time))
    if len(prev_reqs) >= 3:
        return HttpResponse("You have sended too many responses. Kindly wait for 1 hour to send a new verification request.")

    # Grab Codeforces Profile
    handle = request.GET['cfusername']
    response = codeforcesapi(request,handle)
    profile_name = ""

    json_response = json.loads(response.text)
    if json_response["status"]=="FAILED":
        return HttpResponse(json_response["comment"])
    else:
        profile_name = json_response["result"][0]["firstName"]

    # Generate Random Code
    veri_code = "".join(random.choices(string.ascii_letters + string.digits, k = 25))

    # Save user, cf-profile & code in a temporary database
    verification = CodeforcesVerification(user=request.user, handle=handle, profile_name=profile_name, veri_code=veri_code)
    verification.save()

    # Request to change summary to random code at https://codeforces.com/settings/social
    # Also give button for save request to verify if changed
    return HttpResponse(f'Hey {profile_name} <br> Change the last name of your Codeforces account {handle} to {veri_code} in 5 minutes. <br> Visit <a href="https://codeforces.com/settings/social">Profile</a> now to change the details')


# 2. Confirm request to check the changes
@login_required(login_url='')
def VerifyProfile(request):
    # Grab User verification from temporary database
    curr_time = timezone.now()
    range_time = curr_time - timedelta(minutes=5)
    prev_reqs = CodeforcesVerification.objects.filter(user=request.user,req_time__range=(range_time,curr_time))
    if len(prev_reqs)==0:
        return HttpResponse("You do not have any active requests for Codeforces Profile Verification. <br> Kindly send one first or the previous ones may have expired")

    # Start verification for objects
    errs = []
    for req in prev_reqs:
        # Grab handle info of the user from Codeforces API
        response = codeforcesapi(request,req.handle)

        # Verify the code
        json_response = json.loads(response.text)
        if json_response["status"] == "OK":

            # Save the cf-profile to main db if verified
            lastname = json_response["result"][0]["lastName"]
            if lastname==req.veri_code:
                # Save profile
                

                # Send profile saved success message
                req.delete()
                return HttpResponse(f"Your Codeforces Profile has been successfully verified & set to {req.handle}")
            else:
                errs.append("Last Name & Verification Code didn't match")
        else:
            return HttpResponse(json_response["comment"])

    # Since no profile verified, send failed response to user
    found_errors = ""
    for err in errs:
        found_errors = found_errors + "<br>" + err
    return HttpResponse("Your request for codeforces profile could not be verified. <br> Here is the list of errors we found : <br>" + found_errors)