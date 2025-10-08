

from typing import Optional

import requests
from sqlalchemy.dialects.postgresql import insert

from controllers.nfl.models import Player, Team
from extensions import db


SLEEPER_PLAYERS = 'https://api.sleeper.app/v1/players/nfl'

def _slim_name(p: dict) -> Optional[str]:
  full = p.get('full_name')
  if full:
      return full.strip()
  first, last = (p.get('first_name') or '').strip(), (p.get('last_name') or '').strip()
  name = f"{first} {last}".strip()
  return name or None

def import_players_from_sleeper(limit: Optional[int] = None, commit_every: int = 2000) -> dict:
    resp = requests.get(SLEEPER_PLAYERS, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    total = 0
    upserted_teams = 0
    upserted_players = 0

    team_cache: dict[str, int] = {}

    for pid, p in data.items():
      name = _slim_name(p)
      if not name:
        continue

      team_code = (p.get('team') or '').strip().upper() or None
      pos = (p.get('position') or '').strip().upper() or None

      team_id = None
      if team_code:
        if team_code in team_cache:
          team_id = team_cache[team_code]
        else:
          stmt_team = insert(Team.__table__).values(code=team_code).on_conflict_do_nothing(
             index_elements=['code']
          )
          db.session.execute(stmt_team)

          t = Team.query.filter_by(code=team_code).first()
          team_id = t.id if t else None
          team_cache[team_code] = team_id or 0
          upserted_teams += 1
        
      stmt_player = insert(Player.__table__).values(
         ext_source='sleeper',
         ext_id=str(pid),
         full_name=name,
         position=pos,
         team_id=team_id,
         birth_date=p.get('birth_date'),
        #  height_in=p.get('height'),
        #  weight_lb=p.get('weight'),
      ).on_conflict_do_update(
         index_elements=['ext_source', 'ext_id'],
         set_=dict(
            full_name=name,
            position=pos,
            team_id=team_id,
            birth_date=p.get('birth_date'),
            # height_in=p.get('height'),
            # weight_lb=p.get('weight'),
         )
      )
      db.session.execute(stmt_player)
      upserted_players += 1
      total += 1

      if limit and total >= limit:
        break
      if total % commit_every == 0:
        db.session.commit()
    
    db.session.commit()
    return {
      'total_processed': total,
      'upserted_teams': upserted_teams,
      'upserted_players': upserted_players,
    }