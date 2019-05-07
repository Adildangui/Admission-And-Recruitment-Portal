import re
import sys
import numpy as np
from Portal.AdmissionDetails.AdmissionDetails import AdmissionDetails
from Portal.PersonalDetails.PersonalAttr import PersonalAttr
from Portal.PersonalDetails.PersonalDetails import PersonalDetails
from Portal.EducationalQualifications.EducationalQualifications import EducationalQualifications
from Portal.EducationalQualifications.EduAttr import EduAttr
from Portal.WorkExperience.WorkExperience import WorkExperience
from Portal.Attachments.Attachments import Attachments
from Portal.Attachments.AttachmentInfo import AttachmentInfo
from Portal.Attachments.Attachment import Attachment
from Portal.Constraints.ConstraintValidator import ConstraintValidator
from Portal.EducationalQualifications.SubAttr import SubAttr
from Portal.Constraints.ConstraintValidator import AttachmentConstraintValidator

class ConfigParser(object):

        def __init__(self,configFilePath):
               
              self.configFilePath = configFilePath
              self.configFile =  None
              self.fileData = None

              with open(self.configFilePath, 'r') as self.configFile:
                self.fileData = self.configFile.read()

              self.ADStartPattern = "AdmissionDetails:"                          #AD abbreviation for AdmissionDetails
              self.ADEndPattern = "AdmissionDetailsEnd:"

              self.PDStartPattern = "PersonalDetails:"                     #PD abbreviation for PersonalDetails
              self.PDEndPattern = "PersonalDetailsEnd:"

              self.PAStartPattern = "PersonalAttr:"              #PA abbreviation for PersonalAttr
              self.PAEndPattern = "PersonalAttrEnd:"

              self.EQStartPattern = "EducationalQualifications:"           #EQ abbreviation for EducationalQualifications
              self.EQEndPattern = "EducationalQualificationsEnd:"

              self.EAStartPattern = "EduAttr:"                          #EA abbreviation for EduAttr
              self.EAEndPattern = "EduAttrEnd:"

              self.SAStartPattern = "SubAttr:"                          #SA abbreviation for SubAttr
              self.SAEndPattern = "SubAttrEnd:"

              self.WEStartPattern = "WorkExperiences:"                     #WE abbreviation for WorkExperiences
              self.WEEndPattern = "WorkExperiencesEnd:"

              self.ASStartPattern = "Attachments:"          #AS abbreviation for Attachments
              self.ASEndPattern = "AttachmentsEnd:"

              self.AIStartPattern = "AttachmentInfo:"                  #AI  abbreviation for AttachmentInfo
              self.AIEndPattern = "AttachmentInfoEnd:"

              self.AStartPattern = "Attachment:"                  #A  abbreviation for Attachment
              self.AEndPattern = "AttachmentEnd:"

        def getAdmissionDetails(self):
        
               admissionInfo = AdmissionDetails()       
               ADregex = str(self.ADStartPattern + "((.|\n)*?)" + self.ADEndPattern)
               AD = re.findall(ADregex, self.fileData)

               for ADBlock in AD:
                     ADBlockInfo = re.findall(r'(\S[^:]+):\s*(.*\S)', ADBlock[0])
                     for info in ADBlockInfo:
                          if (info[0].lower() == "AdmissionDegree".lower()):
                              admissionInfo.AdmissionDegree = info[1] 
                          elif (info[0].lower() == "AdmissionType".lower()):
                                        admissionInfo.AdmissionType = info[1]
                          elif (info[0].lower() == "AdmissionMonth".lower()):
                                        admissionInfo.AdmissionMonth = info[1] 
                          elif (info[0].lower() == "AdmissionYear".lower()):
                                        admissionInfo.AdmissionYear = info[1]
                          else:
                              print (info[0])
                              raise ValueError('Invalid field ' + info[0] + ' in config')

               return admissionInfo

        def getPersonalDetailsInfo(self):

               personalDetails = PersonalDetails()

               PDregex = str(self.PDStartPattern + "((.|\n)*?)" + self.PDEndPattern)
               PD = str(re.findall(PDregex, self.fileData)[0][0])

               PAregex = str(self.PAStartPattern + "((.|\n)*?)" + self.PAEndPattern)
               PAs = re.findall(PAregex, PD)
               PAs = [pa[0] for pa in PAs]
               listOfPersonalAttr = []   
               listOfUniqeNames = []   


               for PABlock in PAs:
                     SAregex = str(self.SAStartPattern + "((.|\n)*?)" + self.SAEndPattern)
                     
                     PAInfo = re.sub(SAregex, '', str(PABlock))
                     PAInfo = re.findall(r'(\S[^:]+):\s*(.*\S)', str(PAInfo))

                     personalAttr = PersonalAttr()  

                     for info in PAInfo:
                          if (info[0].lower() == "PersonalAttrName".lower()):
                              personalAttr.PersonalAttrName = info[1]
                          elif (info[0].lower() == "PersonalAttrLabel".lower()):
                              personalAttr.PersonalAttrLabel = info[1]
                          elif (info[0].lower() == "MultipleEntries".lower()):
                              personalAttr.MultipleEntries = info[1]
                          elif (info[0].lower() == "IsOptional".lower()):
                              personalAttr.IsOptional = info[1]
                          else:
                              raise ValueError('Invalid field ' + info[0] + ' for PersonalAttr')

                     
                     SAs = re.findall(SAregex, str(PABlock))
                     listOfSubAttr = []

                     for SABlock in SAs:
                          SABlockInfo = re.findall(r'(\S[^:]+):\s*(.*\S)', SABlock[0])
                          subAttr = SubAttr()
                          
                          typeDict = {}
                          constraintDict = {}

                          for info in SABlockInfo:
                              if (info[0].lower() == "SubAttrName".lower()):
                                 subAttr.SubAttrName = info[1]
                                 listOfUniqeNames.append(personalAttr.PersonalAttrName+"."+subAttr.SubAttrName)
                              elif (info[0].lower() == "SubAttrLabel".lower()):
                                 subAttr.SubAttrLabel = info[1]
                              elif (info[0].lower() == "IsTypeString".lower()):
                                 subAttr.IsTypeString = info[1]
                                 typeDict['String'] = subAttr.IsTypeString
                              elif (info[0].lower() == "IsTypeInteger".lower()):
                                 subAttr.IsTypeInteger = info[1]
                                 typeDict['Integer'] = subAttr.IsTypeInteger
                              elif (info[0].lower() == "IsTypeFloat".lower()):
                                 subAttr.IsTypeFloat = info[1]
                                 typeDict['Float'] = subAttr.IsTypeFloat
                              elif (info[0].lower() == "IsTypeDate".lower()):
                                 subAttr.IsTypeDate = info[1]
                                 typeDict['Date'] = subAttr.IsTypeDate
                              elif (info[0].lower() == "IsTypeBoolean".lower()):
                                 subAttr.IsTypeBoolean = info[1]
                                 typeDict['Boolean'] = subAttr.IsTypeBoolean
                              elif (info[0].lower() == "SubAttrChoices".lower()):
                                 subAttr.SubAttrChoices = info[1]
                                 subAttr.SubAttrChoicesFilter = info[1]
                              elif (info[0].lower() == "StringConstraints".lower()):
                                 subAttr.StringConstraints = info[1]
                                 constraintDict['String'] = subAttr.StringConstraints
                              elif (info[0].lower() == "IntegerConstraints".lower()):
                                 subAttr.IntegerConstraints = info[1]
                                 constraintDict['Integer'] = subAttr.IntegerConstraints
                              elif (info[0].lower() == "FPConstraints".lower()):
                                 subAttr.FPConstraints = info[1]
                                 constraintDict['Float'] = subAttr.FPConstraints
                              elif (info[0].lower() == "BooleanConstraints".lower()):
                                 subAttr.BooleanConstraints = info[1]
                                 constraintDict['Boolean'] = subAttr.BooleanConstraints
                              elif (info[0].lower() == "DateConstraints".lower()):
                                 subAttr.DateConstraints = info[1]
                                 constraintDict['Date'] = subAttr.DateConstraints
                              elif (info[0].lower() == "IsOptional".lower()):
                                 subAttr.IsOptional = info[1]
                              else:
                                 raise ValueError('Invalid field ' + info[0] + ' in config')

                          constraintValidator = ConstraintValidator(typeDict,constraintDict)
                          constraintValidator.validate()

                          listOfSubAttr.append(subAttr)

                     personalAttr.ListOfSubAttr = listOfSubAttr 
                     listOfPersonalAttr.append(personalAttr)

               personalDetails.listOfPersonalAttr = listOfPersonalAttr

               if (len(listOfUniqeNames) != len(list(set(listOfUniqeNames)))):
                raise ValueError('PersonalAttrName.SubAttrName must be unique in PersonalDetails')

               return personalDetails

        def getEducationalQualificationsInfo(self):

               educationalQualifications = EducationalQualifications()

               EQregex = str(self.EQStartPattern + "((.|\n)*?)" + self.EQEndPattern)
               EQ = str(re.findall(EQregex, self.fileData)[0][0])

               EAregex = str(self.EAStartPattern + "((.|\n)*?)" + self.EAEndPattern)
               EAs = re.findall(EAregex, EQ)
               EAs = [ea[0] for ea in EAs]
               listOfEduAttr = []      
               listOfUniqeNames = []


               for EABlock in EAs:
                     SAregex = str(self.SAStartPattern + "((.|\n)*?)" + self.SAEndPattern)
                     
                     EAInfo = re.sub(SAregex, '', str(EABlock))
                     EAInfo = re.findall(r'(\S[^:]+):\s*(.*\S)', str(EAInfo))

                     eduAttr = EduAttr()  

                     for info in EAInfo:
                          if (info[0].lower() == "EduAttrName".lower()):
                              eduAttr.EduAttrName = info[1]
                          elif (info[0].lower() == "EduAttrLabel".lower()):
                              eduAttr.EduAttrLabel = info[1]
                          elif (info[0].lower() == "MultipleEntries".lower()):
                              eduAttr.MultipleEntries = info[1]
                          elif (info[0].lower() == "IsOptional".lower()):
                              eduAttr.IsOptional = info[1]
                          else:
                              raise ValueError('Invalid field ' + info[0] + ' for EduAttr')

                     
                     SAs = re.findall(SAregex, str(EABlock))
                     listOfSubAttr = []

                     for SABlock in SAs:
                          SABlockInfo = re.findall(r'(\S[^:]+):\s*(.*\S)', SABlock[0])
                          subAttr = SubAttr()
                          
                          typeDict = {}
                          constraintDict = {}

                          for info in SABlockInfo:
                              if (info[0].lower() == "SubAttrName".lower()):
                                 subAttr.SubAttrName = info[1]
                                 listOfUniqeNames.append(eduAttr.EduAttrName+"."+subAttr.SubAttrName)
                              elif (info[0].lower() == "SubAttrLabel".lower()):
                                 subAttr.SubAttrLabel = info[1]
                              elif (info[0].lower() == "IsTypeString".lower()):
                                 subAttr.IsTypeString = info[1]
                                 typeDict['String'] = subAttr.IsTypeString
                              elif (info[0].lower() == "IsTypeInteger".lower()):
                                 subAttr.IsTypeInteger = info[1]
                                 typeDict['Integer'] = subAttr.IsTypeInteger
                              elif (info[0].lower() == "IsTypeFloat".lower()):
                                 subAttr.IsTypeFloat = info[1]
                                 typeDict['Float'] = subAttr.IsTypeFloat
                              elif (info[0].lower() == "IsTypeDate".lower()):
                                 subAttr.IsTypeDate = info[1]
                                 typeDict['Date'] = subAttr.IsTypeDate
                              elif (info[0].lower() == "IsTypeBoolean".lower()):
                                 subAttr.IsTypeBoolean = info[1]
                                 typeDict['Boolean'] = subAttr.IsTypeBoolean
                              elif (info[0].lower() == "SubAttrChoices".lower()):
                                 subAttr.SubAttrChoices = info[1]
                                 subAttr.SubAttrChoicesFilter = info[1]
                              elif (info[0].lower() == "StringConstraints".lower()):
                                 subAttr.StringConstraints = info[1]
                                 constraintDict['String'] = subAttr.StringConstraints
                              elif (info[0].lower() == "IntegerConstraints".lower()):
                                 subAttr.IntegerConstraints = info[1]
                                 constraintDict['Integer'] = subAttr.IntegerConstraints
                              elif (info[0].lower() == "FPConstraints".lower()):
                                 subAttr.FPConstraints = info[1]
                                 constraintDict['Float'] = subAttr.FPConstraints
                              elif (info[0].lower() == "BooleanConstraints".lower()):
                                 subAttr.BooleanConstraints = info[1]
                                 constraintDict['Boolean'] = subAttr.BooleanConstraints
                              elif (info[0].lower() == "DateConstraints".lower()):
                                 subAttr.DateConstraints = info[1]
                                 constraintDict['Date'] = subAttr.DateConstraints
                              elif (info[0].lower() == "IsOptional".lower()):
                                 subAttr.IsOptional = info[1]
                              else:
                                 raise ValueError('Invalid field ' + info[0] + ' in config')

                          constraintValidator = ConstraintValidator(typeDict,constraintDict)
                          constraintValidator.validate()

                          listOfSubAttr.append(subAttr)

                     eduAttr.ListOfSubAttr = listOfSubAttr 
                     listOfEduAttr.append(eduAttr)

               educationalQualifications.listOfEduAttr = listOfEduAttr

               if (len(listOfUniqeNames) != len(list(set(listOfUniqeNames)))):
                  raise ValueError('EduAttrName.SubAttrName must be unique in EducationalQualifications')

               return educationalQualifications


        def getWorkExperienceInfo(self):

               workExperience = WorkExperience()

               WEregex = str(self.WEStartPattern + "((.|\n)*?)" + self.WEEndPattern)
               WE = str(re.findall(WEregex, self.fileData)[0][0])

               SAregex = str(self.SAStartPattern + "((.|\n)*?)" + self.SAEndPattern)

               WEInfo = re.sub(SAregex, '', str(WE))
               WEInfo = re.findall(r'(\S[^:]+):\s*(.*\S)', str(WEInfo))

               for info in WEInfo:
                     if (info[0].lower() == "MultipleEntries".lower()):
                           workExperience.MultipleEntries = info[1]
                     elif (info[0].lower() == "IsOptional".lower()):
                           workExperience.IsOptional = info[1]
                     else:
                          raise ValueError('Invalid field ' + info[0] + ' for WorkExperience in config')

               SAs = re.findall(SAregex, WE)
               listOfSubAttr = []
               listOfUniqeNames = []

               for SABlock in SAs:
                     SABlockInfo = re.findall(r'(\S[^:]+):\s*(.*\S)', SABlock[0])
                     subAttr = SubAttr()
                     
                     typeDict = {}
                     constraintDict = {}

                     for info in SABlockInfo:
                        if (info[0].lower() == "SubAttrName".lower()):
                           subAttr.SubAttrName = info[1]
                           listOfUniqeNames.append(subAttr.SubAttrName)
                        elif (info[0].lower() == "SubAttrLabel".lower()):
                           subAttr.SubAttrLabel = info[1]
                        elif (info[0].lower() == "IsTypeString".lower()):
                           subAttr.IsTypeString = info[1]
                           typeDict['String'] = subAttr.IsTypeString
                        elif (info[0].lower() == "IsTypeInteger".lower()):
                           subAttr.IsTypeInteger = info[1]
                           typeDict['Integer'] = subAttr.IsTypeInteger
                        elif (info[0].lower() == "IsTypeFloat".lower()):
                           subAttr.IsTypeFloat = info[1]
                           typeDict['Float'] = subAttr.IsTypeFloat
                        elif (info[0].lower() == "IsTypeDate".lower()):
                           subAttr.IsTypeDate = info[1]
                           typeDict['Date'] = subAttr.IsTypeDate
                        elif (info[0].lower() == "IsTypeBoolean".lower()):
                           subAttr.IsTypeBoolean = info[1]
                           typeDict['Boolean'] = subAttr.IsTypeBoolean
                        elif (info[0].lower() == "SubAttrChoices".lower()):
                           subAttr.SubAttrChoices = info[1]
                           subAttr.SubAttrChoicesFilter = info[1]
                        elif (info[0].lower() == "StringConstraints".lower()):
                           subAttr.StringConstraints = info[1]
                           constraintDict['String'] = subAttr.StringConstraints
                        elif (info[0].lower() == "IntegerConstraints".lower()):
                           subAttr.IntegerConstraints = info[1]
                           constraintDict['Integer'] = subAttr.IntegerConstraints
                        elif (info[0].lower() == "FPConstraints".lower()):
                           subAttr.FPConstraints = info[1]
                           constraintDict['Float'] = subAttr.FPConstraints
                        elif (info[0].lower() == "BooleanConstraints".lower()):
                           subAttr.BooleanConstraints = info[1]
                           constraintDict['Boolean'] = subAttr.BooleanConstraints
                        elif (info[0].lower() == "DateConstraints".lower()):
                           subAttr.DateConstraints = info[1]
                           constraintDict['Date'] = subAttr.DateConstraints
                        elif (info[0].lower() == "IsOptional".lower()):
                           subAttr.IsOptional = info[1]
                        else:
                           raise ValueError('Invalid field ' + info[0] + ' in config')

                     constraintValidator = ConstraintValidator(typeDict,constraintDict)
                     constraintValidator.validate()

                     listOfSubAttr.append(subAttr)

               workExperience.ListOfSubAttr = listOfSubAttr

               if (len(listOfUniqeNames) != len(list(set(listOfUniqeNames)))):
                  raise ValueError('SubAttrName must be unique in WorkExperience')

               return workExperience

        def getAttachmentsInfo(self):

               attachments = Attachments()

               ASregex = str(self.ASStartPattern + "((.|\n)*?)" + self.ASEndPattern)
               ASs = str(re.findall(ASregex, self.fileData)[0][0])

               AIregex = str(self.AIStartPattern + "((.|\n)*?)" + self.AIEndPattern)
               AIs = re.findall(AIregex, ASs)
               AIs = [ai[0] for ai in AIs]
               listOfAttachmentInfo = []   
               listOfUniqeNames = []   


               for AIBlock in AIs:
                     Aregex = str(self.AStartPattern + "((.|\n)*?)" + self.AEndPattern)
                     
                     AIInfo = re.sub(Aregex, '', str(AIBlock))
                     AIInfo = re.findall(r'(\S[^:]+):\s*(.*\S)', str(AIInfo))

                     attachmentInfo = AttachmentInfo()  

                     for info in AIInfo:
                          if (info[0].lower() == "AttachmentInfoName".lower()):
                              attachmentInfo.AttachmentInfoName = info[1]
                          elif (info[0].lower() == "AttachmentInfoLabel".lower()):
                              attachmentInfo.AttachmentInfoLabel = info[1]
                          elif (info[0].lower() == "MultipleEntries".lower()):
                              attachmentInfo.MultipleEntries = info[1]
                          elif (info[0].lower() == "IsOptional".lower()):
                              attachmentInfo.IsOptional = info[1]
                          else:
                              raise ValueError('Invalid field ' + info[0] + ' for AttachmentInfo')

                     
                     As = re.findall(Aregex, str(AIBlock))
                     listOfAttachment = []

                     for ABlock in As:
                          ABlockInfo = re.findall(r'(\S[^:]+):\s*(.*\S)', ABlock[0])
                          attachment = Attachment()

                          typeDict = {}

                          for info in ABlockInfo:
                              if (info[0].lower() == "AttachmentName".lower()):
                                 attachment.AttachmentName = info[1]
                                 listOfUniqeNames.append(attachmentInfo.AttachmentInfoName+"."+attachment.AttachmentName)
                              elif (info[0].lower() == "AttachmentLabel".lower()):
                                 attachment.AttachmentLabel = info[1]
                              elif (info[0].lower() == "IsTypeFile".lower()):
                                 attachment.IsTypeFile = info[1]
                                 typeDict['IsTypeFile'] = attachment.IsTypeFile
                              elif (info[0].lower() == "IsTypeImage".lower()):
                                 attachment.IsTypeImage = info[1]
                                 typeDict['IsTypeImage'] = attachment.IsTypeImage
                              elif (info[0].lower() == "IsOptional".lower()):
                                 attachment.IsOptional = info[1]
                              else:
                                 raise ValueError('Invalid field ' + info[0] + ' in config')

                          attachmentConstraintValidator = AttachmentConstraintValidator(typeDict)
                          attachmentConstraintValidator.validate()

                          listOfAttachment.append(attachment)

                     attachmentInfo.ListOfAttachment = listOfAttachment
                     listOfAttachmentInfo.append(attachmentInfo)


               attachments.listOfAttachmentInfo = listOfAttachmentInfo

               if (len(listOfUniqeNames) != len(list(set(listOfUniqeNames)))):
                  raise ValueError('SubAttrName must be unique in WorkExperience')

               return attachments


# def main():
        
#         configParser = ConfigParser("/home/adildangui/Desktop/webDev/djangoProject/Portal/createForm.cfg")
#         print (configParser.getAdmissionDetails())
#         print (configParser.getEducationalQualificationsInfo().listOfEduAttr[2].ListOfSubAttr[0].IsTypeInteger)
#         print (configParser.getWorkExperienceInfo())
#         print (configParser.getAttachmentInfo())

# main()  

