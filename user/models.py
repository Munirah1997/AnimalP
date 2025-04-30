from django.db import models
from django.db.models import Q
import uuid

# Create your models here.

class Tb_User(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=255)
    Phone = models.CharField(max_length=20, unique=True)
    Password = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255, unique=True)
    National_ID = models.CharField(max_length=20,unique=True)
    Account_Type = models.CharField(max_length=10, choices=(
        ('User', 'User'),
        ('Admin', 'Admin'),
        ('EVSecurity', 'EVSecurity')
    ), default='User')
    Nationality=models.CharField(max_length=255,default='Saudi')
    Gender= models.CharField(max_length=10, choices=(
        ('Male', 'Male'),
        ('Female', 'Female'),
    ), default='Male')
    Age = models.PositiveIntegerField()
    Added_Date = models.DateTimeField(auto_now_add=True)
    Deletion_Date = models.DateTimeField(blank=True, null=True)
    Account_Status = models.CharField(max_length=10, choices=(
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Deleted', 'Deleted')
    ), default='Inactive')

    def __str__(self):
        return self.Name 
    


class Tb_Report(models.Model):
    image = models.ImageField(upload_to='Reports/', blank=True, null=True)
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Title = models.CharField(max_length=255)
    alt = models.FloatField(null= False)
    lag=models.FloatField( null= False)
    Note = models.TextField()
    Type = models.CharField(max_length=15, choices=(
        ('Non-Predator', 'Non-Predator'),
        ('Predator', 'Predator')
    ), default='Predator')
        
    
    Verification_Status = models.CharField(max_length=15, choices=(
        ('Not Confirmed', 'Not Confirmed'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected')
    ), default='Not Confirmed')

    Report_Status = models.CharField(max_length=30, choices=(
        ('Dealt With', 'Dealt With'),
        ('Not Dealt With', 'Not Dealt With'),
    ), default='Not Dealt With')
    Added_Date = models.DateTimeField(auto_now_add=True)
    Cancellation_Date = models.DateTimeField(blank=True, null=True)
    IsCancellation = models.BooleanField(default=False)
    Deleted_Date = models.DateTimeField(blank=True, null=True)
    IsDeleted = models.BooleanField(default=False)
    User_ID = models.ForeignKey(
    Tb_User,
    on_delete=models.CASCADE,
    
    )
  
    EVAdmin_ID = models.ForeignKey(
    Tb_User,
    null=True,
    blank=True,
    related_name="admin_reports",
    on_delete=models.SET_NULL
    )
    
    def __str__(self):
        return self.Title
    



class Message(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Sender = models.ForeignKey(Tb_User, on_delete=models.CASCADE, related_name='Sender')
    Receiver = models.ForeignKey(Tb_User, on_delete=models.CASCADE, related_name='Receiver')
    Date_Created = models.DateTimeField(auto_now_add=True)
    alt = models.FloatField(null= True,blank=True,default=0.0)
    lag=models.FloatField( null= True,blank=True,default=0.0) 
    #alt and lag are for sending location will be dealt withh using front ent of flutter
    Text = models.CharField(max_length=500)
    Attachment = models.FileField(blank=True, null=True, upload_to='attachments/')
    IsRead=models.BooleanField(default=False)

    def __str__(self):
        return self.Text