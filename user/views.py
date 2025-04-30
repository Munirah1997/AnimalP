from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Message, Tb_User, Tb_Report
from rest_framework import viewsets
from .serializers import UserSerializer, ReportSerializer,MessageSerializer,SendMessageSerializer, ReceiveMessageSerializer
import uuid
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
def get_users(request):
    users = Tb_User.objects.all()
    serializer = UserSerializer(users, many=True)

    # Get the desired language from the request headers or parameters
    language = request.META.get('HTTP_ACCEPT_LANGUAGE') or request.GET.get('language')
    if language and language.lower().startswith('ar'):
        # If the language is Arabic, translate the response data to Arabic
        translated_data = translate_data(serializer.data, 'ar')
        return Response(translated_data)
    
    # If the language is not specified or it's another language, return the response data as is
    return Response(serializer.data)








class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)


@api_view(['GET'])
def get_messages(request):
    msgs = Message.objects.all()
    serializer = MessageSerializer(msgs, many=True)  
    data = serializer.data

    json_data = json.dumps(data, ensure_ascii=False, cls=CustomJSONEncoder).encode('utf-8')
    return HttpResponse(json_data, content_type='application/json; charset=utf-8')



@api_view(['GET'])
def get_reports(request):
    reports = Tb_Report.objects.all()
    serialized_reports = ReportSerializer(reports, many=True)
    data = serialized_reports.data

    json_data = json.dumps(data, ensure_ascii=False, cls=CustomJSONEncoder).encode('utf-8')
    return HttpResponse(json_data, content_type='application/json; charset=utf-8')

