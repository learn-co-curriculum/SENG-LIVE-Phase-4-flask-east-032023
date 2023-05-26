import React, { useState, useEffect } from 'react'
import styled from 'styled-components'
import { useHistory } from 'react-router-dom'

const initialState = {
  title: '',
  genre: '',
  image: '',
  budget: '',
  director: '',
  description: '',
}

function ProductionFormEdit({updateProduction, production_edit}) {
  const history = useHistory()
  const [ formProduction, setFormProduction ] = useState( initialState )
  
  useEffect( () => setFormProduction( production_edit ), [ production_edit ] )

  const handleFormChange = event => {
    const { name, value } = event.target
    const updateFormProduction = {...formProduction, [ name ]: value }
    setFormProduction( updateFormProduction )
  }


    return (
      <div className='App'>
      {/* {errors.map(error => <h2>{error}</h2>)} */}
      <Form onSubmit={ null }>
        <label>Title </label>
        <input type='text' name='title' value={ formProduction.title } onChange={ handleFormChange }  />
        
        <label> Genre</label>
        <input type='text' name='genre' value={ formProduction.genre } onChange={ handleFormChange }  />
      
        <label>Budget</label>
        <input type='number' name='budget' value={ formProduction.budget} onChange={ handleFormChange } />
      
        <label>Image</label>
        <input type='text' name='image' value={ formProduction.image } onChange={ handleFormChange }  />
      
        <label>Director</label>
        <input type='text' name='director' value={ formProduction.director } onChange={ handleFormChange }  />
      
        <label>Description</label>
        <textarea type='text' rows='4' cols='50' name='description'  value={ formProduction.description } onChange={ handleFormChange } />
      
        <input type='submit' />
      </Form> 
      </div>
    )
  }
  
  export default ProductionFormEdit

  const Form = styled.form`
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