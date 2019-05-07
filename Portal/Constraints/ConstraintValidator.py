import re
import ast

class ConstraintValidator(object):
        
        def __init__(self,typeDict,constraintDict):
               self._typeDict = typeDict
               self._constraintDict = constraintDict

        def validate(self):

               listOfTypeDictValues = list(self._typeDict.values())
               if (listOfTypeDictValues.count(True) is 0 or listOfTypeDictValues.count(True)>1):
                     raise ValueError('Exactly one type must be set to True')

               listOfConstraints = list(self._constraintDict.values())
               areConstraintsSet = {}
        
               for type in self._typeDict.keys():
                     if (self._constraintDict[type]=={}):
                          areConstraintsSet[type]=False
                     else:
                          areConstraintsSet[type]=True

               if (listOfConstraints.count({}) < 4):
                     raise ValueError('Constraints on only one type should be specified') 

               if (not (set(self._typeDict.keys())==set(self._constraintDict.keys()))):
                     raise ValueError ("Validator expects same set of keys for typeDict and constraintDict")

               for key in self._typeDict.keys():
                     if (self._typeDict[key]):
                          for key2 in self._constraintDict.keys():
                              if (not (key == key2) and areConstraintsSet[key2]):
                                 raise ValueError ("Constraints must be specified only on the type of the attribute")
                          

               for key in self._typeDict.keys():
                     if (self._typeDict[key]):
                          constraintKeys = self._constraintDict[key].keys()
                          if ("DBType" not in constraintKeys):
                              raise ValueError ("Specifying DBType corresponding to attribute is must")


               avaiStringConstraints = ['DBType', 'REGEX', 'ValidationType']
               avaiIntegerConstraints = ['DBType', 'GT', 'GTE', 'LT', 'LTE', 'EQ']
               avaiFPConstraints = ['DBType', 'GT', 'LT']
               avaiBooleanConstraints = ['DBType','EQ']
               avaiDateConstraints = ['DBType','GT','LT']

               
               for key in list(self._typeDict.keys()):
                      if (self._typeDict["String"]):
                          for key2, value2 in self._constraintDict[key].items():
                              if (key2.lower()=='DBType'.lower()):
                                 if len(re.findall("VARCHAR", value2 ,re.IGNORECASE)) != 1:
                                   raise ValueError ("Only VARCHAR DBType supported for string")
                              elif (key2.lower()=='REGEX'.lower()):
                                 pass
                              elif (key2.lower()=='ValidationType'.lower()):
                                                if len(re.findall("EMAIL",value2,re.IGNORECASE)) != 1:
                                                        raise ValueError ("Only Email supported as validationType for string/(email)")
                              else: 
                                 raise ValueError ("Only " + str(avaiStringConstraints) + " constraints supported on String")
               
                      if (self._typeDict["Integer"]):

                          if 'GT' in self._constraintDict[key].keys() and 'GTE' in self._constraintDict[key].keys():
                            raise ValueError ("Both GT and GTE should not be specified together")
                          if 'LT' in self._constraintDict[key].keys() and 'LTE' in self._constraintDict[key].keys():
                            raise ValueError ("Both GT and GTE should not be specified together")
                          if 'EQ' in self._constraintDict[key].keys() and len(list(self._constraintDict[key].keys()))>1:
                            raise ValueError ("EQ with other constraints is not supported")
                              
                          for key2, value2 in self._constraintDict[key].items():
                              if (key2.lower()=='DBType'.lower()):
                                 if ((value2.lower() != 'INTEGER'.lower()) and (value2.lower() != 'SMALLINT'.lower()) and (value2.lower() != 'BIGINT'.lower())):
                                   raise ValueError ("Only INTEGER/SMALLINT/BIGINT DBType supported for integers")
                              elif (key2.lower() in ['GT'.lower(), 'GTE'.lower(), 'LT'.lower(), 'LTE'.lower(), 'EQ'.lower()]):
                                 if (not isinstance(ast.literal_eval(value2),int)):
                                   raise ValueError ("At Integer constraint "+ key2 +" integer compared to non Integer type")
                              else:
                                 raise ValueError ("Only " + str(avaiIntegerConstraints) + " constraints supported on INTEGER")    
               
                      if (self._typeDict["Float"]):
                           for key2, value2 in self._constraintDict[key].items():
                              if (key2.lower()=='DBType'.lower()):
                                 if(len(re.findall("FLOAT\([0-9]+\)",value2,re.IGNORECASE)) != 1):
                                   raise ValueError ("Only FLOAT(precision) DBType supported for FLOAT type")
                                   if (len(re.findall("[0-9]+",value2,re.IGNORECASE)) != 1):
                                    raise ValueError ("Precision specified should be Integer type")
                              elif (key2.lower() in ['GT'.lower(), 'LT'.lower()]):
                                 fp = re.findall("\d+\.\d+",value2,re.IGNORECASE)
                                 if (fp != [] and not isinstance(ast.literal_eval(fp[0]),float)):
                                   
                                   raise ValueError ("At FP constraint "+ key2 +" integer compared to non FP type")
                              else:
                                 raise ValueError ("Only " + str(avaiFPConstraints) + " constraints supported on FLOAT")
                                       
                                   
                      if (self._typeDict["Boolean"]):
                           for key2, value2 in self._constraintDict[key].items():
                              if (key2.lower()=='DBType'.lower()):
                                                if(len(re.findall("Boolean",value2,re.IGNORECASE)) != 1):
                                                        raise ValueError ("Only BOOLEAN DBType supported for Boolean type")
                              elif (key2.lower() in ['EQ'.lower()]):
                                 if (value2 != 'True' and value2!='False'):
                                   raise ValueError ("Boolean constraint on " + str(key2)+ " can be either True or False")
                              else:
                                 raise ValueError ("Only " + str(avaiBooleanConstraints) + " constraints supported on FLOAT")
        
                      
                      if (self._typeDict["Date"]):
                           for key2, value2 in self._constraintDict[key].items():
                              if (key2.lower()=='DBType'.lower()):
                                 if(len(re.findall("Date",value2,re.IGNORECASE)) != 1):
                                   raise ValueError ("Only DATE DBType supported for Date")
                              elif ((key2.lower() in ['GT'.lower(), 'LT'.lower()])):
                                 dt = re.findall("[0-9]{4}\-[0-9]{2}\-[0-9]{2}",value2,re.IGNORECASE)
                                 if len(dt) != 1:
                                   raise ValueError ("Date should be specified in the format yyyy-mm-dd")

                     
                     
               return

class AttachmentConstraintValidator(object):

        def __init__(self,attachmentTypeDict):
              self._attachmentTypeDict = attachmentTypeDict

        def validate(self):

              for attachmentType, attachmentValue in self._attachmentTypeDict.items():
                if (not  isinstance(attachmentValue,bool)):
                  raise ValueError ("Value corresponding to attachment type must be boolean")

              attachmentTypeValues = [value for value in list(self._attachmentTypeDict.values())]
              if (attachmentTypeValues.count(True)>1):
                  raise ValueError('Exactly one type must be set to True')
