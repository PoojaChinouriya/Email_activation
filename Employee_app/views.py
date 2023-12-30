from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import logging
from django.core.mail import send_mail
from django.conf import settings

error_logger = logging.getLogger('error_logger')
success_logger = logging.getLogger('success_logger')

class EmployeeAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            employee = Employee.objects.all()
            serializer = EmployeeSerializer(employee, many=True)
            success_logger.info('Employee fetch successfully')
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_logger.error('There is error fetching an employee')
            return Response(data={'details':"There is an error fetching the Employee"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = EmployeeSerializer(data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            success_logger.info(f'Employee with id{serializer.data.get("id")} created successfully')
            send_mail(
                from_email=settings.EMAIL_HOST_USER,
                subject="Employee Creation",
                message=f"Employee created successfully with Employee id {serializer.data.get('id')}.",
                recipient_list=[request.user.email,],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            error_logger.info(f'Error saving data {serializer.errors}')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetail(APIView):

    def get(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee)
            success_logger.info('Employee fetch successfully')
            return Response(serializer.data)
        except Exception as e:
            error_logger.error("There is error fetching the Employee")
            return Response(data={'detail':'Error retriving data'}, status=status.HTTP_400_BAD_REQUEST)



    def put(self, request, pk):
        try:
            employee = self.get_object(pk)
            serializer = EmployeeSerializer(employee, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            success_logger.info('Employee fetch successfully')
            return Response(serializer.data)
        except Exception as e:
            error_logger.error("There is error fetching the Employee")
            return Response(data={'detail':'Error retriving data'}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

