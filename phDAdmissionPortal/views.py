import os
import ast
import uuid
import copy
import sys
import glob
import shutil
import tempfile
import itertools
from builtins import FileExistsError
from django.shortcuts import render
from django.db.models import Q
from Portal.ConfigParser.ConfigParser import ConfigParser
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from phDAdmissionPortal.models import PersonalDetails as PersonalDetailsModel
from phDAdmissionPortal.models import EducationalQualifications as EducationalQualificationsModel
from phDAdmissionPortal.models import WorkExperience as WorkExperienceModel
from phDAdmissionPortal.models import Attachments as AttachmentsModel


# Create your views here.

configParser = ConfigParser(os.path.dirname(os.path.realpath(__file__))+"/createForm.cfg")


def AdmissionDetails(request):

    context = {}
    context['AdmissionDetailsInfo'] = configParser.getAdmissionDetails()

    if (ast.literal_eval(str(request.POST.get('ApplyInfo'))) == True):
        request.session['UUID'] =  str(uuid.uuid1())
        return redirect('PersonalDetails')

    if (ast.literal_eval(str(request.POST.get('AdminLogin'))) == True):
        return redirect('AdminLogin')

    return render(request,"AdmissionDetails.html",context)


def PersonalDetails(request):

    if not request.session.has_key('UUID'):
        return redirect('AdmissionDetails')

    context = {}
    personalDetailsInfo = configParser.getPersonalDetailsInfo()

    dictOfMultipleEntriesPer = {}
    dictOfAddAddMore = {}
    
    if (request.session.get('CompletedConfirmAndSubmitPer')  == None):
        request.session['CompletedConfirmAndSubmitPer'] = []

    completedConfirmAndSubmitPer = request.session['CompletedConfirmAndSubmitPer']
    defaultPerAttrDisplay =  [pAttr.PersonalAttrName for pAttr in personalDetailsInfo.listOfPersonalAttr if pAttr.PersonalAttrName not in completedConfirmAndSubmitPer]

    for personalAttr in personalDetailsInfo.listOfPersonalAttr:
        locals()[personalAttr.PersonalAttrName] = {}
        dictOfMultipleEntriesPer[personalAttr.PersonalAttrName] = locals()[personalAttr.PersonalAttrName] 
    for personalAttr in personalDetailsInfo.listOfPersonalAttr:
        locals()[personalAttr.PersonalAttrName] = {} 
        dictOfAddAddMore[personalAttr.PersonalAttrName] = locals()[personalAttr.PersonalAttrName]
        dictOfAddAddMore[personalAttr.PersonalAttrName]["AddMore"] = "False"
        dictOfAddAddMore[personalAttr.PersonalAttrName]["Add"] = "True"
        dictOfAddAddMore[personalAttr.PersonalAttrName]["RemoveAdd"] = "False"

    context["EditEnable"] =  True
    context["ConfirmEnable"] =  False


    if (request.POST.get('addInfo') is not None):

        addInfo = ast.literal_eval(request.POST.get('addInfo'))

        personalAttrName = addInfo[0]
        dictOfMultipleEntriesPer = ast.literal_eval(str(addInfo[1]))
        dictOfAddAddMore = ast.literal_eval(str(addInfo[2]))

        personalAttr = [pAttr for pAttr in personalDetailsInfo.listOfPersonalAttr if (pAttr.PersonalAttrName == personalAttrName)][0]
        personalAttrDict = {}

        for subAttr in personalAttr.ListOfSubAttr:
            if (subAttr.SubAttrChoices):
                if ((str(request.POST.get(subAttr.SubAttrName))).startswith('Other')):
                    personalAttrDict[subAttr.SubAttrName] = request.POST.get(str(subAttr.SubAttrName+"Other"))
                else:
                    personalAttrDict[subAttr.SubAttrName] = str(request.POST.get(subAttr.SubAttrName)).split(":")[0]
            else:
                personalAttrDict[subAttr.SubAttrName] = request.POST.get(subAttr.SubAttrName)

        maxim = 0
        if (dictOfMultipleEntriesPer[personalAttrName]):
            maxim = max(dictOfMultipleEntriesPer[personalAttrName], key=int)

        allSubAttrHaveChoices = True

        for subAttr in personalAttr.ListOfSubAttr:
            if (not subAttr.SubAttrChoices):
                allSubAttrHaveChoices = False
                break

        tempPersonalAttrDict = copy.deepcopy(personalAttrDict)
        for subAttr in personalAttr.ListOfSubAttr:
            if (subAttr.SubAttrChoices and not ((str(request.POST.get(subAttr.SubAttrName))).startswith('Other')) ):
                del tempPersonalAttrDict[subAttr.SubAttrName]

        if (list(filter(lambda a: a != '' , list(tempPersonalAttrDict.values()))) or allSubAttrHaveChoices):
            dictOfMultipleEntriesPer[personalAttrName][maxim+1] = personalAttrDict
            dictOfAddAddMore[personalAttrName]["AddMore"] = "True"
            dictOfAddAddMore[personalAttrName]["Add"] = "False"
            dictOfAddAddMore[personalAttrName]["RemoveAdd"] = "False"    

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False

    elif (request.POST.get('addMoreInfo') is not None):

        addMoreInfo = ast.literal_eval(request.POST.get('addMoreInfo'))

        personalAttrName = addMoreInfo[0]
        dictOfMultipleEntriesPer = ast.literal_eval(str(addMoreInfo[1]))
        dictOfAddAddMore = ast.literal_eval(str(addMoreInfo[2]))

        dictOfAddAddMore[personalAttrName]["AddMore"] = "False"
        dictOfAddAddMore[personalAttrName]["Add"] = "True"
        dictOfAddAddMore[personalAttrName]["RemoveAdd"] = "False"

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False

    elif (request.POST.get('deleteInfo') is not None):

        deleteInfo = ast.literal_eval(request.POST.get('deleteInfo'))

        personalAttrName = deleteInfo[0]
        personalAttrNameId = deleteInfo[1]
        dictOfMultipleEntriesPer = ast.literal_eval(str(deleteInfo[2]))
        dictOfAddAddMore = ast.literal_eval(str(deleteInfo[3]))

        del dictOfMultipleEntriesPer[personalAttrName][int(personalAttrNameId)]

        maxim = 1
        if (dictOfMultipleEntriesPer[personalAttrName]):
            maxim = max(dictOfMultipleEntriesPer[personalAttrName], key=int)

        currIter = 1
        tempDict = {}

        for iter in range(1,maxim+1):
            if iter != int(personalAttrNameId):
                tempDict[currIter] = dictOfMultipleEntriesPer[personalAttrName][iter]
                currIter +=1

        dictOfMultipleEntriesPer[personalAttrName] = tempDict

        if (not dictOfMultipleEntriesPer[personalAttrName]):
            dictOfAddAddMore[personalAttrName]["AddMore"] = "False"
            dictOfAddAddMore[personalAttrName]["Add"] = "True"
        else:
            dictOfAddAddMore[personalAttrName]["AddMore"] = "True"
            dictOfAddAddMore[personalAttrName]["Add"] = "False"

        dictOfAddAddMore[personalAttrName]["RemoveAdd"] = "False"

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False

    elif (request.POST.get('removeAddInfo') is not None):

        removeAddInfo = ast.literal_eval(request.POST.get('removeAddInfo'))

        personalAttrName = removeAddInfo[0]
        dictOfMultipleEntriesPer = ast.literal_eval(str(removeAddInfo[1]))
        dictOfAddAddMore = ast.literal_eval(str(removeAddInfo[2]))

        dictOfAddAddMore[personalAttrName]["AddMore"] = "True"
        dictOfAddAddMore[personalAttrName]["Add"] = "False"
        dictOfAddAddMore[personalAttrName]["RemoveAdd"] = "False"

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False

    elif (request.POST.get('nextInfo') is not None):

        nextInfo = ast.literal_eval(str(request.POST.get('nextInfo')))

        personalAttrName = str(nextInfo[0])
        dictOfMultipleEntriesPer = ast.literal_eval(str(nextInfo[1]))
        dictOfAddAddMore = ast.literal_eval(str(nextInfo[2])) 

        for pAttr in personalDetailsInfo.listOfPersonalAttr:
            if pAttr.PersonalAttrName == personalAttrName:
                personalAttr = pAttr

        personalAttrName = personalAttr.PersonalAttrName
        personalAttrDict = {}
        for subAttr in personalAttr.ListOfSubAttr:
            personalAttrDict[subAttr.SubAttrName] = request.POST.get(subAttr.SubAttrName)    

        maxim = 0

        for subAttr in personalAttr.ListOfSubAttr:
            if (subAttr.SubAttrChoices):
                if ((str(request.POST.get(subAttr.SubAttrName))).startswith('Other')):
                    personalAttrDict[subAttr.SubAttrName] = request.POST.get(str(subAttr.SubAttrName+"Other"))
                else:
                    personalAttrDict[subAttr.SubAttrName] = str(request.POST.get(subAttr.SubAttrName)).split(":")[0]
            else:
                personalAttrDict[subAttr.SubAttrName] = request.POST.get(subAttr.SubAttrName)

        if (dictOfMultipleEntriesPer[personalAttrName]):
            maxim = max(dictOfMultipleEntriesPer[personalAttrName], key=int)            

        allSubAttrHaveChoices = True
        for subAttr in personalAttr.ListOfSubAttr:
            if (not subAttr.SubAttrChoices):
                allSubAttrHaveChoices = False
                break

        tempPersonalAttrDict = copy.deepcopy(personalAttrDict)
        for subAttr in personalAttr.ListOfSubAttr:
            if (subAttr.SubAttrChoices and not ((str(request.POST.get(subAttr.SubAttrName))).startswith('Other')) ):
                del tempPersonalAttrDict[subAttr.SubAttrName]

        listOfAllSubAttrValues = []
        for subAttr in personalAttr.ListOfSubAttr:
            listOfAllSubAttrValues.append(personalAttrDict[subAttr.SubAttrName])

        if ((list(filter(lambda a: a != None , list(tempPersonalAttrDict.values()))) and list(filter(lambda a: a != '' , list(tempPersonalAttrDict.values())))) or (allSubAttrHaveChoices and list(filter(lambda a: a != 'None' , listOfAllSubAttrValues)))):

           dictOfMultipleEntriesPer[personalAttrName][maxim+1] = personalAttrDict

        context["EditEnable"] =  False
        context["ConfirmEnable"] =  True

    elif (request.POST.get('goBackAndEditInfo') is not None):

        goBackAndEditInfo = ast.literal_eval(request.POST.get('goBackAndEditInfo'))

        dictOfMultipleEntriesPer = ast.literal_eval(str(goBackAndEditInfo[0]))
        dictOfAddAddMore = ast.literal_eval(str(goBackAndEditInfo[1]))

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False           

    elif (request.POST.get('confirmAndSubmitPerInfo') is not None):

        confirmAndSubmitInfo = ast.literal_eval(str(request.POST.get('confirmAndSubmitPerInfo')))

        perAttrName = str(confirmAndSubmitInfo[0])
        dictOfMultipleEntriesPer = ast.literal_eval(str(confirmAndSubmitInfo[1]))

        completedConfirmAndSubmitPer = request.session.get('CompletedConfirmAndSubmitPer')
        completedConfirmAndSubmitPer.append(perAttrName)
        request.session['CompletedConfirmAndSubmitPer'] = completedConfirmAndSubmitPer

        if (perAttrName == personalDetailsInfo.listOfPersonalAttr[-1].PersonalAttrName):
            request.session['DictOfMultipleEntriesPer'] = dictOfMultipleEntriesPer
            return redirect('EducationalQualifications')
        else:
            defaultPerAttrDisplay =  [pAttr.PersonalAttrName for pAttr in personalDetailsInfo.listOfPersonalAttr if pAttr.PersonalAttrName not in completedConfirmAndSubmitPer]
        

    context['DictOfAddAddMore'] = dictOfAddAddMore
    context['DictOfMultipleEntriesPer'] = dictOfMultipleEntriesPer    
    context['PersonalDetailsInfo'] = personalDetailsInfo
    context['CompletedConfirmAndSubmitPer'] = completedConfirmAndSubmitPer
    context['DefaultPerAttrDisplay'] = defaultPerAttrDisplay

    return render(request,"PersonalDetails.html",context)


