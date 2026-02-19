import './assets/global.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout/Layout'
import Home from './pages/Home'
import { Hero } from './components/Hero/Hero'
import { Community } from './pages/Community'
import { Discussion } from './pages/community/Discussion'


// // Fixed: value should be string to match SelectOption type
// const options = [
//   {label: "First", value: "1"},
//   {label: "Second", value: "2"},
//   {label: "Third", value: "3"},
//   {label: "Fourth", value: "4"}
// ]

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/Hero"element={<Hero />}/>
          <Route path="/Home"element={<Hero />}/>
          <Route path="/community" element={<Community />} />
          <Route path="/community/discussion" element={<Discussion />} />
        </Routes>
        </Layout>
    </BrowserRouter>
  )
}

export default App