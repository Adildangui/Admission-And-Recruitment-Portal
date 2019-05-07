import re
import ast
from Portal.Attachments.Attachment import Attachment


class AttachmentInfo(object):
        
        def __init__(self):
               self._AttachmentInfoName = None
               self._AttachmentInfoLabel = None
               self._ListOfAttachment = []
               self._MultipleEntries = False
               self._IsOptional = False      

        @property
        def AttachmentInfoName(self):
                return self._AttachmentInfoName

        @AttachmentInfoName.setter
        def AttachmentInfoName(self,attachmentInfoName):
                if (type(attachmentInfoName) is not str):
                        raise ValueError('AttachmentInfoName must be type String')
                self._AttachmentInfoName = str(attachmentInfoName)

        @property
        def AttachmentInfoLabel(self):
                return self._AttachmentInfoLabel

        @AttachmentInfoLabel.setter
        def AttachmentInfoLabel(self,attachmentInfoLabel):
                if (type(attachmentInfoLabel) is not str):
                        raise ValueError('AttachmentInfoLabel must be type String')
                self._AttachmentInfoLabel = str(attachmentInfoLabel)

        @property
        def listOfAttachment(self):
                return self.__listOfAttachment

        @listOfAttachment.setter
        def listOfAttachment(self, listOfAttachment):
                self.__listOfAttachment =  []
                for item in listOfAttachment:
                        if isinstance(item, Attachment):
                                self.__listOfAttachment.append(item)
                        else:
                                raise ValueError('Only Attachment type allowed')

        @property
        def MultipleEntries(self):
                return self._MultipleEntries

        @MultipleEntries.setter
        def MultipleEntries(self,multipleEntries):
                if (not isinstance(ast.literal_eval(str(multipleEntries)),bool)):
                        raise ValueError('MultipleEntries must be type Boolean')
                self._MultipleEntries = ast.literal_eval(str(multipleEntries))

        @property
        def IsOptional(self):
                return self._IsOptional

        @IsOptional.setter
        def IsOptional(self,isOptional):
                if (not isinstance(ast.literal_eval(str(isOptional)),bool)):
                        raise ValueError('IsOptional must be type Boolean')
                self._IsOptional = ast.literal_eval(str(isOptional))

