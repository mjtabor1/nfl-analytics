import { useEffect, useState } from "react";
import { fetchAllPlayers } from "../api/sleeperApi";
import { Box, CircularProgress, Container } from "@mui/material";


export default function PlayersList() {
  const [loading, setLoading] = useState(true);
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    const loadPlayers = async () => {
      setLoading(true);
      const allPlayers = await fetchAllPlayers();
      console.log('Loaded players:', allPlayers);
      setPlayers(Object.values(allPlayers));
      setLoading(false);
    }
    loadPlayers();
  }, [])

  return (
    <Container sx={{ mt: 4}}>
      {loading ? (
        <Box display="flex" justifyContent="center" mt={4}>
          <CircularProgress />
        </Box>
      ) : (
        <Box>
          <h2>Players List</h2>
        </Box>
      )}
    </Container>
  )
}