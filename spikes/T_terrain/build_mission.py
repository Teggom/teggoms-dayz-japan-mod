#!/usr/bin/env python3
r"""build_mission.py - (re)build the test mission japan_dev\mission\japantest.japantestisland\ from vanilla CE files plus
every drop-in under japan_dev\test\.

    python japan_dev\spikes\T_terrain\build_mission.py

Vanilla source: P:\DZ\worlds\chernarusplus\ce (the extracted game data). The server's own
mpmissions\dayzOffline.chernarusplus is byte-identical to it except where this server's mods were added (types,
events, event spawns, environment, economy core), so the extract is the clean vanilla copy. Nothing in mpmissions is
modified.

Merged on every run:
  test/types/*.xml               bare <type> elements  -> db/types.xml (same name replaces the vanilla entry)
  test/ce/*_mapgroupproto.xml    bare <group> elements -> mapgroupproto.xml
  test/ce/*_mapgrouppos.xml      bare <group> elements -> mapgrouppos.xml; a group sitting within 10 m of a building
                                 build_world.py baked into the wrp gets that object's exact engine position / yaw
  test/spawns/<X>.json           copied to spawns/, listed in cfggameplay.json objectSpawnersArr
  test/spawns/<X>_creatures.txt  "Class x z yaw" -> init.c (standing at ground height, no navmesh = no movement)
  test/items/*.txt               "Class [count]" -> init.c item grid: rows from (1000, 975), 1.5 m spacing, y 25.0
Infected, animal and vehicle spawning is off (economy.xml + every event inactive except Loot).
Leaves storage_* alone (delete it by hand to reset persistence). Never touches the server.
"""
import glob
import json
import math
import os
import re
import shutil
import struct
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.abspath(os.path.join(HERE, "..", ".."))
MISSION = os.path.join(DEV, "mission", "japantest.japantestisland")
TEST = os.path.join(DEV, "test")
VANILLA = r"P:\DZ\worlds\chernarusplus\ce"
VANILLA_MISSION = os.path.join(os.path.dirname(DEV), "mpmissions", "dayzOffline.chernarusplus")
WORLD = 2048

ITEM_ORIGIN = (1000.0, 975.0)
ITEM_STEP = 1.5
ITEMS_PER_ROW = 32          # x 1000 .. 1046.5; rows go south (z 975, 973.5, ...), clear of the weapon range (z <= 950)
SPAWN = (1024.0, 985.0)

LOG = []


def log(m):
    LOG.append(m)
    print(m, flush=True)


def wb(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text.encode("utf-8"))


def rd(path):
    with open(path, "rb") as f:
        return f.read().decode("utf-8", "replace")


