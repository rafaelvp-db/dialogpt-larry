import React from "react";
import ReactDOM from "react-dom/client";
import "./style.css";
import Chat from "./Chat"

export default function App() {
  return (
    <div className="mainSection">
      <div className="heading">
        <img src="https://us-east-1.linodeobjects.com/gunaxin/2011/06/larry_david.jpg" className="larry-avatar"/>
        <span> Larry David</span>
      </div>  
      <Chat />
    </div>
  );
}