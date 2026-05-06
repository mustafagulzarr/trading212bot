from py_common.compliance.aaoifi_inhouse import InHouseAAOIFIProvider
from py_common.compliance.mock import MockComplianceProvider
from py_common.compliance.musaffa import MusaffaProvider
from py_common.compliance.zoya import ZoyaProvider


def get_provider(name: str):
    registry = {
        "in_house_aaoifi": InHouseAAOIFIProvider,
        "mock": MockComplianceProvider,
        "musaffa": MusaffaProvider,
        "zoya": ZoyaProvider,
    }
    if name not in registry:
        raise ValueError(f"Unsupported compliance provider: {name}")
    return registry[name]()
