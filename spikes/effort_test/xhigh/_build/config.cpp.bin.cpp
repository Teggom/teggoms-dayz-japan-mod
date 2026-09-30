class CfgPatches
{
	class JP_EffTest_xhigh
	{
		units[]={};
		weapons[]={};
		requiredVersion=0.1;
		requiredAddons[]=
		{
			"DZ_Data",
			"JP_Common"
		};
	};
};
class CfgVehicles
{
	class HouseNoDestruct;
	class JP_EffTest_xhigh_Tansu: HouseNoDestruct
	{
		scope=1;
		displayName="Tansu (clothing chest of drawers)";
		model="\JP\effort_test\xhigh\jp_f_tansu.p3d";
	};
	class JP_EffTest_xhigh_Tansu_Ransacked: HouseNoDestruct
	{
		scope=1;
		displayName="Tansu (clothing chest of drawers, ransacked)";
		model="\JP\effort_test\xhigh\jp_f_tansu_ransacked.p3d";
	};
};
