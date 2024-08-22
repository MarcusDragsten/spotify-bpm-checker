import React, { useState } from 'react';
import axios from 'axios';
import viteLogo from '../public/vite.svg';
import reactLogo from './assets/react.svg';

const App: React.FC = () => {
  const [count, setCount] = useState(0);
  const [data, setData] = useState<string | null>(null);
  const [playlistId, setPlaylistId] = useState<string>('');

  const fetchData = () => {
    if (playlistId) {
      axios.get(`http://127.0.0.1:8000/bpm-playlist/${playlistId}`)
        .then(response => {
          setData(response.data);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    }
  };

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <div>
        <h2>API Data:</h2>
        {data ? <p>{data}</p> : <p>Loading...</p>}
      </div>
      <div>
        <input 
          type="text" 
          value={playlistId} 
          onChange={(e) => setPlaylistId(e.target.value)} 
          placeholder="Enter playlist ID" 
        />
        <button onClick={fetchData}>Fetch Playlist Data</button>
      </div>
    </>
  );
}

export default App;