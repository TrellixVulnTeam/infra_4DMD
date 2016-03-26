from infra.system.core.meta.metaartefactkeygenerator import MetaArtefactKeyGenerator
import logging

class GolangProjectDistributionBuildKeyGenerator(MetaArtefactKeyGenerator):

	def generate(self, data, delimiter = ":"):
		# return a list of fields
		keys = []
		for key in ["artefact", "product", "distribution", "build"]:
			if key not in data:
				raise ValueError("golang-project-distribution-build: %s key missing" % key)

			keys.append(data[key])

		return delimiter.join(keys)
