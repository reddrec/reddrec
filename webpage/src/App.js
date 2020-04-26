import React, {useState, useEffect} from 'react'
import fetchRecommendations from './recommendations'
import axios from 'axios'
import './App.css'

// const Search = () => {
//   return (
//     <form className="Search">
//       <label className="search-box">
//         <input className="search-input" id="search" type="text" placeholder="Username" />
//       </label>
//       {/* <input className="okButton" type="submit" value="Ok" /> */}
//     </form>
//   )
// }

const Recommendation = (props) => {
  return (
    <div className="recommendation">
      <h3>{"r/" + props.subreddit}</h3>
      <h4>{"Confidence: " + props.confidence}</h4>
    </div>
  )
}

const App = () => {
  const [data, setData] = useState(0)
  const [query, setQuery] = useState('jess2187')
  const [url, setUrl] = useState(
    '/recommend/jess2187',
  )
  const [isLoading, setIsLoading] = useState(false)
  const [isError, setIsError] = useState(false)

  useEffect(() => {
    const fetchData = async () => {
      setIsError(false)
      setIsLoading(true)
      try {
        const result = await axios(url)
        setData(result.data)
      } catch (error) {
        setIsError(true)
      }
      setIsLoading(false)
    };
    fetchData()
  }, [url])
  
  return (
    <div className="App">
      <div className="Header">
        <h1>Reddit Recommender</h1>
        <p>Find new gaming subreddits!</p>
      </div>
      <div className="Search">
        <div className="search-box">
          <input
            className="search-input"
            type="text"
            value={query}
            placeholder="Username"
            onChange={event => setQuery(event.target.value)}
          />
        </div>
        <input 
          className="okButton" 
          type="submit" 
          value="Ok" 
          onClick={() =>
            setUrl(`/recommend/${query}`)
          }/>
      </div>

      {isError && <div>Something went wrong ...</div>}
      
      { isLoading ? (
        <div>Loading ...</div>
      ) : (
        <div>
          {/* {data.recommendations.map(item => (
            <Recommendation subreddit={item.subreddit} confidence={item.confidence} />
          ))} */}
          {console.log(data)}
        </div>
      )}

      {/* <img src='./loading.gif' className="App-logo" alt="logo" /> */}
      {/* {recommendationComponents} */}
    </div>
  )
}

export default App
