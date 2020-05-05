import React, {useState} from 'react'
import {useSelector, useDispatch} from 'react-redux'
import fetchRecommendations from './recommendations'
import {resetGlobalState} from './actions'
import './App.css'

const Search = ({isLoading}) => {
  const [query, setQuery] = useState('')
  const dispatch = useDispatch()

  return (
    <form className='Search'
        onSubmit={event => {
          dispatch(fetchRecommendations(query))
          event.preventDefault()
      }}>
        <div className='SearchBox'>
          <input
            className='SearchInput'
            autoCorrect='off'
            spellCheck='false'
            type='text'
            disabled= {isLoading && 'disabled'}
            autoFocus
            value = {query}
            placeholder='Your Reddit Username'
            onChange={event => setQuery(event.target.value)}
          />
        </div>
      </form>
  )
}

const Modal = ({ onClose, title, body }) => {
  return (
    <div className='Overlay'>
      <div className='Modal'>

        <div className='ModalBody'>
          <button
            className='ModalClose'
            type='button'
            onClick={onClose}
          >
            X
          </button>
          {/* <br></br> */}
          <div className='ModalContent'>
            <h1>{title}</h1>
            <h2>{body}</h2>
          </div>
        </div>
      </div>
    </div>
  )
  // return content
}

const Recommendations = (props) => {
  if (props.recs && props.recs.recommendations.length == 0) {
    return <h2>Sorry, that user isn't much of a gamer.</h2>
  }

  const rec = props.recs && props.recs.recommendations.map((item, i) => (
    <Recommendation key={i} subreddit={item.subreddit} confidence={item.confidence} />
  ))
  return (
    <div className='Recommendations'>
      {props.recs && <h1>{props.recs.username + '’s recommendations'}</h1>}
      {rec}
    </div>
  )
}

const Recommendation = (props) => {
  return (
    <div className='Recommendation'>
      <a href={'https://www.reddit.com/r/'+ props.subreddit + '/'} target={'_blank'}>{'r/' + props.subreddit}</a>
      <p>{'Confidence: ' + props.confidence}</p>
    </div>
  )
}

const App = () => {
  const isLoading = useSelector(state => state.loading)
  const error = useSelector(state => state.error)
  const recommendations = useSelector(state => state.recommendations)

  const dispatch = useDispatch()

  return (
    <div className='App'>
      <div className='Header'>
        <h1>Reddrec</h1>
        <p>Find new gaming subreddits!</p>
      </div>
      <Search isLoading={isLoading}/>

      <div>
        { error &&
          <Modal title={error.cause} body={error.body} onClose={() => dispatch(resetGlobalState())} />
        }
        { isLoading ? (
          <img src='../loading-png-gif.gif' height='50' width='50'></img>
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
