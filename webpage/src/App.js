import React, {useState} from 'react'
import {useSelector, useDispatch} from 'react-redux'
import fetchRecommendations from './recommendations'
import './App.css'


const Search = () => {
  const [query, setQuery] = useState('jess2187')
  const dispatch = useDispatch()
  
  return (
    <form className="Search" 
        onSubmit={event => {
          dispatch(fetchRecommendations(query)) 
          event.preventDefault()
      }}>
        <div className="SearchBox">
          <input
            className="SearchInput"
            type="text"
            value = {query}
            placeholder="Username"
            onChange={event => setQuery(event.target.value)}
          />
        </div>
      </form>
  )
}


const Recommendations = (props) => {
  return (
    props.recs && props.recs.recommendations.map((item, i) => (
      <Recommendation key ={i} subreddit={item.subreddit} confidence={item.confidence} />
    ))
  )
}

const Recommendation = (props) => {
  return (
    <div className="recommendation">
      <h3>{"r/" + props.subreddit}</h3>
      <h4>{"Confidence: " + props.confidence}</h4>
    </div>
  )
}

const Error = (props) => {
  return (
    <div>
      <h3>Something went wrong :(</h3>
    </div>
  )
}

const App = () => {
  const [query, setQuery] = useState('jess2187')

  const isLoading = useSelector(state => state.loading)
  const isError = useSelector(state => state.error)
  const username = useSelector(state => state.username)
  const recommendations = useSelector(state => state.recommendations)

  const dispatch = useDispatch()

  return (
    <div className="App">
      <div className="Header">
        <h1>Reddrec</h1>
        <p>Find new gaming subreddits!</p>
      </div>
      <Search/>
      
      <div>  
        {isError && <Error/>}

        { isLoading ? (
          <div>Loading ...</div>
        ) : (
          <div>
            <Recommendations recs={recommendations} />
            {console.log(recommendations)}
          </div>
        )}

      </div>
    </div>
  )
}

export default App