def EducationalQualifications(request):

    if ((not request.session.has_key('UUID')) or (not request.session.has_key('DictOfMultipleEntriesPer'))):
        return redirect('AdmissionDetails')

    context = {}
    educationalQualificationsInfo = configParser.getEducationalQualificationsInfo()

    dictOfMultipleEntriesEdu = {}
    dictOfAddAddMore = {}

    if (request.session.get('CompletedConfirmAndSubmitEdu')  == None):
        request.session['CompletedConfirmAndSubmitEdu'] = []

    completedConfirmAndSubmitEdu = request.session['CompletedConfirmAndSubmitEdu']
    defaultEduAttrDisplay =  [eAttr.EduAttrName for eAttr in educationalQualificationsInfo.listOfEduAttr if eAttr.EduAttrName not in completedConfirmAndSubmitEdu]

    for eduAttr in educationalQualificationsInfo.listOfEduAttr:
        locals()[eduAttr.EduAttrName] = {}
        dictOfMultipleEntriesEdu[eduAttr.EduAttrName] = locals()[eduAttr.EduAttrName] 
    for eduAttr in educationalQualificationsInfo.listOfEduAttr:
        locals()[eduAttr.EduAttrName] = {} 
        dictOfAddAddMore[eduAttr.EduAttrName] = locals()[eduAttr.EduAttrName]
        dictOfAddAddMore[eduAttr.EduAttrName]["AddMore"] = "False"
        dictOfAddAddMore[eduAttr.EduAttrName]["Add"] = "True"
        dictOfAddAddMore[eduAttr.EduAttrName]["RemoveAdd"] = "False"

    context["EditEnable"] =  True
    context["ConfirmEnable"] =  False


    if (request.POST.get('addInfo') is not None):

        addInfo = ast.literal_eval(request.POST.get('addInfo'))

        eduAttrName = addInfo[0]
        dictOfMultipleEntriesEdu = ast.literal_eval(str(addInfo[1]))
        dictOfAddAddMore = ast.literal_eval(str(addInfo[2]))

        eduAttr = [eAttr for eAttr in educationalQualificationsInfo.listOfEduAttr if (eAttr.EduAttrName == eduAttrName)][0]
        eduAttrDict = {}

        for subAttr in eduAttr.ListOfSubAttr:
            if (subAttr.SubAttrChoices):
                if ((str(request.POST.get(subAttr.SubAttrName))).startswith('Other')):
                    eduAttrDict[subAttr.SubAttrName] = request.POST.get(str(subAttr.SubAttrName+"Other"))
                else:
                    eduAttrDict[subAttr.SubAttrName] = str(request.POST.get(subAttr.SubAttrName)).split(":")[0]
            else:
                eduAttrDict[subAttr.SubAttrName] = request.POST.get(subAttr.SubAttrName)

        maxim = 0
        if (dictOfMultipleEntriesEdu[eduAttrName]):
            maxim = max(dictOfMultipleEntriesEdu[eduAttrName], key=int)

        allSubAttrHaveChoices = True
        for subAttr in eduAttr.ListOfSubAttr:
            if (not subAttr.SubAttrChoices):
                allSubAttrHaveChoices = False
                break

        tempEduAttrDict = copy.deepcopy(eduAttrDict)

        for subAttr in eduAttr.ListOfSubAttr:
            if (subAttr.SubAttrChoices and not ((str(request.POST.get(subAttr.SubAttrName))).startswith('Other'))):
                del tempEduAttrDict[subAttr.SubAttrName]

        if (list(filter(lambda a: a != '' , list(tempEduAttrDict.values()))) or allSubAttrHaveChoices):
            dictOfMultipleEntriesEdu[eduAttrName][maxim+1] = eduAttrDict
            dictOfAddAddMore[eduAttrName]["AddMore"] = "True"
            dictOfAddAddMore[eduAttrName]["Add"] = "False"
            dictOfAddAddMore[eduAttrName]["RemoveAdd"] = "False"    

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False

    elif (request.POST.get('addMoreInfo') is not None):

        addMoreInfo = ast.literal_eval(request.POST.get('addMoreInfo'))

        eduAttrName = addMoreInfo[0]
        dictOfMultipleEntriesEdu = ast.literal_eval(str(addMoreInfo[1]))
        dictOfAddAddMore = ast.literal_eval(str(addMoreInfo[2]))

        dictOfAddAddMore[eduAttrName]["AddMore"] = "False"
        dictOfAddAddMore[eduAttrName]["Add"] = "True"
        dictOfAddAddMore[eduAttrName]["RemoveAdd"] = "False"

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False

    elif (request.POST.get('deleteInfo') is not None):

        deleteInfo = ast.literal_eval(request.POST.get('deleteInfo'))

        eduAttrName = deleteInfo[0]
        eduAttrNameId = deleteInfo[1]
        dictOfMultipleEntriesEdu = ast.literal_eval(str(deleteInfo[2]))
        dictOfAddAddMore = ast.literal_eval(str(deleteInfo[3]))

        del dictOfMultipleEntriesEdu[eduAttrName][int(eduAttrNameId)]

        maxim = 1
        if (dictOfMultipleEntriesEdu[eduAttrName]):
            maxim = max(dictOfMultipleEntriesEdu[eduAttrName], key=int)

        currIter = 1
        tempDict = {}

        for iter in range(1,maxim+1):
            if iter != int(eduAttrNameId):
                tempDict[currIter] = dictOfMultipleEntriesEdu[eduAttrName][iter]
                currIter +=1

        dictOfMultipleEntriesEdu[eduAttrName] = tempDict

        if (not dictOfMultipleEntriesEdu[eduAttrName]):
            dictOfAddAddMore[eduAttrName]["AddMore"] = "False"
            dictOfAddAddMore[eduAttrName]["Add"] = "True"
        else:
            dictOfAddAddMore[eduAttrName]["AddMore"] = "True"
            dictOfAddAddMore[eduAttrName]["Add"] = "False"

        dictOfAddAddMore[eduAttrName]["RemoveAdd"] = "False"

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False

    elif (request.POST.get('removeAddInfo') is not None):

        removeAddInfo = ast.literal_eval(request.POST.get('removeAddInfo'))

        eduAttrName = removeAddInfo[0]
        dictOfMultipleEntriesEdu = ast.literal_eval(str(removeAddInfo[1]))
        dictOfAddAddMore = ast.literal_eval(str(removeAddInfo[2]))

        dictOfAddAddMore[eduAttrName]["AddMore"] = "True"
        dictOfAddAddMore[eduAttrName]["Add"] = "False"
        dictOfAddAddMore[eduAttrName]["RemoveAdd"] = "False"

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False

    elif (request.POST.get('nextInfo') is not None):

        nextInfo = ast.literal_eval(str(request.POST.get('nextInfo')))

        eduAttrName = str(nextInfo[0])
        dictOfMultipleEntriesEdu = ast.literal_eval(str(nextInfo[1]))
        dictOfAddAddMore = ast.literal_eval(str(nextInfo[2])) 

        for eAttr in educationalQualificationsInfo.listOfEduAttr:
            if eAttr.EduAttrName == eduAttrName:
                eduAttr = eAttr    

        eduAttrName = eduAttr.EduAttrName
        eduAttrDict = {}
        for subAttr in eduAttr.ListOfSubAttr:
            eduAttrDict[subAttr.SubAttrName] = request.POST.get(subAttr.SubAttrName)    

        maxim = 0

        for subAttr in eduAttr.ListOfSubAttr:
            if (subAttr.SubAttrChoices):
                if ((str(request.POST.get(subAttr.SubAttrName))).startswith('Other')):
                    eduAttrDict[subAttr.SubAttrName] = request.POST.get(str(subAttr.SubAttrName+"Other"))
                else:
                    eduAttrDict[subAttr.SubAttrName] = str(request.POST.get(subAttr.SubAttrName)).split(":")[0]
            else:
                eduAttrDict[subAttr.SubAttrName] = request.POST.get(subAttr.SubAttrName)

        if (dictOfMultipleEntriesEdu[eduAttrName]):
            maxim = max(dictOfMultipleEntriesEdu[eduAttrName], key=int)            
    
        allSubAttrHaveChoices = True
        for subAttr in eduAttr.ListOfSubAttr:
            if (not subAttr.SubAttrChoices):
                allSubAttrHaveChoices = False
                break

        tempEduAttrDict = copy.deepcopy(eduAttrDict)

        for subAttr in eduAttr.ListOfSubAttr:
            if (subAttr.SubAttrChoices and not ((str(request.POST.get(subAttr.SubAttrName))).startswith('Other'))):
                del tempEduAttrDict[subAttr.SubAttrName]

        listOfAllSubAttrValues = []
        for subAttr in eduAttr.ListOfSubAttr:
            listOfAllSubAttrValues.append(eduAttrDict[subAttr.SubAttrName])

        if ((list(filter(lambda a: a != None , list(tempEduAttrDict.values()))) and list(filter(lambda a: a != '' , list(tempEduAttrDict.values())))) or (allSubAttrHaveChoices and list(filter(lambda a: a != 'None' , listOfAllSubAttrValues)))):
            dictOfMultipleEntriesEdu[eduAttrName][maxim+1] = eduAttrDict

        context["EditEnable"] =  False
        context["ConfirmEnable"] =  True

    elif (request.POST.get('goBackAndEditInfo') is not None):

        goBackAndEditInfo = ast.literal_eval(request.POST.get('goBackAndEditInfo'))

        dictOfMultipleEntriesEdu = ast.literal_eval(str(goBackAndEditInfo[0]))
        dictOfAddAddMore = ast.literal_eval(str(goBackAndEditInfo[1]))

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False            

    elif (request.POST.get('confirmAndSubmitEduInfo') is not None):

        confirmAndSubmitInfo = ast.literal_eval(str(request.POST.get('confirmAndSubmitEduInfo')))

        eduAttrName = str(confirmAndSubmitInfo[0])
        dictOfMultipleEntriesEdu = ast.literal_eval(str(confirmAndSubmitInfo[1]))
            
        completedConfirmAndSubmitEdu = request.session.get('CompletedConfirmAndSubmitEdu')
        completedConfirmAndSubmitEdu.append(eduAttrName)
        request.session['CompletedConfirmAndSubmitEdu'] = completedConfirmAndSubmitEdu

        if (eduAttrName == educationalQualificationsInfo.listOfEduAttr[-1].EduAttrName):
            request.session['DictOfMultipleEntriesEdu'] = dictOfMultipleEntriesEdu
            return redirect('WorkExperience')
        else:
            defaultEduAttrDisplay =  [eAttr.EduAttrName for eAttr in educationalQualificationsInfo.listOfEduAttr if eAttr.EduAttrName not in completedConfirmAndSubmitEdu]


    context['DictOfAddAddMore'] = dictOfAddAddMore
    context['DictOfMultipleEntriesEdu'] = dictOfMultipleEntriesEdu
    context['EducationalQualificationsInfo'] = educationalQualificationsInfo
    context['CompletedConfirmAndSubmitEdu'] = completedConfirmAndSubmitEdu
    context['DefaultEduAttrDisplay'] = defaultEduAttrDisplay

    return render(request,"EducationalQualifications.html",context)


