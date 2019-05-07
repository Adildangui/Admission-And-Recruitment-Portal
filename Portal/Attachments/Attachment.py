import ast

class Attachment(object): 
        
        def __inti__(self):

               self._AttachmentName = ""
               self._AttachmentLabel = ""
               self._IsTypeFile = False
               self._IsTypeImage = False
               self._IsOptional = False

        @property
        def AttachmentName(self):
                return self._AttachmentName

        @AttachmentName.setter
        def AttachmentName(self,attachmentName):
                if (type(attachmentName) is not str):
                        raise ValueError('AttachmentName must be type String')
                self._AttachmentName = str(attachmentName)

        @property
        def AttachmentLabel(self):
                return self._AttachmentLabel

        @AttachmentLabel.setter
        def AttachmentLabel(self,attachmentLabel):
                if (type(attachmentLabel) is not str):
                        raise ValueError('AttachmentLabel must be type String')
                self._AttachmentLabel = str(attachmentLabel)

        @property
        def IsTypeFile(self):
                return self._IsTypeFile

        @IsTypeFile.setter
        def IsTypeFile(self,isTypeFile):
                if (not isinstance(ast.literal_eval(str(isTypeFile)),bool)):
                        raise ValueError('IsTypeFile must be type Boolean')
                self._IsTypeFile = ast.literal_eval(str(isTypeFile))

        @property
        def IsTypeImage(self):
                return self._IsTypeImage

        @IsTypeImage.setter
        def IsTypeImage(self,isTypeImage):
                if (not isinstance(ast.literal_eval(str(isTypeImage)),bool)):
                        raise ValueError('IsTypeImage must be type Boolean')
                self._IsTypeImage = ast.literal_eval(str(isTypeImage))

        @property
        def IsOptional(self):
                return self._IsOptional

        @IsOptional.setter
        def IsOptional(self,isOptional):
                if (not isinstance(ast.literal_eval(str(isOptional)),bool)):
                        raise ValueError('IsOptional must be type Boolean')
                self._IsOptional = ast.literal_eval(str(isOptional))