def bare_elements(text, tag):
    """Every top-level <tag ...>...</tag> or <tag .../> element in a drop-in file (comments removed)."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out = []
    pat = re.compile(r"<%s\b[^>]*?/>|<%s\b[^>]*>.*?</%s>" % (tag, tag, tag), re.S)
    for m in pat.finditer(text):
        out.append(m.group(0))
    return out


def attr(el, name):
    m = re.search(r'\b%s="([^"]*)"' % name, el)
    return m.group(1) if m else None


# ------------------------------------------------------------------------------------------------------
TEST_LOOT_MAX = 40   # the island has ~3 loot buildings (~90 points); vanilla Chernarus nominals flood the
                     # respawner ("causing search overtime" x thousands, 2026-09-27 boot) - keep a small sample


def shrink_vanilla_loot(van):
    """Keep ~40 common Town/Village floor items at nominal 1 / min 1; every other vanilla type nominal 0 / min 0."""
    kept = [0]
    wanted = {"tools", "food", "clothes", "containers"}

    def fix(m):
        blk = m.group(0)
        nom = re.search(r"<nominal>(\d+)</nominal>", blk)
        if not nom or int(nom.group(1)) == 0:
            return blk
        cats = set(re.findall(r'<category name="([^"]+)"', blk))
        uses = set(re.findall(r'<usage name="([^"]+)"', blk))
        keep = kept[0] < TEST_LOOT_MAX and (cats & wanted) and (uses & {"Town", "Village"})
        n = 1 if keep else 0
        if keep:
            kept[0] += 1
        blk = re.sub(r"<nominal>\d+</nominal>", "<nominal>%d</nominal>" % n, blk, count=1)
        blk = re.sub(r"<min>\d+</min>", "<min>%d</min>" % n, blk, count=1)
        return blk

    van = re.sub(r'<type name="[^"]+">.*?</type>', fix, van, flags=re.S)
    log("types: vanilla loot shrunk to %d items at nominal 1 (TEST_LOOT_MAX)" % kept[0])
    return van


def build_types():
    van = shrink_vanilla_loot(rd(os.path.join(VANILLA, "db", "types.xml")))
    add = []
    for path in sorted(glob.glob(os.path.join(TEST, "types", "*.xml"))):
        els = bare_elements(rd(path), "type")
        log("types: %d from %s" % (len(els), os.path.basename(path)))
        add.extend(els)
    names = [attr(e, "name") for e in add]
    for n in names:
        pat = re.compile(r'\s*<type name="%s">.*?</type>' % re.escape(n), re.S)
        if pat.search(van):
            van = pat.sub("", van, count=1)
            log("  types: %s replaces the vanilla entry" % n)
    body = "".join("\n    " + e.strip() for e in add)
    van = van.replace("</types>", body + ("\n" if add else "") + "</types>")
    wb(os.path.join(MISSION, "db", "types.xml"), van)


def build_events():
    van = rd(os.path.join(VANILLA, "db", "events.xml"))

    def repl(m):
        block = m.group(0)
        name = attr(block, "name")
        if name == "Loot":
            return block
        return re.sub(r"<active>\s*1\s*</active>", "<active>0</active>", block)
    out = re.sub(r"<event name=\"[^\"]+\">.*?</event>", repl, van, flags=re.S)
    active = re.findall(r'<event name="([^"]+)">(?:(?!</event>).)*<active>1</active>', out, flags=re.S)
    log("events: every event inactive except %s" % active)
    wb(os.path.join(MISSION, "db", "events.xml"), out)


def build_economy():
    van = rd(os.path.join(VANILLA, "db", "economy.xml"))
    van = re.sub(r'<animals [^>]*/>', '<animals init="0" load="0" respawn="0" save="0"/>', van)
    van = re.sub(r'<zombies [^>]*/>', '<zombies init="0" load="0" respawn="0" save="0"/>', van)
    van = re.sub(r'<vehicles [^>]*/>', '<vehicles init="0" load="0" respawn="0" save="0"/>', van)
    wb(os.path.join(MISSION, "db", "economy.xml"), van)


def build_mapgroups(info):
    # prototypes
    van = rd(os.path.join(VANILLA, "mapgroupproto.xml"))
    add = []
    for path in sorted(glob.glob(os.path.join(TEST, "ce", "*_mapgroupproto.xml"))):
        els = bare_elements(rd(path), "group")
        log("mapgroupproto: %d groups from %s" % (len(els), os.path.basename(path)))
        add.extend(els)
    for e in add:
        n = attr(e, "name")
        pat = re.compile(r'\n\s*<group name="%s">.*?</group>' % re.escape(n), re.S)
        if pat.search(van):
            van = pat.sub("", van, count=1)
            log("  mapgroupproto: %s replaces the vanilla prototype" % n)
    idx = van.rfind("</prototype>")
    van = van[:idx] + "".join("\t\t" + e.strip() + "\n" for e in add) + van[idx:]
    wb(os.path.join(MISSION, "mapgroupproto.xml"), van)

    # positions: the control house + drop-ins, snapped to the exact wrp objects
    placed = info.get("placed", []) if info else []
    groups = []
    for path in sorted(glob.glob(os.path.join(TEST, "ce", "*_mapgrouppos.xml"))):
        els = bare_elements(rd(path), "group")
        log("mapgrouppos: %d groups from %s" % (len(els), os.path.basename(path)))
        for e in els:
            groups.append((os.path.basename(path), e))
    lines = []
    have = set()
    for src, e in groups:
        name = attr(e, "name")
        pos = [float(v) for v in (attr(e, "pos") or "0 0 0").split()]
        snap = None
        best = 10.0
        for o in placed:
            base = os.path.splitext(os.path.basename(o["p3d"].replace("\\", "/")))[0].lower()
            d = math.hypot(o["pos"][0] - pos[0], o["pos"][2] - pos[2])
            # SH1 (2026-10-01): the NEAREST object of the class (was: the last one within 10 m, which sent two of
            # three identical sheds 8 m apart to their neighbours' spots)
            if name and name.lower() == "land_" + base and d < best:
                snap, best = o, d
        if snap:
            yaw = snap["yaw"]
            new = '<group name="%s" pos="%.6f %.6f %.6f" rpy="0.000000 0.000000 %.6f" a="%.6f" />' % (
                name, snap["pos"][0], snap["pos"][1], snap["pos"][2], yaw, 90.0 - yaw)
            if abs(snap["pos"][1] - pos[1]) > 0.01 or math.hypot(snap["pos"][0] - pos[0], snap["pos"][2] - pos[2]) > 0.01:
                log("  mapgrouppos: %s from %s snapped to the wrp object: (%.3f %.3f %.3f) -> (%.3f %.3f %.3f)" % (
                    name, src, pos[0], pos[1], pos[2], snap["pos"][0], snap["pos"][1], snap["pos"][2]))
            else:
                log("  mapgrouppos: %s from %s matches its wrp object exactly (%.3f %.3f %.3f)" % (
                    name, src, snap["pos"][0], snap["pos"][1], snap["pos"][2]))
            lines.append(new)
            have.add(snap["p3d"].lower())
        else:
            lines.append(e.strip())
            log("  mapgrouppos: %s from %s kept as written (no wrp object of that class within 10 m - fine for runtime-spawned buildings)" % (name, src))
    house = info.get("house") if info else None
    if house:
        yaw = house["yaw"]
        lines.append('<group name="%s" pos="%.6f %.6f %.6f" rpy="0.000000 0.000000 %.6f" a="%.6f" />' % (
            house["class"], house["pos"][0], house["pos"][1], house["pos"][2], yaw, 90.0 - yaw))
        log("mapgrouppos: control house %s at (%.1f, %.2f, %.1f)" % (house["class"], house["pos"][0], house["pos"][1], house["pos"][2]))
    text = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n<map>\n' + "".join("    " + l + "\n" for l in lines) + "</map>\n"
    wb(os.path.join(MISSION, "mapgrouppos.xml"), text)


def build_areaflags():
    """2048 x 2048 cells of 1 m (512 x 512 crashed the server: INT_DIVIDE_BY_ZERO in CE InitOffline, 2026-09-27;
    every working map on this server uses 2048 or 4096 cells) (5-int header, uint32 usage plane, int 8, uint8 value plane, row 0 = south - the Chernarus layout). Every cell: usage Town + Village, value Tier1 + Tier2."""
    usages = re.findall(r'<usage name="([^"]+)"', rd(os.path.join(VANILLA, "cfglimitsdefinition.xml")))
    values = re.findall(r'<value name="([^"]+)"', rd(os.path.join(VANILLA, "cfglimitsdefinition.xml")))
    ubits = (1 << usages.index("Town")) | (1 << usages.index("Village"))
    vbits = (1 << values.index("Tier1")) | (1 << values.index("Tier2"))
    n = 2048
    # REAL layout (derived 2026-09-27 from the server's own code + every working map's file size): 5 ints
    # (w, h, world x, world z, usage bits), the usage plane, ONE int (value bits), the value plane. The first
    # version wrote a 6th header int instead; the server then read the last usage cell (0x180 = 384) as the value
    # bit depth, 32 / 384 = 0, and crashed with INT_DIVIDE_BY_ZERO in CE InitOffline.
    raw = struct.pack("<5i", n, n, WORLD, WORLD, 32)
    raw += np.full(n * n, ubits, "<u4").tobytes()
    raw += struct.pack("<i", 8) + np.full(n * n, vbits, np.uint8).tobytes()
    with open(os.path.join(MISSION, "areaflags.map"), "wb") as f:
        f.write(raw)
    log("areaflags.map: %dx%d cells of %.0f m, usage 0x%x (Town|Village), value 0x%x (Tier1|Tier2), %d bytes"
        % (n, n, WORLD / n, ubits, vbits, len(raw)))


def build_spawnpoints():
    x, z = SPAWN
    block = """        <spawn_params>
            <min_dist_infected>0</min_dist_infected>
            <max_dist_infected>1</max_dist_infected>
            <min_dist_player>0</min_dist_player>
            <max_dist_player>2000</max_dist_player>
            <min_dist_static>0</min_dist_static>
            <max_dist_static>2</max_dist_static>
        </spawn_params>
        <generator_params>
            <grid_density>4</grid_density>
            <grid_width>6</grid_width>
            <grid_height>6</grid_height>
            <min_dist_static>0</min_dist_static>
            <max_dist_static>2</max_dist_static>
            <min_steepness>-45</min_steepness>
            <max_steepness>45</max_steepness>
        </generator_params>
        <group_params>
            <enablegroups>true</enablegroups>
            <groups_as_regular>true</groups_as_regular>
            <lifetime>120</lifetime>
            <counter>-1</counter>
        </group_params>
        <generator_posbubbles>
            <group name="TestYard">
                <pos x="%.1f" z="%.1f" />
            </group>
        </generator_posbubbles>