def WorkExperience(request):

    if ((not request.session.has_key('UUID')) or (not request.session.has_key('DictOfMultipleEntriesPer')) or  (not request.session.has_key('DictOfMultipleEntriesEdu'))):
        return redirect('AdmissionDetails')

    context = {}
    workExperienceInfo = configParser.getWorkExperienceInfo()

    dictOfMultipleWorkExperiences = {}
    dictOfAddAddMore = {}

    dictOfAddAddMore["AddMore"] = "False"
    dictOfAddAddMore["Add"] = "True"
    dictOfAddAddMore["RemoveAdd"] = "False"

    context["EditEnable"] =  True
    context["ConfirmEnable"] =  False

    if (request.POST.get('addInfo') is not None):

        addInfo = ast.literal_eval(request.POST.get('addInfo'))

        dictOfMultipleWorkExperiences = ast.literal_eval(str(addInfo[0]))
        dictOfAddAddMore = ast.literal_eval(str(addInfo[1]))

        workExpDict = {}

        for subAttr in workExperienceInfo.ListOfSubAttr:
            if (subAttr.SubAttrChoices):
                if ((str(request.POST.get(subAttr.SubAttrName))).startswith('Other')):
                    workExpDict[subAttr.SubAttrName] = request.POST.get(str(subAttr.SubAttrName+"Other"))
                else:
                    workExpDict[subAttr.SubAttrName] = str(request.POST.get(subAttr.SubAttrName)).split(":")[0]
            else:
                workExpDict[subAttr.SubAttrName] = request.POST.get(subAttr.SubAttrName)

        maxim = 0
        if (dictOfMultipleWorkExperiences):
            maxim = max(dictOfMultipleWorkExperiences, key=int)

        allSubAttrHaveChoices = True
        for subAttr in workExperienceInfo.ListOfSubAttr:
            if (not subAttr.SubAttrChoices):
                allSubAttrHaveChoices = False
                break

        tempWorkExpDict = copy.deepcopy(workExpDict)
        for subAttr in workExperienceInfo.ListOfSubAttr:
            if (subAttr.SubAttrChoices and not ((str(request.POST.get(subAttr.SubAttrName))).startswith('Other'))):
                del tempWorkExpDict[subAttr.SubAttrName]

        if (list(filter(lambda a: a != '' , list(tempWorkExpDict.values()))) or allSubAttrHaveChoices):
            dictOfMultipleWorkExperiences[maxim+1] = workExpDict
            dictOfAddAddMore["AddMore"] = "True"
            dictOfAddAddMore["Add"] = "False"
            dictOfAddAddMore["RemoveAdd"] = "False"

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False

    elif (request.POST.get('addMoreInfo') is not None):

        addMoreInfo = ast.literal_eval(request.POST.get('addMoreInfo'))

        dictOfMultipleWorkExperiences = ast.literal_eval(str(addMoreInfo[0]))
        dictOfAddAddMore = ast.literal_eval(str(addMoreInfo[1]))

        dictOfAddAddMore["AddMore"] = "False"
        dictOfAddAddMore["Add"] = "True"
        dictOfAddAddMore["RemoveAdd"] = "False"

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False

    elif (request.POST.get('deleteInfo') is not None):

        deleteInfo = ast.literal_eval(request.POST.get('deleteInfo'))

        workExpId = deleteInfo[0]
        dictOfMultipleWorkExperiences = ast.literal_eval(str(deleteInfo[1]))
        dictOfAddAddMore = ast.literal_eval(str(deleteInfo[2]))

        del dictOfMultipleWorkExperiences[int(workExpId)]

        maxim = 1
        if (dictOfMultipleWorkExperiences):
            maxim = max(dictOfMultipleWorkExperiences, key=int)

        currIter = 1
        tempDict = {}

        for iter in range(1,maxim+1):
            if iter != int(workExpId):
                tempDict[currIter] = dictOfMultipleWorkExperiences[iter]
                currIter +=1

        dictOfMultipleWorkExperiences = tempDict

        if (not dictOfMultipleWorkExperiences):
            dictOfAddAddMore["AddMore"] = "False"
            dictOfAddAddMore["Add"] = "True"
        else:
            dictOfAddAddMore["AddMore"] = "True"
            dictOfAddAddMore["Add"] = "False"

        dictOfAddAddMore["RemoveAdd"] = "False"

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False

    elif (request.POST.get('removeAddInfo') is not None):

        removeAddInfo = ast.literal_eval(request.POST.get('removeAddInfo'))

        dictOfMultipleWorkExperiences = ast.literal_eval(str(removeAddInfo[0]))
        dictOfAddAddMore = ast.literal_eval(str(removeAddInfo[1]))

        dictOfAddAddMore["AddMore"] = "True"
        dictOfAddAddMore["Add"] = "False"
        dictOfAddAddMore["RemoveAdd"] = "False"

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False

    elif (request.POST.get('nextInfo') is not None):

        nextInfo = ast.literal_eval(request.POST.get('nextInfo'))

        dictOfMultipleWorkExperiences = ast.literal_eval(str(nextInfo[0]))
        dictOfAddAddMore = ast.literal_eval(str(nextInfo[1]))    

        workExpDict = {}
        for subAttr in workExperienceInfo.ListOfSubAttr:
            workExpDict[subAttr.SubAttrName] = request.POST.get(subAttr.SubAttrName)    

        maxim = 0

        if (dictOfMultipleWorkExperiences):
            maxim = max(dictOfMultipleWorkExperiences, key=int)            

        allSubAttrHaveChoices = True
        for subAttr in workExperienceInfo.ListOfSubAttr:
            if (not subAttr.SubAttrChoices):
                allSubAttrHaveChoices = False
                break

        tempWorkExpDict = copy.deepcopy(workExpDict)
        for subAttr in workExperienceInfo.ListOfSubAttr:
            if (subAttr.SubAttrChoices and not ((str(request.POST.get(subAttr.SubAttrName))).startswith('Other'))):
                del tempWorkExpDict[subAttr.SubAttrName]

        listOfAllSubAttrValues = []
        for subAttr in workExperienceInfo.ListOfSubAttr:
            listOfAllSubAttrValues.append(workExpDict[subAttr.SubAttrName])

        if ((list(filter(lambda a: a != None , list(tempWorkExpDict.values()))) and list(filter(lambda a: a != '' , list(tempWorkExpDict.values())))) or (allSubAttrHaveChoices and list(filter(lambda a: a != 'None' , listOfAllSubAttrValues)))):
            dictOfMultipleWorkExperiences[maxim+1] = workExpDict

        context["EditEnable"] =  False
        context["ConfirmEnable"] =  True

    elif (request.POST.get('goBackAndEditInfo') is not None):

        goBackAndEditInfo = ast.literal_eval(request.POST.get('goBackAndEditInfo'))

        dictOfMultipleWorkExperiences = ast.literal_eval(str(goBackAndEditInfo[0]))
        dictOfAddAddMore = ast.literal_eval(str(goBackAndEditInfo[1]))

        context["EditEnable"] =  True
        context["ConfirmEnable"] =  False            

    elif (request.POST.get('confirmAndSubmitWorkInfo') is not None):

        confirmAndSubmitInfo = ast.literal_eval(request.POST.get('confirmAndSubmitWorkInfo'))

        dictOfMultipleWorkExperiences = ast.literal_eval(str(confirmAndSubmitInfo[0]))
        request.session['DictOfMultipleWorkExperiences'] = dictOfMultipleWorkExperiences
        return redirect('Attachments')

    context['DictOfAddAddMore'] = dictOfAddAddMore
    context['DictOfMultipleWorkExperiences'] = dictOfMultipleWorkExperiences
    context['WorkExperienceInfo'] = workExperienceInfo

    return render(request,"WorkExperience.html",context)


