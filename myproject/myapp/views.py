from django.shortcuts import render
from rest_framework import generics, status
from .serializers import *
from rest_framework.response import Response
from django.utils import timezone

class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = ('Register SuccessFully')
        return Response({'message':message,'data':serializer.data})

class PunchinView(generics.GenericAPIView):
    serializer_class = PunchinSerializer

    def post(self, request):
        data = request.data
        serializer = PunchinSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = User.objects.filter(email=email).first()
            if user:
                if user.password == password:
                    if user.punchin_time:
                        message = "Already punched in"
                        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
                    user.punchin_time = timezone.now()
                    user.is_in = True
                    user.save()
                    message = "Punch-in successful"
                    return Response({'message': message, 'data': serializer.data}, status=status.HTTP_200_OK)
                else:
                    message = "Wrong Password"
                    return Response({'message': message}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                message = "User not found"
                return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PunchoutView(generics.GenericAPIView):
    serializer_class = PunchinSerializer

    def post(self, request):
        data = request.data
        serializer = PunchinSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = User.objects.filter(email=email).first()
            if user:
                if user.password == password:
                    if not user.punchin_time:
                        message = "Punch-in first before punching out"
                        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
                    if user.punchout_time:
                        message = "Already punched out"
                        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
                    user.punchout_time = timezone.now()
                    user.is_out = True
                    user.save()
                    total_working_time = user.punchout_time - user.punchin_time
                    total_working_hours = total_working_time.seconds // 3600
                    total_working_minutes = (total_working_time.seconds % 3600) // 60
                    user.working = (total_working_hours * 60) + total_working_minutes
                    
                    # ------------   Calculate minutes  ----------------
    
                    # total_working_minutes = total_working_time.total_seconds() // 60
                    # user.working = total_working_minutes
                    user.save()
                    message = "Punch-out successful"
                    return Response({'message': message,'Today Working Hours':user.working,'data': serializer.data}, status=status.HTTP_200_OK)
                else:
                    message = "Wrong Password"
                    return Response({'message': message}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                message = "User not found"
                return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        