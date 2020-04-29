export const PERFORM_REQUEST = 'PERFORM_REQUEST'
export const API_ERROR = 'API_ERROR'
export const GOT_RESULTS = 'GOT_RESULTS'
export const RESET_STATE = 'RESET_STATE'

export const resetGlobalState = () => ({
	type: RESET_STATE
})

export const performRequest = (username) => ({
  type: PERFORM_REQUEST,
  username
})

export const apiError = (cause, body='An unknown error occurred.') => ({
  type: API_ERROR,
	cause,
	  body
})

export const gotResults = (data) => ({
  type: GOT_RESULTS,
  data
})
