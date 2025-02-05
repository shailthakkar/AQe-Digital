import React, { useState, useRef, useEffect } from "react";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

function HomePage() {
  const { t } = useTranslation();
  const [teamsDropdownOpen, setTeamsDropdownOpen] = useState(false);
  const [selectedYear, setSelectedYear] = useState(null);
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [teamPlayers, setTeamPlayers] = useState([]);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(0);
  const [playerPage, setPlayerPage] = useState(0);
  const [loadingTeams, setLoadingTeams] = useState(false);
  const [loadingPlayers, setLoadingPlayers] = useState(false);

  const teamsPerPage = 10;
  const playersPerPage = 10;
  const sliderRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (sliderRef.current && !sliderRef.current.contains(event.target)) {
        setTeamsDropdownOpen(false);
        setSelectedYear(null);
      }
    };
    document.addEventListener("click", handleClickOutside);
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  const handleYearSelect = (year) => {
    setSelectedYear(year);
    fetchTeams(year);
  };

  const fetchTeams = async (year) => {
    setLoadingTeams(true);
    try {
      const response = await fetch(
        `https://statsapi.mlb.com/api/v1/schedule?sportId=1&season=${year}&gameType=R`
      );
      const data = await response.json();
      const teamData = [];
      data.dates.forEach((date) => {
        date.games.forEach((game) => {
          teamData.push(
            {
              name: t(game.teams.home.team.name),
              id: game.teams.home.team.id,
              gamePk: game.gamePk,
            },
            {
              name: t(game.teams.away.team.name),
              id: game.teams.away.team.id,
              gamePk: game.gamePk,
            }
          );
        });
      });

      const uniqueTeams = Array.from(
        new Map(teamData.map((team) => [team.id, team])).values()
      );
      setTeams(uniqueTeams);
      setError(null);
    } catch (error) {
      console.error("Error fetching teams:", error);
      setError("Failed to fetch teams. Please try again.");
    } finally {
      setLoadingTeams(false);
    }
  };

  const fetchPlayersForGame = async (gamePk) => {
    setLoadingPlayers(true);
    setPlayerPage(0);
    try {
      const response = await fetch(
        `https://statsapi.mlb.com/api/v1.1/game/${gamePk}/feed/live`
      );
      const data = await response.json();
      const players = Object.values(data.gameData.players).map((player) => ({
        id: player.id,
        fullName: player.fullName,
        position: player.primaryPosition.name,
      }));

      setTeamPlayers(players);
    } catch (error) {
      console.error("Error fetching players:", error);
      setError("Failed to fetch players. Please try again.");
    } finally {
      setLoadingPlayers(false);
    }
  };

  const handleTeamSelect = (team) => {
    setSelectedTeam(team.name);
    fetchPlayersForGame(team.gamePk);
  };

  const handlePlayerSelect = (player) => {
    navigate(`/player/${player.fullName}`, {
      state: {
        playerName: player.fullName,
        position: player.position,
        profileImage: player.profileImage || "default-image-url",
      },
    });
  };

  const handlePlayerClick = (player) => {
    navigate(`/player/${(player.fullName)}`, {
      state: {
        playerName: player.fullName,
        position: player.position,
        profileImage: player.profileImage || "default-image-url",
      },
    });
  };

  const paginatedTeams = teams.slice(
    currentPage * teamsPerPage,
    (currentPage + 1) * teamsPerPage
  );

  const paginatedPlayers = teamPlayers.slice(
    playerPage * playersPerPage,
    (playerPage + 1) * playersPerPage
  );

  return (
    <div className="flex flex-col lg:flex-row h-screen bg-gray-900 text-white">
      {/* Sidebar */}
      <div
        className="w-full lg:w-72 bg-gray-800 p-4 border-b-4 lg:border-r-4 border-green-600 h-full overflow-y-auto"
        ref={sliderRef}
      >
        <button
          className="bg-green-600 text-white font-bold px-4 py-2 w-full rounded-lg flex justify-between items-center"
          onClick={() => setTeamsDropdownOpen(!teamsDropdownOpen)}
        >
          {t("show_teams")} {teamsDropdownOpen ? <FaChevronUp /> : <FaChevronDown />}
        </button>

        {teamsDropdownOpen && (
          <div className="mt-3">
            <h3 className="text-lg font-semibold">{t("select_year")}</h3>
            <button
              className="w-full bg-green-600 py-2 rounded-md font-bold mt-2"
              onClick={() => handleYearSelect("2024")}
            >
              2024
            </button>

            {selectedYear && (
              <div className="mt-3">
                <h3 className="text-lg font-semibold">
                  {t("teams")} ({selectedYear})
                </h3>
                {loadingTeams ? (
                  <p className="text-gray-500">{t("loading_teams")}</p>
                ) : (
                  <ul>
                    {paginatedTeams.length > 0 ? (
                      paginatedTeams.map((team, index) => (
                        <li
                          key={index}
                          className={`p-2 hover:bg-gray-700 rounded-md cursor-pointer ${
                            selectedTeam === team.name ? "bg-green-600" : ""
                          }`}
                          onClick={() => handleTeamSelect(team)}
                        >
                          {team.name}
                        </li>
                      ))
                    ) : (
                      <p className="text-gray-500">{t("no_teams_found")}</p>
                    )}
                  </ul>
                )}
                <div className="flex justify-between mt-2">
                  <button
                    className="bg-gray-600 px-4 py-2 rounded-md"
                    onClick={() =>
                      setCurrentPage((prev) => Math.max(prev - 1, 0))
                    }
                    disabled={currentPage === 0}
                  >
                    {t("back")}
                  </button>
                  <button
                    className="bg-gray-600 px-4 py-2 rounded-md"
                    onClick={() =>
                      setCurrentPage((prev) =>
                        prev < Math.ceil(teams.length / teamsPerPage) - 1
                          ? prev + 1
                          : prev
                      )
                    }
                    disabled={
                      currentPage >= Math.ceil(teams.length / teamsPerPage) - 1
                    }
                  >
                    {t("next")}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="flex-1 p-6 pt-24">
        {selectedTeam && (
          <div className="bg-gray-800 p-4 rounded-lg shadow-lg">
            <h2 className="text-xl font-bold text-green-500">
              {t("players_for")} {selectedTeam}
            </h2>
            {error && <p className="text-red-500">{error}</p>}
            {loadingPlayers ? (
              <p className="text-gray-500">{t("loading_players")}</p>
            ) : (
              <ul className="mt-3">
                {paginatedPlayers.length > 0 ? (
                  paginatedPlayers.map((player, index) => (
                    <li
                      key={index}
                      className="py-2 cursor-pointer"
                      onClick={() => handlePlayerClick(player)} // Handle player click
                    >
                      <span className="text-white">{t(player.fullName)}</span>
                      <span className="text-gray-400 text-sm">
                        {" "}
                        - {player.position}
                      </span>
                    </li>
                  ))
                ) : (
                  <p className="text-gray-500">{t("no_players_found")}</p>
                )}
              </ul>
            )}
            <div className="flex justify-between mt-2">
              <button
                className="bg-gray-600 px-4 py-2 rounded-md"
                onClick={() => setPlayerPage((prev) => Math.max(prev - 1, 0))}
                disabled={playerPage === 0}
              >
                {t("back")}
              </button>
              <button
                className="bg-gray-600 px-4 py-2 rounded-md"
                onClick={() =>
                  setPlayerPage((prev) =>
                    prev < Math.ceil(teamPlayers.length / playersPerPage) - 1
                      ? prev + 1
                      : prev
                  )
                }
                disabled={
                  playerPage >=
                  Math.ceil(teamPlayers.length / playersPerPage) - 1
                }
              >
                {t("next")}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default HomePage;