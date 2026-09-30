class CfgPatches
{
	class JP_EffTest_max
	{
		units[]=
		{
			"JP_EffTest_max_Tansu",
			"JP_EffTest_max_Tansu_Ransacked"
		};
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
	class JP_EffTest_max_Tansu: HouseNoDestruct
	{
		scope=2;
		displayName="Tansu (clothing chest)";
		model="\JP\effort_test\max\jp_f_tansu.p3d";
	};
	class JP_EffTest_max_Tansu_Ransacked: HouseNoDestruct
	{
		scope=2;
		displayName="Tansu (clothing chest), ransacked";
		model="\JP\effort_test\max\jp_f_tansu_ransacked.p3d";
	};
};
