city.py

# =============================================================
#  GREEN LOOP — city.py
#  Person 1's file
#
#  What this file does:
#    1. Creates a simulated city with 30 bins (the Hash Table)
#    2. Simulates bins filling up over time
#    3. Provides helper functions for the rest of the team
#
#  DSA used here: HASH TABLE (Python dictionary)
#  Why: Lets us look up any bin instantly by its ID — O(1) time
# =============================================================

import random  # already built into Python, nothing to install


# =============================================================
#  SECTION 1 — CONSTANTS
#  These never change while the program runs.
#  Think of them as the rules of our city.
# =============================================================

# How much each zone's bins fill up per simulated hour
# Format: "zone name": (minimum fill per hour, maximum fill per hour)
ZONE_FILL_RATES = {
    "market":      (8, 15),   # busy markets — fills fast
    "residential": (2, 5),    # homes — slow and steady
    "school":      (2, 14),   # unpredictable — slow in morning, burst at lunch/home time
}

# Thresholds — when do we start worrying about a bin?
THRESHOLD_URGENT   = 70   # above 70% → needs collection soon
THRESHOLD_CRITICAL = 85   # above 85% → needs collection NOW, health risk


# =============================================================
#  SECTION 2 — CREATE THE CITY
#  This is our Hash Table.
#  Key   = Bin ID (like "B001")
#  Value = Dictionary with all the bin's details
# =============================================================

def create_city():
    """
    Builds the city and returns it as a dictionary (hash table).
    Each bin is stored with a unique ID as the key.

    Returns:
        dict: The full city — 30 bins, each with id, location, fill_level, zone
    """

    city_bins = {}  # our hash table starts empty

    # ----------------------------------------------------------
    # Bin definitions — (bin_id, (x, y location), zone_type)
    # Think of x,y as a grid map of Pune
    # Grid goes from (0,0) bottom-left to (10,10) top-right
    # ----------------------------------------------------------

    bin_definitions = [

        # --- MARKET ZONE --- near areas like Mandai, Laxmi Road, MG Road
        # These are the busiest bins — they fill up fastest
        ("B001", (2, 8),  "market"),
        ("B002", (3, 7),  "market"),
        ("B003", (4, 8),  "market"),
        ("B004", (3, 9),  "market"),
        ("B005", (5, 8),  "market"),

        # --- SCHOOL ZONE --- near schools and colleges
        # These are unpredictable — quiet in morning, burst at 4pm
        ("B006", (2, 6),  "school"),
        ("B007", (5, 5),  "school"),
        ("B008", (8, 7),  "school"),
        ("B009", (7, 8),  "school"),
        ("B010", (4, 5),  "school"),

        # --- RESIDENTIAL ZONE --- homes in Kothrud, Aundh, Baner etc.
        # These fill slowly and predictably
        ("B011", (1, 3),  "residential"),
        ("B012", (2, 2),  "residential"),
        ("B013", (1, 5),  "residential"),
        ("B014", (3, 3),  "residential"),
        ("B015", (4, 2),  "residential"),
        ("B016", (6, 3),  "residential"),
        ("B017", (7, 2),  "residential"),
        ("B018", (8, 4),  "residential"),
        ("B019", (9, 3),  "residential"),
        ("B020", (6, 6),  "residential"),
        ("B021", (9, 6),  "residential"),
        ("B022", (8, 2),  "residential"),
        ("B023", (6, 9),  "residential"),
        ("B024", (1, 8),  "residential"),
        ("B025", (5, 1),  "residential"),
        ("B026", (9, 9),  "residential"),
        ("B027", (7, 5),  "residential"),
        ("B028", (3, 1),  "residential"),
        ("B029", (1, 1),  "residential"),
        ("B030", (9, 1),  "residential"),
    ]

    # ----------------------------------------------------------
    # Now create each bin and store it in the hash table
    # This is where the Hash Table is actually built
    # ----------------------------------------------------------

    for bin_id, location, zone in bin_definitions:
        city_bins[bin_id] = {
            "id":         bin_id,
            "location":   location,
            "fill_level": random.randint(10, 45),  # random starting fill 10–45%
            "zone":       zone,
        }

    return city_bins


# =============================================================
#  SECTION 3 — SIMULATE TIME PASSING
#  Every time this is called, one "hour" passes in the city.
#  Bins fill up based on their zone type.
# =============================================================

def simulate_one_hour(city_bins):
    """
    Simulates one hour passing. Every bin fills up a little.
    Market bins fill fast. Residential bins fill slowly.
    No bin goes above 100%.

    Args:
        city_bins (dict): The current state of the city

    Returns:
        dict: The updated city after one hour
    """

    for bin_id in city_bins:
        zone = city_bins[bin_id]["zone"]               # what zone is this bin?
        min_rate, max_rate = ZONE_FILL_RATES[zone]     # get fill rate for this zone
        increase = random.randint(min_rate, max_rate)  # random fill within range

        current_fill = city_bins[bin_id]["fill_level"]
        new_fill = current_fill + increase

        # Never go above 100%
        city_bins[bin_id]["fill_level"] = min(100, new_fill)

    return city_bins


# =============================================================
#  SECTION 4 — HELPER FUNCTIONS
#  These are small tools that Persons 2, 3, and 4 will use.
# =============================================================

def empty_bin(city_bins, bin_id):
    """
    Empties a bin after the truck collects it.
    Called by Person 3 (the router) after visiting a bin.

    Args:
        city_bins (dict): The city
        bin_id    (str):  Which bin to empty e.g. "B003"

    Returns:
        dict: Updated city with that bin now at 0%
    """
    city_bins[bin_id]["fill_level"] = 0
    return city_bins


def get_bins_above(city_bins, threshold):
    """
    Returns all bins whose fill level is at or above a threshold.
    Called by Person 2 (alerts) and Person 3 (router).

    Args:
        city_bins (dict): The city
        threshold (int):  The fill % to check against e.g. 70

    Returns:
        list: All bin dictionaries at or above that fill level
    """
    result = []
    for bin_id in city_bins:
        if city_bins[bin_id]["fill_level"] >= threshold:
            result.append(city_bins[bin_id])
    return result


def get_bin_by_id(city_bins, bin_id):
    """
    Returns a single bin's data by its ID.
    This is the Hash Table lookup — instant, O(1).

    Args:
        city_bins (dict): The city
        bin_id    (str):  The bin to look up e.g. "B007"

    Returns:
        dict: That bin's data, or None if not found
    """
    return city_bins.get(bin_id, None)


def get_city_summary(city_bins):
    """
    Returns a summary of the whole city's current state.
    Useful for Person 4's display.

    Returns:
        dict: counts of empty, normal, urgent, critical bins
    """
    summary = {
        "total":    len(city_bins),
        "empty":    0,   # 0–30%
        "normal":   0,   # 31–69%
        "urgent":   0,   # 70–84%
        "critical": 0,   # 85–100%
    }

    for bin_id in city_bins:
        fill = city_bins[bin_id]["fill_level"]
        if fill <= 30:
            summary["empty"] += 1
        elif fill <= 69:
            summary["normal"] += 1
        elif fill <= 84:
            summary["urgent"] += 1
        else:
            summary["critical"] += 1

    return summary


# =============================================================
#  SECTION 5 — TEST
#  Run this file directly to make sure everything works.
#  In VS Code: right click → Run Python File in Terminal
#  Or in terminal: python city.py
# =============================================================

