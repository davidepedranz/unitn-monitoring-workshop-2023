import React from "react";
import "todomvc-app-css/index.css";

const App: React.FC = () => {
  return (
    <footer className="info">
    <p>
      Created with <span role="img" aria-label="love">💚</span>, freely inspired by{" "}
      <a
        href="http://todomvc.com/"
        target="_blank"
        rel="noopener noreferrer"
      >
        TodoMVC
      </a>
    </p>
  </footer>
);
};

export default App;