import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './auth/AuthContext'
import Callback from './auth/Callback'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import PlaylistResults from './pages/PlaylistResults'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <div className="min-h-screen bg-spotify-black">
          <Navbar />
          <main>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/callback" element={<Callback />} />
              <Route path="/playlist/:id" element={<PlaylistResults />} />
              <Route path="*" element={<Home />} />
            </Routes>
          </main>
        </div>
      </AuthProvider>
    </BrowserRouter>
  )
}