if __name__ == "__main__":

    print("=" * 55)
    print("  GREEN LOOP — City Module Test")
    print("=" * 55)

    # --- Test 1: Create the city ---
    print("\n[TEST 1] Creating city...")
    city = create_city()
    print(f"  City created with {len(city)} bins.")
    print(f"\n  {'BIN':<6} {'ZONE':<14} {'LOCATION':<12} {'FILL':>6}")
    print("  " + "-" * 42)
    for bin_id in city:
        b = city[bin_id]
        print(f"  {b['id']:<6} {b['zone']:<14} "
              f"{str(b['location']):<12} {b['fill_level']:>5}%")

    # --- Test 2: Simulate hours passing ---
    print("\n[TEST 2] Simulating 4 hours passing...")
    print(f"\n  {'BIN':<6} {'ZONE':<14} {'HOUR 0':>8} {'HOUR 1':>8} "
          f"{'HOUR 2':>8} {'HOUR 3':>8} {'HOUR 4':>8}")
    print("  " + "-" * 60)

    # Save starting fills
    starting_fills = {b: city[b]["fill_level"] for b in city}

    # Save fills after each hour
    hour_fills = {b: [starting_fills[b]] for b in city}
    for hour in range(4):
        city = simulate_one_hour(city)
        for b in city:
            hour_fills[b].append(city[b]["fill_level"])

    # Print ALL 30 bins
    for bin_id in hour_fills:
        fills = hour_fills[bin_id]
        bar = "█" * (fills[-1] // 10)
        print(f"  {bin_id:<6} {city[bin_id]['zone']:<14} "
              f"{fills[0]:>7}% {fills[1]:>7}% {fills[2]:>7}% "
              f"{fills[3]:>7}% {fills[4]:>7}%  {bar}")

    # --- Test 3: Get urgent and critical bins ---
    print("\n[TEST 3] Checking for urgent and critical bins after 4 hours...")
    urgent   = get_bins_above(city, THRESHOLD_URGENT)
    critical = get_bins_above(city, THRESHOLD_CRITICAL)
    print(f"  Bins at or above {THRESHOLD_URGENT}% (urgent):   {len(urgent)}")
    print(f"  Bins at or above {THRESHOLD_CRITICAL}% (critical): {len(critical)}")
    print(f"\n  {'BIN':<6} {'ZONE':<14} {'FILL':>6}  STATUS")
    print("  " + "-" * 40)
    for b in sorted(urgent, key=lambda x: x["fill_level"], reverse=True):
        if b["fill_level"] >= THRESHOLD_CRITICAL:
            status = "🔴 CRITICAL — collect immediately"
        else:
            status = "🟡 URGENT   — collect soon"
        print(f"  {b['id']:<6} {b['zone']:<14} {b['fill_level']:>5}%  {status}")

    # --- Test 4: Hash table lookup ---
    print("\n[TEST 4] Hash table lookup — finding B007 directly...")
    result = get_bin_by_id(city, "B007")
    if result:
        print(f"  Found: {result}")

    # --- Test 5: Empty a bin ---
    print("\n[TEST 5] Truck empties bin B007...")
    print(f"  Before: Fill = {city['B007']['fill_level']}%")
    city = empty_bin(city, "B007")
    print(f"  After:  Fill = {city['B007']['fill_level']}%")

    # --- Test 6: City summary ---
    print("\n[TEST 6] Overall city summary...")
    summary = get_city_summary(city)
    for key, val in summary.items():
        print(f"  {key:10}: {val}")

    print("\n" + "=" * 55)
    print("  All tests passed. city.py is ready.")
    print("  Hand off city_bins to Persons 2, 3, and 4.")
    print("=" * 55)






























alerts.py

# =============================================================
#  GREEN LOOP — alerts.py
#  Person 2's file
#
#  What this file does:
#    1. Scans all 30 bins and detects which need attention
#    2. Sorts them by urgency using a Min-Heap (priority queue)
#    3. Fires alerts — urgent warnings and critical emergencies
#    4. Gives Person 3 (the router) a ready-to-use priority list
#
#  DSA used here: MIN-HEAP (Python's heapq module)
#  Why: A heap always keeps the most urgent bin at the top.
#       Inserting a bin = O(log n). Getting most urgent = O(1).
#       Much faster than sorting the list every single time.
#
#  Depends on: city.py (Person 1's file)
# =============================================================

import heapq   # built into Python — no installation needed
from city import (
    create_city,
    simulate_one_hour,
    get_bins_above,
    THRESHOLD_URGENT,
    THRESHOLD_CRITICAL,
)


# =============================================================
#  SECTION 1 — CONSTANTS
# =============================================================

# Fill level categories with labels and symbols
STATUS_EMPTY    = "empty"     # 0  – 30%
STATUS_NORMAL   = "normal"    # 31 – 69%
STATUS_URGENT   = "urgent"    # 70 – 84%
STATUS_CRITICAL = "critical"  # 85 – 100%

# How we display each status in the terminal
STATUS_DISPLAY = {
    STATUS_EMPTY:    ("🟢", "EMPTY    "),
    STATUS_NORMAL:   ("🔵", "NORMAL   "),
    STATUS_URGENT:   ("🟡", "URGENT   "),
    STATUS_CRITICAL: ("🔴", "CRITICAL "),
}


# =============================================================
#  SECTION 2 — DETERMINE BIN STATUS
#  Given a fill level, return what category it falls into
# =============================================================

def get_status(fill_level):
    """
    Returns the status label for a given fill level.

    Args:
        fill_level (int): 0 to 100

    Returns:
        str: one of 'empty', 'normal', 'urgent', 'critical'
    """
    if fill_level >= THRESHOLD_CRITICAL:
        return STATUS_CRITICAL
    elif fill_level >= THRESHOLD_URGENT:
        return STATUS_URGENT
    elif fill_level > 30:
        return STATUS_NORMAL
    else:
        return STATUS_EMPTY


# =============================================================
#  SECTION 3 — BUILD THE PRIORITY QUEUE (THE HEAP)
#
#  This is the core DSA of Person 2's work.
#
#  A Min-Heap always puts the SMALLEST value at the top.
#  We want the MOST URGENT bin at the top.
#  Most urgent = HIGHEST fill level.
#
#  Trick: we store fill level as NEGATIVE number.
#  So a bin at 95% is stored as -95.
#  -95 < -70, so 95% bin sits at the top of the min-heap.
#  This is the standard trick to turn a min-heap into a max-heap.
# =============================================================

def build_priority_queue(city_bins, min_fill=0):
    """
    Scans all bins and pushes them into a min-heap sorted by urgency.
    Most urgent bin (highest fill %) always sits at the top.

    Args:
        city_bins (dict): The city from Person 1
        min_fill  (int):  Only include bins at or above this fill level
                          Default 0 means include all bins

    Returns:
        list: A heap (list managed by heapq) of tuples:
              (-fill_level, bin_id, bin_data)
              Negative fill so highest fill = top of heap
    """
    heap = []  # starts empty

    for bin_id in city_bins:
        bin_data  = city_bins[bin_id]
        fill      = bin_data["fill_level"]

        if fill >= min_fill:
            # We push a tuple: (priority, bin_id, bin_data)
            # Priority = -fill_level (negative so highest fill = top)
            # bin_id is included so ties break alphabetically — consistent ordering
            heapq.heappush(heap, (-fill, bin_id, bin_data))

    return heap


# =============================================================
#  SECTION 4 — SCAN AND ALERT
#  Goes through the heap and fires alerts for urgent/critical bins
# =============================================================

def scan_and_alert(city_bins):
    """
    Scans all bins, builds the priority queue, and prints alerts
    for any bin that is urgent or critical.

    Args:
        city_bins (dict): The current city state

    Returns:
        tuple: (urgent_heap, critical_list)
               urgent_heap  — heap of all bins at 70%+, sorted by urgency
               critical_list — plain list of only the critical bins (85%+)
    """

    # Build heap of only bins that need attention (70%+)
    urgent_heap = build_priority_queue(city_bins, min_fill=THRESHOLD_URGENT)

    # Separately collect critical bins for emergency alerts
    critical_list = get_bins_above(city_bins, THRESHOLD_CRITICAL)

    # --- Fire critical alerts first ---
    if critical_list:
        print(f"\n  {'!' * 52}")
        print(f"  ⚠  EMERGENCY — {len(critical_list)} BIN(S) ARE CRITICAL")
        print(f"  {'!' * 52}")
        # Sort critical bins highest fill first
        for b in sorted(critical_list, key=lambda x: x["fill_level"], reverse=True):
            print(f"  🔴 {b['id']} | Zone: {b['zone']:<14} | "
                  f"Fill: {b['fill_level']:>3}% | Location: {b['location']}"
                  f"  ← COLLECT IMMEDIATELY")
        print(f"  {'!' * 52}")
    else:
        print("\n  ✅  No critical bins at this time.")

    # --- Then show all urgent bins ---
    urgent_only = get_bins_above(city_bins, THRESHOLD_URGENT)
    non_critical_urgent = [
        b for b in urgent_only if b["fill_level"] < THRESHOLD_CRITICAL
    ]

    if non_critical_urgent:
        print(f"\n  ⚠  {len(non_critical_urgent)} bin(s) are URGENT (collect soon):")
        for b in sorted(non_critical_urgent,
                        key=lambda x: x["fill_level"], reverse=True):
            print(f"  🟡 {b['id']} | Zone: {b['zone']:<14} | "
                  f"Fill: {b['fill_level']:>3}% | Location: {b['location']}")
    else:
        print("  ✅  No urgent-only bins at this time.")

    return urgent_heap, critical_list


# =============================================================
#  SECTION 5 — PEEK AT TOP OF HEAP
#  Used by Person 3 (the router) to see the most urgent bin
#  without removing it from the heap
# =============================================================

def peek_top(heap):
    """
    Returns the most urgent bin without removing it from the heap.
    If heap is empty, returns None.

    Args:
        heap (list): The priority heap

    Returns:
        dict or None: The most urgent bin's data
    """
    if not heap:
        return None
    # heap[0] is always the top — tuple: (-fill, bin_id, bin_data)
    return heap[0][2]


# =============================================================
#  SECTION 6 — POP FROM HEAP
#  Used by Person 3 to take the most urgent bin off the heap
#  after the truck has been dispatched to it
# =============================================================

def pop_most_urgent(heap):
    """
    Removes and returns the most urgent bin from the heap.
    After this call, the next most urgent bin becomes the top.

    Args:
        heap (list): The priority heap

    Returns:
        dict or None: The bin data of the most urgent bin
    """
    if not heap:
        return None
    neg_fill, bin_id, bin_data = heapq.heappop(heap)
    return bin_data


# =============================================================
#  SECTION 7 — FULL STATUS BOARD
#  Prints every single bin's current status — all 30
#  Used by Person 4 (display) for the city overview
# =============================================================

def print_full_status_board(city_bins):
    """
    Prints a full status board of all 30 bins.
    Sorted by fill level — highest first.
    Every bin gets a colour-coded status label.

    Args:
        city_bins (dict): The current city state
    """

    # Sort all bins by fill level, highest first
    sorted_bins = sorted(
        city_bins.values(),
        key=lambda b: b["fill_level"],
        reverse=True
    )

    print(f"\n  {'BIN':<6} {'ZONE':<14} {'LOCATION':<12} {'FILL':>5}  "
          f"{'BAR':<12} STATUS")
    print("  " + "-" * 68)

    for b in sorted_bins:
        fill    = b["fill_level"]
        status  = get_status(fill)
        symbol, label = STATUS_DISPLAY[status]
        bar     = "█" * (fill // 10)   # each block = 10%
        spaces  = " " * (10 - len(bar))

        print(f"  {b['id']:<6} {b['zone']:<14} {str(b['location']):<12} "
              f"{fill:>4}%  {bar}{spaces}  {symbol} {label}")

    print("  " + "-" * 68)

    # Summary counts at the bottom
    counts = {s: 0 for s in [STATUS_EMPTY, STATUS_NORMAL,
                               STATUS_URGENT, STATUS_CRITICAL]}
    for b in city_bins.values():
        counts[get_status(b["fill_level"])] += 1

    print(f"\n  SUMMARY →  "
          f"🟢 Empty: {counts[STATUS_EMPTY]}  "
          f"🔵 Normal: {counts[STATUS_NORMAL]}  "
          f"🟡 Urgent: {counts[STATUS_URGENT]}  "
          f"🔴 Critical: {counts[STATUS_CRITICAL]}  "
          f"| Total: {len(city_bins)}")


# =============================================================
#  SECTION 8 — SIMULATE LIVE MONITORING
#  Runs for several hours, printing alerts as bins fill up.
#  This is the "live system" feel for the demo.
# =============================================================

def live_monitor(city_bins, hours=6):
    """
    Simulates the system monitoring bins over several hours.
    Each hour, bins fill up and the system checks for alerts.

    Args:
        city_bins (dict): Starting city state
        hours     (int):  How many hours to simulate

    Returns:
        dict: Final city state after all hours
    """

    print(f"\n  Monitoring city for {hours} hours...\n")
    print("  " + "=" * 52)

    for hour in range(1, hours + 1):
        city_bins = simulate_one_hour(city_bins)
        print(f"\n  ⏰  HOUR {hour}")

        # Quick fill summary for this hour
        critical = get_bins_above(city_bins, THRESHOLD_CRITICAL)
        urgent   = get_bins_above(city_bins, THRESHOLD_URGENT)
        non_crit = [b for b in urgent if b["fill_level"] < THRESHOLD_CRITICAL]

        if critical:
            print(f"  🔴 {len(critical)} CRITICAL bin(s)  "
                  f"🟡 {len(non_crit)} urgent bin(s)")
            for b in sorted(critical,
                            key=lambda x: x["fill_level"], reverse=True):
                print(f"      ⚠  {b['id']} ({b['zone']}) "
                      f"at {b['fill_level']}% — EMERGENCY")
        elif non_crit:
            print(f"  🟡 {len(non_crit)} urgent bin(s) — no critical yet")
            for b in sorted(non_crit,
                            key=lambda x: x["fill_level"], reverse=True):
                print(f"      →  {b['id']} ({b['zone']}) at {b['fill_level']}%")
        else:
            print("  ✅  All bins within normal range.")

        print("  " + "-" * 52)

    return city_bins


# =============================================================
#  SECTION 9 — TEST
#  Run this file directly to check everything works.
#  In VS Code: right click → Run Python File in Terminal
#  Or in terminal: python alerts.py
# =============================================================

if __name__ == "__main__":

    print("=" * 56)
    print("  GREEN LOOP — Alert System Test")
    print("=" * 56)

    # --- Setup: create city ---
    print("\n  Setting up city...")
    city = create_city()
    print(f"  30 bins created.\n")

    # --- Test 1: Full status board at start ---
    print("[TEST 1] Full status board — all 30 bins at start:")
    print_full_status_board(city)

    # --- Test 2: Live monitoring over 6 hours ---
    print("\n[TEST 2] Live monitoring — 6 hours of simulation:")
    city = live_monitor(city, hours=6)

    # --- Test 3: Full status board after 6 hours ---
    print("\n[TEST 3] Full status board after 6 hours:")
    print_full_status_board(city)

    # --- Test 4: Scan and fire alerts ---
    print("\n[TEST 4] Running full alert scan...")
    urgent_heap, critical_list = scan_and_alert(city)

    # --- Test 5: Heap operations ---
    print("\n[TEST 5] Heap operations — peek and pop:")
    print(f"  Heap size: {len(urgent_heap)} bins queued")

    top = peek_top(urgent_heap)
    if top:
        print(f"  Most urgent bin (peek):  "
              f"{top['id']} at {top['fill_level']}% — NOT removed from heap")

    popped = pop_most_urgent(urgent_heap)
    if popped:
        print(f"  Most urgent bin (pop):   "
              f"{popped['id']} at {popped['fill_level']}% — REMOVED from heap")

    next_top = peek_top(urgent_heap)
    if next_top:
        print(f"  Next most urgent (peek): "
              f"{next_top['id']} at {next_top['fill_level']}%")
    print(f"  Heap size after pop: {len(urgent_heap)} bins remaining")

    # --- Test 6: Build heap with all bins and show order ---
    print("\n[TEST 6] Priority queue — full dispatch order for truck:")
    full_heap = build_priority_queue(city, min_fill=THRESHOLD_URGENT)
    print(f"  {len(full_heap)} bins queued for collection, in priority order:\n")
    print(f"  {'RANK':<6} {'BIN':<6} {'ZONE':<14} {'FILL':>5}  STATUS")
    print("  " + "-" * 44)
    rank = 1
    temp_heap = list(full_heap)   # copy so we don't destroy the original
    heapq.heapify(temp_heap)
    while temp_heap:
        b = pop_most_urgent(temp_heap)
        symbol, label = STATUS_DISPLAY[get_status(b["fill_level"])]
        print(f"  {rank:<6} {b['id']:<6} {b['zone']:<14} "
              f"{b['fill_level']:>4}%  {symbol} {label}")
        rank += 1

    print("\n" + "=" * 56)
    print("  All tests passed. alerts.py is ready.")
    print("  urgent_heap is ready to hand off to Person 3 (router).")
    print("=" * 56)








































router.py


# =============================================================
#  GREEN LOOP — router.py
#  Person 3's file
#
#  What this file does:
#    1. Builds the city as a Graph (bins = nodes, roads = edges)
#    2. Calculates distances between all bins
#    3. Uses a Greedy Algorithm to build the truck's route
#    4. Handles truck capacity — trip ends when truck is full
#    5. Returns the ordered stop list to Person 4 (display)
#
#  DSA used here:
#    GRAPH         — city represented as adjacency list
#    GREEDY        — always go to nearest urgent bin next
#
#  Why Greedy?
#    At every step the truck asks one question:
#    "Which urgent bin is closest to where I am right now?"
#    It picks that one. Repeats. Simple, fast, good enough.
#
#  Depends on: city.py and alerts.py
# =============================================================

import math
from city import (
    create_city,
    simulate_one_hour,
    empty_bin,
    THRESHOLD_URGENT,
    THRESHOLD_CRITICAL,
)
from alerts import (
    build_priority_queue,
    scan_and_alert,
    print_full_status_board,
    live_monitor,
)


# =============================================================
#  SECTION 1 — CONSTANTS
# =============================================================

TRUCK_CAPACITY   = 10    # truck can collect max 10 bins per trip
TRUCK_START      = (0, 0)  # truck depot — bottom left of the city grid
COLLECTION_THRESHOLD = THRESHOLD_URGENT  # only collect bins at 70%+


# =============================================================
#  SECTION 2 — DISTANCE CALCULATION
#  Euclidean distance between two points on the grid.
#  This is the "road distance" in our simulated city.
# =============================================================

def distance(loc1, loc2):
    """
    Calculates straight-line distance between two grid locations.

    Args:
        loc1 (tuple): (x, y) of first location
        loc2 (tuple): (x, y) of second location

    Returns:
        float: distance between the two points, rounded to 2 decimals
    """
    x1, y1 = loc1
    x2, y2 = loc2
    return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), 2)