def Attachments(request):

    if ((not request.session.has_key('UUID')) or (not request.session.has_key('DictOfMultipleEntriesPer')) or \
        (not request.session.has_key('DictOfMultipleEntriesEdu')) or \
        (not request.session.has_key('DictOfMultipleWorkExperiences'))):
        return redirect('AdmissionDetails')

    context = {}
    attachmentsInfo = configParser.getAttachmentsInfo()

    if (request.session.get('CompletedConfirmAndSubmitAttachments')  == None):
        request.session['CompletedConfirmAndSubmitAttachments'] = []

    completedConfirmAndSubmitAttachments = request.session['CompletedConfirmAndSubmitAttachments']
    defaultAttachmentsInfoDisplay =  [att.AttachmentInfoName for att in attachmentsInfo.listOfAttachmentInfo if att.AttachmentInfoName not in completedConfirmAndSubmitAttachments]

    dictOfMultipleEntriesAttachmentsFileNames = {}
    intialDictOfMultipleEntriesAttachmentsFileNames = {}
    dictOfAddAddMore = {}

    tempDir = None

    if (request.session.has_key('TempDir')):
        tempDir = request.session.get('TempDir')
    else:
        tempDir = tempfile.mkdtemp()
        request.session['TempDir'] = tempDir

    for attachmentInfo in attachmentsInfo.listOfAttachmentInfo:
      locals()[attachmentInfo.AttachmentInfoName] = {} 
      dictOfMultipleEntriesAttachmentsFileNames[attachmentInfo.AttachmentInfoName] = locals()[attachmentInfo.AttachmentInfoName]
    for attachmentInfo in attachmentsInfo.listOfAttachmentInfo:
      locals()[attachmentInfo.AttachmentInfoName] = {} 
      dictOfAddAddMore[attachmentInfo.AttachmentInfoName] = locals()[attachmentInfo.AttachmentInfoName]
      dictOfAddAddMore[attachmentInfo.AttachmentInfoName]["AddMore"] = "False"
      dictOfAddAddMore[attachmentInfo.AttachmentInfoName]["Add"] = "True"
      dictOfAddAddMore[attachmentInfo.AttachmentInfoName]["RemoveAdd"] = "False"

    intialDictOfMultipleEntriesAttachmentsFileNames = copy.deepcopy(dictOfMultipleEntriesAttachmentsFileNames)

    context["EditEnable"] =  True
    context["ConfirmEnable"] =  False

    if (request.POST.get('addInfo') is not None):

      addInfo = ast.literal_eval(request.POST.get('addInfo'))
      attachmentInfoName = addInfo[0]
      dictOfAddAddMore = ast.literal_eval(str(addInfo[1]))
      dictOfMultipleEntriesAttachmentsFileNames = ast.literal_eval(str(addInfo[2]))

      attachmentInfo = [aI for aI in attachmentsInfo.listOfAttachmentInfo if (aI.AttachmentInfoName == attachmentInfoName)][0]
      attachmentInfoDict = {}
      attachmentInfoFileNamesDict = {}

      for attachment in attachmentInfo.ListOfAttachment:
          if (request.FILES.get(attachment.AttachmentName)):
              attachmentInfoDict[attachment.AttachmentName] = request.FILES.get(attachment.AttachmentName)
              attachmentInfoFileNamesDict[attachment.AttachmentName] = request.FILES.get(attachment.AttachmentName).name

      maxim = 0
      if (dictOfMultipleEntriesAttachmentsFileNames[attachmentInfoName]):
        maxim = max(dictOfMultipleEntriesAttachmentsFileNames[attachmentInfoName], key=int)

      if (list(filter(lambda a: a != '' , list(attachmentInfoDict.values())))):

        for attachmentName, attachmentFile in attachmentInfoDict.items():

            dirName = tempDir + "/" + attachmentInfoName + "/" + str(maxim+1) + "/" + str(attachmentName)

            if not os.path.exists(dirName):
                os.makedirs(dirName)

            if (attachmentInfoFileNamesDict[attachmentName].split(".")[-1] == 'pdf'):
                attachmentNameWithEXT = attachmentName + ".pdf"
            else:
                attachmentNameWithEXT = attachmentName

            with open(os.path.join(dirName,attachmentNameWithEXT), "wb") as file:
                file.write(attachmentFile.read())

        dictOfMultipleEntriesAttachmentsFileNames[attachmentInfoName][maxim+1] = attachmentInfoFileNamesDict
        dictOfAddAddMore[attachmentInfoName]["AddMore"] = "True"
        dictOfAddAddMore[attachmentInfoName]["Add"] = "False"
        dictOfAddAddMore[attachmentInfoName]["RemoveAdd"] = "False"  

      context["EditEnable"] =  True
      context["ConfirmEnable"] =  False

    elif (request.POST.get('addMoreInfo') is not None):

      addMoreInfo = ast.literal_eval(request.POST.get('addMoreInfo'))

      attachmentInfoName = addMoreInfo[0]
      dictOfAddAddMore = ast.literal_eval(str(addMoreInfo[1]))
      dictOfMultipleEntriesAttachmentsFileNames = ast.literal_eval(str(addMoreInfo[2]))

      dictOfAddAddMore[attachmentInfoName]["AddMore"] = "False"
      dictOfAddAddMore[attachmentInfoName]["Add"] = "True"
      dictOfAddAddMore[attachmentInfoName]["RemoveAdd"] = "False"

      context["EditEnable"] =  True
      context["ConfirmEnable"] =  False

    elif (request.POST.get('deleteInfo') is not None):

      deleteInfo = ast.literal_eval(request.POST.get('deleteInfo'))

      attachmentInfoName = deleteInfo[0]
      attachmentInfoNameId = deleteInfo[1]
      dictOfAddAddMore = ast.literal_eval(str(deleteInfo[2]))
      dictOfMultipleEntriesAttachmentsFileNames = ast.literal_eval(str(deleteInfo[3]))

      dirName = tempDir + "/" + attachmentInfoName + "/" + str(int(attachmentInfoNameId)) 

      if os.path.exists(dirName) and os.path.isdir(dirName):
        shutil.rmtree(dirName)

      del dictOfMultipleEntriesAttachmentsFileNames[attachmentInfoName][int(attachmentInfoNameId)]

      maxim = 1
      if (dictOfMultipleEntriesAttachmentsFileNames[attachmentInfoName]):
        maxim = max(dictOfMultipleEntriesAttachmentsFileNames[attachmentInfoName], key=int)

      currIter = 1
      tempFileNamesDict = {}

      for iter in range(1,maxim+1):
        if iter != int(attachmentInfoNameId):
          newDirName = tempDir + "/" + attachmentInfoName + "/" + str(currIter)
          oldDirName = tempDir + "/" + attachmentInfoName + "/" + str(iter)

          os.rename(oldDirName,newDirName)
          tempFileNamesDict[currIter] = dictOfMultipleEntriesAttachmentsFileNames[attachmentInfoName][iter]
          currIter +=1

      dictOfMultipleEntriesAttachmentsFileNames[attachmentInfoName] = tempFileNamesDict

      if (not dictOfMultipleEntriesAttachmentsFileNames[attachmentInfoName]):
        dictOfAddAddMore[attachmentInfoName]["AddMore"] = "False"
        dictOfAddAddMore[attachmentInfoName]["Add"] = "True"
      else:
        dictOfAddAddMore[attachmentInfoName]["AddMore"] = "True"
        dictOfAddAddMore[attachmentInfoName]["Add"] = "False"

      dictOfAddAddMore[attachmentInfoName]["RemoveAdd"] = "False"

      context["EditEnable"] =  True
      context["ConfirmEnable"] =  False

    elif (request.POST.get('removeAddInfo') is not None):

      removeAddInfo = ast.literal_eval(request.POST.get('removeAddInfo'))

      attachmentInfoName = removeAddInfo[0]
      dictOfAddAddMore = ast.literal_eval(str(removeAddInfo[1]))
      dictOfMultipleEntriesAttachmentsFileNames = ast.literal_eval(str(removeAddInfo[2]))

      dictOfAddAddMore[attachmentInfoName]["AddMore"] = "True"
      dictOfAddAddMore[attachmentInfoName]["Add"] = "False"
      dictOfAddAddMore[attachmentInfoName]["RemoveAdd"] = "False"

      context["EditEnable"] =  True
      context["ConfirmEnable"] =  False

    elif (request.POST.get('nextInfo') is not None):

      nextInfo = ast.literal_eval(str(request.POST.get('nextInfo')))

      attachmentInfoName = str(nextInfo[0]) 
      dictOfAddAddMore = ast.literal_eval(str(nextInfo[1]))
      dictOfMultipleEntriesAttachmentsFileNames = ast.literal_eval(str(nextInfo[2]))

      for aInfo in attachmentsInfo.listOfAttachmentInfo:
        if (aInfo.AttachmentInfoName == attachmentInfoName):
            attachmentInfo = aInfo

      attachmentInfoName = attachmentInfo.AttachmentInfoName
      attachmentInfoDict = {}
      attachmentInfoFileNamesDict = {}

      for attachment in attachmentInfo.ListOfAttachment:
        if (request.FILES.get(attachment.AttachmentName)):
          attachmentInfoDict[attachment.AttachmentName] = request.FILES.get(attachment.AttachmentName)
          attachmentInfoFileNamesDict[attachment.AttachmentName] = request.FILES.get(attachment.AttachmentName).name

      maxim = 0
      if (dictOfMultipleEntriesAttachmentsFileNames[attachmentInfoName]):
        maxim = max(dictOfMultipleEntriesAttachmentsFileNames[attachmentInfoName], key=int)

      if (list(filter(lambda a: a != None , list(attachmentInfoDict.values()))) and list(filter(lambda a: a != '' , list(attachmentInfoDict.values())))):

          for attachmentName, attachmentFile in attachmentInfoDict.items():

              dirName = tempDir + "/" + attachmentInfoName + "/" + str(maxim+1) + "/" + str(attachmentName)

              if not os.path.exists(dirName):
                  os.makedirs(dirName)

              if (attachmentInfoFileNamesDict[attachmentName].split(".")[-1] == 'pdf'):
                  attachmentNameWithEXT = attachmentName + ".pdf"
              else:
                  attachmentNameWithEXT = attachmentName

              with open(os.path.join(dirName,attachmentNameWithEXT), "wb") as file:
                  file.write(attachmentFile.read())

          dictOfMultipleEntriesAttachmentsFileNames[attachmentInfoName][maxim+1] = attachmentInfoFileNamesDict  

      context["EditEnable"] =  False
      context["ConfirmEnable"] =  True

    elif (request.POST.get('goBackAndEditInfo') is not None):

      goBackAndEditInfo = ast.literal_eval(request.POST.get('goBackAndEditInfo'))

      dictOfAddAddMore = ast.literal_eval(str(goBackAndEditInfo[0]))
      dictOfMultipleEntriesAttachmentsFileNames = ast.literal_eval(str(goBackAndEditInfo[1]))

      context["EditEnable"] =  True
      context["ConfirmEnable"] =  False     

    elif (request.POST.get('confirmAndSubmitAttachmentsInfo') is not None):

        confirmAndSubmitInfo = ast.literal_eval(str(request.POST.get('confirmAndSubmitAttachmentsInfo')))

        attachmentInfoName = str(confirmAndSubmitInfo[0])
        dictOfMultipleEntriesAttachmentsFileNames = ast.literal_eval(str(confirmAndSubmitInfo[1]))
            
        completedConfirmAndSubmitAttachments = request.session.get('CompletedConfirmAndSubmitAttachments')
        completedConfirmAndSubmitAttachments.append(attachmentInfoName)
        request.session['CompletedConfirmAndSubmitAttachments'] = completedConfirmAndSubmitAttachments

        if (attachmentInfoName == attachmentsInfo.listOfAttachmentInfo[-1].AttachmentInfoName):
            request.session['DictOfMultipleEntriesAttachmentsFileNames'] = dictOfMultipleEntriesAttachmentsFileNames
            return redirect('Success')
        else:
            defaultAttachmentsInfoDisplay =  [att.AttachmentInfoName for att in attachmentsInfo.listOfAttachmentInfo if att.AttachmentInfoName not in completedConfirmAndSubmitAttachments]

    else:
      if (not request.session.has_key('TempDir')):
          tempDir = tempfile.mkdtemp()
      elif (dictOfMultipleEntriesAttachmentsFileNames == intialDictOfMultipleEntriesAttachmentsFileNames):
          shutil.rmtree(request.session.get('TempDir'))
          tempDir = tempfile.mkdtemp()
      else:
          tempDir = request.session.get('TempDir')

    request.session['TempDir'] = tempDir
    context['DictOfAddAddMore'] = dictOfAddAddMore
    context['AttachmentsInfo'] = attachmentsInfo
    context['DictOfMultipleEntriesAttachmentsFileNames'] = dictOfMultipleEntriesAttachmentsFileNames
    context['CompletedConfirmAndSubmitAttachments'] = completedConfirmAndSubmitAttachments
    context['DefaultAttachmentsInfoDisplay'] = defaultAttachmentsInfoDisplay

    return render(request,"Attachments.html",context)

