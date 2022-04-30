import json
from typing import List, Dict, Tuple

if __name__ == '__main__':
    with open('data/sectors_dump.json') as f:
        orig = json.load(f)

    data: Dict[str, List[Tuple[str, str]]] = {}

    for sec in orig:
        worlds = sec['Worlds']['Results']['Items']
        sec_name = worlds[0]['World']['Sector']
        data[sec_name] = []
        for w in worlds:
            if len(w['World']['Name']) > 0 and '?' not in w['World']['Uwp']:
                data[sec_name].append((w['World']['Name'], w['World']['Uwp']))

        # Remove sectors with less than 25 worlds in them
        if len(data[sec_name]) < 25:
            del data[sec_name]

    with open('data/map.json', 'w') as f:
        json.dump(data, f, indent=4)