""" % (x, z)
    text = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n<playerspawnpoints>\n'
    for sec in ("fresh", "hop", "travel"):
        text += "    <%s>\n%s    </%s>\n" % (sec, block, sec)
    text += "</playerspawnpoints>\n"
    wb(os.path.join(MISSION, "cfgplayerspawnpoints.xml"), text)


def build_weather():
    van = rd(os.path.join(VANILLA, "cfgweather.xml"))
    van = van.replace('<weather reset="0" enable="0">', '<weather reset="1" enable="1">')

    def setblock(text, tag, current, limits, extra=None):
        m = re.search(r"<%s>.*?</%s>" % (tag, tag), text, re.S)
        b = m.group(0)
        b = re.sub(r'<current [^>]*/>', current, b)
        b = re.sub(r'<limits [^>]*/>', limits, b)
        if extra:
            b = re.sub(r'<changelimits [^>]*/>', extra, b)
        return text.replace(m.group(0), b)
    van = setblock(van, "overcast", '<current actual="0.12" time="120" duration="3600" />', '<limits min="0.05" max="0.3" />')
    van = setblock(van, "fog", '<current actual="0.02" time="120" duration="3600" />', '<limits min="0.0" max="0.04" />')
    van = setblock(van, "rain", '<current actual="0.0" time="60" duration="3600" />', '<limits min="0.0" max="0.0" />')
    van = setblock(van, "windMagnitude", '<current actual="3.0" time="120" duration="600" />', '<limits min="1.0" max="6.0" />',
                   '<changelimits min="0.0" max="3.0" />')
    wb(os.path.join(MISSION, "cfgweather.xml"), van.replace(
        "<!-- 'reset' and 'enable' are a bool",
        "<!-- japantest: clear spring (overcast 0.05-0.3, no rain, light wind), reset on every boot -->\n<!-- 'reset' and 'enable' are a bool"))


def build_gameplay(spawn_files):
    van = rd(os.path.join(VANILLA, "cfggameplay.json"))
    arr = ", ".join('"%s"' % s for s in spawn_files)
    out = van.replace('"objectSpawnersArr": []', '"objectSpawnersArr": [%s]' % arr)
    assert ('"objectSpawnersArr": [%s]' % arr) in out
    json.loads(out)
    wb(os.path.join(MISSION, "cfggameplay.json"), out)


def copy_spawns():
    dst = os.path.join(MISSION, "spawns")
    shutil.rmtree(dst, ignore_errors=True)
    files = []
    for path in sorted(glob.glob(os.path.join(TEST, "spawns", "*.json"))):
        try:
            data = json.loads(rd(path))
            n = len(data.get("Objects", []))
        except (ValueError, AttributeError) as e:
            log("  WARNING spawns/%s is not valid JSON (%s) - skipped" % (os.path.basename(path), e))
            continue
        os.makedirs(dst, exist_ok=True)
        shutil.copyfile(path, os.path.join(dst, os.path.basename(path)))
        files.append("spawns/" + os.path.basename(path))
        log("object spawner: spawns/%s (%d objects)" % (os.path.basename(path), n))
    return files


def read_items():
    items = []
    for path in sorted(glob.glob(os.path.join(TEST, "items", "*.txt"))):
        for line in rd(path).splitlines():
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            parts = line.split()
            cls = parts[0]
            cnt = 1
            if len(parts) > 1:
                try:
                    cnt = max(1, int(parts[1]))
                except ValueError:
                    pass
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", cls):
                log("  WARNING items/%s: %r is not a class name - skipped" % (os.path.basename(path), cls))
                continue
            items.extend([(cls, os.path.basename(path))] * cnt)
    return items


def read_creatures():
    out = []
    for path in sorted(glob.glob(os.path.join(TEST, "spawns", "*_creatures.txt"))):
        for line in rd(path).splitlines():
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            p = line.split()
            try:
                cls, x, z = p[0], float(p[1]), float(p[2])
                yaw = float(p[3]) if len(p) > 3 else 0.0
            except (ValueError, IndexError):
                log("  WARNING %s: bad line %r" % (os.path.basename(path), line))
                continue
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", cls):
                continue
            out.append((cls, x, z, yaw, os.path.basename(path)))
    return out


INIT_TEMPLATE = r"""// japantest.japantestisland - GENERATED by japan_dev/spikes/T_terrain/build_mission.py. Do not edit by hand:
// edit the test/ drop-ins (or the template in build_mission.py) and rerun the script.
// Vanilla dayzOffline init.c, minus the September date reset (this island is spring), plus the test layout:
//   * every class from test/items/*.txt on the ground, rows from (1000, 975) at 1.5 m (@NITEMS@ items)
//   * every line of test/spawns/*_creatures.txt standing at ground height (@NCREATURES@ creatures)
// Both are spawned once, when the first player connects (so CE cleanup cannot run before anyone is near), and are
// not saved to storage (ECE_NOPERSISTENCY_WORLD), so a restart never duplicates them.
// New characters spawn at the yard, (1024, 985), facing north.

