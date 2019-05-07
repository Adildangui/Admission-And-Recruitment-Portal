import re
import ast
from Portal.WorkExperience.SubAttr import SubAttr

class WorkExperience(object):
        
        def __init__(self):
               self._ListOfSubAttr = []
               self._MultipleEntries = False
               self._IsOptional = False      

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