def Success(request):

    
    if ((not request.session.has_key('UUID')) or (not request.session.has_key('DictOfMultipleEntriesPer')) or  \
        (not request.session.has_key('DictOfMultipleEntriesEdu')) or \
        (not request.session.has_key('DictOfMultipleWorkExperiences')) or (not request.session.has_key('TempDir'))):
        return redirect('AdmissionDetails')
    

    UUID = request.session.get('UUID')
    DictOfMultipleEntriesPer = request.session.get('DictOfMultipleEntriesPer')
    DictOfMultipleEntriesEdu = request.session.get('DictOfMultipleEntriesEdu')
    DictOfMultipleWorkExperiences = request.session.get('DictOfMultipleWorkExperiences')
    DictOfMultipleEntriesAttachmentsFileNames = request.session.get('DictOfMultipleEntriesAttachmentsFileNames')
    TempDir = request.session.get('TempDir')

    personalDetailsInfo = configParser.getPersonalDetailsInfo()
    educationalQualificationsInfo = configParser.getEducationalQualificationsInfo()
    workExperienceInfo = configParser.getWorkExperienceInfo()
    attachmentsInfo = configParser.getAttachmentsInfo()

    for personalAttr in personalDetailsInfo.listOfPersonalAttr:  
        for key,value in DictOfMultipleEntriesPer.items(): 
            if key == personalAttr.PersonalAttrName:
                for key2, value2 in value.items():
                    dbEntryDict = {}
                    dbEntryDict['UUID'] = UUID
                    for subAttr in personalAttr.ListOfSubAttr:
                        columnName = personalAttr.PersonalAttrName + "_" + subAttr.SubAttrName
                        dbEntryDict[columnName] = value2[subAttr.SubAttrName]
                    personalDetailsModelInstance = PersonalDetailsModel()
                    #print (dbEntryDict)
                    for dbColumnName, dbColumnValue in dbEntryDict.items():
                        setattr(personalDetailsModelInstance, dbColumnName, dbColumnValue)

                    personalDetailsModelInstance.save()

    for eduAttr in educationalQualificationsInfo.listOfEduAttr:  
        for key,value in DictOfMultipleEntriesEdu.items(): 
            if key == eduAttr.EduAttrName:
                for key2, value2 in value.items():
                    dbEntryDict = {}
                    dbEntryDict['UUID'] = UUID
                    for subAttr in eduAttr.ListOfSubAttr:
                        columnName = eduAttr.EduAttrName + "_" + subAttr.SubAttrName
                        dbEntryDict[columnName] = value2[subAttr.SubAttrName]
                    educationalQualificationsModelInstance = EducationalQualificationsModel()
                    #print (dbEntryDict)
                    for dbColumnName, dbColumnValue in dbEntryDict.items():
                        setattr(educationalQualificationsModelInstance, dbColumnName, dbColumnValue)

                    educationalQualificationsModelInstance.save()

    
    for key,value in DictOfMultipleWorkExperiences.items(): 
            dbEntryDict = {}
            dbEntryDict['UUID'] = UUID
            for subAttr in workExperienceInfo.ListOfSubAttr:
                columnName = subAttr.SubAttrName
                dbEntryDict[columnName] = value[subAttr.SubAttrName]
            workExperienceModelInstance = WorkExperienceModel()
            #print (dbEntryDict)
            for dbColumnName, dbColumnValue in dbEntryDict.items():
                setattr(workExperienceModelInstance, dbColumnName, dbColumnValue)

            workExperienceModelInstance.save()


    fs = FileSystemStorage()
    for attachmentInfo in attachmentsInfo.listOfAttachmentInfo:  
        for key,value in DictOfMultipleEntriesAttachmentsFileNames.items(): 
            if key == attachmentInfo.AttachmentInfoName:
                for key2, value2 in value.items():
                    dbEntryDict = {}
                    dbEntryDict['UUID'] = UUID
                    for attachment in attachmentInfo.ListOfAttachment:
                        dirName = TempDir +"/" + attachmentInfo.AttachmentInfoName + "/" + str(str(key2) + "/") + attachment.AttachmentName + "/*"
                        fileName = glob.glob(dirName)[0]
                        file = open(fileName,"rb")

                        lf = tempfile.NamedTemporaryFile(dir='/tmp')
                        lf.write(file.read())
                        mediaFilename = fs.save(os.path.basename(fileName), lf)
                        lf.close()
                        
                        fileUrl = fs.url(mediaFilename)

                        columnName = attachmentInfo.AttachmentInfoName + "_" + attachment.AttachmentName
                        dbEntryDict[columnName] = fileUrl

                    attachmentsModelInstance = AttachmentsModel()
                    #print (dbEntryDict)
                    for dbColumnName, dbColumnValue in dbEntryDict.items():
                        setattr(attachmentsModelInstance, dbColumnName, dbColumnValue)

                    attachmentsModelInstance.save()

    context = {}
    
    return redirect('logout')


def AdminLogin(request):

    context = {}

    #print (request.POST.get('userName'))
    #print (request.POST.get('password'))
    if (request.POST.get('userName') == "admin" and request.POST.get('password') == "adminadmin"):

        request.session['userName'] = "admin" 
        request.session['password'] = "adminadmin"
        return redirect('AdminPrimaryView')

    elif (request.POST.get('userName') == None and request.POST.get('password') == None):
        return render(request,"AdminLogin.html",context)
    else:
        context['invalid'] = "Invalid Credentials"
        return render(request,"AdminLogin.html",context) 

    return render(request,"AdminLogin.html",context) 

def AdminPrimaryView(request):

    context = {}

    if (request.session.get('userName') != "admin" or request.session.get('password') != "adminadmin"):
        return render(request,"AdminLogin.html",context)

    if (request.POST.get('SelectAll') != None):
        return redirect('AdminResultView')

    if (request.POST.get('Filter') != None):
        return redirect('AdminFilterView')

    return render(request,"AdminPrimaryView.html",context) 

