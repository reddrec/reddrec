import {createStore, applyMiddleware} from 'redux'
import logger from 'redux-logger'
import thunk from 'redux-thunk'
import {PERFORM_REQUEST, API_ERROR, GOT_RESULTS} from './actions'

const preloadedState = {
    loading: false,
    error: null,
    username: null,
    recommendations: null
}

const reducer = (state = {}, action) => {
    switch (action.type) {
        case PERFORM_REQUEST:
            return {
                ...state,
                username: action.username,
                loading: true
            }

        case API_ERROR:
            return {
                ...state,
                error: {
                    cause: action.cause,
                    body: action.body
                },
                loading: false
            }
        
        case GOT_RESULTS:
            return {
                ...state,
                recommendations: action.data,
                loading: false
            }

        default:
            return state
    }
}

export default createStore(reducer, preloadedState, applyMiddleware(thunk, logger))
