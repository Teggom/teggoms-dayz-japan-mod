"""model.cfg and config.cpp text for kit buildings."""

MODELCFG_HEAD = """class CfgSkeletons
{
\tclass Default
\t{
\t\tisDiscrete=1;
\t\tskeletonInherit="";
\t\tskeletonBones[]={};
\t};
%s};
class CfgModels
{
\tclass Default
\t{
\t\tsectionsInherit="";
\t\tsections[]={};
\t\tskeletonName="";
\t};
%s};
"""


def skeleton_name(model):
    return model.params["name"] + "_skeleton"


def modelcfg_parts(model):
    """(skeleton class text, model class text) for one building."""
    bones = ",\n".join('\t\t\t"%s",""' % d.bone for d in model.doors)
    sk = ("\tclass %s: Default\n\t{\n\t\tskeletonInherit=\"Default\";\n\t\tskeletonBones[]=\n\t\t{\n%s\n\t\t};\n\t};\n"
          % (skeleton_name(model), bones))
    anims = ""
    for d in model.doors:
        # translation: offset is in multiples of the axis length; the axis is exactly 1 m long, so offset1 is
        # the slide distance in metres either way it is read
        anims += ("\t\t\tclass %s\n\t\t\t{\n\t\t\t\ttype=\"translation\";\n\t\t\t\tsource=\"%s\";\n"
                  "\t\t\t\tselection=\"%s\";\n\t\t\t\taxis=\"%s_axis\";\n\t\t\t\tmemory=1;\n"
                  "\t\t\t\tminValue=0;\n\t\t\t\tmaxValue=1;\n\t\t\t\toffset0=0;\n\t\t\t\toffset1=%.4f;\n\t\t\t};\n"
                  % (d.cfg, d.cfg, d.bone, d.bone, d.slide / d.axis_len))
    mdl = ("\tclass %s: Default\n\t{\n\t\tskeletonName=\"%s\";\n\t\tclass Animations\n\t\t{\n%s\t\t};\n\t};\n"
           % (model.params["name"], skeleton_name(model), anims))
    return sk, mdl


def modelcfg(models):
    sks = "".join(modelcfg_parts(m)[0] for m in models)
    mds = "".join(modelcfg_parts(m)[1] for m in models)
    return MODELCFG_HEAD % (sks, mds)


def _armor(indent, proj, melee, frag):
    t = "\t" * indent
    out = ""
    for name, dmg in (("Projectile", proj), ("Melee", melee), ("FragGrenade", frag)):
        out += ("%sclass %s\n%s{\n%s\tclass Health\n%s\t{\n%s\t\tdamage=%s;\n%s\t};\n%s\tclass Blood\n%s\t{\n"
                "%s\t\tdamage=0;\n%s\t};\n%s\tclass Shock\n%s\t{\n%s\t\tdamage=0;\n%s\t};\n%s};\n"
                % (t, name, t, t, t, t, dmg, t, t, t, t, t, t, t, t, t, t))
    return out


def config_class(model, model_path):
    p = model.params
    doors = ""
    for d in model.doors:
        doors += ("\t\t\tclass %s\n\t\t\t{\n\t\t\t\tdisplayName=\"%s\";\n\t\t\t\tcomponent=\"%s\";\n"
                  "\t\t\t\tsoundPos=\"%s_action\";\n\t\t\t\tanimPeriod=%g;\n\t\t\t\tinitPhase=0;\n"
                  "\t\t\t\tinitOpened=%g;\n\t\t\t\tsoundOpen=\"%s\";\n\t\t\t\tsoundClose=\"%s\";\n"
                  "\t\t\t\tsoundLocked=\"%s\";\n\t\t\t\tsoundOpenABit=\"%s\";\n\t\t\t};\n"
                  % (d.cfg, d.display, d.cfg, d.bone, d.anim_period, d.init_opened, d.sound_open, d.sound_close,
                     d.sound_locked, d.sound_openabit))
    zones = ""
    for d in model.doors:
        zones += ("\t\t\t\tclass %s\n\t\t\t\t{\n\t\t\t\t\tclass Health\n\t\t\t\t\t{\n\t\t\t\t\t\thitpoints=1000;\n"
                  "\t\t\t\t\t\ttransferToGlobalCoef=0;\n\t\t\t\t\t};\n\t\t\t\t\tcomponentNames[]=\n\t\t\t\t\t{\n"
                  "\t\t\t\t\t\t\"%s\"\n\t\t\t\t\t};\n\t\t\t\t\tfatalInjuryCoef=-1;\n\t\t\t\t\tclass ArmorType\n"
                  "\t\t\t\t\t{\n%s\t\t\t\t\t};\n\t\t\t\t};\n"
                  % (d.cfg, d.bone, _armor(6, 3, 5, 10)))
    txt = ("\tclass %s: HouseNoDestruct\n\t{\n\t\tscope=1;\n\t\tdisplayName=\"%s\";\n\t\tmodel=\"%s\";\n"
           "\t\tclass Doors\n\t\t{\n%s\t\t};\n"
           "\t\tclass DamageSystem\n\t\t{\n\t\t\tclass GlobalHealth\n\t\t\t{\n\t\t\t\tclass Health\n\t\t\t\t{\n"
           "\t\t\t\t\thitpoints=1000;\n\t\t\t\t};\n\t\t\t};\n\t\t\tclass GlobalArmor\n\t\t\t{\n%s\t\t\t};\n"
           "\t\t\tclass DamageZones\n\t\t\t{\n%s\t\t\t};\n\t\t};\n\t};\n"
           % (p["class"], p.get("display", p["class"]), model_path, doors, _armor(4, 0, 0, 0), zones))
    return txt


def config_cpp(models, model_paths):
    classes = "".join(config_class(m, mp) for m, mp in zip(models, model_paths))
    return ("class CfgPatches\n{\n\tclass JP_Structures\n\t{\n\t\tunits[]={};\n\t\tweapons[]={};\n"
            "\t\trequiredVersion=0.1;\n\t\trequiredAddons[]=\n\t\t{\n\t\t\t\"DZ_Data\",\n"
            "\t\t\t\"DZ_Structures_Residential\"\n\t\t};\n\t};\n};\n"
            "class CfgVehicles\n{\n\tclass HouseNoDestruct;\n%s};\n" % classes)
