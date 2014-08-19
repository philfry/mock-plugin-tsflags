# vim:expandtab:autoindent:tabstop=4:shiftwidth=4:filetype=python:textwidth=0:
from mockbuild.trace_decorator import decorate, traceLog

import mockbuild.util

requires_api_version = "1.0"

decorate(traceLog())
def init(rootObj, conf):
	TSflags(rootObj, conf)

class TSflags(object):
	"""This plugin will append "--setopt=tsflags" to every yum call.
	   The flags are specified using --plugin-option tsflags:flags=foo,bar

	   This can be useful to skip %-scripts when (un-)installing packages.

       Please note that this plugin conflicts with the selinux-plugin.
	"""

	decorate(traceLog())
	def __init__(self, rootObj, conf):
		self.rootObj = rootObj
		self.conf = conf
		rootObj.addHook("preyum", self._tsPreYumHook)
		rootObj.addHook("postyum", self._tsPostYumHook)

	decorate(traceLog())
	def _tsPreYumHook(self):
		self._originalUtilDo = mockbuild.util.do
		mockbuild.util.do = self._tsDoYum

	decorate(traceLog())
	def _tsPostYumHook(self):
		mockbuild.util.do = self._originalUtilDo

	decorate(traceLog())
	def _tsDoYum(self, command, *args, **kargs):
		options = ""
		try:
			self.conf['flags']
			options = "--setopt=tsflags="+self.conf['flags']
			
		except KeyError:
			print("please specify at least a tsflag:")
			print("\t--plugin-option tsflags:flags=foo")

		if type(command) is list:
			if command[0].startswith(self.rootObj.yum_path):
				command.append(options)
		elif type(command) is str:
			if command.startswith(self.rootObj.yum_path):
				command += " %s" % options

		return self._originalUtilDo(command, *args, **kargs)
