import pip
import pprint
installed_packages = pip.get_installed_distributions()
installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
     for i in installed_packages])
pprint.pprint(installed_packages_list)

import cv2
print cv2.__version__
