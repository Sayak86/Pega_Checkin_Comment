import re
import copy
from typing import Dict, Any, List

SEGMENT_MAP = {
    'pySteps': 'Step',
    'pyParamArray': 'Param',
    'pyWhenArray': 'When',
    'pyPropertySets': 'PropertySet',
    'pyPages': 'Page',
    'pyPreconditions': 'Precondition',
    'pyTransitions': 'Transition',
    'pyLocalVariables': 'LocalVar',
    'pyLoopInfo': 'Loop',
    'pySecurity': 'Security',
    'pyClassName': 'Class',
    'pyMethodArray': 'Method',
    'pyConnectArray': 'Connect',
    'pyMappingArray': 'Mapping',
    'pyTargetArray': 'Target',
    'pySourceArray': 'Source',
    'pyRelationArray': 'Relation',
    'pyExpressionArray': 'Expression',
}

SEGMENT_PATTERN = re.compile(r'\.(\w+?)(?:\((\d+)\))?(?=\.|$)')

NOISE_FIELDS = {'pxObjClass', 'pxTextChangeList'}


def resolve_pega_path(raw_ref: str) -> str:
    if not raw_ref:
        return raw_ref

    parts = []
    for match in SEGMENT_PATTERN.finditer(raw_ref):
        name, index = match.group(1), match.group(2)
        readable = SEGMENT_MAP.get(name, name)
        if index:
            parts.append(f"{readable} {index}")
        else:
            parts.append(readable)

    return " > ".join(parts) if parts else raw_ref


def preprocess_pxresults(rule_diff_data: Dict[str, Any]) -> Dict[str, Any]:
    enriched = copy.deepcopy(rule_diff_data)
    px_results = enriched.get("pxResults", [])

    for item in px_results:
        current_ref = item.get("pxCurrentReference", "")
        if current_ref:
            item["resolved_path"] = resolve_pega_path(current_ref)

        previous_ref = item.get("pxPreviousReference", "")
        if previous_ref:
            item["resolved_previous_path"] = resolve_pega_path(previous_ref)

        for field in NOISE_FIELDS:
            item.pop(field, None)

    return enriched
