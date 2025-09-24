import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import { BrowserRouter, Routes, Route, Outlet, Link } from "react-router-dom";
function Home() {
  return (
    <div>
      <h1>Home</h1>
      <nav>
        <Link to="dashboard">Dashboard</Link> |{" "}
        <Link to="profile">Profile</Link>
      </nav>
      <Outlet />
    </div>
  );
}

function Dashboard() {
  return <div>Dashboard Page</div>;
}

function Profile() {
  return <div>Profile Page</div>;
}

function App() {

  return (
   <BrowserRouter>
      <Routes>
        <Route path="home" element={<Home />}>
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="profile" element={<Profile />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
