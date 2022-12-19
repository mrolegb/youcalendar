/* eslint-disable require-jsdoc */
import React from 'react';
import './App.css';
import ChannelsForm from './forms/channels';
import Videos from './forms/videos';

function App() {
  return (
    <div className="App">
      <Videos />
      <ChannelsForm />
    </div>
  );
}

export default App;
