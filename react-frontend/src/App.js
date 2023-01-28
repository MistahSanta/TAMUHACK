import React, { Component } from 'react';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="rounded-square">
        <nav className="top-bar">
          <span>CBRE</span>
          <span>Dashboard</span>
          <img src="src\assets\settings-gear.svg" alt="" />
        </nav>
        <div className="main">
          <div className="flex-row">
            <nav className="sidebar">
                <span>Dashboard</span>
                <span>teams</span>
                <span>insights</span>
            </nav>

            {/*This is jonathan's part */}
            <div className="main-content">
            Testing my part

            </div>
          </div>
        </div>
      </div>

    );
  }
}

export default App;
