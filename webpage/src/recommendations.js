import axios from 'axios'
import {apiError, performRequest, gotResults} from './actions'

const REFRESH_TIME_MS = 500

const throwUnknownResp = (response) => {
  throw `Unknown API response ${response.status}: ${response.data}`
}

const fetchRecommendations = (username) => {
  return (dispatch) => {
		dispatch(performRequest(username))
		axios.get(`/recommend/${username}`)
			.then(response => {
				switch (response.status) {
					case 200:
						dispatch(gotResults(response.data))
						break
					case 202:
						const retry = fetchRecommendations(username)
						setTimeout(() => dispatch(retry), REFRESH_TIME_MS)
						break
					default:
						throwUnknownResp(response)
				}
			})
			.catch(error => {
				if (!error.response) {
					dispatch(apiError('Connection issue?', 'Please try again later.'))
					return
				}

				let cause
				const response = error.response

				switch (response.status) {
					case 404:
						cause = 'Not Found'
						break
					case 400:
						cause = 'Bad Request'
						break
					case 500:
						cause = 'Server broken'
						break
					default:
						throwUnknownResp(response)
				}
				dispatch(apiError(cause, response.data.error))
			})
	}
}

export default fetchRecommendations
