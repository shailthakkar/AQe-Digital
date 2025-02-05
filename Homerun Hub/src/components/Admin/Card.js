import React from "react";
const Card = ({ title, children }) => {
  return (
    <div className="bg-gray-800 p-5 shadow-md rounded-xl">
      <h2 className="text-xl text-white font-semibold mb-3">{title}</h2>
      <div>{children}</div>
    </div>
  );
};

export default Card;