# =============================================================
#  SECTION 3 — BUILD THE GRAPH
#
#  The city is represented as a Graph.
#  Nodes  = bins (each bin is a point on the grid)
#  Edges  = roads between every pair of bins
#  Weight = distance between the two bins
#
#  We use an adjacency list — a dictionary where:
#    Key   = bin ID
#    Value = list of (neighbour_bin_id, distance) tuples
#
#  Every bin is connected to every other bin (complete graph)
#  because the truck can theoretically drive anywhere.
# =============================================================

def build_graph(city_bins):
    """
    Builds a complete weighted graph of the city.
    Every bin is connected to every other bin with a distance edge.

    Args:
        city_bins (dict): The city from Person 1

    Returns:
        dict: Adjacency list — { bin_id: [(neighbour_id, dist), ...] }
    """

    graph = {}
    bin_ids = list(city_bins.keys())

    # Create an entry for every bin
    for bin_id in bin_ids:
        graph[bin_id] = []

    # Connect every bin to every other bin
    for i in range(len(bin_ids)):
        for j in range(len(bin_ids)):
            if i != j:  # don't connect a bin to itself
                id_a = bin_ids[i]
                id_b = bin_ids[j]
                loc_a = city_bins[id_a]["location"]
                loc_b = city_bins[id_b]["location"]
                dist  = distance(loc_a, loc_b)
                graph[id_a].append((id_b, dist))

    # Sort each bin's neighbour list by distance — nearest first
    # This makes the greedy step faster — just pick the first valid one
    for bin_id in graph:
        graph[bin_id].sort(key=lambda x: x[1])

    return graph


