import React from "react";
import Card from "../../components/Admin/Card";

const AdminPanel = () => {
  return (
    <div>
      <div className="mt-5 mx-5 grid gap-4 grid-cols-1 md:grid-cols-2 text-green-600">
        <Card title="Live Match Scores">
          <p className="">Live scores and updates...</p>
        </Card>
        <Card title="Upcoming Matches">
          <p>Details about upcoming matches...</p>
        </Card>
      </div>
    </div>
  );
};

export default AdminPanel;
