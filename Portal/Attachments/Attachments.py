from Portal.Attachments.AttachmentInfo import AttachmentInfo

class Attachments(object):
        
        def __init__(self):
                self.listOfAttachmentInfo = [] 

        @property
        def listOfAttachmentInfo(self):
                return self.__listOfAttachmentInfo

        @listOfAttachmentInfo.setter
        def listOfAttachmentInfo(self, listOfAttachmentInfo):
                self.__listOfAttachmentInfo =  []
                for item in listOfAttachmentInfo:
                        if isinstance(item, AttachmentInfo):
                                self.__listOfAttachmentInfo.append(item)
                        else:
                                raise ValueError('Only AttachmentInfo type allowed')


