import json
import os
import jsonschema
from ruamel.yaml import YAML
from cffconvert.behavior_1_2_x.apalike import ApalikeObject
from cffconvert.behavior_1_2_x.bibtex import BibtexObject
from cffconvert.behavior_1_2_x.codemeta import CodemetaObject
from cffconvert.behavior_1_2_x.endnote import EndnoteObject
from cffconvert.behavior_1_2_x.ris import RisObject
from cffconvert.behavior_1_2_x.schemaorg import SchemaorgObject
from cffconvert.behavior_1_2_x.zenodo import ZenodoObject
from cffconvert.contracts.citation import Contract
from cffconvert.root import get_package_root


class Citation_1_2_x(Contract):  # nopep8

    supported_cff_versions = [
        "1.2.0"
    ]

    def __init__(self, cffstr, cffversion):
        self.cffstr = cffstr
        self.cffversion = cffversion
        self.cffobj = self._parse()
        self.schema = self._get_schema()

    def _get_schema(self):
        schema_path = os.path.join(get_package_root(), "schemas", "1.2.0", "schema.json")
        with open(schema_path, "rt") as fid:
            return json.loads(fid.read())

    def _parse(self):
        # instantiate the YAML module:
        yaml = YAML(typ="safe")

        # while loading, convert timestamps to string
        yaml.constructor.yaml_constructors[u'tag:yaml.org,2002:timestamp'] = \
            yaml.constructor.yaml_constructors[u'tag:yaml.org,2002:str']

        cffobj = yaml.load(self.cffstr)

        if not isinstance(cffobj, dict):
            raise ValueError("Provided CITATION.cff does not seem valid YAML.")

        return cffobj

    def as_apalike(self):
        return ApalikeObject(self.cffobj).print()

    def as_bibtex(self, reference='YourReferenceHere'):
        return BibtexObject(self.cffobj).print(reference)

    def as_cff(self):
        return self.cffstr

    def as_codemeta(self):
        return CodemetaObject(self.cffobj).print()

    def as_endnote(self):
        return EndnoteObject(self.cffobj).print()

    def as_ris(self):
        return RisObject(self.cffobj).print()

    def as_schemaorg(self):
        return SchemaorgObject(self.cffobj).print()

    def as_zenodo(self):
        return ZenodoObject(self.cffobj).print()

    def validate(self):
        jsonschema.validate(instance=self.cffobj, schema=self.schema, format_checker=jsonschema.FormatChecker())