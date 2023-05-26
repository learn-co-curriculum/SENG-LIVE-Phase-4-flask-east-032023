import React, {useState} from 'react'
import styled from 'styled-components'
import { useHistory } from 'react-router-dom'

const initialState = {
  title: '',
  genre: '',
  budget: '',
  image: '',
  director: '',
  description: '',
}

function ProductionForm({addProduction}) {

  const history = useHistory()
  // 7.✅ Build out form to handle post request

  const [ formData, setFormData ] = useState( initialState )

  const handleFormData = event => {
    const { name, value } = event.target
    const updateFormData = {...formData, [ name ] : value }
    setFormData( updateFormData )
  }

  const handleSubmit = event => {
    event.preventDefault()
    addProduction( formData )
    setFormData( initialState )
  }

    return (
      <div className='App'>
      <Form onSubmit = { handleSubmit }>
        <label>Title </label>
        <input 
          type='text'
          name='title'
          value = { formData.title }
          onChange = { handleFormData }
          required
          />
        
        <label> Genre</label>
        <input type='text' 
        name='genre' 
        value = { formData.genre }
        onChange = { handleFormData }
        />
      
        <label>Budget</label>
        <input type='number' 
        name='budget' 
        min = '0' 
        value = { formData.budget }
        onChange = { handleFormData }
        />
      
        <label>Image</label>
        <input type='text' 
        name='image'  
        value = { formData.image }
        onChange = { handleFormData }
        />
      
        <label>Director</label>
        <input type='text' 
        name='director'
        value = { formData.director }
        onChange = { handleFormData }
        />
      
        <label>Description</label>
        <textarea type='text' rows='4' cols='50' 
        name='description' 
        value = { formData.description }
        onChange = { handleFormData }
        />
      
        <input type='submit' />
      </Form> 
      </div>
    )
  }
  
  export default ProductionForm

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