import React, {useState} from 'react'
import {useSelector, useDispatch} from 'react-redux'
import fetchRecommendations from './recommendations'
import {resetGlobalState} from './actions'
import './App.css'


const Search = () => {
  const [query, setQuery] = useState('')
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
            autoCorrect="off"
            spellCheck="false"
            type="text"
            autoFocus
            value = {query}
            placeholder="Your Reddit Username"
            onChange={event => setQuery(event.target.value)}
          />
        </div>
      </form>
  )
}

const Recommendations = (props) => {
  return (
    props.recs && props.recs.recommendations.map((item, i) => (
      <Recommendation key={i} subreddit={item.subreddit} confidence={item.confidence} />
    ))
  )
}

const Recommendation = (props) => {
  return (
    <div className="Recommendation">
      {'r/' + props.subreddit}
      {'Confidence: ' + props.confidence}
    </div>
  )
}

const Modal = ({ onClose, title, body }) => {
  return (
    <div className="overlay">
      <div className="modal">
        <button
          className="modal-close"
          type="button"
          onClick={onClose}
        >
          X
        </button>
        <div className="modal-body">{title+'--'+body}</div>
      </div>
    </div>
  )
  // return content
}

const App = () => {
  const [query, setQuery] = useState('')

  const isLoading = useSelector(state => state.loading)
  const error = useSelector(state => state.error)
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
        { error &&
          <Modal title={error.cause} body={error.body} onClose={() => dispatch(resetGlobalState())} />
        }
        { isLoading ? (
          <div>Loading ...</div>
        ) : (
          <div>
            <Recommendations recs={recommendations} />
          </div>
        )}

      </div>
    </div>
  )
}

export default App
