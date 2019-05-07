from Portal.PersonalDetails.PersonalAttr import PersonalAttr

class PersonalDetails(object):

        def __init__(self):
               self.listOfPersonalAttr = []

        @property
        def listOfPersonalAttr(self):
               return self.__listOfPersonalAttr

        @listOfPersonalAttr.setter
        def listOfPersonalAttr(self, listOfPersonalAttr):
                self.__listOfPersonalAttr =  []
                for item in listOfPersonalAttr:
                        if isinstance(item, PersonalAttr):
                                self.__listOfPersonalAttr.append(item)
                        else:
                                raise ValueError('Only PersonalAttr type allowed')

