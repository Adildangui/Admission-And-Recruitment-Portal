import re
import ast
from Portal.PersonalDetails.SubAttr import SubAttr

class PersonalAttr(object):
        
        def __init__(self):
               self._PersonalAttrName = None
               self._PersonalAttrLabel = None
               self._ListOfSubAttr = []
               self._MultipleEntries = False
               self._IsOptional = False      

        @property
        def PersonalAttrName(self):
                return self._PersonalAttrName

        @PersonalAttrName.setter
        def PersonalAttrName(self,PersonalAttrName):
                if (type(PersonalAttrName) is not str):
                        raise ValueError('PersonalAttrName must be type String')
                self._PersonalAttrName = str(PersonalAttrName)

        @property
        def PersonalAttrLabel(self):
                return self._PersonalAttrLabel

        @PersonalAttrLabel.setter
        def PersonalAttrLabel(self,PersonalAttrLabel):
                if (type(PersonalAttrLabel) is not str):
                        raise ValueError('PersonalAttrLabel must be type String')
                self._PersonalAttrLabel = str(PersonalAttrLabel)

        @property
        def listOfSubAttr(self):
                return self.__listOfSubAttr

        @listOfSubAttr.setter
        def listOfSubAttr(self, listOfSubAttr):
                self.__listOfSubAttr =  []
                for item in listOfSubAttr:
                        if isinstance(item, SubAttr):
                                self.__listOfSubAttr.append(item)
                        else:
                                raise ValueError('Only SubAttr type allowed')

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

