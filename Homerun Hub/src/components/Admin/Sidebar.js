import React, { useState } from "react";
import { useTranslation } from "react-i18next";

const Sidebar = ({
  playerName = "Default Name",
  position = "Unknown",
  profileImage,
}) => {
  const [profileImageState] = useState(profileImage);
  const { t } = useTranslation();
  // Function to get first two letters from name
  const getInitials = (name) => {
    if (!name) return "";
    return name
      .split(" ")
      .map((word) => word[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <div className="w-62 min-h-screen bg-gray-800 text-white flex flex-col items-center p-4 border-r-4 border-green-600">
      {/* Profile Picture Section */}
      <label className="relative cursor-pointer mb-2">
        <div className="w-28 h-28 rounded-full bg-gray-600 flex items-center justify-center text-white text-2xl font-bold border-3 border-green-600">
          {profileImageState ? (
            <img
              src={profileImageState}
              alt="Profile"
              className="w-full h-full object-cover rounded-full text-center"
            />
          ) : (
            getInitials(t(playerName))
          )}
        </div>
      </label>
      {/* Player Name and Position */}
      <h3 className="text-2xl font-semibold mt-2 text-center">{t(playerName)}</h3>
      <p className="text-gray-400 text-sm">{t(position)}</p>
    </div>
  );
};

export default Sidebar;