import React, {useState} from 'react'
import {useHistory} from 'react-router-dom'
import styled from "styled-components";

const initialState = {
  name: '',
  email: ''
}

function Authentication({updateUser}) {
  const [signUp, setSignUp] = useState(false)
  const history = useHistory()

  const [ formState, setFormState ] = useState( initialState )

  const [ formErrors, setFormErrors ] = useState( null )

  const renderFormErrors = () => {
    return formErrors.map( error => <>{ error }</> )
  }

  const changeFormState = ( event ) => {
    const { name, value } = event.target
    const updateFormState = {... formState, [ name ]: value }
    setFormState( updateFormState )
  }

  // 3.4 There is a button that toggles the component between login and sign up.
  const handleClick = () => setSignUp((signUp) => !signUp)
  
  
  const userLoginOrCreation = ( event ) => {
    event.preventDefault()
    
    const postRequest = {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'accept': 'application/json'
      },
      body: JSON.stringify( formState )
    }
    
    // if signUp is true use the path '/users' else use '/login' (we will be writing login soon)
    fetch( signUp ? '/users' : '/login', postRequest )
    .then( r => r.json() )
    // Complete the post and test our '/users' route 
    // 3.4 On a successful POST add the user to state (updateUser is passed down from app through props) and redirect to the Home page.
    .then( user => {
      if ( !user.errors ) {
        updateUser( user )
        history.push( '/' )
        setFormState( initialState )
      } else {
        setFormErrors( user.errors )
      }
    })
  }
  
  // 4.✅ return to server/app.py to build the next route
  
  // 3.✅ Finish building the authentication form 
  // 3.3 on submit create a POST. 
  return (
    <> 
        <h2 style={{color:'red'}}> { formErrors ? renderFormErrors() : null }</h2>
        <h2>Please Log in or Sign up!</h2>
        <h2>{signUp?'Already a member?':'Not a member?'}</h2>
        <button onClick={handleClick}>{signUp?'Log In!':'Register now!'}</button>
        <Form onSubmit={ userLoginOrCreation }>
        <label>
          Username
          </label>
        <input type='text' name='name' value={ formState.name } onChange={ changeFormState } />
        {signUp&&(
          <>
          <label>
          Email
          </label>
          <input type='text' name='email' value={ formState.email } onChange={ changeFormState } />
          </>
        )}
        <input type='submit' value={signUp?'Sign Up!':'Log In!'} />
      </Form>
        </>
    )
}

export default Authentication

export const Form = styled.form`
display:flex;
flex-direction:column;
width: 400px;
margin:auto;
font-family:Arial;
font-size:30px;
input[type=submit]{
  background-color:#42ddf5;
  color: white;
  height:40px;
  font-family:Arial;
  font-size:30px;
  margin-top:10px;
  margin-bottom:10px;
}
`