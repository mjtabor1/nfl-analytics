

const BASE_URL = 'https://api.sleeper.app/v1';

const LS_KEY = 'sleeper_players_cache_v1';

export async function fetchAllPlayers() {
  const cached = localStorage.getItem(LS_KEY);
  if (cached) {
    try {
      return JSON.parse(cached);
    } catch (e) {
      console.error('Error parsing cached players:', e);
    }
  }
  const resp = await fetch(`${BASE_URL}/players/nfl`, { method: 'GET' });
  if (!resp.ok) {
    throw new Error(`Error fetching players: ${resp.statusText}`);
  }
  const data = await resp.json();
  console.log('Fetched Players Data:', Object.values(data).slice(0,5));
  const mappedData = {};
  for (const [id, player] of Object.entries(data) ) {
    const name = (player.full_name || `${player.first_name} ${player.last_name}`).trim();
    const inactive = player.status === "Inactive";
    if (!name || inactive) continue;
    mappedData[id] = {
      player_id: id,
      full_name: name,
      position: player.position,
      team: player.team,
      status: player.status
    }
  }
  localStorage.setItem(LS_KEY, JSON.stringify(mappedData));
  return mappedData;
}