def AdminFilterView(request):

    context = {}

    if (request.session.get('userName') != "admin" or request.session.get('password') != "adminadmin"):
        return redirect('AdminLogin')

    personalDetailsInfo = configParser.getPersonalDetailsInfo()
    educationalQualificationsInfo = configParser.getEducationalQualificationsInfo()
    workExperienceInfo = configParser.getWorkExperienceInfo()
    defaultDisplay = ['PersonalDetails','EducationalQualifications','WorkExperiences']
    completedSubmit = []

    personalDetailsConstraint = {}
    educationalQualificationsConstraint = {}
    workExperienceConstraints = {}

    request.session['PersonalDetailsConstraint'] =  None
    request.session['EducationalQualificationsConstraint'] = None
    request.session['WorkExperienceConstraints'] = None

    atLeastOneChoiceConstraintNotAny = None

    if (request.session.get('AtLeastOneChoiceConstraintNotAny') == None):
        atLeastOneChoiceConstraintNotAny =  False
    else:
        atLeastOneChoiceConstraintNotAny = request.session.get('AtLeastOneChoiceConstraintNotAny')

    context = {}

    if (request.POST.get('SubmitPerConstraints') is not None):

        submitInfo = ast.literal_eval(request.POST.get('SubmitPerConstraints'))

        educationalQualificationsConstraint = submitInfo[1]
        workExperienceConstraints = submitInfo[2]

        for personalAttr in personalDetailsInfo.listOfPersonalAttr:
            personalAttrName = personalAttr.PersonalAttrName
            for subAttr in personalAttr.ListOfSubAttr:
                subAttrName = subAttr.SubAttrName

                personalDetailsConstraint[personalAttrName+"."+subAttrName] = {}
                if not subAttr.SubAttrChoicesFilter:
                    for constraint in ['eq','gt','gte','lt','lte','startswith', 'endswith', 'contains',\
                                    'noteq','notgt','notgte','notlt','notlte','notstartswith', 'notendswith', 'notcontains']:
                        attrName =  personalAttrName+"."+subAttrName+constraint
                        if (request.POST.get(attrName) != None and request.POST.get(attrName) != ''): 
                            personalDetailsConstraint[personalAttrName+"."+subAttrName][constraint] = request.POST.get(attrName)
                else:
                    for constraint in ['eq','noteq']:
                        attrName =  personalAttrName+"."+subAttrName+constraint
                        if (request.POST.get(attrName) != None and request.POST.get(attrName) != ''): 
                            if (request.POST.get(attrName).lower() != 'Any'.lower()):
                                personalDetailsConstraint[personalAttrName+"."+subAttrName][constraint] = request.POST.get(attrName)
                            if (constraint=='noteq' and request.POST.get(attrName).lower() == 'True'.lower() and request.POST.get(personalAttrName+"."+subAttrName+'eq').lower() == 'Any'.lower()):
                                atLeastOneChoiceConstraintNotAny = True

        defaultDisplay = ['EducationalQualifications','WorkExperiences']
        completedSubmit = ['PersonalDetails']


    if (request.POST.get('SubmitEduConstraints') is not None):

        submitInfo = ast.literal_eval(request.POST.get('SubmitEduConstraints'))

        personalDetailsConstraint = submitInfo[0]
        workExperienceConstraints = submitInfo[2]

        for eduAttr in educationalQualificationsInfo.listOfEduAttr:
            eduAttrName = eduAttr.EduAttrName
            for subAttr in eduAttr.ListOfSubAttr:
                subAttrName = subAttr.SubAttrName

                educationalQualificationsConstraint[eduAttrName+"."+subAttrName] = {}
                if not subAttr.SubAttrChoicesFilter:
                    for constraint in ['eq','gt','gte','lt','lte','startswith', 'endswith', 'contains',\
                                    'noteq','notgt','notgte','notlt','notlte','notstartswith', 'notendswith', 'notcontains']:
                        attrName =  eduAttrName+"."+subAttrName+constraint
                        if (request.POST.get(attrName) != None and request.POST.get(attrName) != ''): 
                            educationalQualificationsConstraint[eduAttrName+"."+subAttrName][constraint] = request.POST.get(attrName)
                else:
                    for constraint in ['eq','noteq']:
                        attrName =  eduAttrName+"."+subAttrName+constraint
                        if (request.POST.get(attrName) != None and request.POST.get(attrName) != ''):
                            if (request.POST.get(attrName).lower() != 'Any'.lower()): 
                                educationalQualificationsConstraint[eduAttrName+"."+subAttrName][constraint] = request.POST.get(attrName)
                            if (constraint=='noteq' and request.POST.get(attrName).lower() == 'True'.lower() and request.POST.get(eduAttrName+"."+subAttrName+'eq').lower() == 'Any'.lower()):
                                atLeastOneChoiceConstraintNotAny = True

        defaultDisplay = ['WorkExperiences']
        completedSubmit = ['PersonalDetails', 'EducationalQualifications']


    if (request.POST.get('SubmitWorkConstraints') is not None):

        submitInfo = ast.literal_eval(request.POST.get('SubmitWorkConstraints'))

        personalDetailsConstraint = submitInfo[0]
        educationalQualificationsConstraint = submitInfo[1]

        for subAttr in workExperienceInfo.ListOfSubAttr:
            subAttrName = subAttr.SubAttrName

            workExperienceConstraints[subAttrName] = {}
            if not subAttr.SubAttrChoicesFilter:
                for constraint in ['eq','gt','gte','lt','lte','startswith', 'endswith', 'contains',\
                                    'noteq','notgt','notgte','notlt','notlte','notstartswith', 'notendswith', 'notcontains']:
                    attrName =  subAttrName+constraint
                    if (request.POST.get(attrName) != None and request.POST.get(attrName) != ''): 
                        workExperienceConstraints[subAttrName][constraint] = request.POST.get(attrName)
            else:
                for constraint in ['eq','noteq']:
                    attrName =  subAttrName+constraint
                    if (request.POST.get(attrName) != None and request.POST.get(attrName) != ''): 
                        if (request.POST.get(attrName).lower() != 'Any'.lower()):
                            workExperienceConstraints[subAttrName][constraint] = request.POST.get(attrName)
                        if (constraint=='noteq' and request.POST.get(attrName).lower() == 'True'.lower() and request.POST.get(subAttrName+'eq').lower() == 'Any'.lower()):
                            atLeastOneChoiceConstraintNotAny = True

        defaultDisplay = []
        completedSubmit = ['PersonalDetails', 'EducationalQualifications', 'WorkExperiences']

        request.session['PersonalDetailsConstraint'] =  personalDetailsConstraint
        request.session['EducationalQualificationsConstraint'] = educationalQualificationsConstraint
        request.session['WorkExperienceConstraints'] = workExperienceConstraints
        request.session['AtLeastOneChoiceConstraintNotAny'] = atLeastOneChoiceConstraintNotAny

        return redirect('AdminResultView')

    context['PersonalDetailsInfo'] = personalDetailsInfo
    context['EducationalQualificationsInfo'] = educationalQualificationsInfo
    context['WorkExperienceInfo'] = workExperienceInfo
    context['DefaultDisplay'] = defaultDisplay
    context['CompletedSubmit'] = completedSubmit
    context['ListOfTabs'] = ['PersonalDetails','EducationalQualifications','WorkExperiences']
    context['PersonalDetailsConstraint'] =  personalDetailsConstraint
    context['EducationalQualificationsConstraint'] = educationalQualificationsConstraint
    context['WorkExperienceConstraints'] = workExperienceConstraints
    request.session['AtLeastOneChoiceConstraintNotAny'] = atLeastOneChoiceConstraintNotAny

    return render(request,"AdminFilterView.html",context)
    
