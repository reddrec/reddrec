import React from 'react'
import './App.css'

function Search() {
  return (

    <form className="Search">
      <label className="search-box">
        <input className="search-input" id="search" type="text" placeholder="Username" />
      </label>
      {/* <input className="okButton" type="submit" value="Ok" /> */}
    </form>
    
  )
}

function Recommendation(props){
  return (
    <div className="recommendation">
      <h3>{"#" + props.score + ":"}</h3>
      <h3 style={{paddingLeft:"10px"}}>{"r/" + props.subreddit}</h3>
    </div>
  )
}

function App() {
  let recommendations = [
    {
      subreddit: "animalcrossing",
      score: "1"
    },
    {
      subreddit: "nintendoswitch",
      score: "2"
    },
    {
      subreddit: "thesims",
      score: "3"
    }
  ]



  let recommendationComponents = recommendations.map((item, i) => <Recommendation key={i} {...item} />)
  
  return (
    <div className="App">
      <div className="Header">
        <h1>Reddit Recommender</h1>
        <p>Find new gaming subreddits!</p>
      </div>
      <Search/>
      {/* <img src='./loading.gif' className="App-logo" alt="logo" /> */}
      {recommendationComponents}
    </div>
  )
}

export default App;