void main()
{
	//INIT ECONOMY--------------------------------------
	Hive ce = CreateHive();
	if ( ce )
		ce.InitOffline();
}

class CustomMission: MissionServer
{
	protected bool m_JPTestSpawned;
	protected int m_JPTestItemsOk;
	protected int m_JPTestItemsBad;
	protected int m_JPTestCreaturesOk;
	protected int m_JPTestCreaturesBad;

	void SetRandomHealth(EntityAI itemEnt)
	{
		if ( itemEnt )
		{
			float rndHlt = Math.RandomFloat( 0.45, 0.65 );
			itemEnt.SetHealth01( "", "", rndHlt );
		}
	}

	void JPTest_Item(string cls, float x, float z)
	{
		vector pos = Vector(x, 25.0, z);
		Object obj = GetGame().CreateObjectEx(cls, pos, ECE_PLACE_ON_SURFACE | ECE_NOPERSISTENCY_WORLD);
		if ( !obj )
		{
			m_JPTestItemsBad = m_JPTestItemsBad + 1;
			Print("[JPTest] item class not found: " + cls);
			return;
		}
		EntityAI ent = EntityAI.Cast(obj);
		if ( ent )
			ent.SetLifetime(3888000);
		m_JPTestItemsOk = m_JPTestItemsOk + 1;
	}