def AdminResultView(request):

    context = {}

    if (request.session.get('userName') != "admin" or request.session.get('password') != "adminadmin"):
        return redirect('AdminLogin')

    if (request.POST.get('ResetSubmit') == "True"):
        request.session['PersonalDetailsConstraint'] =  None
        request.session['EducationalQualificationsConstraint'] = None
        request.session['WorkExperienceConstraints'] = None
        request.session['AtLeastOneChoiceConstraintNotAny'] = None
        return redirect('AdminFilterView')

    if (request.POST.get('Logout') == "True"):
        request.session['userName'] = None
        request.session['password'] = None
        request.session['PersonalDetailsConstraint'] =  None
        request.session['EducationalQualificationsConstraint'] = None
        request.session['WorkExperienceConstraints'] = None
        request.session['AtLeastOneChoiceConstraintNotAny'] = None
        return redirect('AdminLogin')

    personalDetailsConstraint = {}
    educationalQualificationsConstraint = {}
    workExperienceConstraint = {}

    if (request.session.get('PersonalDetailsConstraint')):
        personalDetailsConstraint = request.session.get('PersonalDetailsConstraint')
    if (request.session.get('EducationalQualificationsConstraint')):
        educationalQualificationsConstraint = request.session.get('EducationalQualificationsConstraint')
    if (request.session.get('WorkExperienceConstraints')):
        workExperienceConstraint = request.session.get('WorkExperienceConstraints')

    personalDetailsInfo = configParser.getPersonalDetailsInfo()
    educationalQualificationsInfo = configParser.getEducationalQualificationsInfo()
    workExperienceInfo = configParser.getWorkExperienceInfo()
    attachmentsInfo = configParser.getAttachmentsInfo()
    
    listOfUUID = []
    for uuid in PersonalDetailsModel.objects.only('UUID'):
        listOfUUID.append(getattr(uuid, 'UUID'))
    for uuid in EducationalQualificationsModel.objects.only('UUID'):
        listOfUUID.append(getattr(uuid, 'UUID'))
    for uuid in WorkExperienceModel.objects.only('UUID'):
        listOfUUID.append(getattr(uuid, 'UUID'))

    if request.session.get('AtLeastOneChoiceConstraintNotAny') == True:
        setOfUUID = set([])
    else:
        setOfUUID = set(listOfUUID)

    for personalAttr in personalDetailsInfo.listOfPersonalAttr:
        for subAttr in personalAttr.ListOfSubAttr:
            key = personalAttr.PersonalAttrName+"."+subAttr.SubAttrName
            dbColumnName = personalAttr.PersonalAttrName+"_"+subAttr.SubAttrName

            kwargsDBColumnNotNone = {
            dbColumnName+'__exact': None,
            }

            if key in personalDetailsConstraint:
                if "eq" in personalDetailsConstraint[key]:
                    if "noteq" in personalDetailsConstraint[key] and personalDetailsConstraint[key]['noteq'] == "True":
                        kwargs = {
                        dbColumnName+'__exact': personalDetailsConstraint[key]['eq'],
                        }           
                        resultSet = PersonalDetailsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID             
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"exact"] = personalDetailsConstraint[key]['eq']
                        resultSet = PersonalDetailsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "gt" in personalDetailsConstraint[key]:
                    if "notgt" in personalDetailsConstraint[key] and personalDetailsConstraint[key]['notgt'] == "True":
                        kwargs = {
                        dbColumnName+'__gt': personalDetailsConstraint[key]['gt'],
                        }           
                        resultSet = PersonalDetailsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID 
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"gt"] = personalDetailsConstraint[key]['gt']
                        resultSet = PersonalDetailsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "gte" in personalDetailsConstraint[key]:
                    if "notgte" in personalDetailsConstraint[key] and personalDetailsConstraint[key]['notgte'] == "True":
                        kwargs = {
                        dbColumnName+'__gte': personalDetailsConstraint[key]['gte'],
                        }           
                        resultSet = PersonalDetailsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"gte"] = personalDetailsConstraint[key]['gte']
                        resultSet = PersonalDetailsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "lt" in personalDetailsConstraint[key]:
                    if "notlt" in personalDetailsConstraint[key] and personalDetailsConstraint[key]['notlt'] == "True":
                        kwargs = {
                        dbColumnName+'__lt': personalDetailsConstraint[key]['lt'],
                        }           
                        resultSet = PersonalDetailsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"lt"] = personalDetailsConstraint[key]['lt']
                        resultSet = PersonalDetailsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "lte" in personalDetailsConstraint[key]:
                    if "notlte" in personalDetailsConstraint[key] and personalDetailsConstraint[key]['notlte'] == "True":
                        kwargs = {
                        dbColumnName+'__lte': personalDetailsConstraint[key]['lte'],
                        }           
                        resultSet = PersonalDetailsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"lte"] = personalDetailsConstraint[key]['lte']
                        resultSet = PersonalDetailsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "startswith" in personalDetailsConstraint[key]:
                    if "notstartswith" in personalDetailsConstraint[key] and personalDetailsConstraint[key]['notstartswith'] == "True":
                        kwargs = {
                        dbColumnName+'__istartswith': personalDetailsConstraint[key]['startswith'],
                        }           
                        resultSet = PersonalDetailsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"istartswith"] = personalDetailsConstraint[key]['startswith']
                        resultSet = PersonalDetailsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "endswith" in personalDetailsConstraint[key]:
                    if "notendswith" in personalDetailsConstraint[key] and personalDetailsConstraint[key]['notendswith'] == "True":
                        kwargs = {
                        dbColumnName+'__iendswith': personalDetailsConstraint[key]['endswith'],
                        }           
                        resultSet = PersonalDetailsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"iendswith"] = personalDetailsConstraint[key]['endswith']
                        resultSet = PersonalDetailsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "contains" in personalDetailsConstraint[key]:
                    if "notcontains" in personalDetailsConstraint[key] and personalDetailsConstraint[key]['notcontains'] == "True":
                        kwargs = {
                        dbColumnName+'__icontains': personalDetailsConstraint[key]['contains'],
                        }           
                        resultSet = PersonalDetailsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"icontains"] = personalDetailsConstraint[key]['contains']
                        resultSet = PersonalDetailsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID


    #print (setOfUUID)

    for eduAttr in educationalQualificationsInfo.listOfEduAttr:
        for subAttr in eduAttr.ListOfSubAttr:
            key = eduAttr.EduAttrName+"."+subAttr.SubAttrName
            dbColumnName = eduAttr.EduAttrName+"_"+subAttr.SubAttrName

            kwargsDBColumnNotNone = {
            dbColumnName+'__exact': None,
            }

            if key in educationalQualificationsConstraint:
                if "eq" in educationalQualificationsConstraint[key]:
                    if "noteq" in educationalQualificationsConstraint[key] and educationalQualificationsConstraint[key]['noteq'] == "True":
                        kwargs = {
                        dbColumnName+'__exact': educationalQualificationsConstraint[key]['eq'],
                        }           
                        resultSet = EducationalQualificationsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID             
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"exact"] = educationalQualificationsConstraint[key]['eq']
                        resultSet = EducationalQualificationsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "gt" in educationalQualificationsConstraint[key]:
                    if "notgt" in educationalQualificationsConstraint[key] and educationalQualificationsConstraint[key]['notgt'] == "True":
                        kwargs = {
                        dbColumnName+'__gt': educationalQualificationsConstraint[key]['gt'],
                        }           
                        resultSet = EducationalQualificationsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID 
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"gt"] = educationalQualificationsConstraint[key]['gt']
                        resultSet = EducationalQualificationsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "gte" in educationalQualificationsConstraint[key]:
                    if "notgte" in educationalQualificationsConstraint[key] and educationalQualificationsConstraint[key]['notgte'] == "True":
                        kwargs = {
                        dbColumnName+'__gte': educationalQualificationsConstraint[key]['gte'],
                        }           
                        resultSet = EducationalQualificationsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"gte"] = educationalQualificationsConstraint[key]['gte']
                        resultSet = EducationalQualificationsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "lt" in educationalQualificationsConstraint[key]:
                    if "notlt" in educationalQualificationsConstraint[key] and educationalQualificationsConstraint[key]['notlt'] == "True":
                        kwargs = {
                        dbColumnName+'__lt': educationalQualificationsConstraint[key]['lt'],
                        }           
                        resultSet = EducationalQualificationsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"lt"] = educationalQualificationsConstraint[key]['lt']
                        resultSet = EducationalQualificationsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "lte" in educationalQualificationsConstraint[key]:
                    if "notlte" in educationalQualificationsConstraint[key] and educationalQualificationsConstraint[key]['notlte'] == "True":
                        kwargs = {
                        dbColumnName+'__lte': educationalQualificationsConstraint[key]['lte'],
                        }           
                        resultSet = EducationalQualificationsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"lte"] = educationalQualificationsConstraint[key]['lte']
                        resultSet = EducationalQualificationsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "startswith" in educationalQualificationsConstraint[key]:
                    if "notstartswith" in educationalQualificationsConstraint[key] and educationalQualificationsConstraint[key]['notstartswith'] == "True":
                        kwargs = {
                        dbColumnName+'__istartswith': educationalQualificationsConstraint[key]['startswith'],
                        }           
                        resultSet = EducationalQualificationsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"istartswith"] = educationalQualificationsConstraint[key]['startswith']
                        resultSet = EducationalQualificationsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "endswith" in educationalQualificationsConstraint[key]:
                    if "notendswith" in educationalQualificationsConstraint[key] and educationalQualificationsConstraint[key]['notendswith'] == "True":
                        kwargs = {
                        dbColumnName+'__iendswith': educationalQualificationsConstraint[key]['endswith'],
                        }           
                        resultSet = EducationalQualificationsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"iendswith"] = educationalQualificationsConstraint[key]['endswith']
                        resultSet = EducationalQualificationsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                if "contains" in educationalQualificationsConstraint[key]:
                    if "notcontains" in educationalQualificationsConstraint[key] and educationalQualificationsConstraint[key]['notcontains'] == "True":
                        kwargs = {
                        dbColumnName+'__icontains': educationalQualificationsConstraint[key]['contains'],
                        }           
                        resultSet = EducationalQualificationsModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID
                    else:
                        kwargs = {}
                        kwargs[dbColumnName+"__"+"icontains"] = educationalQualificationsConstraint[key]['contains']
                        resultSet = EducationalQualificationsModel.objects.filter(**kwargs)
                        resultSetUUID = set([item.UUID for item in resultSet])
                        setOfUUID = resultSetUUID & setOfUUID

    #print (setOfUUID)

    for subAttr in workExperienceInfo.ListOfSubAttr:
        key = subAttr.SubAttrName
        dbColumnName = subAttr.SubAttrName

        kwargsDBColumnNotNone = {
        dbColumnName+'__exact': None,
        }

        if key in workExperienceConstraint:
            if "eq" in workExperienceConstraint[key]:
                if "noteq" in workExperienceConstraint[key] and workExperienceConstraint[key]['noteq'] == "True":
                    kwargs = {
                    dbColumnName+'__exact': workExperienceConstraint[key]['eq'],
                    }           
                    resultSet = WorkExperienceModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID             
                else:
                    kwargs = {}
                    kwargs[dbColumnName+"__"+"exact"] = workExperienceConstraint[key]['eq']
                    resultSet = WorkExperienceModel.objects.filter(**kwargs)
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID
            if "gt" in workExperienceConstraint[key]:
                if "notgt" in workExperienceConstraint[key] and workExperienceConstraint[key]['notgt'] == "True":
                    kwargs = {
                    dbColumnName+'__gt': workExperienceConstraint[key]['gt'],
                    }           
                    resultSet = WorkExperienceModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID 
                else:
                    kwargs = {}
                    kwargs[dbColumnName+"__"+"gt"] = workExperienceConstraint[key]['gt']
                    resultSet = WorkExperienceModel.objects.filter(**kwargs)
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID
            if "gte" in workExperienceConstraint[key]:
                if "notgte" in workExperienceConstraint[key] and workExperienceConstraint[key]['notgte'] == "True":
                    kwargs = {
                    dbColumnName+'__gte': workExperienceConstraint[key]['gte'],
                    }           
                    resultSet = WorkExperienceModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID
                else:
                    kwargs = {}
                    kwargs[dbColumnName+"__"+"gte"] = workExperienceConstraint[key]['gte']
                    resultSet = WorkExperienceModel.objects.filter(**kwargs)
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID
            if "lt" in workExperienceConstraint[key]:
                if "notlt" in workExperienceConstraint[key] and workExperienceConstraint[key]['notlt'] == "True":
                    kwargs = {
                    dbColumnName+'__lt': workExperienceConstraint[key]['lt'],
                    }           
                    resultSet = WorkExperienceModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID
                else:
                    kwargs = {}
                    kwargs[dbColumnName+"__"+"lt"] = workExperienceConstraint[key]['lt']
                    resultSet = WorkExperienceModel.objects.filter(**kwargs)
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID
            if "lte" in workExperienceConstraint[key]:
                if "notlte" in workExperienceConstraint[key] and workExperienceConstraint[key]['notlte'] == "True":
                    kwargs = {
                    dbColumnName+'__lte': workExperienceConstraint[key]['lte'],
                    }           
                    resultSet = WorkExperienceModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID
                else:
                    kwargs = {}
                    kwargs[dbColumnName+"__"+"lte"] = workExperienceConstraint[key]['lte']
                    resultSet = WorkExperienceModel.objects.filter(**kwargs)
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID
            if "startswith" in workExperienceConstraint[key]:
                if "notstartswith" in workExperienceConstraint[key] and workExperienceConstraint[key]['notstartswith'] == "True":
                    kwargs = {
                    dbColumnName+'__istartswith': workExperienceConstraint[key]['startswith'],
                    }           
                    resultSet = WorkExperienceModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID
                else:
                    kwargs = {}
                    kwargs[dbColumnName+"__"+"istartswith"] = workExperienceConstraint[key]['startswith']
                    resultSet = WorkExperienceModel.objects.filter(**kwargs)
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID
            if "endswith" in workExperienceConstraint[key]:
                if "notendswith" in workExperienceConstraint[key] and workExperienceConstraint[key]['notendswith'] == "True":
                    kwargs = {
                    dbColumnName+'__iendswith': workExperienceConstraint[key]['endswith'],
                    }           
                    resultSet = WorkExperienceModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID
                else:
                    kwargs = {}
                    kwargs[dbColumnName+"__"+"iendswith"] = workExperienceConstraint[key]['endswith']
                    resultSet = WorkExperienceModel.objects.filter(**kwargs)
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID
            if "contains" in workExperienceConstraint[key]:
                if "notcontains" in workExperienceConstraint[key] and workExperienceConstraint[key]['notcontains'] == "True":
                    kwargs = {
                    dbColumnName+'__icontains': workExperienceConstraint[key]['contains'],
                    }           
                    resultSet = WorkExperienceModel.objects.filter(~Q(**kwargsDBColumnNotNone)).filter(~Q(**kwargs))
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID
                else:
                    kwargs = {}
                    kwargs[dbColumnName+"__"+"icontains"] = workExperienceConstraint[key]['contains']
                    resultSet = WorkExperienceModel.objects.filter(**kwargs)
                    resultSetUUID = set([item.UUID for item in resultSet])
                    setOfUUID = resultSetUUID & setOfUUID

    #print (setOfUUID)

    filteredCandidates = {}

    for uuid in setOfUUID:

        filteredCandidates[uuid] = {}

        personalDetailsDB = PersonalDetailsModel.objects.filter(UUID = uuid)
        #print (personalDetailsDB.query)
        dictOfMultipleEntriesPer = {}

        for personalAttr in personalDetailsInfo.listOfPersonalAttr:
             locals()[personalAttr.PersonalAttrName] = {}
             dictOfMultipleEntriesPer[personalAttr.PersonalAttrName] = locals()[personalAttr.PersonalAttrName]

        for personalAttr in personalDetailsInfo.listOfPersonalAttr:
 
            personalAttrName = personalAttr.PersonalAttrName
            personalDetailsColumnNames = []

            for subAttr in personalAttr.ListOfSubAttr:
                columnName = personalAttr.PersonalAttrName + "_" + subAttr.SubAttrName
                personalDetailsColumnNames.append(columnName)
            
            for personalDetail in personalDetailsDB:
                personalAttrDict = {}
                for columnName in personalDetailsColumnNames:
                    personalAttrDict[columnName.split("_")[-1]] = getattr(personalDetail, columnName)

                if (not all(item is None for item in list(personalAttrDict.values()))):
                    maxim = 0
                    if (dictOfMultipleEntriesPer[personalAttrName]):
                        maxim = max(dictOfMultipleEntriesPer[personalAttrName], key=int)
                    dictOfMultipleEntriesPer[personalAttrName][maxim+1] = personalAttrDict
        

        #print (dictOfMultipleEntriesPer)
        filteredCandidates[uuid]['DictOfMultipleEntriesPer'] = dictOfMultipleEntriesPer

        educationalQualificationsDB = EducationalQualificationsModel.objects.filter(UUID = uuid)
        dictOfMultipleEntriesEdu = {}

        for eduAttr in educationalQualificationsInfo.listOfEduAttr:
            locals()[eduAttr.EduAttrName] = {}
            dictOfMultipleEntriesEdu[eduAttr.EduAttrName] = locals()[eduAttr.EduAttrName]

        for eduAttr in educationalQualificationsInfo.listOfEduAttr:
     
            eduAttrName = eduAttr.EduAttrName
            educationalQualificationsColumnNames = []

            for subAttr in eduAttr.ListOfSubAttr:
                columnName = eduAttr.EduAttrName + "_" + subAttr.SubAttrName
                educationalQualificationsColumnNames.append(columnName)
                
            for educationalQualification in educationalQualificationsDB:
                eduAttrDict = {}
                for columnName in educationalQualificationsColumnNames:
                    eduAttrDict[columnName.split("_")[-1]] = getattr(educationalQualification, columnName)

                if (not all(item is None for item in list(eduAttrDict.values()))):
                    maxim = 0
                    if (dictOfMultipleEntriesEdu[eduAttrName]):
                        maxim = max(dictOfMultipleEntriesEdu[eduAttrName], key=int)
                    dictOfMultipleEntriesEdu[eduAttrName][maxim+1] = eduAttrDict
                    

        #print (dictOfMultipleEntriesEdu)
        filteredCandidates[uuid]['DictOfMultipleEntriesEdu'] = dictOfMultipleEntriesEdu


        workExperienceDB = WorkExperienceModel.objects.filter(UUID = uuid)
        dictOfMultipleWorkExperiences = {}

        workExperienceColumnNames = []

        for subAttr in workExperienceInfo.ListOfSubAttr:
            columnName = subAttr.SubAttrName
            workExperienceColumnNames.append(columnName)
            
        for workExperience in workExperienceDB:
            workExpDict = {}
            for columnName in workExperienceColumnNames:
                workExpDict[columnName.split("_")[-1]] = getattr(workExperience, columnName)

            if (not all(item is None for item in list(workExpDict.values()))):
                maxim = 0
                if (dictOfMultipleWorkExperiences):
                    maxim = max(dictOfMultipleWorkExperiences, key=int)
                dictOfMultipleWorkExperiences[maxim+1] = workExpDict
                    

        #print (dictOfMultipleWorkExperiences)
        filteredCandidates[uuid]['DictOfMultipleWorkExperiences'] = dictOfMultipleWorkExperiences

        attachmentsDB = AttachmentsModel.objects.filter(UUID = uuid)
        dictOfMultipleEntriesAttachments = {}

        for attachmentInfo in attachmentsInfo.listOfAttachmentInfo:
            locals()[attachmentInfo.AttachmentInfoName] = {}
            dictOfMultipleEntriesAttachments[attachmentInfo.AttachmentInfoName] = locals()[attachmentInfo.AttachmentInfoName]

        for attachmentInfo in attachmentsInfo.listOfAttachmentInfo:
     
            attachmentInfoName = attachmentInfo.AttachmentInfoName
            attachmentsColumnNames = []

            for attachment in attachmentInfo.ListOfAttachment:
                columnName = attachmentInfo.AttachmentInfoName + "_" + attachment.AttachmentName
                attachmentsColumnNames.append(columnName)
                
            for attachmentItem in attachmentsDB:
                attachmentInfoDict = {}
                for columnName in attachmentsColumnNames:
                    attachmentInfoDict[columnName.split("_")[-1]] = getattr(attachmentItem, columnName)

                if (not all(item is None for item in list(attachmentInfoDict.values()))):
                    maxim = 0
                    if (dictOfMultipleEntriesAttachments[attachmentInfoName]):
                        maxim = max(dictOfMultipleEntriesAttachments[attachmentInfoName], key=int)
                    dictOfMultipleEntriesAttachments[attachmentInfoName][maxim+1] = attachmentInfoDict

        #print (dictOfMultipleEntriesAttachments)
        filteredCandidates[uuid]['DictOfMultipleEntriesAttachments'] = dictOfMultipleEntriesAttachments    

    context['FilteredCandidates'] = filteredCandidates
    context['PersonalDetailsInfo'] = personalDetailsInfo
    context['EducationalQualificationsInfo'] = educationalQualificationsInfo
    context['WorkExperienceInfo'] = workExperienceInfo
    context['AttachmentsInfo'] = attachmentsInfo


    return render(request,"AdminResultView.html",context)



