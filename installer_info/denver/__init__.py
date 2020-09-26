'''
Denver is a project targeting python developers for easy and fast development
with the modules provided within it.

The Developers who are using other IDE which support code completion might
not know that all the modules are imported by default when importing this package.
'''

#  Copyright (c) 2020 Xcodz.
#  All Rights Reserved.

__author__ = 'Xcodz'
__version__ = '2020.6.4'
__all__ = []

def ispackage(path):
	if '__init__.py' in os.listdir(path):
		return True
	else:
		return False


#import system
if __name__ != "__main__": #Imported as a package
	import os, sys
	sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/py'))
	sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)+'/../external_packages'))
	from . import log
	log.conf['debug'] = False
	LOG = log.Logger("RESX32_X64 Package Importer")
	LOG.format = "{level}:{name}:{msg}{error}\n"
	for x in os.listdir(os.path.dirname(__file__)):
		path = os.path.abspath(os.path.join(os.path.dirname(__file__),x))
		name,ext = os.path.splitext(os.path.basename(path))[0], os.path.splitext(path)[-1]
		LOG.debug(f"Module Name is {name}, Ext is {ext}, path is {path}")
		if (ext in ['.py', '.pyw', '.pyc', '.pyd']) and name[0:2] != '__' and os.path.isfile(path):
			try:
				__all__.append(name)
				exec(f"from . import {name}")
				LOG.debug(f"Successfull importing {name} ")
			except Exception as e:
				LOG.warning(f"Error importing {name}:",error = e)
		if os.path.isdir(path):
			if ispackage(path):
				try:
					__all__.append(name)
					exec(f"from . import {name}")
					LOG.debug(f"Successfull importing package {name}")
				except Exception as e:
					LOG.warning("Error importing package {name}:", error = e)
	#cleanup
	del LOG, ext, name, path, x, ispackage, sys