	void JPTest_Creature(string cls, float x, float z, float yaw)
	{
		float y = GetGame().SurfaceY(x, z);
		vector pos = Vector(x, y, z);
		Object obj = GetGame().CreateObjectEx(cls, pos, ECE_PLACE_ON_SURFACE | ECE_INITAI | ECE_EQUIP_ATTACHMENTS | ECE_NOPERSISTENCY_WORLD);
		if ( !obj )
		{
			m_JPTestCreaturesBad = m_JPTestCreaturesBad + 1;
			Print("[JPTest] creature class not found: " + cls);
			return;
		}
		obj.SetOrientation(Vector(yaw, 0, 0));
		m_JPTestCreaturesOk = m_JPTestCreaturesOk + 1;
	}

	void JPTest_SpawnAll()
	{
		if ( m_JPTestSpawned )
			return;
		m_JPTestSpawned = true;
		Print("[JPTest] spawning the test layout");
@ITEMS@
@CREATURES@
		string msg = "[JPTest] items ok " + m_JPTestItemsOk.ToString();
		msg += ", items missing " + m_JPTestItemsBad.ToString();
		msg += ", creatures ok " + m_JPTestCreaturesOk.ToString();
		msg += ", creatures missing " + m_JPTestCreaturesBad.ToString();
		Print(msg);
	}

	override void InvokeOnConnect(PlayerBase player, PlayerIdentity identity)
	{
		super.InvokeOnConnect(player, identity);
		JPTest_SpawnAll();
	}

