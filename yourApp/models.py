import os
import re
from django.db import models
from Portal.ConfigParser.ConfigParser import ConfigParser

# Create your models here.

configParser = ConfigParser(os.path.dirname(os.path.realpath(__file__))+"/createForm.cfg")
admissionDetailsInfo = configParser.getAdmissionDetails()


class PersonalDetails(models.Model):

  personalDetailsInfo = configParser.getPersonalDetailsInfo()

  UUID = models.CharField(max_length=255,null=False)

  for personalAttr in personalDetailsInfo.listOfPersonalAttr:
    for subAttr in personalAttr.ListOfSubAttr:
      columnName = personalAttr.PersonalAttrName + "_" + subAttr.SubAttrName
      dbType = None

      if (subAttr.IsTypeString):
        dbType = subAttr.StringConstraints['DBType']
        maxLength = int(re.findall(r'\d+', dbType)[0])
        locals()[columnName] = models.CharField(max_length=maxLength,null=True)
      elif (subAttr.IsTypeInteger):
        dbType = subAttr.IntegerConstraints['DBType']
        if (dbType.lower() == "smallint" or dbType.lower()=="integer"):
          locals()[columnName] = models.IntegerField(null=True, blank=True)
        elif (dbType.lower() == "bigint"):
          locals()[columnName] = models.BigIntegerField(null=True, blank=True)
      elif (subAttr.IsTypeFloat):
        dbType = subAttr.FPConstraints['DBType']
        locals()[columnName] = models.FloatField(null=True, blank=True)
      elif (subAttr.IsTypeDate):
        dbType = subAttr.DateConstraints['DBType']
        locals()[columnName] = models.DateField(null=True)
      elif (subAttr.IsTypeBoolean):
        dbType = subAttr.BooleanConstraints['DBType']
        locals()[columnName] = models.BooleanField(null=True)
      else:
        pass

  class Meta:
      db_table = str(admissionDetailsInfo.AdmissionType + '_' + admissionDetailsInfo.AdmissionDegree + '_' + admissionDetailsInfo.AdmissionMonth + \
        '_' + admissionDetailsInfo.AdmissionYear + '_' + 'PersonalDetails').replace(" ", "")

  pass 

class EducationalQualifications(models.Model):

  educationalQualificationsInfo = configParser.getEducationalQualificationsInfo()

  UUID = models.CharField(max_length=255,null=False)

  for eduAttr in educationalQualificationsInfo.listOfEduAttr:
    for subAttr in eduAttr.ListOfSubAttr:
      columnName = eduAttr.EduAttrName + "_" + subAttr.SubAttrName
      dbType = None

      if (subAttr.IsTypeString):
        dbType = subAttr.StringConstraints['DBType']
        maxLength = int(re.findall(r'\d+', dbType)[0])
        locals()[columnName] = models.CharField(max_length=maxLength,null=True)
      elif (subAttr.IsTypeInteger):
        dbType = subAttr.IntegerConstraints['DBType']
        if (dbType.lower() == "smallint" or dbType.lower()=="integer"):
          locals()[columnName] = models.IntegerField(null=True, blank=True)
        elif (dbType.lower() == "bigint"):
          locals()[columnName] = models.BigIntegerField(null=True, blank=True)
      elif (subAttr.IsTypeFloat):
        dbType = subAttr.FPConstraints['DBType']
        locals()[columnName] = models.FloatField(null=True, blank=True)
      elif (subAttr.IsTypeDate):
        dbType = subAttr.DateConstraints['DBType']
        locals()[columnName] = models.DateField(null=True)
      elif (subAttr.IsTypeBoolean):
        dbType = subAttr.BooleanConstraints['DBType']
        locals()[columnName] = models.BooleanField(null=True)
      else:
        pass

  class Meta:
    db_table = str(admissionDetailsInfo.AdmissionType + '_' + admissionDetailsInfo.AdmissionDegree + '_' + admissionDetailsInfo.AdmissionMonth + \
    '_' + admissionDetailsInfo.AdmissionYear + '_' + 'EducationalQualifications').replace(" ", "")

class WorkExperience(models.Model):

  workExperienceInfo = configParser.getWorkExperienceInfo()

  UUID = models.CharField(max_length=255,null=False)

  for subAttr in workExperienceInfo.ListOfSubAttr:
    columnName = subAttr.SubAttrName
    dbType = None

    if (subAttr.IsTypeString):
      dbType = subAttr.StringConstraints['DBType']
      maxLength = int(re.findall(r'\d+', dbType)[0])
      locals()[columnName] = models.CharField(max_length=maxLength,null=True)
    elif (subAttr.IsTypeInteger):
        dbType = subAttr.IntegerConstraints['DBType']
        if (dbType.lower() == "smallint" or dbType.lower()=="integer"):
          locals()[columnName] = models.IntegerField(null=True, blank=True)
        elif (dbType.lower() == "bigint"):
          locals()[columnName] = models.BigIntegerField(null=True, blank=True)
    elif (subAttr.IsTypeFloat):
      dbType = subAttr.FPConstraints['DBType']
      locals()[columnName] = models.FloatField(null=True, blank=True)
    elif (subAttr.IsTypeDate):
      dbType = subAttr.DateConstraints['DBType']
      locals()[columnName] = models.DateField(null=True)
    elif (subAttr.IsTypeBoolean):
      dbType = subAttr.BooleanConstraints['DBType']
      locals()[columnName] = models.BooleanField(null=True)
    else:
      pass

  class Meta:
    db_table = str(admissionDetailsInfo.AdmissionType + '_' + admissionDetailsInfo.AdmissionDegree + '_' + admissionDetailsInfo.AdmissionMonth + \
    '_' + admissionDetailsInfo.AdmissionYear + '_' + 'WorkExperience').replace(" ", "")

class Attachments(models.Model):

  attachmentsInfo = configParser.getAttachmentsInfo()

  UUID = models.CharField(max_length=255,null=False)

  for attachmentInfo in attachmentsInfo.listOfAttachmentInfo:
    for attachment in attachmentInfo.ListOfAttachment:
      columnName = attachmentInfo.AttachmentInfoName + "_" + attachment.AttachmentName
      dbType = None

      if (attachment.IsTypeFile):
        maxLength = 255
        locals()[columnName] = models.CharField(max_length=maxLength,null=True)
      else:
        pass

  class Meta:
    db_table = str(admissionDetailsInfo.AdmissionType + '_' + admissionDetailsInfo.AdmissionDegree + '_' + admissionDetailsInfo.AdmissionMonth + \
    '_' + admissionDetailsInfo.AdmissionYear + '_' + 'Attachments').replace(" ", "")
