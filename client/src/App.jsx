import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './App.css'

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" />
        <Route path="/signup" />
        <Route path="/" element={<div>Hello World</div>}/>
        <Route path="/dashboards/:id" />
      </Routes>
    </BrowserRouter>
  )
}

export default App