	override PlayerBase CreateCharacter(PlayerIdentity identity, vector pos, ParamsReadContext ctx, string characterName)
	{
		Entity playerEnt;
		float sx = @SPAWNX@ + Math.RandomFloatInclusive(-1.5, 1.5);
		float sz = @SPAWNZ@;
		float sy = GetGame().SurfaceY(sx, sz);
		vector spawnPos = Vector(sx, sy, sz);
		playerEnt = GetGame().CreatePlayer( identity, characterName, spawnPos, 0, "NONE" );
		Class.CastTo( m_player, playerEnt );

		GetGame().SelectPlayer( identity, m_player );
		m_player.SetOrientation(Vector(0, 0, 0));

		return m_player;
	}

	override void StartingEquipSetup(PlayerBase player, bool clothesChosen)
	{
		EntityAI itemClothing;
		EntityAI itemEnt;
		float rand;

		itemClothing = player.FindAttachmentBySlotName( "Body" );
		if ( itemClothing )
		{
			SetRandomHealth( itemClothing );

			itemEnt = itemClothing.GetInventory().CreateInInventory( "BandageDressing" );
			player.SetQuickBarEntityShortcut(itemEnt, 2);

			string chemlightArray[] = { "Chemlight_White", "Chemlight_Yellow", "Chemlight_Green", "Chemlight_Red" };
			int rndIndex = Math.RandomInt( 0, 4 );
			itemEnt = itemClothing.GetInventory().CreateInInventory( chemlightArray[rndIndex] );
			SetRandomHealth( itemEnt );
			player.SetQuickBarEntityShortcut(itemEnt, 1);

			rand = Math.RandomFloatInclusive( 0.0, 1.0 );
			if ( rand < 0.35 )
				itemEnt = player.GetInventory().CreateInInventory( "Apple" );
			else if ( rand > 0.65 )
				itemEnt = player.GetInventory().CreateInInventory( "Pear" );
			else
				itemEnt = player.GetInventory().CreateInInventory( "Plum" );
			player.SetQuickBarEntityShortcut(itemEnt, 3);
			SetRandomHealth( itemEnt );
		}

		itemClothing = player.FindAttachmentBySlotName( "Legs" );
		if ( itemClothing )
			SetRandomHealth( itemClothing );

		itemClothing = player.FindAttachmentBySlotName( "Feet" );
	}
};