# =============================================================
#  SECTION 4 — GREEDY ROUTE ALGORITHM
#
#  This is the core algorithm of Person 3's work.
#
#  How it works:
#    1. Start at the truck depot (0, 0)
#    2. Look at all urgent bins (70%+) that haven't been visited
#    3. Find the nearest one to current location
#    4. Drive there. Add it to the route. Mark as visited.
#    5. Repeat from the new location until:
#       - No more urgent bins, OR
#       - Truck is full (capacity reached)
#    6. Return the ordered route
#
#  Why is this "Greedy"?
#    Because at every step we make the locally best choice
#    (nearest bin) without looking ahead. We're greedy — we
#    take the best available option right now.
# =============================================================

def greedy_route(city_bins, graph, truck_start=TRUCK_START,
                 capacity=TRUCK_CAPACITY, threshold=COLLECTION_THRESHOLD):
    """
    Builds an optimised collection route using the Greedy algorithm.
    Always goes to the nearest urgent bin from current position.

    Args:
        city_bins    (dict):  The city from Person 1
        graph        (dict):  The city graph from build_graph()
        truck_start  (tuple): Starting location of the truck
        capacity     (int):   Max bins the truck can carry
        threshold    (int):   Minimum fill % to collect a bin

    Returns:
        tuple: (route, total_distance, bins_skipped)
            route          — ordered list of bin dicts the truck visits
            total_distance — total km driven
            bins_skipped   — number of bins below threshold (not collected)
    """

    # --- Setup ---
    current_location = truck_start
    visited          = set()      # bin IDs we've already collected
    route            = []         # the ordered list of stops
    total_distance   = 0.0

    # Find all bins that need collection (above threshold)
    bins_to_collect = {
        bin_id: city_bins[bin_id]
        for bin_id in city_bins
        if city_bins[bin_id]["fill_level"] >= threshold
    }

    bins_skipped = len(city_bins) - len(bins_to_collect)

    # --- Greedy loop ---
    while len(route) < capacity and bins_to_collect:

        nearest_bin  = None
        nearest_dist = float("inf")   # start with infinity

        # Look at every unvisited urgent bin
        for bin_id, bin_data in bins_to_collect.items():
            if bin_id in visited:
                continue

            bin_location = bin_data["location"]
            dist_to_bin  = distance(current_location, bin_location)

            # Is this bin closer than the current nearest?
            if dist_to_bin < nearest_dist:
                nearest_dist = dist_to_bin
                nearest_bin  = bin_data

        # If no bin found, we're done
        if nearest_bin is None:
            break

        # Drive to the nearest bin
        total_distance  += nearest_dist
        current_location = nearest_bin["location"]
        visited.add(nearest_bin["id"])
        route.append({
            "bin":      nearest_bin,
            "distance": round(nearest_dist, 2),
            "cumulative_distance": round(total_distance, 2),
        })

        # Remove from bins_to_collect so we don't visit again
        del bins_to_collect[nearest_bin["id"]]

    # Add return to depot distance
    return_dist     = distance(current_location, truck_start)
    total_distance += return_dist

    return route, round(total_distance, 2), bins_skipped


# =============================================================
#  SECTION 5 — CALCULATE FUEL SAVED
#  Compare our optimised route vs the old "visit all bins" method
# =============================================================

def calculate_fuel_saved(city_bins, optimised_distance, truck_start=TRUCK_START):
    """
    Calculates how much distance (and therefore fuel) was saved
    by using our system vs visiting all 30 bins blindly.

    Args:
        city_bins          (dict):  The city
        optimised_distance (float): Distance our route covers
        truck_start        (tuple): Depot location

    Returns:
        dict: old_distance, saved_distance, percentage_saved
    """

    # Simulate the "dumb" route — visits all bins in order, no optimization
    old_distance   = 0.0
    prev_location  = truck_start

    for bin_id in city_bins:
        loc          = city_bins[bin_id]["location"]
        old_distance += distance(prev_location, loc)
        prev_location = loc

    # Return to depot
    old_distance += distance(prev_location, truck_start)
    old_distance  = round(old_distance, 2)

    saved      = round(old_distance - optimised_distance, 2)
    percentage = round((saved / old_distance) * 100, 1) if old_distance > 0 else 0

    return {
        "old_distance":    old_distance,
        "saved_distance":  saved,
        "percentage_saved": percentage,
    }


# =============================================================
#  SECTION 6 — PRINT THE ROUTE
#  Clean, readable output of the truck's planned route
# =============================================================

def print_route(route, total_distance, bins_skipped, fuel_data, truck_start=TRUCK_START):
    """
    Prints the truck's route in a clean, readable format.
    Shows each stop, distance driven, and bin details.

    Args:
        route          (list):  Ordered stops from greedy_route()
        total_distance (float): Total km driven
        bins_skipped   (int):   Bins not collected (below threshold)
        fuel_data      (dict):  From calculate_fuel_saved()
        truck_start    (tuple): Depot location
    """

    print(f"\n  {'=' * 54}")
    print(f"  🚛  TRUCK ROUTE — OPTIMISED COLLECTION PLAN")
    print(f"  {'=' * 54}")
    print(f"  Depot start: {truck_start}")
    print(f"  Capacity:    {TRUCK_CAPACITY} bins per trip")
    print(f"  Threshold:   Collecting bins at {COLLECTION_THRESHOLD}%+")
    print(f"  {'=' * 54}\n")

    if not route:
        print("  ✅  No bins need collection right now.")
        print("  All bins are below the collection threshold.")
        return

    print(f"  {'STOP':<5} {'BIN':<6} {'ZONE':<14} {'FILL':>5}  "
          f"{'DIST':>7}  {'CUMULATIVE':>10}  STATUS")
    print("  " + "-" * 62)

    for i, stop in enumerate(route, 1):
        b    = stop["bin"]
        dist = stop["distance"]
        cum  = stop["cumulative_distance"]

        if b["fill_level"] >= THRESHOLD_CRITICAL:
            status = "🔴 CRITICAL"
        else:
            status = "🟡 URGENT"

        print(f"  {i:<5} {b['id']:<6} {b['zone']:<14} "
              f"{b['fill_level']:>4}%  "
              f"{dist:>6} km  {cum:>9} km  {status}")

    print("  " + "-" * 62)
    print(f"  Return to depot: +{distance(route[-1]['bin']['location'], truck_start)} km")
    print(f"\n  {'TRIP SUMMARY':}")
    print(f"  {'─' * 40}")
    print(f"  Bins collected       : {len(route)}")
    print(f"  Bins skipped (empty) : {bins_skipped}")
    print(f"  Total distance       : {total_distance} km")
    print(f"  {'─' * 40}")
    print(f"  Old route (all bins) : {fuel_data['old_distance']} km")
    print(f"  Distance saved       : {fuel_data['saved_distance']} km")
    print(f"  Fuel saving          : {fuel_data['percentage_saved']}%")
    print(f"  {'─' * 40}")

    # Estimate litres saved (average truck = 0.35 litres per km)
    litres_saved = round(fuel_data["saved_distance"] * 0.35, 1)
    print(f"  Est. fuel saved      : ~{litres_saved} litres")
    print(f"  {'=' * 54}")


# =============================================================
#  SECTION 7 — FULL DISPATCH
#  Master function that ties everything together.
#  Called by main.py and used by Person 4 for the display.
# =============================================================

def dispatch_truck(city_bins):
    """
    Full end-to-end dispatch:
      1. Builds the graph
      2. Runs the greedy router
      3. Empties collected bins in the city data
      4. Calculates fuel savings
      5. Prints the route
      6. Returns everything for Person 4

    Args:
        city_bins (dict): Current city state

    Returns:
        tuple: (route, total_distance, bins_skipped, fuel_data, city_bins)
    """

    graph = build_graph(city_bins)

    route, total_distance, bins_skipped = greedy_route(
        city_bins, graph
    )

    fuel_data = calculate_fuel_saved(city_bins, total_distance)

    print_route(route, total_distance, bins_skipped, fuel_data)

    # Empty the bins the truck visited
    for stop in route:
        bin_id    = stop["bin"]["id"]
        city_bins = empty_bin(city_bins, bin_id)

    return route, total_distance, bins_skipped, fuel_data, city_bins


# =============================================================
#  SECTION 8 — TEST
#  Run this file directly to check everything works.
#  In VS Code terminal: python router.py
# =============================================================

if __name__ == "__main__":

    print("=" * 56)
    print("  GREEN LOOP — Router Module Test")
    print("=" * 56)

    # --- Setup ---
    print("\n  Creating city and simulating 5 hours...")
    city  = create_city()
    for _ in range(5):
        city = simulate_one_hour(city)
    print("  Done.\n")

    # --- Test 1: Show city state before routing ---
    print("[TEST 1] City status before dispatch:")
    print_full_status_board(city)

    # --- Test 2: Build the graph ---
    print("\n[TEST 2] Building city graph...")
    graph = build_graph(city)
    print(f"  Graph built. {len(graph)} nodes (bins).")
    print(f"  Sample — B001's 5 nearest neighbours:")
    for neighbour_id, dist in graph["B001"][:5]:
        print(f"    → {neighbour_id} at {dist} km")

    # --- Test 3: Run greedy route ---
    print("\n[TEST 3] Running greedy route algorithm...")
    route, total_dist, skipped = greedy_route(city, graph)
    print(f"  Route generated. {len(route)} stops planned.")

    # --- Test 4: Full dispatch with printed route ---
    print("\n[TEST 4] Full truck dispatch:")
    route, total_dist, skipped, fuel_data, city = dispatch_truck(city)

    # --- Test 5: City state after truck collected bins ---
    print("\n[TEST 5] City status AFTER truck collected bins:")
    print_full_status_board(city)

    # --- Test 6: Simulate 3 more hours — bins fill up again ---
    print("\n[TEST 6] Simulating 3 more hours — bins filling again...")
    for _ in range(3):
        city = simulate_one_hour(city)

    print("\n  City status after 3 more hours:")
    print_full_status_board(city)

    print("\n[TEST 7] Second dispatch — new route after bins refill:")
    route, total_dist, skipped, fuel_data, city = dispatch_truck(city)

    print("\n" + "=" * 56)
    print("  All tests passed. router.py is ready.")
    print("  dispatch_truck() is ready for Person 4 (display).")
    print("=" * 56)




