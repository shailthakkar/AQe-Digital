import React, { useEffect, useState } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import Plot from "react-plotly.js";
import Sidebar from "../components/Admin/Sidebar";
import { useTranslation } from "react-i18next";

const PlayerDashboard = () => {
  const { t } = useTranslation();
  const { playerName: playerNameFromUrl } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const { playerName: passedPlayerName, position } = location.state || {};
  const finalPlayerName = passedPlayerName || playerNameFromUrl;

  const [players, setPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState(finalPlayerName);
  const [figures, setFigures] = useState([]);
  const [loading, setLoading] = useState(true);
  const [commentary, setCommentary] = useState("");
  const [videoLink, setVideoLink] = useState("");

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:8000/api/dashboard.json?player=${selectedPlayer}`)
      .then((response) => {
        setPlayers(response.data);
        setSelectedPlayer(response.data[0] || finalPlayerName);
      })
      .catch((error) => console.error("Error fetching players:", error));
  }, [finalPlayerName]);

  useEffect(() => {
    if (!selectedPlayer) return;

    const fetchPlayerData = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/dashboard.json?player=${selectedPlayer}`
        );
        if (response.data.error) {
          console.error(response.data.error);
          setFigures([]);
        } else {
          setFigures(response.data.dashboard);
        }

        const commentaryResponse = await axios.get(
          `http://127.0.0.1:8000/api/best-commentary?player=${selectedPlayer}`
        );
        if (commentaryResponse.data.error) {
          console.error(commentaryResponse.data.error);
        } else {
          setVideoLink(commentaryResponse.data.video_link);
          setCommentary(commentaryResponse.data.commentary);
        }
      } catch (error) {
        console.error("Error fetching player data:", error);
        setFigures([]);
      } finally {
        setLoading(false);
      }
    };

    fetchPlayerData();
  }, [selectedPlayer]);

  return (
    <div style={{ display: "flex" }}>
      <Sidebar playerName={selectedPlayer} position={position} />
      <div style={{ flex: 1, position: "relative" }} className="p-4">
        {/* Back Button */}
        <button
          onClick={() => navigate("/")}
          style={{
            position: "fixed",
            bottom: "20px",
            right: "20px",
            zIndex: 1000,
          }}
          className="bg-gray-600 text-white px-4 py-2 rounded-md"
        >
          Back
        </button>

        <h2 className="text-3xl font-bold">{t(selectedPlayer)}'{t("s Performance")}</h2>

        {loading ? (
          <p className="text-gray-500 mt-4">Loading data...</p>
        ) : (
          <>
            {videoLink && (
              <div className="mt-4 bg-white p-4 rounded-lg shadow">
                <h3 className="text-xl font-bold">Clip of the Most Recent Shot</h3>
                <div className="mt-2">
                  {videoLink.includes("youtube.com") ||
                  videoLink.includes("youtu.be") ? (
                    <iframe
                      width="100%"
                      height="315"
                      src={`https://www.youtube.com/embed/${
                        videoLink.split("v=")[1]
                      }`}
                      title="YouTube video player"
                      frameBorder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                    ></iframe>
                  ) : (
                    <video controls width="100%" height="500">
                      <source src={videoLink} type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                  )}
                </div>
              </div>
            )}

            {commentary && (
              <div className="mt-4 bg-white p-4 rounded-lg shadow">
                <h3 className="text-xl font-bold">Analysis of the Shot</h3>
                <p className="text-gray-700">{commentary}</p>
              </div>
            )}
            {figures.length > 0 ? (
              <div className="mt-4">
                {figures.map((figure, index) => {
                  const parsedFigure = JSON.parse(figure);
                  return (
                    <div
                      key={index}
                      className="bg-white p-4 mb-4 rounded-lg shadow"
                    >
                      <Plot
                        data={parsedFigure.data}
                        layout={{
                          ...parsedFigure.layout,
                          width: window.innerWidth * 0.8,
                          height: 400,
                        }}
                        style={{ maxWidth: "100%", height: "auto" }}
                      />
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="mt-4">
                <p className="text-gray-500">
                  No data available for this player.
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default PlayerDashboard;