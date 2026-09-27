class CfgPatches
{
	class JP_Weapons
	{
		units[]=
		{
			"JP_Katana",
			"JP_Yari",
			"JP_Ammo_Ya"
		};
		weapons[]=
		{
			"JP_Yumi",
			"JP_Yumi_XB"
		};
		requiredVersion=0.1;
		requiredAddons[]=
		{
			"DZ_Data",
			"DZ_Scripts",
			"DZ_Weapons_Melee",
			"DZ_Weapons_Melee_Blade",
			"DZ_Gear_Crafting",
			"DZ_Weapons_Archery",
			"DZ_Weapons_Archery_Bow_Recurve",
			"DZ_Weapons_Archery_Crossbow",
			"DZ_Weapons_Ammunition",
			"DZ_Weapons_Projectiles"
		};
	};
};
class CfgMods
{
	class JP_Weapons
	{
		dir="JP";
		picture="";
		action="";
		hideName=1;
		hidePicture=1;
		name="JP Weapons";
		credits="";
		author="Stephen";
		authorID="0";
		version="0.1";
		extra=0;
		type="mod";
		dependencies[]=
		{
			"World"
		};
		class defs
		{
			class worldScriptModule
			{
				value="";
				files[]=
				{
					"JP/weapons/scripts/4_World"
				};
			};
		};
	};
};
class CfgVehicles
{
	class Inventory_Base;
	class Sword;
	class Spear;
	class FxRound_HuntingBolt;
	class JP_Katana: Sword
	{
		scope=2;
		displayName="Katana";
		descriptionShort="A curved, single-edged two-handed sword with a silk-wrapped hilt.";
		model="\JP\weapons\katana\jp_katana.p3d";
		weight=1200;
		itemSize[]={2,8};
		hiddenSelections[]={};
		class DamageSystem
		{
			class GlobalHealth
			{
				class Health
				{
					hitpoints=200;
					healthLevels[]=
					{
						
						{
							1,
							
							{
								"JP\weapons\data\jp_steel.rvmat",
								"JP\weapons\data\jp_brass.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_silk.rvmat"
							}
						},
						
						{
							0.69999999,
							
							{
								"JP\weapons\data\jp_steel.rvmat",
								"JP\weapons\data\jp_brass.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_silk.rvmat"
							}
						},
						
						{
							0.5,
							
							{
								"JP\weapons\data\jp_steel.rvmat",
								"JP\weapons\data\jp_brass.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_silk.rvmat"
							}
						},
						
						{
							0.30000001,
							
							{
								"JP\weapons\data\jp_steel.rvmat",
								"JP\weapons\data\jp_brass.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_silk.rvmat"
							}
						},
						
						{
							0,
							
							{
								"JP\weapons\data\jp_steel.rvmat",
								"JP\weapons\data\jp_brass.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_silk.rvmat"
							}
						}
					};
				};
			};
		};
	};
	class JP_Yari: Spear
	{
		scope=2;
		displayName="Yari";
		descriptionShort="A straight-bladed spear (su-yari) on a lacquered shaft.";
		model="\JP\weapons\yari\jp_yari.p3d";
		weight=1600;
		itemSize[]={1,9};
		hiddenSelections[]={};
		class DamageSystem
		{
			class GlobalHealth
			{
				class Health
				{
					hitpoints=150;
					healthLevels[]=
					{
						
						{
							1,
							
							{
								"JP\weapons\data\jp_lacquer.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_brass.rvmat",
								"JP\weapons\data\jp_steel.rvmat"
							}
						},
						
						{
							0.69999999,
							
							{
								"JP\weapons\data\jp_lacquer.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_brass.rvmat",
								"JP\weapons\data\jp_steel.rvmat"
							}
						},
						
						{
							0.5,
							
							{
								"JP\weapons\data\jp_lacquer.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_brass.rvmat",
								"JP\weapons\data\jp_steel.rvmat"
							}
						},
						
						{
							0.30000001,
							
							{
								"JP\weapons\data\jp_lacquer.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_brass.rvmat",
								"JP\weapons\data\jp_steel.rvmat"
							}
						},
						
						{
							0,
							
							{
								"JP\weapons\data\jp_lacquer.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_brass.rvmat",
								"JP\weapons\data\jp_steel.rvmat"
							}
						}
					};
				};
			};
		};
		class MeleeModes
		{
			class Default
			{
				ammo="MeleeSharpLight_3";
				range=2;
			};
			class Heavy
			{
				ammo="MeleeSharpHeavy_3";
				range=2;
			};
			class Sprint
			{
				ammo="MeleeSharpHeavy_3";
				range=3.9000001;
			};
		};
	};
	class FxRound_JP_Ya: FxRound_HuntingBolt
	{
		model="\JP\weapons\ya\jp_ya.p3d";
	};
};
class CfgMagazines
{
	class Ammo_HuntingBolt;
	class JP_Ammo_Ya: Ammo_HuntingBolt
	{
		scope=2;
		displayName="Ya";
		descriptionShort="Bamboo arrows with an iron head and barred feathers, for the yumi. Recoverable after a shot.";
		model="\JP\weapons\ya\jp_ya.p3d";
		weight=30;
		itemSize[]={6,1};
		count=10;
		ammo="Bullet_JP_Ya";
		class DamageSystem
		{
			class GlobalHealth
			{
				class Health
				{
					hitpoints=120;
					healthLevels[]=
					{
						
						{
							1,
							
							{
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						},
						
						{
							0.69999999,
							
							{
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						},
						
						{
							0.5,
							
							{
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						},
						
						{
							0.30000001,
							
							{
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						},
						
						{
							0,
							
							{
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						}
					};
				};
			};
		};
	};
};
class CfgAmmo
{
	class Bullet_HuntingBolt;
	class Bullet_JP_Ya: Bullet_HuntingBolt
	{
		scope=1;
		proxyShape="\JP\weapons\ya\jp_ya.p3d";
		round="FxRound_JP_Ya";
		spawnPileType="JP_Ammo_Ya";
		initSpeed=80;
		typicalSpeed=80;
		airFriction=-0.0016;
		weight=0.029999999;
	};
};
class Mode_SemiAuto;
class CfgWeapons
{
	class RecurveBow;
	class Crossbow_Base;
	class JP_Yumi: RecurveBow
	{
		scope=2;
		displayName="Yumi";
		descriptionShort="A tall, asymmetric Japanese bow of lacquered bamboo. Shoots ya.";
		model="\JP\weapons\yumi\jp_yumi.p3d";
		weight=800;
		itemSize[]={5,10};
		chamberSize=1;
		chamberedRound="";
		chamberableFrom[]=
		{
			"JP_Ammo_Ya"
		};
		magazines[]={};
		hiddenSelections[]={};
		simpleHiddenSelections[]=
		{
			"bullet"
		};
		class Single: Mode_SemiAuto
		{
			soundSetShot[]=
			{
				"Crossbow_Shot_SoundSet"
			};
			reloadTime=1;
			recoil="recoil_bow";
			recoilProne="recoil_bow";
			dispersion=0.0015;
			magazineSlot="magazine";
		};
		class DamageSystem
		{
			class GlobalHealth
			{
				class Health
				{
					hitpoints=150;
					healthLevels[]=
					{
						
						{
							1,
							
							{
								"JP\weapons\data\jp_bow.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_hemp.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						},
						
						{
							0.69999999,
							
							{
								"JP\weapons\data\jp_bow.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_hemp.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						},
						
						{
							0.5,
							
							{
								"JP\weapons\data\jp_bow.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_hemp.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						},
						
						{
							0.30000001,
							
							{
								"JP\weapons\data\jp_bow.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_hemp.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						},
						
						{
							0,
							
							{
								"JP\weapons\data\jp_bow.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_hemp.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						}
					};
				};
			};
		};
	};
	class JP_Yumi_XB: Crossbow_Base
	{
		scope=2;
		displayName="Yumi (crossbow handling)";
		descriptionShort="The yumi on the crossbow's animations: loads, fires and recovers ya.";
		model="\JP\weapons\yumi\jp_yumi_xb.p3d";
		weight=800;
		itemSize[]={5,10};
		chamberableFrom[]=
		{
			"JP_Ammo_Ya"
		};
		attachments[]={};
		hiddenSelections[]={};
		hiddenSelectionsTextures[]={};
		simpleHiddenSelections[]=
		{
			"bullet"
		};
		boneRemap[]={};
		class DamageSystem
		{
			class GlobalHealth
			{
				class Health
				{
					hitpoints=150;
					healthLevels[]=
					{
						
						{
							1,
							
							{
								"JP\weapons\data\jp_bow.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_hemp.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						},
						
						{
							0.69999999,
							
							{
								"JP\weapons\data\jp_bow.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_hemp.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						},
						
						{
							0.5,
							
							{
								"JP\weapons\data\jp_bow.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_hemp.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						},
						
						{
							0.30000001,
							
							{
								"JP\weapons\data\jp_bow.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_hemp.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						},
						
						{
							0,
							
							{
								"JP\weapons\data\jp_bow.rvmat",
								"JP\weapons\data\jp_iron.rvmat",
								"JP\weapons\data\jp_hemp.rvmat",
								"JP\weapons\data\jp_bamboo.rvmat",
								"JP\weapons\data\jp_feather.rvmat"
							}
						}
					};
				};
			};
		};
	};
};
