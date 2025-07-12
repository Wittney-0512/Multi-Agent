import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import './App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>多Agent聊天演示</h1>
      </header>
      <main className="app-main">
        <ChatInterface />
      </main>
      <footer className="app-footer">
        <p>多Agent聊天演示 - React + FastAPI</p>
      </footer>
    </div>
  )
}

export default App