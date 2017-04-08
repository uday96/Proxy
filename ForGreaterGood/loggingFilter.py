import logging
from django.conf import settings

class ModuleFilter(logging.Filter):

	def filter(self, record):
		BaseDirPath = settings.BASE_DIR+"/"
		currPath = record.pathname
		currPath = currPath.replace(BaseDirPath,"")
		mymodule = currPath.split("/")[0]
		record.mymodule = mymodule
		return True