Mission CreateCustomMission(string path)
{
	return new CustomMission();
}
"""


def build_init(items, creatures):
    il = []
    for k, (cls, src) in enumerate(items):
        row, col = divmod(k, ITEMS_PER_ROW)
        x = ITEM_ORIGIN[0] + col * ITEM_STEP
        z = ITEM_ORIGIN[1] - row * ITEM_STEP
        il.append('\t\tJPTest_Item("%s", %.2f, %.2f);' % (cls, x, z))
    cl = ['\t\tJPTest_Creature("%s", %.2f, %.2f, %.1f);' % (cls, x, z, yaw) for cls, x, z, yaw, src in creatures]
    text = (INIT_TEMPLATE.replace("@ITEMS@", "\n".join(il) if il else "\t\t// (no test/items/*.txt yet)")
            .replace("@CREATURES@", "\n".join(cl) if cl else "\t\t// (no test/spawns/*_creatures.txt yet)")
            .replace("@NITEMS@", str(len(items))).replace("@NCREATURES@", str(len(creatures)))
            .replace("@SPAWNX@", "%.1f" % SPAWN[0]).replace("@SPAWNZ@", "%.1f" % SPAWN[1]))
    check_enforce(text)
    wb(os.path.join(MISSION, "init.c"), text)
    if items:
        rows = (len(items) - 1) // ITEMS_PER_ROW + 1
        log("init.c: %d items in %d rows (x 1000..%.1f, z 975..%.1f), %d creatures" % (
            len(items), rows, ITEM_ORIGIN[0] + (min(len(items), ITEMS_PER_ROW) - 1) * ITEM_STEP,
            ITEM_ORIGIN[1] - (rows - 1) * ITEM_STEP, len(creatures)))
        if ITEM_ORIGIN[1] - (rows - 1) * ITEM_STEP < 952:
            log("  WARNING: the item grid now reaches the weapon range (z <= 950)")
    else:
        log("init.c: no items, %d creatures" % len(creatures))


def check_enforce(text):
    """The cheap offline checks from the project's Enforce gotchas: braces, no line-leading binary operator, no
    ternary, no bool.ToString, no reserved names as locals, no over-long concatenations."""
    assert text.count("{") == text.count("}"), "brace mismatch"
    assert text.count("(") == text.count(")"), "paren mismatch"
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("//"):
            continue
        assert not re.match(r"^(\+|-(?!\d)|\*|/(?!/)|&&|\|\|)", s), "line %d starts with an operator" % n
        assert " ? " not in s, "line %d: ternary" % n
        assert s.count(" + ") <= 15, "line %d: formula too complex" % n
        assert not re.search(r"\b(owned|out|proto|native|autoptr|inout|notnull|sealed|volatile|external)\s*[;=]", s), \
            "line %d: reserved word as a name" % n


def main():
    if not os.path.isdir(VANILLA):
        print("P: is not mapped (need %s). Run:  subst P: D:\\DayZToolsExtract" % VANILLA)
        return 2
    os.makedirs(MISSION, exist_ok=True)
    info_path = os.path.join(HERE, "world_info.json")
    info = json.loads(rd(info_path)) if os.path.isfile(info_path) else None
    if not info:
        log("WARNING: spikes/T_terrain/world_info.json missing - run build_world.py first (no control house in mapgrouppos)")
    # clean everything we generate (never storage_*)
    for name in os.listdir(MISSION):
        if name.startswith("storage_"):
            continue
        p = os.path.join(MISSION, name)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    # 1. vanilla copies
    for fn in ("cfgeconomycore.xml", "cfgignorelist.xml", "cfglimitsdefinition.xml", "cfglimitsdefinitionuser.xml",
               "cfgrandompresets.xml", "cfgspawnabletypes.xml", "cfgundergroundtriggers.json", "mapclusterproto.xml",
               "mapgroupdirt.xml"):
        shutil.copyfile(os.path.join(VANILLA, fn), os.path.join(MISSION, fn))
    os.makedirs(os.path.join(MISSION, "db"), exist_ok=True)
    shutil.copyfile(os.path.join(VANILLA, "db", "globals.xml"), os.path.join(MISSION, "db", "globals.xml"))
    shutil.copyfile(os.path.join(VANILLA_MISSION, "db", "messages.xml"), os.path.join(MISSION, "db", "messages.xml"))
    # 2. emptied for this world
    wb(os.path.join(MISSION, "cfgeventspawns.xml"), '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n<eventposdef>\n</eventposdef>\n')
    wb(os.path.join(MISSION, "cfgeventgroups.xml"), '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<eventgroupdef>\n</eventgroupdef>\n')
    wb(os.path.join(MISSION, "cfgenvironment.xml"), '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n<env>\n\t<territories>\n\t</territories>\n</env>\n')
    wb(os.path.join(MISSION, "cfgeffectarea.json"), '{\n\t"Areas": [],\n\t"SafePositions": [[%.1f, %.1f]]\n}\n' % SPAWN)
    # 3. generated / merged
    build_economy()
    build_events()
    build_types()
    build_mapgroups(info)
    build_areaflags()
    build_spawnpoints()
    build_weather()
    build_gameplay(copy_spawns())
    items = read_items()
    creatures = read_creatures()
    for cls, x, z, yaw, src in creatures:
        log("creature: %s at (%.1f, %.1f) yaw %.0f from %s" % (cls, x, z, yaw, src))
    build_init(items, creatures)
    # 4. sanity: every xml parses
    import xml.etree.ElementTree as ET
    bad = 0
    for root, _, files in os.walk(MISSION):
        if os.path.basename(root).startswith("storage_"):
            continue
        for fn in files:
            p = os.path.join(root, fn)
            if fn.endswith(".xml"):
                try:
                    ET.parse(p)
                except ET.ParseError as e:
                    log("XML ERROR %s: %s" % (os.path.relpath(p, MISSION), e))
                    bad += 1
            elif fn.endswith(".json"):
                try:
                    json.loads(rd(p))
                except ValueError as e:
                    log("JSON ERROR %s: %s" % (os.path.relpath(p, MISSION), e))
                    bad += 1
    n = sum(len(f) for _, _, f in os.walk(MISSION))
    log("mission: %s - %d files, %s" % (MISSION, n, "all xml/json parse" if not bad else "%d PARSE ERRORS" % bad))
    with open(os.path.join(DEV, "data", "T_terrain", "build_mission.log"), "wb") as f:
        f.write("\n".join(LOG).encode("utf-8"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
