

class AdmissionDetails(object):
	
	def __init__(self):
		self._AdmissionDegree = None
		self._AdmissionType = None
		self._AdmissionMonth = None
		self._AdmissionYear = None

		return

	@property
	def AdmissionDegree(self):
            return self._AdmissionDegree

	@AdmissionDegree.setter
	def AdmissionDegree(self,admissionDegree):
		if (type(admissionDegree) is not str):
			raise ValueError('AdmissionDegree must be type String')
		self._AdmissionDegree = str(admissionDegree)

	@property
	def AdmissionType(self):
		return self._AdmissionType

	@AdmissionType.setter        
	def AdmissionType(self,admissionType):
		if (type(admissionType) is not str):
			raise ValueError('AdmissionType must be type String')
		self._AdmissionType = str(admissionType)

	@property
	def AdmissionMonth(self):
		return self._AdmissionMonth

	@AdmissionMonth.setter
	def AdmissionMonth(self,admissionMonth):
		if (type(admissionMonth) is not str):
			raise ValueError('AdmissionMonth must be type String')
		self._AdmissionMonth = str(admissionMonth)
        
	@property
	def AdmissionYear(self):
		return self._AdmissionYear
       
	@AdmissionYear.setter 
	def AdmissionYear(self,admissionYear):
		if (type(admissionYear) is not str):
			raise ValueError('AdmissionYear must be type String')
		self._AdmissionYear = str(admissionYear)



