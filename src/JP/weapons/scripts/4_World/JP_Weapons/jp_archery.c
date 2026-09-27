// JP_Weapons spike A: archery scripts.
//
// JP_Yumi (config parent RecurveBow): the vanilla bows have NO weapon state machine (Archery_Base.c
// never builds one, so every load/fire request is ignored), and the bow animation set they use
// (player_main_bow.asi) binds no WeaponOperations clips, so the vanilla chambering states would wait
// for anim events (BulletShow / BulletInChamber) that never come. This FSM therefore nocks the ya in
// script, on a timer, with no animation, and fires through the vanilla WeaponFireLast state (the shot
// itself is TryFireWeapon on state entry; the state also leaves on its own reload timeout).
//
// JP_Yumi_XB (config parent Crossbow_Base) keeps the vanilla crossbow FSM untouched.
// Both only add: hide the nocked ya ("bullet" selection) when it leaves the string.

class JP_YaNock extends WeaponStateBase
{
	protected float m_Elapsed;
	protected bool m_TimeoutSent;
	static const float NOCK_TIME = 0.9;

	override void OnEntry(WeaponEventBase e)
	{
		super.OnEntry(e);
		m_Elapsed = 0;
		m_TimeoutSent = false;
		if (!e)
			return;

		Magazine pile = e.m_magazine;
		if (!pile)
			return;

		int mi = m_weapon.GetCurrentMuzzle();
		float dmg;
		string ammoType;
		if (pile.ServerAcquireCartridge(dmg, ammoType))
		{
			if (m_weapon.PushCartridgeToChamber(mi, dmg, ammoType))
			{
				m_weapon.ShowBullet(mi);
				m_weapon.SetCharged(true);
			}
		}
	}

	override void OnUpdate(float dt)
	{
		super.OnUpdate(dt);
		m_Elapsed += dt;
		if (m_TimeoutSent || m_Elapsed < NOCK_TIME)
			return;

		DayZPlayer p;
		Class.CastTo(p, m_weapon.GetHierarchyParent());
		if (m_weapon.CanProcessWeaponEvents())
		{
			m_TimeoutSent = true;
			m_weapon.ProcessWeaponEvent(new WeaponEventReloadTimeout(p));
		}
	}

	override bool IsWaitingForActionFinish()
	{
		return true;
	}
}

class JP_Yumi extends Archery_Base
{
	override RecoilBase SpawnRecoilObject()
	{
		return new CrossbowRecoil(this);
	}

	override void InitStateMachine()
	{
		m_abilities.Insert(new AbilityRecord(WeaponActions.CHAMBERING, WeaponActionChamberingTypes.CHAMBERING_CROSSBOW_OPENED));
		m_abilities.Insert(new AbilityRecord(WeaponActions.FIRE, WeaponActionFireTypes.FIRE_NORMAL));

		WeaponStableState E = new XBUncockedEmpty(this, NULL, XBAnimState.uncocked);
		WeaponStableState L = new XBLoaded(this, NULL, XBAnimState.cocked);
		WeaponStateBase Nock = new JP_YaNock(this, NULL);
		WeaponStateBase Shoot = new WeaponFireLast(this, NULL, WeaponActions.FIRE, WeaponActionFireTypes.FIRE_NORMAL);

		WeaponEventBase evLoad = new WeaponEventLoad1Bullet;
		WeaponEventBase evTrigger = new WeaponEventTrigger;
		WeaponEventBase evFin = new WeaponEventHumanCommandActionFinished;
		WeaponEventBase evAbort = new WeaponEventHumanCommandActionAborted;
		WeaponEventBase evTimeout = new WeaponEventReloadTimeout;

		m_fsm = new WeaponFSM();

		// nock: leaves only on its own timer (or an abort)
		m_fsm.AddTransition(new WeaponTransition(E, evLoad, Nock));
		m_fsm.AddTransition(new WeaponTransition(Nock, evTimeout, L, NULL, new WeaponGuardChamberFull(this)));
		m_fsm.AddTransition(new WeaponTransition(Nock, evTimeout, E));
		m_fsm.AddTransition(new WeaponTransition(Nock, evAbort, L, NULL, new WeaponGuardChamberFull(this)));
		m_fsm.AddTransition(new WeaponTransition(Nock, evAbort, E));

		// loose
		m_fsm.AddTransition(new WeaponTransition(L, evTrigger, Shoot));
		m_fsm.AddTransition(new WeaponTransition(Shoot, evFin, E));
		m_fsm.AddTransition(new WeaponTransition(Shoot, evAbort, E));
		m_fsm.AddTransition(new WeaponTransition(Shoot, evTimeout, E));

		SelectionBulletHide();
		EffectBulletHide(0);

		SetInitialState(E);
		m_fsm.Start();
	}

	override float GetChanceToJam()
	{
		return 0.0;
	}

	override void OnFire(int muzzle_index)
	{
		super.OnFire(muzzle_index);
		HideBullet(muzzle_index);
	}
}

class JP_Yumi_XB extends Crossbow_Base
{
	override void OnFire(int muzzle_index)
	{
		super.OnFire(muzzle_index);
		HideBullet(muzzle_index);
	}

	override void OnDebugSpawnEx(DebugSpawnParams params)
	{
		SpawnAmmo("JP_Ammo_Ya", SAMF_DEFAULT);
	}
}