display.py

# =============================================================
#  GREEN LOOP — display.py
#  Person 4's file
#
#  What this file does:
#    1. Draws an ASCII map of the city grid with all 30 bins
#    2. Animates the truck moving through its route stop by stop
#    3. Prints a live hourly monitoring dashboard
#    4. Prints the final trip report with all statistics
#    5. Shows a before vs after comparison of the city
#
#  DSA used here:
#    Uses all three — Hash Table (city lookup), Heap (status
#    checks), Graph + Greedy (route display)
#    Person 4 is the layer that makes everything VISIBLE.
#
#  Depends on: city.py, alerts.py, router.py
# =============================================================

import time
import os
from city import (
    create_city,
    simulate_one_hour,
    THRESHOLD_URGENT,
    THRESHOLD_CRITICAL,
)
from alerts import (
    get_status,
    print_full_status_board,
    scan_and_alert,
    STATUS_CRITICAL,
    STATUS_URGENT,
    STATUS_NORMAL,
    STATUS_EMPTY,
)
from router import (
    dispatch_truck,
    build_graph,
    greedy_route,
    calculate_fuel_saved,
    TRUCK_START,
    TRUCK_CAPACITY,
)


# =============================================================
#  SECTION 1 — CONSTANTS AND SYMBOLS
# =============================================================

# Grid size — our city is an 11x11 grid (coordinates 0 to 10)
GRID_SIZE = 11

# Symbols used on the ASCII map
SYMBOL_EMPTY    = "░"   # bin is fine, below 30%
SYMBOL_NORMAL   = "▒"   # bin is normal, 31-69%
SYMBOL_URGENT   = "▓"   # bin needs collection soon, 70-84%
SYMBOL_CRITICAL = "█"   # bin is critical, 85%+
SYMBOL_TRUCK    = "🚛"  # truck's current position
SYMBOL_DEPOT    = "🏭"  # truck depot
SYMBOL_VISITED  = "✓"   # bin already collected this trip
SYMBOL_EMPTY_CELL = "·" # nothing at this grid cell


# =============================================================
#  SECTION 2 — CLEAR SCREEN
#  Clears the terminal for clean animation
# =============================================================

def clear_screen():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


# =============================================================
#  SECTION 3 — DRAW THE ASCII CITY MAP
#
#  Draws an 11x11 grid. Each cell is either:
#    - A bin symbol (showing its fill status)
#    - The truck position
#    - The depot
#    - Empty space
#
#  The map is the visual centrepiece of the demo.
# =============================================================

def draw_map(city_bins, truck_location=TRUCK_START,
             visited_bins=None, route=None):
    """
    Draws the ASCII city map showing all bins, truck, and depot.

    Args:
        city_bins     (dict): Current city state
        truck_location(tuple): Where the truck is right now (x, y)
        visited_bins  (set):  Bin IDs already collected this trip
        route         (list): Planned route stops (to show path)
    """

    if visited_bins is None:
        visited_bins = set()

    # Build a lookup: (x, y) → bin data
    # So we can quickly find what's at each grid cell
    location_to_bin = {}
    for bin_id in city_bins:
        loc = city_bins[bin_id]["location"]
        location_to_bin[loc] = city_bins[bin_id]

    # Build a set of route locations for path display
    route_locations = set()
    if route:
        for stop in route:
            route_locations.add(stop["bin"]["location"])

    print("\n  " + "─" * 50)
    print("  📍  GREEN LOOP — CITY MAP")
    print("  " + "─" * 50)

    # Print column numbers across the top
    print("     ", end="")
    for x in range(GRID_SIZE):
        print(f" {x} ", end="")
    print()
    print("     " + "───" * GRID_SIZE)

    # Print each row of the grid (top to bottom, y goes 10 down to 0)
    for y in range(GRID_SIZE - 1, -1, -1):
        print(f"  {y:2} │", end="")   # row number on left

        for x in range(GRID_SIZE):
            cell = (x, y)

            if cell == TRUCK_START and cell == truck_location:
                # Truck is at depot
                print(" D ", end="")

            elif cell == truck_location:
                # Truck is here
                print(" T ", end="")

            elif cell == TRUCK_START:
                # Depot (truck not here)
                print(" D ", end="")

            elif cell in location_to_bin:
                bin_data = location_to_bin[cell]
                bin_id   = bin_data["id"]
                fill     = bin_data["fill_level"]

                if bin_id in visited_bins:
                    print(" ✓ ", end="")   # already collected
                else:
                    status = get_status(fill)
                    if status == STATUS_CRITICAL:
                        print(" █ ", end="")
                    elif status == STATUS_URGENT:
                        print(" ▓ ", end="")
                    elif status == STATUS_NORMAL:
                        print(" ▒ ", end="")
                    else:
                        print(" ░ ", end="")
            else:
                print(" · ", end="")   # empty cell

        print()   # newline after each row

    print("     " + "───" * GRID_SIZE)

    # Legend
    print()
    print("  LEGEND:")
    print("  D = Depot (truck start)    T = Truck location")
    print("  █ = CRITICAL (85%+)        ▓ = URGENT (70-84%)")
    print("  ▒ = Normal (31-69%)        ░ = Empty (0-30%)")
    print("  ✓ = Collected this trip")
    print("  " + "─" * 50)


# =============================================================
#  SECTION 4 — PRINT BIN DETAILS NEXT TO MAP
#  Shows a quick summary panel beside the map for the demo
# =============================================================

