import unittest

from .act import ScanDistributionBuildAct
from infra.system.artefacts.artefacts import (
	ARTEFACT_GOLANG_PROJECT_INFO_FEDORA,
	ARTEFACT_GOLANG_IPPREFIX_TO_PACKAGE_NAME,
	ARTEFACT_GOLANG_PROJECT_DISTRIBUTION_PACKAGES,
	ARTEFACT_GOLANG_PROJECT_DISTRIBUTION_EXPORTED_API,
	ARTEFACT_GOLANG_IPPREFIX_TO_RPM
)

class ScanDistributionBuildActTest(unittest.TestCase):

	def test(self):

		data = {
			"product": "Fedora",
			"distribution": "f24",
			"build": {
				"name": "etcd-2.2.4-2.fc24",
				"rpms": [
					{
						"name": "etcd-devel-2.2.4-2.fc24.noarch.rpm"
					}
				]
			}
		}

		expected = {
			ARTEFACT_GOLANG_PROJECT_DISTRIBUTION_EXPORTED_API: {},
			ARTEFACT_GOLANG_PROJECT_DISTRIBUTION_PACKAGES: {},
			ARTEFACT_GOLANG_IPPREFIX_TO_RPM: {}
		}

		a = ScanDistributionBuildAct()
		a.setData(data)
		# Don't execute the act, just return empty data
		self.assertEqual(a.getData(), expected)
