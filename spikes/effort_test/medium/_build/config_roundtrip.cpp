class CfgPatches
{
	class JP_EffTest_medium
	{
		units[]=
		{
			"JP_EffTest_medium_Tansu",
			"JP_EffTest_medium_Tansu_Ransacked"
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
	class JP_EffTest_medium_Tansu: HouseNoDestruct
	{
		scope=1;
		displayName="Tansu (clothing chest)";
		model="\JP\effort_test\medium\jp_efftest_medium_tansu.p3d";
	};
	class JP_EffTest_medium_Tansu_Ransacked: HouseNoDestruct
	{
		scope=1;
		displayName="Tansu (clothing chest), ransacked";
		model="\JP\effort_test\medium\jp_efftest_medium_tansu_ransacked.p3d";
	};
};
