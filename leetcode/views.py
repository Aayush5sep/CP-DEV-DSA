from django.shortcuts import render
import requests
from django.http import HttpResponse, JsonResponse
import json
from rest_framework.response import Response
import string
import random
from leetcode.models import PendingVerification
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone

# Create your views here.


def leetcodeapi(request,body,variables):
    # username = "AayushGoyal93"
    # body = """
    # query($username:String!){
    #     recentAcSubmissionList( username:$username  limit:20 )
    #     {
    #         id
    #         title
    #         titleSlug
    #         timestamp
    #     }
    # }
    # """
    leetcode_url = "https://leetcode.com/graphql"
    response = requests.post(url=leetcode_url, json={"query": body, "variables":variables})
    return response
    # response = requests.post(url=leetcode_url, json={"query": body, "variables":{"username":username}})
    # if response.status_code == 200:
    #     return HttpResponse(response.content)
    #     return JsonResponse(json.loads(response.text))



# Verify Leetcode Profile

# 1. Request to get steps to verify 
@login_required(login_url='')
def AddProfile(request):
    # Prevent Too Much Requests
    curr_time = timezone.now()
    range_time = curr_time - timedelta(hours=1)
    prev_reqs = PendingVerification.objects.filter(user=request.user,req_time__range=(range_time,curr_time))
    if len(prev_reqs) >= 3:
        return HttpResponse("You have sended too many responses. Kindly wait for 1 hour to send a new verification request.")

    # Grab Leetcode Profile
    leetname = request.GET['leetusername']
    body = """
    query($username:String!){
        matchedUser( username: $username)
        {
            username
            profile{
                realName
                aboutMe
            }
        }
    }
    """
    variables={
        "username":leetname
    }
    response = leetcodeapi(request,body,variables)
    profile_name = ""

    if response.status_code == 200:
        json_response = json.loads(response.text)
        try:
            err = json_response["errors"][0]["message"]
            return HttpResponse(err)
        except Exception as e:
            profile_name = json_response["data"]["matchedUser"]["profile"]["realName"]
    else:
        return HttpResponse("We are currently facing some issue. Kindly try again later")

    # Generate Random Code
    veri_code = "".join(random.choices(string.ascii_letters + string.digits, k = 25))

    # Save user, leet-profile & code in a temporary database
    verification = PendingVerification(user=request.user, leetusername=leetname, profile_name=profile_name, veri_code=veri_code)
    verification.save()

    # Request to change summary to random code at https://leetcode.com/profile/
    # Also give button for save request to verify if changed
    return HttpResponse(f'Hey {profile_name} <br> Change the summary of your Leetcode account {leetname} to {veri_code} in 5 minutes. <br> Visit <a href="https://leetcode.com/profile/">Profile</a> now to change the summary')
    pass

# 2. Confirm request to check the changes
@login_required(login_url='')
def VerifyProfile(request):
    # Grab User verification from temporary database
    curr_time = timezone.now()
    range_time = curr_time - timedelta(minutes=5)
    prev_reqs = PendingVerification.objects.filter(user=request.user,req_time__range=(range_time,curr_time))
    if len(prev_reqs)==0:
        return HttpResponse("You do not have any active requests for Leetcode Profile Verification. <br> Kindly send one first or the previous ones may have expired")

    # Start verification for objects
    errs = []
    for req in prev_reqs:
        # Grab aboutMe of the user from Leetcode API
        body = """
        query($username:String!){
            matchedUser( username: $username)
            {
                username
                profile{
                    realName
                    aboutMe
                }
            }
        }
        """
        variables={
            "username":req.leetusername
        }
        response = leetcodeapi(request,body,variables)

        # Verify the code
        if response.status_code == 200:
            json_response = json.loads(response.text)
            try:
                errs.append(json_response["errors"][0]["message"])
            except Exception as e:
                # Save the leet-profile to main db if verified
                summary = json_response["data"]["matchedUser"]["profile"]["aboutMe"]
                if summary==req.veri_code:
                    # Save profile
                    

                    # Send profile saved success message
                    req.delete()
                    return HttpResponse(f"Your Leetcode Profile has been successfully verified & set to {req.leetusername}")
                else:
                    errs.append("Summary & Verification Code didn't match")
        else:
            return HttpResponse("We are currently facing some issue. Kindly try again later")

    # Since no profile verified, send failed response to user
    found_errors = ""
    for err in errs:
        found_errors = found_errors + "<br>" + err
    return HttpResponse("Your request for leetcode profile could not be verified. <br> Here is the list of errors we found : <br>" + found_errors)