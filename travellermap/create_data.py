import json
from typing import List, Dict, Tuple

if __name__ == '__main__':
    with open('data/sectors_dump.json') as f:
        orig = json.load(f)

    data: Dict[str, List[Tuple[str, str, str]]] = {}

    for sec in orig:
        worlds = sec['Worlds']['Results']['Items']
        sec_name = worlds[0]['World']['Sector']
        data[sec_name] = []
        for w in worlds:
            hexc: str = str(w['World']['HexX']).zfill(2) + str(w['World']['HexY']).zfill(2)
            uwp: str = w['World']['Uwp']
            hexc: str = w['World']['HexX'] + w['World']['HexY']
            if len(w['World']['Name']) > 0 and '?' not in uwp:
                for i in range(1, len(uwp)):
                    if uwp[i] > 'F':
                        uwp = uwp[:i] + 'F' + uwp[i+1:]
                data[sec_name].append((w['World']['Name'], uwp, hexc))

        # Remove sectors with less than 25 worlds in them
        if len(data[sec_name]) < 25:
            del data[sec_name]

    with open('data/map.json', 'w') as f:
        json.dump(data, f, indent=4)
