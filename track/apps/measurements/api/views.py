import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import Payment
from devices.authentication import ApiKeyAuthentication
from .serializers import GpsMeasurementSerializer
from users.models import User

Pay = Payment()

class userView(APIView):
    def get(self,request,tagid):
        user = User.objects.get(tag=tagid)
        amount = user.amount
        if (amount == 0):
            message = "Insufficient funds kindly recharge your account."
            Pay.send_sms(user.phone_number, message)
            Pay.stk_push(user.phone_number,5)

        return Response(amount)

class userclear_credits_View(APIView):
    def get(self,request,tagid):
        user = User.objects.get(tag=tagid)
        user.amount = 0
        user.save()
        message = "Limit reached. Kindly recharge your account."
        Pay.send_sms(user.phone_number, message)
        Pay.stk_push(user.phone_number,5)


        return Response("Balance cleared.")

class stk_push_api(APIView):
    def post(self, request):
        data = (request.data)        
        phone = (data["Body"]nn["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"])
        amount = (data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"])
        user = User.objects.get(phone_number="+254"+str(phone)[-9:])
        user.amount = int(amount*200)
        user.save()

        message = "You have successfully topped up KES 5.00."
        Pay.send_sms(user.phone_number, message)


        return Response("updated", status=status.HTTP_201_CREATED)

class MeasurementView(APIView):
    authentication_classes = (ApiKeyAuthentication,)
    def post(self, request):
        context = {'device': request.user,}
        print(request.data)
        serializer = GpsMeasurementSerializer(data=request.data, context=context)
        if not serializer.is_valid():
            data = {
                'status': 'error',
                'errors': serializer.errors,
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        print(context)

        serializer.save()

        data = {
            'status': 'ok',
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

