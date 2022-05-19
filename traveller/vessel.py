from typing import Dict, Optional

_ship_share_value = 2_000

vessels: Dict[str, int] = {
    # Vessels
    'Asteroid Miner': 33_219,
    'Courier': 35_928,
    'Destroyer': 422_775,
    'Dreadnought': 2_768_145,
    'Frontier Trader': 82_314,
    'Heavy Cruiser': 1_146_915,
    'Light Cruiser': 597_870,
    'Merchant Freighter': 59_814,
    'Merchant Liner': 70_209,
    'Merchant Trader': 34_929,
    'Patrol Frigate': 180_675,
    'Raider': 310_851,
    'Research Vessel': 73_809,
    'Survey Vessel': 120_969,
    'System Defense Boat': 171_574,
    'System Monitor': 610_461,
    'Yacht': 26_388,

    # Small Crafts
    'Cutter': 24_305,
    'Fighter': 10_841,
    'Launch': 4_797,
    'Pinnace': 18_567,
    'Ship\'s Boat': 16_677,
    'Shuttle': 25_587
}


def get_best(ship_shares: int) -> Optional[str]:
    val = ship_shares * _ship_share_value

    ship: Optional[str] = None
    maxc: int = 0

    for k, cost in vessels.items():
        if val >= cost > maxc:
            ship = k
            maxc = cost

    return ship
