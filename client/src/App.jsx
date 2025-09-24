import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './App.css'
import HomePage from './pages/Home'

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<div>Here is our login page</div>} />
        <Route path="/signup" />
        <Route path="/" element={<HomePage />}/>
        <Route path="/dashboards/:id" />
      </Routes>
    </BrowserRouter>
  )
}

export default App