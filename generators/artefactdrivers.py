import json
from .classhelper import ClassHelper

def generateDriver(key):
	lines = []
	lines.append("from .artefactdriver import ArtefactDriver")
	lines.append("from infra.system.artefacts.artefacts import %s" % key["artefact"])

	obj = ClassHelper(key)
	lines.append("\nclass %sDriver(ArtefactDriver):\n" % obj.class_name())

	lines.append("\tdef __init__(self):\n")

	lines.append("\t\tArtefactDriver.__init__(self, %s)\n" % key["artefact"])

	return "\n".join(lines)

def generateFF(key_spec):
	lines = []
	lines.append("from infra.system.artefacts import artefacts")

	for key in key_spec:
		obj = ClassHelper(key)
		lines.append("from .%s import %sDriver" % (obj.class_filename(), obj.class_name()))

	lines.append("\nclass ArtefactDriverFactory:\n")
	lines.append("\tdef build(self, artefact):\n")

	for key in key_spec:
		obj = ClassHelper(key)

		lines.append("\t\tif artefact == artefacts.%s:" % key["artefact"])
		lines.append("\t\t\treturn %sDriver()\n" % obj.class_name())

	lines.append("\t\traise ValueError(\"Invalid artefact: %s\" % artefact)")

	return "\n".join(lines)

def generateFileStorageArtefactFactory(key_spec):
	lines = []
	lines.append("from infra.system.artefacts import artefacts")
	lines.append("from .artefactdriver import ArtefactDriver")
	lines.append("\nclass ArtefactDriverFactory(object):\n")
	lines.append("\tdef __init__(self):")
	lines.append("\t\tself.working_directory = \"/var/lib/gofed/simplefilestorage\"")
	lines.append("\t\tself.artefacts = []\n")

	for key in key_spec:
		lines.append("\t\tself.artefacts.append(artefacts.%s)" % key["artefact"])

	lines.append("")
	lines.append("\tdef build(self, artefact):")
	lines.append("\t\tif artefact not in self.artefacts:")
	lines.append("\t\t\traise KeyError(\"Artefact '%s' not supported\" % artefact)\n")
	lines.append("\t\treturn ArtefactDriver(self.working_directory, artefact)")

	return "\n".join(lines)

if __name__ == "__main__":
	with open("generators/artefacts.json", "r") as f:
		keys = json.load(f)

	# generate file storage artefact driver factory
	with open("system/plugins/simplefilestorage/artefactdriverfactory.py", "w") as f:
		f.write(generateFileStorageArtefactFactory(keys))
		print("system/plugins/simplefilestorage/artefactdriverfactory.py")

	# generate driver factory
	with open("system/plugins/simpleetcdstorage/artefactdriverfactory.py", "w") as f:
		f.write(generateFF(keys))
		print("system/plugins/simpleetcdstorage/artefactdriverfactory.py")

	for key in keys:
		obj = ClassHelper(key)
		with open("system/plugins/simpleetcdstorage/%s" % obj.class_filename_ext(), "w") as f:
			f.write(generateDriver(key))
			print("system/plugins/simpleetcdstorage/%s" % obj.class_filename_ext())
