import ast

class SubAttr(object):

        def __init__(self):
               
               self._SubAttrName =  ""
               self._SubAttrLabel = ""
               self._IsTypeString = False
               self._IsTypeInteger = False
               self._IsTypeFloat = False
               self._IsTypeDate = False
               self._IsTypeBoolean = False
               self._SubAttrChoices = []
               self._SubAttrChoicesFilter = [] 
               self._StringConstraints = {}
               self._IntegerConstraints = {}
               self._FPConstraints = {}
               self._BooleanConstraints = {}
               self._DateConstraints = {}
               self._IsOptional = False      

        @property
        def SubAttrName(self):
                return self._SubAttrName

        @SubAttrName.setter
        def SubAttrName(self,subAttrName):
                if (type(subAttrName) is not str):
                        raise ValueError('SubAttrName must be type String')
                self._SubAttrName = str(subAttrName)

        @property
        def SubAttrLabel(self):
                return self._SubAttrLabel

        @SubAttrLabel.setter
        def SubAttrLabel(self,subAttrLabel):
                if (type(subAttrLabel) is not str):
                        raise ValueError('SubAttrLabel must be type String')
                self._SubAttrLabel = str(subAttrLabel)

        @property
        def IsTypeString(self):
                return self._IsTypeString

        @IsTypeString.setter
        def IsTypeString(self,isTypeString):
                if (not isinstance(ast.literal_eval(str(isTypeString)),bool)):
                        raise ValueError('IsTypeString must be type Boolean')
                self._IsTypeString = ast.literal_eval(str(isTypeString))

        @property
        def IsTypeInteger(self):
                return self._IsTypeInteger

        @IsTypeInteger.setter
        def IsTypeInteger(self,isTypeInteger):
                if (not isinstance(ast.literal_eval(str(isTypeInteger)),bool)):
                        raise ValueError('IsTypeInteger must be type Boolean')
                self._IsTypeInteger = ast.literal_eval(str(isTypeInteger))

        @property
        def IsTypeFloat(self):
                return self._IsTypeFloat

        @IsTypeFloat.setter
        def IsTypeFloat(self,isTypeFloat):
                if (not isinstance(ast.literal_eval(str(isTypeFloat)),bool)):
                        raise ValueError('IsTypeFloat must be type Boolean')
                self._IsTypeFloat = ast.literal_eval(str(isTypeFloat))

        @property
        def IsTypeDate(self):
                return self._IsTypeDate

        @IsTypeDate.setter
        def IsTypeDate(self,isTypeDate):
                if (not isinstance(ast.literal_eval(str(isTypeDate)),bool)):
                        raise ValueError('IsTypeDate must be type Boolean')
                self._IsTypeDate = ast.literal_eval(str(isTypeDate))

        @property
        def IsTypeBoolean(self):
                return self._IsTypeBoolean

        @IsTypeBoolean.setter
        def IsTypeBoolean(self,isTypeBoolean):
                if (not isinstance(ast.literal_eval(str(isTypeBoolean)),bool)):
                        raise ValueError('IsTypeBoolean must be type Boolean')
                self._IsTypeBoolean = ast.literal_eval(str(isTypeBoolean))

        @property
        def SubAttrChoices(self):
                return self._SubAttrChoices

        @SubAttrChoices.setter
        def SubAttrChoices(self,subAttrChoices):
                if (not isinstance(ast.literal_eval(str(subAttrChoices)),list)):
                        raise ValueError('SubAttrChoices must be type List of choice of String type')

                for choice in (ast.literal_eval(str(subAttrChoices))):
                        if (type(choice) is not str):
                                raise ValueError('Choices must be of type String')

                self._SubAttrChoices = ast.literal_eval(str(subAttrChoices)) 
                if (self._SubAttrChoices):
                    self._SubAttrChoices.append('Other')

        @property
        def SubAttrChoicesFilter(self):
                return self._SubAttrChoicesFilter

        @SubAttrChoicesFilter.setter
        def SubAttrChoicesFilter(self,subAttrChoicesFilter):
                if (not isinstance(ast.literal_eval(str(subAttrChoicesFilter)),list)):
                        raise ValueError('SubAttrChoicesFilter must be type List of choice of String type')

                for choice in (ast.literal_eval(str(subAttrChoicesFilter))):
                        if (type(choice) is not str):
                                raise ValueError('Choices must be of type String')

                self._SubAttrChoicesFilter = ast.literal_eval(str(subAttrChoicesFilter)) 
                if (self._SubAttrChoicesFilter):
                    self._SubAttrChoicesFilter = ['Any'] + self._SubAttrChoicesFilter

        @property
        def StringConstraints(self):
                return self._StringConstraints

        @StringConstraints.setter
        def StringConstraints(self,stringConstraints):
                if (not isinstance(ast.literal_eval(str(stringConstraints)),dict)):
                        raise ValueError('StringConstraints must be specified as dictionary')

                self._StringConstraints = ast.literal_eval(str(stringConstraints))

        @property
        def IntegerConstraints(self):
                return self._IntegerConstraints

        @IntegerConstraints.setter
        def IntegerConstraints(self,integerConstraints):
                if (not isinstance(ast.literal_eval(str(integerConstraints)),dict)):
                        raise ValueError('IntegerConstraints must be specified as dictionary')

                self._IntegerConstraints = ast.literal_eval(str(integerConstraints))

        @property
        def FPConstraints(self):
                return self._FPConstraints

        @FPConstraints.setter
        def FPConstraints(self,fpConstraints):
                if (not isinstance(ast.literal_eval(str(fpConstraints)),dict)):
                        raise ValueError('FPConstraints must be specified as dictionary')

                self._FPConstraints = ast.literal_eval(str(fpConstraints))

        @property
        def BooleanConstraints(self):
                return self._BooleanConstraints

        @BooleanConstraints.setter
        def BooleanConstraints(self,booleanConstraints):
                if (not isinstance(ast.literal_eval(str(booleanConstraints)),dict)):
                        raise ValueError('BooleanConstraints must be specified as dictionary')

                self._BooleanConstraints = ast.literal_eval(str(booleanConstraints))                

        @property
        def DateConstraints(self):
                return self._DateConstraints

        @DateConstraints.setter
        def DateConstraints(self,dateConstraints):
                if (not isinstance(ast.literal_eval(str(dateConstraints)),dict)):
                        raise ValueError('DateConstraints must be specified as dictionary')

                self._DateConstraints = ast.literal_eval(str(dateConstraints))

        @property
        def IsOptional(self):
                return self._IsOptional

        @IsOptional.setter
        def IsOptional(self,isOptional):
                if (not isinstance(ast.literal_eval(str(isOptional)),bool)):
                        raise ValueError('IsOptional must be type Boolean')
                self._IsOptional = ast.literal_eval(str(isOptional))