@api_view(['GET'])
def delete_report(request, report_id):
    report = get_object_or_404(Tb_Report, pk=report_id)
    if report:
        report.IsDeleted=True
        report.save()
        return Response({"msg":"Report Deleted Successfuly"},status=200)
    return Response({"error": "Report not found"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def cancel_report(request, report_id):
    report = get_object_or_404(Tb_Report, pk=report_id)
    if report:
        report.IsCancellation=True
        report.save()
        return Response({"msg":"Report Canceled Successfuly"},status=200)
    return Response({"error": "Report not found"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def resend_report(request, report_id):
    report = get_object_or_404(Tb_Report, pk=report_id)
    if report:
        report.IsCancellation=False
        report.save()
        return Response({"msg":"Report Canceled Successfuly"},status=200)
    return Response({"error": "Report not found"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def update_user(request):
    User_ID = request.data.get('User_ID')
    Name = request.data.get('Name')
    Phone = request.data.get('Phone')
    Email = request.data.get('Email')
    National_ID = request.data.get('National_ID')
    Age = request.data.get('Age')
    Password=request.data.get('Password')
    try:
        user = Tb_User.objects.filter(ID=User_ID).update(Name=Name, Phone=Phone, Email=Email, National_ID=National_ID, Age=Age, Password=Password)
        return Response({"msg": "Account updated successfully"}, status=200)
    except Tb_User.DoesNotExist:
        print("Account not found")
        return Response({"error": "Account not found"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def delete_user(request):
    User_ID = request.data.get('User_ID')
    try:
        user = Tb_User.objects.filter(ID=User_ID).delete()
        return Response({"error": "Account deleted successfully"}, status=200)
    except Tb_User.DoesNotExist:
        print("Account not found")
        return Response({"error": "Account not found"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def update_user_status(request):
    User_ID = request.data.get('User_ID')
    Status = request.data.get('Status')
    try:
        user = Tb_User.objects.filter(ID=User_ID).update(Account_Status=Status)
        return Response({"msg":"Status Updated Successfuly"},status=200)
    except Tb_User.DoesNotExist:
        print("Account not found")
        return Response({"error": "Account not found"}, status=status.HTTP_401_UNAUTHORIZED)



class LoginView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")
        account_type = request.data.get("account_type")

        print("Request data:", request.data)

        try:
            user = Tb_User.objects.get(Phone=phone, Account_Type=account_type, Account_Status='Active')
            if user.Password == password:
                print("User found:", user)
                serializer = UserSerializer(user)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                print("Incorrect password")
                return Response({"error": "Incorrect phone number or password"}, status=status.HTTP_401_UNAUTHORIZED)
        except Tb_User.DoesNotExist:
            print("Account not found")
            return Response({"error": "Account not found"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@parser_classes([MultiPartParser])
def add_report(request):
    print("Request data:", request.data)  # Print the received data
    
    user_id = request.data.get('User_ID')
    title = request.data.get('Title')
    lat = request.data.get('alt')
    lng = request.data.get('lag')
    note = request.data.get('Note')
    report_type = request.data.get('Type')
    image = request.FILES.get('Image')
    
    if user_id and title and lat and lng and note and report_type and image:
        try:
            user = Tb_User.objects.get(ID=user_id)  # Fetch the user instance using the user_id
            report = Tb_Report(User_ID=user, Title=title, alt=lat, lag=lng, Note=note, Type=report_type, image=image)
            report.save()
            serializer = ReportSerializer(report)
            return JsonResponse(serializer.data, status=201)
        except Tb_User.DoesNotExist:
            print("User not found")  # Print error message
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    else:
        print("Invalid data")  # Print error message
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)






@api_view(['PUT'])
@parser_classes([MultiPartParser])
@csrf_exempt
def update_report(request):
    print("Request data:", request.data)

    report_id = request.data.get('ID')
    user_id = request.data.get('User_ID')
    title = request.data.get('Title')
    lat = request.data.get('alt')
    lng = request.data.get('lag')
    note = request.data.get('Note')
    report_type = request.data.get('Type')
    image = request.FILES.get('image')

    if report_id and user_id and title and lat and lng and note and report_type:
        try:
            user = Tb_User.objects.get(ID=user_id)
            report = Tb_Report.objects.get(ID=report_id, User_ID=user)
            report.Title = title
            report.alt = lat
            report.lag = lng
            report.Note = note
            report.Type = report_type
            if image is not None:
                report.image = image
            report.save()
            return Response({"message": "Report updated successfully"}, status=200)
        except Tb_User.DoesNotExist:
            print("User or report not found")
            return Response({"error": "User or report not found"}, status=400)
    else:
        print("Invalid data")
        return Response({"error": "Invalid data"}, status=400)

@api_view(['PUT'])
def update_report_status(request, report_id):
    try:
        report = Tb_Report.objects.get(pk=report_id)
    except Tb_Report.DoesNotExist:
        return Response({'message': 'Report not found'}, status=404)

    new_report_status = request.data.get('report_status')
    evadmin_id = request.data.get('evadmin_id')

    if not new_report_status or not evadmin_id:
        return Response({'message': 'Invalid request'}, status=400)

    try:
        evadmin = Tb_User.objects.get(pk=evadmin_id)
    except Tb_User.DoesNotExist:
        return Response({'message': 'Admin not found'}, status=404)

    report.Report_Status = new_report_status
    report.EVAdmin_ID = evadmin
    report.save()

    return Response({'message': 'Report status updated successfully'}, status=200)

@api_view(['PUT'])
def update_verification_status(request, report_id):
    try:
        report = Tb_Report.objects.get(pk=report_id)
    except Tb_Report.DoesNotExist:
        return Response({'message': 'Report not found'}, status=404)

    new_verification_status = request.data.get('verification_status')
    evadmin_id = request.data.get('evadmin_id')

    if not new_verification_status or not evadmin_id:
        return Response({'message': 'Invalid request'}, status=400)

    try:
        evadmin = Tb_User.objects.get(pk=evadmin_id)
    except Tb_User.DoesNotExist:
        return Response({'message': 'Admin not found'}, status=404)

    report.Verification_Status = new_verification_status
    report.EVAdmin_ID = evadmin
    report.save()

    return Response({'message': 'Verification status updated successfully'}, status=200)

class UserViewSet(viewsets.ModelViewSet):
    queryset = Tb_User.objects.all()
    serializer_class = UserSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = SendMessageSerializer

    def create(self, request, *args, **kwargs):
        sender_id = request.data.get('Sender')
        receiver_id = request.data.get('Receiver')
        text = request.data.get('Text')
        alt = request.data.get('alt')
        lag = request.data.get('lag')

        sender = Tb_User.objects.get(ID=sender_id)
        receiver = Tb_User.objects.get(ID=receiver_id)

        message = Message.objects.create(Sender=sender, Receiver=receiver, Text=text, alt=alt, lag=lag)
        serializer = SendMessageSerializer(message)

        return Response(serializer.data)
    


class SendMessageView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)  # Allow file uploads

    def post(self, request, *args, **kwargs):
        sender_id = request.data.get('Sender')
        receiver_id = request.data.get('Receiver')
        text = request.data.get('Text')
        alt = request.data.get('alt')
        lag = request.data.get('lag')
        attachment = request.data.get('Attachment')  # Get file from request data

        sender = Tb_User.objects.get(ID=sender_id)
        receiver = Tb_User.objects.get(ID=receiver_id)

        # Create message and save attachment
        message = Message.objects.create(
            Sender=sender, 
            Receiver=receiver, 
            Text=text, 
            alt=alt, 
            lag=lag, 
            Attachment=attachment,  # Save file as attachment
        )
        
        serializer = SendMessageSerializer(message)

        return Response(serializer.data)

    
class RetrieveMessagesView(APIView):
    def get(self, request, *args, **kwargs):
        sender_id = request.query_params.get('Sender')
        receiver_id = request.query_params.get('Receiver')

        sender = Tb_User.objects.get(ID=sender_id)
        receiver = Tb_User.objects.get(ID=receiver_id)

        messages = Message.objects.filter(Q(Sender=sender, Receiver=receiver) | Q(Sender=receiver, Receiver=sender)).order_by('-Date_Created')
        serializer = MessageSerializer(messages, many=True)



class GetOrCreateChatView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('UserId')
        phone = request.data.get('Phone')

        user1 = get_object_or_404(Tb_User, ID=user_id)
        user2 = get_object_or_404(Tb_User, Phone=phone)

        chat = Message.objects.filter(Q(Sender=user1, Receiver=user2) | Q(Sender=user2, Receiver=user1)).first()
        if not chat:
            chat = Message.objects.create(Sender=user1, Receiver=user2, Text='')
            serializer = SendMessageSerializer(chat)
            return Response(serializer.data)

        # If chat exists, fetch the chat messages or provide the required response
        # Implement as per your requirement

        return Response({"message": "Chat already exists."})


class MessagesView(APIView):
    def get(self, request, *args, **kwargs):
        sender_id = request.GET.get('SenderId')
        receiver_id = request.GET.get('ReceiverId')

        if not sender_id or not receiver_id:
            return Response({"error": "Sender and Receiver ID must be provided"}, status=400)

        try:
            sender = Tb_User.objects.get(ID=sender_id)
            receiver = Tb_User.objects.get(ID=receiver_id)
        except Tb_User.DoesNotExist:
            return Response({"error": "Sender or Receiver does not exist"}, status=404)

        messages = Message.objects.filter(
            Q(Sender=sender, Receiver=receiver) | Q(Sender=receiver, Receiver=sender)
        ).order_by('Date_Created')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    

class UpdateMessageIsReadView(APIView):
    
    def put(self, request):
        receiver_id = request.data.get('receiver_id')
        message_id = request.data.get('message_id')
        
        if not receiver_id or not message_id:
            return Response({'message': 'Receiver ID and Message ID are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the message object
        message = get_object_or_404(Message, Receiver_id=receiver_id, ID=message_id)
        
        # Update the IsRead field
        message.IsRead = True
        message.save()
        
        # Serialize and return the updated message object
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class UpdateMessageStatusView(APIView):
#     def put(self, request, *args, **kwargs):
#         sender_id = request.GET.get('SenderId')
#         receiver_id = request.GET.get('ReceiverId')

#         if not sender_id or not receiver_id:
#             return Response({"error": "Sender and Receiver ID must be provided"}, status=500)

#         try:
#             sender = Tb_User.objects.get(ID=sender_id)
#             receiver = Tb_User.objects.get(ID=receiver_id)
#         except Tb_User.DoesNotExist:
#             return Response({"error": "Sender or Receiver does not exist"}, status=404)
#         messages = Message.objects.filter(
#             Q(Sender=sender, Receiver=receiver))
#         # Serialize the updated messages
#         messages.update(IsRead=True)

#         serializer = MessageSerializer(messages, many=True)

#         return Response(serializer.data)

class UpdateMessageStatusView(APIView):
    """
    Update Message IsRead Status
    """

    def put(self, request, sender_uuid, receiver_uuid, format=None):
        # Optional: Check if the logged-in user is authorized to perform this operation
        
        # Filter messages based on sender_uuid and receiver_uuid
        messages = Message.objects.filter(Q(Sender=sender_uuid) & Q(Receiver=receiver_uuid))

        # Update IsRead to True for the filtered messages
        messages.update(IsRead=True)

        # Optional: Serialize the updated messages
        # serializer = MessageSerializer(messages, many=True)
        
        # Return success response
        return Response({'status': 'success', 'message': 'Message status updated successfully'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_message_status(request):
    if request.method == 'PUT':
        sender_id = request.GET.get('SenderId')
        receiver_id = request.GET.get('ReceiverId')

        # if not sender_id or not receiver_id:
        #     return Response({"error": "Sender and Receiver ID must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = Tb_User.objects.get(ID=sender_id)
            receiver = Tb_User.objects.get(ID=receiver_id)
        except Tb_User.DoesNotExist:
            return Response({"error": "Sender or Receiver does not exist"}, status=status.HTTP_404_NOT_FOUND)

        messages = Message.objects.filter(Q(Sender=sender, Receiver=receiver))
        
        # Change the status of each message and save
        for message in messages:
            message.IsRead = True
            message.save()

        # Serialize the updated messages
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)
    