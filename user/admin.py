from django.contrib import admin

# Register your models here.

from user.models import Tb_User,Tb_Report,Message

# Register your models here.
class Tb_UserInstanceInline(admin.ModelAdmin):
    list_display = (
"ID",
"Name",
"Phone",
"Password",
"Email",
"National_ID",
"Account_Type",
"Age",
"Added_Date",
"Deletion_Date",
"Account_Status"
 )
    
class Tb_ReportInstanceInline(admin.ModelAdmin):
    list_display = (
"ID",
"Title",
"Note",
"Type",
"Report_Status",
"Added_Date",
"Cancellation_Date",
"IsCancellation",
"Deleted_Date",
"IsDeleted",
"User_ID",
"EVAdmin_ID",
 )
class MessageInstanceInline(admin.ModelAdmin):
    list_display = (
"ID",
"Sender",
"Receiver",
"Date_Created", 
"Text",
"Attachment",
"IsRead",
 )
    




admin.site.register(Tb_User, Tb_UserInstanceInline)
admin.site.register(Tb_Report, Tb_ReportInstanceInline)
admin.site.register(Message, MessageInstanceInline)