# def TestView(request):
#     #a = PersonalDetailsModel.objects.all() 
#     #print (a.query)

#     #a = PersonalDetailsModel.objects.raw('SELECT  * FROM "FullTime_PhD_January_2019_PersonalDetails" WHERE "FullTime_PhD_January_2019_PersonalDetails"."NameDescription_Name" < %s',["Adil Arun Dangui"]) 

#     #a = a & PersonalDetailsModel.objects.filter(PrimaryAddressDescription_PrimaryAddressPinCode__lt = "502285")
#     #a = a & PersonalDetailsModel.objects.filter(PrimaryAddressDescription_PrimaryAddressState = "Telangana")
#     #a = a & PersonalDetailsModel.objects.filter(PrimaryAddressDescription_PrimaryAddress = "IITH")

#     #a = PersonalDetailsModel.objects.filter(PrimaryAddressDescription_PrimaryAddressPinCode__startswith="40")

#     kwargsNotNone = {
#     #'PrimaryAddressDescription_PrimaryAddressPinCode__icontains': '03',
#     'PrimaryAddressDescription_PrimaryAddressPinCode__exact': None,
#     }

#     kwargsNot = {
#     'PrimaryAddressDescription_PrimaryAddressPinCode__icontains': '14',
#     }

#     a = PersonalDetailsModel.objects.filter(~Q(**kwargsNotNone)).filter(~Q(**kwargsNot))
#     # locals()["PrimaryAddressDescription_PrimaryAddressPinCode__startswith"] = "40"
#     # print (columnNameConstraint)
#     # a = PersonalDetailsModel.objects.filter(locals()["PrimaryAddressDescription_PrimaryAddressPinCode__startswith"])
#     print (a)

#     for i in a:
#         print (i.PrimaryAddressDescription_PrimaryAddressPinCode)
#         print (i.UUID)
#         print (i.PrimaryAddressDescription_PrimaryAddressState)
#         print (i.NameDescription_Name)


#     return