def print_bin_panel(city_bins):
    """
    Prints a compact two-column panel of all 30 bins
    sorted by fill level.

    Args:
        city_bins (dict): Current city state
    """

    sorted_bins = sorted(
        city_bins.values(),
        key=lambda b: b["fill_level"],
        reverse=True
    )

    print("\n  " + "─" * 50)
    print("  📊  BIN STATUS PANEL — ALL 30 BINS")
    print("  " + "─" * 50)
    print(f"  {'BIN':<6} {'FILL':>5}  {'BAR':<12}  {'STATUS'}")
    print("  " + "─" * 50)

    for b in sorted_bins:
        fill   = b["fill_level"]
        status = get_status(fill)
        bar    = "█" * (fill // 10)

        if status == STATUS_CRITICAL:
            label = "🔴 CRITICAL"
        elif status == STATUS_URGENT:
            label = "🟡 URGENT"
        elif status == STATUS_NORMAL:
            label = "🔵 Normal"
        else:
            label = "🟢 Empty"

        print(f"  {b['id']:<6} {fill:>4}%  {bar:<12}  {label}")

    print("  " + "─" * 50)


# =============================================================
#  SECTION 5 — ANIMATE THE TRUCK ROUTE
#  Shows the truck moving stop by stop through the route.
#  This is the demo showpiece.
# =============================================================

def animate_route(city_bins, route, delay=1.5):
    """
    Animates the truck moving through its route.
    Each stop: redraws the map with truck at new location,
    prints what the truck is doing, waits, then moves on.

    Args:
        city_bins (dict): Current city state
        route     (list): Ordered stops from router
        delay     (float): Seconds to wait between stops
    """

    visited = set()
    truck_location = TRUCK_START

    print("\n  🚛  TRUCK DISPATCH STARTING...")
    print(f"  Truck leaving depot at {TRUCK_START}")
    time.sleep(delay)

    # Show starting map
    clear_screen()
    print("\n  " + "=" * 50)
    print("  🚛  GREEN LOOP — LIVE TRUCK DISPATCH")
    print("  " + "=" * 50)
    draw_map(city_bins, truck_location=TRUCK_START, visited_bins=visited)
    print(f"\n  🏭  Truck at DEPOT {TRUCK_START} — ready to dispatch")
    time.sleep(delay)

    # Move through each stop
    for i, stop in enumerate(route, 1):
        b    = stop["bin"]
        dist = stop["distance"]
        cum  = stop["cumulative_distance"]

        truck_location = b["location"]
        visited.add(b["id"])

        clear_screen()
        print("\n  " + "=" * 50)
        print("  🚛  GREEN LOOP — LIVE TRUCK DISPATCH")
        print("  " + "=" * 50)

        draw_map(city_bins, truck_location=truck_location,
                 visited_bins=visited, route=route)

        print(f"\n  STOP {i} of {len(route)}")
        print(f"  {'─' * 40}")

        if b["fill_level"] >= THRESHOLD_CRITICAL:
            print(f"  🔴 CRITICAL BIN COLLECTED")
        else:
            print(f"  🟡 URGENT BIN COLLECTED")

        print(f"  Bin:      {b['id']} ({b['zone']})")
        print(f"  Location: {b['location']}")
        print(f"  Fill:     {b['fill_level']}% → 0% after collection")
        print(f"  Distance: {dist} km this leg")
        print(f"  Total so far: {cum} km")
        print(f"  {'─' * 40}")
        print(f"  Bins collected: {i} / {len(route)}")
        print(f"  Remaining stops: {len(route) - i}")

        time.sleep(delay)

    # Return to depot
    clear_screen()
    print("\n  " + "=" * 50)
    print("  🚛  GREEN LOOP — LIVE TRUCK DISPATCH")
    print("  " + "=" * 50)
    draw_map(city_bins, truck_location=TRUCK_START,
             visited_bins=visited, route=route)
    print(f"\n  🏭  Truck returned to DEPOT")
    print(f"  ✅  Trip complete. {len(route)} bins collected.")
    time.sleep(delay)


# =============================================================
#  SECTION 6 — LIVE MONITORING DASHBOARD
#  Shows the city state changing hour by hour
# =============================================================

def live_dashboard(city_bins, hours=6, delay=1.5):
    """
    Shows the city map updating hour by hour as bins fill up.
    Fires visual alerts when bins go critical.

    Args:
        city_bins (dict): Starting city state
        hours     (int):  How many hours to show
        delay     (float): Seconds between hours

    Returns:
        dict: Final city state
    """

    for hour in range(1, hours + 1):
        city_bins = simulate_one_hour(city_bins)

        clear_screen()
        print("\n  " + "=" * 50)
        print(f"  ⏰  GREEN LOOP — LIVE MONITORING  |  HOUR {hour}")
        print("  " + "=" * 50)

        draw_map(city_bins)

        # Count statuses
        counts = {s: 0 for s in
                  [STATUS_EMPTY, STATUS_NORMAL, STATUS_URGENT, STATUS_CRITICAL]}
        for b in city_bins.values():
            counts[get_status(b["fill_level"])] += 1

        print(f"\n  Hour {hour} summary:")
        print(f"  🟢 Empty: {counts[STATUS_EMPTY]}  "
              f"🔵 Normal: {counts[STATUS_NORMAL]}  "
              f"🟡 Urgent: {counts[STATUS_URGENT]}  "
              f"🔴 Critical: {counts[STATUS_CRITICAL]}")

        # Fire alerts if needed
        from alerts import get_bins_above
        critical = get_bins_above(city_bins, THRESHOLD_CRITICAL)
        if critical:
            print(f"\n  {'⚠' * 20}")
            print(f"  EMERGENCY — {len(critical)} CRITICAL BIN(S):")
            for b in sorted(critical,
                            key=lambda x: x["fill_level"], reverse=True):
                print(f"    🔴 {b['id']} ({b['zone']}) at {b['fill_level']}%")
            print(f"  {'⚠' * 20}")

        time.sleep(delay)

    return city_bins


# =============================================================
#  SECTION 7 — FINAL TRIP REPORT
#  Printed after every dispatch. The summary card.
# =============================================================

def print_trip_report(route, total_distance, bins_skipped,
                      fuel_data, hour, trip_number):
    """
    Prints a clean, full trip report after a dispatch.

    Args:
        route          (list):  The route taken
        total_distance (float): Total km driven
        bins_skipped   (int):   Bins not collected
        fuel_data      (dict):  Savings data
        hour           (int):   What hour this dispatch happened
        trip_number    (int):   Which trip number this is
    """

    print("\n  " + "=" * 54)
    print(f"  📋  TRIP REPORT — DISPATCH #{trip_number}  |  HOUR {hour}")
    print("  " + "=" * 54)

    if not route:
        print("  No bins needed collection this trip.")
        print("  " + "=" * 54)
        return

    print(f"\n  ROUTE TAKEN:")
    print(f"  {'─' * 44}")
    print(f"  Start → DEPOT {TRUCK_START}")
    for i, stop in enumerate(route, 1):
        b = stop["bin"]
        flag = "🔴" if b["fill_level"] >= THRESHOLD_CRITICAL else "🟡"
        print(f"  Stop {i:<2} → {b['id']} ({b['zone']:<12}) "
              f"{b['fill_level']:>3}% {flag}  +{stop['distance']} km")
    print(f"  End   → DEPOT {TRUCK_START}")

    print(f"\n  STATISTICS:")
    print(f"  {'─' * 44}")
    print(f"  Trip number          : #{trip_number}")
    print(f"  Dispatched at hour   : {hour}")
    print(f"  Bins collected       : {len(route)}")
    print(f"  Bins skipped         : {bins_skipped} (below threshold)")
    print(f"  Total distance       : {total_distance} km")
    print(f"  {'─' * 44}")
    print(f"  SAVINGS vs old system:")
    print(f"  Old route distance   : {fuel_data['old_distance']} km")
    print(f"  Distance saved       : {fuel_data['saved_distance']} km")
    print(f"  Fuel saving          : {fuel_data['percentage_saved']}%")
    litres = round(fuel_data["saved_distance"] * 0.35, 1)
    co2    = round(fuel_data["saved_distance"] * 0.35 * 2.68, 1)
    print(f"  Est. fuel saved      : ~{litres} litres")
    print(f"  Est. CO₂ avoided     : ~{co2} kg")
    print("  " + "=" * 54)


# =============================================================
#  SECTION 8 — BEFORE VS AFTER COMPARISON
#  Shows the city map before and after truck collection
# =============================================================

def before_after(city_before, city_after):
    """
    Prints a side-by-side before and after bin status comparison.

    Args:
        city_before (dict): City state before dispatch
        city_after  (dict): City state after dispatch
    """

    print("\n  " + "=" * 60)
    print("  🔄  BEFORE vs AFTER — BIN STATUS COMPARISON")
    print("  " + "=" * 60)
    print(f"  {'BIN':<6} {'BEFORE':>8}  {'AFTER':>8}  CHANGE")
    print("  " + "─" * 50)

    for bin_id in city_before:
        before_fill = city_before[bin_id]["fill_level"]
        after_fill  = city_after[bin_id]["fill_level"]
        change      = after_fill - before_fill

        if change < 0:
            change_str = f"↓ {abs(change)}%  ✅ collected"
        elif change == 0:
            change_str = f"→ no change"
        else:
            change_str = f"↑ {change}%"

        print(f"  {bin_id:<6} {before_fill:>7}%  {after_fill:>7}%  {change_str}")

    print("  " + "=" * 60)


# =============================================================
#  SECTION 9 — TEST
#  Run this file directly to see the full visual demo.
#  In VS Code terminal: python display.py
#
#  NOTE: This test uses time.sleep() for animation.
#        Set FAST_MODE = True below to skip delays.
# =============================================================

FAST_MODE = False   # ← Set to False for full animated demo
                    #   Set to True for instant output (testing)

if __name__ == "__main__":

    DELAY = 0 if FAST_MODE else 1.5   # seconds between frames

    print("=" * 56)
    print("  GREEN LOOP — Display Module Test")
    if FAST_MODE:
        print("  Running in FAST MODE (no animation delays)")
    else:
        print("  Running in ANIMATED MODE (1.5s delays)")
    print("=" * 56)

    # --- Setup ---
    print("\n  Creating city...")
    city = create_city()
    print("  30 bins created.\n")

    # --- Test 1: Draw initial map ---
    print("[TEST 1] City map at start:")
    draw_map(city)

    # --- Test 2: Bin status panel ---
    print("\n[TEST 2] Bin status panel — all 30 bins:")
    print_bin_panel(city)

    # --- Test 3: Live monitoring for 5 hours ---
    print("\n[TEST 3] Live dashboard — 5 hours of monitoring:")
    if FAST_MODE:
        # In fast mode just simulate and show final state
        for _ in range(5):
            city = simulate_one_hour(city)
        print("  (5 hours simulated)")
        draw_map(city)
        print_bin_panel(city)
    else:
        city = live_dashboard(city, hours=5, delay=DELAY)

    # --- Test 4: Save city state before dispatch ---
    import copy
    city_before = copy.deepcopy(city)

    # --- Test 5: Dispatch and animate ---
    print("\n[TEST 4] Running alert scan before dispatch:")
    urgent_heap, critical_list = scan_and_alert(city)

    print("\n[TEST 5] Dispatching truck and animating route:")
    graph = build_graph(city)
    route, total_dist, skipped = greedy_route(city, graph)

    if FAST_MODE:
        # Just show the map with route planned
        draw_map(city, visited_bins=set(), route=route)
        print(f"\n  Route planned: {len(route)} stops")
        for i, stop in enumerate(route, 1):
            b = stop["bin"]
            print(f"  Stop {i}: {b['id']} ({b['zone']}) at {b['fill_level']}%")
    else:
        animate_route(city, route, delay=DELAY)

    # Actually dispatch (empties bins)
    route, total_dist, skipped, fuel_data, city = dispatch_truck(city)

    # --- Test 6: Trip report ---
    print("\n[TEST 6] Trip report:")
    print_trip_report(route, total_dist, skipped, fuel_data,
                      hour=5, trip_number=1)

    # --- Test 7: Before vs after ---
    print("\n[TEST 7] Before vs after comparison:")
    before_after(city_before, city)

    # --- Test 8: Map after collection ---
    print("\n[TEST 8] City map AFTER truck collected bins:")
    draw_map(city)

    # --- Test 9: Simulate more hours and second dispatch ---
    print("\n[TEST 9] Simulating 4 more hours and running second dispatch...")
    for _ in range(4):
        city = simulate_one_hour(city)

    city_before_2 = copy.deepcopy(city)
    route2, total_dist2, skipped2, fuel_data2, city = dispatch_truck(city)
    print_trip_report(route2, total_dist2, skipped2, fuel_data2,
                      hour=9, trip_number=2)

    print("\n[TEST 10] Final city map after second dispatch:")
    draw_map(city)

    print("\n" + "=" * 56)
    print("  All tests passed. display.py is ready.")
    print("  Set FAST_MODE = False for the animated demo.")
    print("=" * 56)










main.py


# =============================================================
#  GREEN LOOP — display.py
#  Person 4's file
#
#  What this file does:
#    1. Draws an ASCII map of the city grid with all 30 bins
#    2. Animates the truck moving through its route stop by stop
#    3. Prints a live hourly monitoring dashboard
#    4. Prints the final trip report with all statistics
#    5. Shows a before vs after comparison of the city
#
#  DSA used here:
#    Uses all three — Hash Table (city lookup), Heap (status
#    checks), Graph + Greedy (route display)
#    Person 4 is the layer that makes everything VISIBLE.
#
#  Depends on: city.py, alerts.py, router.py
# =============================================================

import time
import os
from city import (
    create_city,
    simulate_one_hour,
    THRESHOLD_URGENT,
    THRESHOLD_CRITICAL,
)
from alerts import (
    get_status,
    print_full_status_board,
    scan_and_alert,
    STATUS_CRITICAL,
    STATUS_URGENT,
    STATUS_NORMAL,
    STATUS_EMPTY,
)
from router import (
    dispatch_truck,
    build_graph,
    greedy_route,
    calculate_fuel_saved,
    TRUCK_START,
    TRUCK_CAPACITY,
)


# =============================================================
#  SECTION 1 — CONSTANTS AND SYMBOLS
# =============================================================

# Grid size — our city is an 11x11 grid (coordinates 0 to 10)
GRID_SIZE = 11

# Symbols used on the ASCII map
SYMBOL_EMPTY    = "░"   # bin is fine, below 30%
SYMBOL_NORMAL   = "▒"   # bin is normal, 31-69%
SYMBOL_URGENT   = "▓"   # bin needs collection soon, 70-84%
SYMBOL_CRITICAL = "█"   # bin is critical, 85%+
SYMBOL_TRUCK    = "🚛"  # truck's current position
SYMBOL_DEPOT    = "🏭"  # truck depot
SYMBOL_VISITED  = "✓"   # bin already collected this trip
SYMBOL_EMPTY_CELL = "·" # nothing at this grid cell


# =============================================================
#  SECTION 2 — CLEAR SCREEN
#  Clears the terminal for clean animation
# =============================================================

def clear_screen():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


# =============================================================
#  SECTION 3 — DRAW THE ASCII CITY MAP
#
#  Draws an 11x11 grid. Each cell is either:
#    - A bin symbol (showing its fill status)
#    - The truck position
#    - The depot
#    - Empty space
#
#  The map is the visual centrepiece of the demo.
# =============================================================

def draw_map(city_bins, truck_location=TRUCK_START,
             visited_bins=None, route=None):
    """
    Draws the ASCII city map showing all bins, truck, and depot.

    Args:
        city_bins     (dict): Current city state
        truck_location(tuple): Where the truck is right now (x, y)
        visited_bins  (set):  Bin IDs already collected this trip
        route         (list): Planned route stops (to show path)
    """

    if visited_bins is None:
        visited_bins = set()

    # Build a lookup: (x, y) → bin data
    # So we can quickly find what's at each grid cell
    location_to_bin = {}
    for bin_id in city_bins:
        loc = city_bins[bin_id]["location"]
        location_to_bin[loc] = city_bins[bin_id]

    # Build a set of route locations for path display
    route_locations = set()
    if route:
        for stop in route:
            route_locations.add(stop["bin"]["location"])

    print("\n  " + "─" * 50)
    print("  📍  GREEN LOOP — CITY MAP")
    print("  " + "─" * 50)

    # Print column numbers across the top
    print("     ", end="")
    for x in range(GRID_SIZE):
        print(f" {x} ", end="")
    print()
    print("     " + "───" * GRID_SIZE)

    # Print each row of the grid (top to bottom, y goes 10 down to 0)
    for y in range(GRID_SIZE - 1, -1, -1):
        print(f"  {y:2} │", end="")   # row number on left

        for x in range(GRID_SIZE):
            cell = (x, y)

            if cell == TRUCK_START and cell == truck_location:
                # Truck is at depot
                print(" D ", end="")

            elif cell == truck_location:
                # Truck is here
                print(" T ", end="")

            elif cell == TRUCK_START:
                # Depot (truck not here)
                print(" D ", end="")

            elif cell in location_to_bin:
                bin_data = location_to_bin[cell]
                bin_id   = bin_data["id"]
                fill     = bin_data["fill_level"]

                if bin_id in visited_bins:
                    print(" ✓ ", end="")   # already collected
                else:
                    status = get_status(fill)
                    if status == STATUS_CRITICAL:
                        print(" █ ", end="")
                    elif status == STATUS_URGENT:
                        print(" ▓ ", end="")
                    elif status == STATUS_NORMAL:
                        print(" ▒ ", end="")
                    else:
                        print(" ░ ", end="")
            else:
                print(" · ", end="")   # empty cell

        print()   # newline after each row

    print("     " + "───" * GRID_SIZE)

    # Legend
    print()
    print("  LEGEND:")
    print("  D = Depot (truck start)    T = Truck location")
    print("  █ = CRITICAL (85%+)        ▓ = URGENT (70-84%)")
    print("  ▒ = Normal (31-69%)        ░ = Empty (0-30%)")
    print("  ✓ = Collected this trip")
    print("  " + "─" * 50)


# =============================================================
#  SECTION 4 — PRINT BIN DETAILS NEXT TO MAP
#  Shows a quick summary panel beside the map for the demo
# =============================================================

def print_bin_panel(city_bins):
    """
    Prints a compact two-column panel of all 30 bins
    sorted by fill level.

    Args:
        city_bins (dict): Current city state
    """

    sorted_bins = sorted(
        city_bins.values(),
        key=lambda b: b["fill_level"],
        reverse=True
    )

    print("\n  " + "─" * 50)
    print("  📊  BIN STATUS PANEL — ALL 30 BINS")
    print("  " + "─" * 50)
    print(f"  {'BIN':<6} {'FILL':>5}  {'BAR':<12}  {'STATUS'}")
    print("  " + "─" * 50)

    for b in sorted_bins:
        fill   = b["fill_level"]
        status = get_status(fill)
        bar    = "█" * (fill // 10)

        if status == STATUS_CRITICAL:
            label = "🔴 CRITICAL"
        elif status == STATUS_URGENT:
            label = "🟡 URGENT"
        elif status == STATUS_NORMAL:
            label = "🔵 Normal"
        else:
            label = "🟢 Empty"

        print(f"  {b['id']:<6} {fill:>4}%  {bar:<12}  {label}")

    print("  " + "─" * 50)


# =============================================================
#  SECTION 5 — ANIMATE THE TRUCK ROUTE
#  Shows the truck moving stop by stop through the route.
#  This is the demo showpiece.
# =============================================================

def animate_route(city_bins, route, delay=1.5):
    """
    Animates the truck moving through its route.
    Each stop: redraws the map with truck at new location,
    prints what the truck is doing, waits, then moves on.

    Args:
        city_bins (dict): Current city state
        route     (list): Ordered stops from router
        delay     (float): Seconds to wait between stops
    """

    visited = set()
    truck_location = TRUCK_START

    print("\n  🚛  TRUCK DISPATCH STARTING...")
    print(f"  Truck leaving depot at {TRUCK_START}")
    time.sleep(delay)

    # Show starting map
    clear_screen()
    print("\n  " + "=" * 50)
    print("  🚛  GREEN LOOP — LIVE TRUCK DISPATCH")
    print("  " + "=" * 50)
    draw_map(city_bins, truck_location=TRUCK_START, visited_bins=visited)
    print(f"\n  🏭  Truck at DEPOT {TRUCK_START} — ready to dispatch")
    time.sleep(delay)

    # Move through each stop
    for i, stop in enumerate(route, 1):
        b    = stop["bin"]
        dist = stop["distance"]
        cum  = stop["cumulative_distance"]

        truck_location = b["location"]
        visited.add(b["id"])

        clear_screen()
        print("\n  " + "=" * 50)
        print("  🚛  GREEN LOOP — LIVE TRUCK DISPATCH")
        print("  " + "=" * 50)

        draw_map(city_bins, truck_location=truck_location,
                 visited_bins=visited, route=route)

        print(f"\n  STOP {i} of {len(route)}")
        print(f"  {'─' * 40}")

        if b["fill_level"] >= THRESHOLD_CRITICAL:
            print(f"  🔴 CRITICAL BIN COLLECTED")
        else:
            print(f"  🟡 URGENT BIN COLLECTED")

        print(f"  Bin:      {b['id']} ({b['zone']})")
        print(f"  Location: {b['location']}")
        print(f"  Fill:     {b['fill_level']}% → 0% after collection")
        print(f"  Distance: {dist} km this leg")
        print(f"  Total so far: {cum} km")
        print(f"  {'─' * 40}")
        print(f"  Bins collected: {i} / {len(route)}")
        print(f"  Remaining stops: {len(route) - i}")

        time.sleep(delay)

    # Return to depot
    clear_screen()
    print("\n  " + "=" * 50)
    print("  🚛  GREEN LOOP — LIVE TRUCK DISPATCH")
    print("  " + "=" * 50)
    draw_map(city_bins, truck_location=TRUCK_START,
             visited_bins=visited, route=route)
    print(f"\n  🏭  Truck returned to DEPOT")
    print(f"  ✅  Trip complete. {len(route)} bins collected.")
    time.sleep(delay)


# =============================================================
#  SECTION 6 — LIVE MONITORING DASHBOARD
#  Shows the city state changing hour by hour
# =============================================================

def live_dashboard(city_bins, hours=6, delay=1.5):
    """
    Shows the city map updating hour by hour as bins fill up.
    Fires visual alerts when bins go critical.

    Args:
        city_bins (dict): Starting city state
        hours     (int):  How many hours to show
        delay     (float): Seconds between hours

    Returns:
        dict: Final city state
    """

    for hour in range(1, hours + 1):
        city_bins = simulate_one_hour(city_bins)

        clear_screen()
        print("\n  " + "=" * 50)
        print(f"  ⏰  GREEN LOOP — LIVE MONITORING  |  HOUR {hour}")
        print("  " + "=" * 50)

        draw_map(city_bins)

        # Count statuses
        counts = {s: 0 for s in
                  [STATUS_EMPTY, STATUS_NORMAL, STATUS_URGENT, STATUS_CRITICAL]}
        for b in city_bins.values():
            counts[get_status(b["fill_level"])] += 1

        print(f"\n  Hour {hour} summary:")
        print(f"  🟢 Empty: {counts[STATUS_EMPTY]}  "
              f"🔵 Normal: {counts[STATUS_NORMAL]}  "
              f"🟡 Urgent: {counts[STATUS_URGENT]}  "
              f"🔴 Critical: {counts[STATUS_CRITICAL]}")

        # Fire alerts if needed
        from alerts import get_bins_above
        critical = get_bins_above(city_bins, THRESHOLD_CRITICAL)
        if critical:
            print(f"\n  {'⚠' * 20}")
            print(f"  EMERGENCY — {len(critical)} CRITICAL BIN(S):")
            for b in sorted(critical,
                            key=lambda x: x["fill_level"], reverse=True):
                print(f"    🔴 {b['id']} ({b['zone']}) at {b['fill_level']}%")
            print(f"  {'⚠' * 20}")

        time.sleep(delay)

    return city_bins


# =============================================================
#  SECTION 7 — FINAL TRIP REPORT
#  Printed after every dispatch. The summary card.
# =============================================================

def print_trip_report(route, total_distance, bins_skipped,
                      fuel_data, hour, trip_number):
    """
    Prints a clean, full trip report after a dispatch.

    Args:
        route          (list):  The route taken
        total_distance (float): Total km driven
        bins_skipped   (int):   Bins not collected
        fuel_data      (dict):  Savings data
        hour           (int):   What hour this dispatch happened
        trip_number    (int):   Which trip number this is
    """

    print("\n  " + "=" * 54)
    print(f"  📋  TRIP REPORT — DISPATCH #{trip_number}  |  HOUR {hour}")
    print("  " + "=" * 54)

    if not route:
        print("  No bins needed collection this trip.")
        print("  " + "=" * 54)
        return

    print(f"\n  ROUTE TAKEN:")
    print(f"  {'─' * 44}")
    print(f"  Start → DEPOT {TRUCK_START}")
    for i, stop in enumerate(route, 1):
        b = stop["bin"]
        flag = "🔴" if b["fill_level"] >= THRESHOLD_CRITICAL else "🟡"
        print(f"  Stop {i:<2} → {b['id']} ({b['zone']:<12}) "
              f"{b['fill_level']:>3}% {flag}  +{stop['distance']} km")
    print(f"  End   → DEPOT {TRUCK_START}")

    print(f"\n  STATISTICS:")
    print(f"  {'─' * 44}")
    print(f"  Trip number          : #{trip_number}")
    print(f"  Dispatched at hour   : {hour}")
    print(f"  Bins collected       : {len(route)}")
    print(f"  Bins skipped         : {bins_skipped} (below threshold)")
    print(f"  Total distance       : {total_distance} km")
    print(f"  {'─' * 44}")
    print(f"  SAVINGS vs old system:")
    print(f"  Old route distance   : {fuel_data['old_distance']} km")
    print(f"  Distance saved       : {fuel_data['saved_distance']} km")
    print(f"  Fuel saving          : {fuel_data['percentage_saved']}%")
    litres = round(fuel_data["saved_distance"] * 0.35, 1)
    co2    = round(fuel_data["saved_distance"] * 0.35 * 2.68, 1)
    print(f"  Est. fuel saved      : ~{litres} litres")
    print(f"  Est. CO₂ avoided     : ~{co2} kg")
    print("  " + "=" * 54)


# =============================================================
#  SECTION 8 — BEFORE VS AFTER COMPARISON
#  Shows the city map before and after truck collection
# =============================================================

def before_after(city_before, city_after):
    """
    Prints a side-by-side before and after bin status comparison.

    Args:
        city_before (dict): City state before dispatch
        city_after  (dict): City state after dispatch
    """

    print("\n  " + "=" * 60)
    print("  🔄  BEFORE vs AFTER — BIN STATUS COMPARISON")
    print("  " + "=" * 60)
    print(f"  {'BIN':<6} {'BEFORE':>8}  {'AFTER':>8}  CHANGE")
    print("  " + "─" * 50)

    for bin_id in city_before:
        before_fill = city_before[bin_id]["fill_level"]
        after_fill  = city_after[bin_id]["fill_level"]
        change      = after_fill - before_fill

        if change < 0:
            change_str = f"↓ {abs(change)}%  ✅ collected"
        elif change == 0:
            change_str = f"→ no change"
        else:
            change_str = f"↑ {change}%"

        print(f"  {bin_id:<6} {before_fill:>7}%  {after_fill:>7}%  {change_str}")

    print("  " + "=" * 60)


# =============================================================
#  SECTION 9 — TEST
#  Run this file directly to see the full visual demo.
#  In VS Code terminal: python display.py
#
#  NOTE: This test uses time.sleep() for animation.
#        Set FAST_MODE = True below to skip delays.
# =============================================================

FAST_MODE = True   # ← Set to False for full animated demo
                    #   Set to True for instant output (testing)

if __name__ == "__main__":

    DELAY = 0 if FAST_MODE else 1.5   # seconds between frames

    print("=" * 56)
    print("  GREEN LOOP — Display Module Test")
    if FAST_MODE:
        print("  Running in FAST MODE (no animation delays)")
    else:
        print("  Running in ANIMATED MODE (1.5s delays)")
    print("=" * 56)

    # --- Setup ---
    print("\n  Creating city...")
    city = create_city()
    print("  30 bins created.\n")

    # --- Test 1: Draw initial map ---
    print("[TEST 1] City map at start:")
    draw_map(city)

    # --- Test 2: Bin status panel ---
    print("\n[TEST 2] Bin status panel — all 30 bins:")
    print_bin_panel(city)

    # --- Test 3: Live monitoring for 5 hours ---
    print("\n[TEST 3] Live dashboard — 5 hours of monitoring:")
    if FAST_MODE:
        # In fast mode just simulate and show final state
        for _ in range(5):
            city = simulate_one_hour(city)
        print("  (5 hours simulated)")
        draw_map(city)
        print_bin_panel(city)
    else:
        city = live_dashboard(city, hours=5, delay=DELAY)

    # --- Test 4: Save city state before dispatch ---
    import copy
    city_before = copy.deepcopy(city)

    # --- Test 5: Dispatch and animate ---
    print("\n[TEST 4] Running alert scan before dispatch:")
    urgent_heap, critical_list = scan_and_alert(city)

    print("\n[TEST 5] Dispatching truck and animating route:")
    graph = build_graph(city)
    route, total_dist, skipped = greedy_route(city, graph)

    if FAST_MODE:
        # Just show the map with route planned
        draw_map(city, visited_bins=set(), route=route)
        print(f"\n  Route planned: {len(route)} stops")
        for i, stop in enumerate(route, 1):
            b = stop["bin"]
            print(f"  Stop {i}: {b['id']} ({b['zone']}) at {b['fill_level']}%")
    else:
        animate_route(city, route, delay=DELAY)

    # Actually dispatch (empties bins)
    route, total_dist, skipped, fuel_data, city = dispatch_truck(city)

    # --- Test 6: Trip report ---
    print("\n[TEST 6] Trip report:")
    print_trip_report(route, total_dist, skipped, fuel_data,
                      hour=5, trip_number=1)

    # --- Test 7: Before vs after ---
    print("\n[TEST 7] Before vs after comparison:")
    before_after(city_before, city)

    # --- Test 8: Map after collection ---
    print("\n[TEST 8] City map AFTER truck collected bins:")
    draw_map(city)

    # --- Test 9: Simulate more hours and second dispatch ---
    print("\n[TEST 9] Simulating 4 more hours and running second dispatch...")
    for _ in range(4):
        city = simulate_one_hour(city)

    city_before_2 = copy.deepcopy(city)
    route2, total_dist2, skipped2, fuel_data2, city = dispatch_truck(city)
    print_trip_report(route2, total_dist2, skipped2, fuel_data2,
                      hour=9, trip_number=2)

    print("\n[TEST 10] Final city map after second dispatch:")
    draw_map(city)

    print("\n" + "=" * 56)
    print("  All tests passed. display.py is ready.")
    print("  Set FAST_MODE = False for the animated demo.")
    print("=" * 56)
