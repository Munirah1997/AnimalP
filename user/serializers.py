from rest_framework import serializers
from .models import Tb_User,Tb_Report,Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tb_User
        fields = ('ID', 'Name', 'Phone', 'Password', 'Email', 'National_ID', 'Account_Type', 'Nationality', 'Gender', 'Age', 'Added_Date', 'Deletion_Date', 'Account_Status')

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tb_Report
        fields = ['image', 'ID', 'Title', 'alt', 'lag', 'Note', 'Type', 'Verification_Status', 'Report_Status', 'Added_Date', 'Cancellation_Date', 'IsCancellation', 'Deleted_Date', 'IsDeleted', 'User_ID','EVAdmin_ID']

class MessageSerializer(serializers.ModelSerializer):
    Sender = UserSerializer(read_only=True)
    Receiver = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['Sender', 'Receiver', 'Date_Created', 'alt', 'lag', 'Text', 'Attachment','IsRead','ID']


class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['Sender', 'Receiver', 'Text', 'alt', 'lag', 'Attachment','IsRead','ID','Date_Created']

class ReceiveMessageSerializer(serializers.ModelSerializer):
    Sender = UserSerializer()
    class Meta:
        model = Message
        fields = ['Sender', 'Text', 'alt', 'lag', 'Date_Created','IsRead','ID']
        
