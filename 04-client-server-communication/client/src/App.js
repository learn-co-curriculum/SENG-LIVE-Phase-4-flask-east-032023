// 📚 Review With Students:
    // Request response cycle
    //Note: This was build using v5 of react-router-dom
import { Route, Switch, useHistory } from 'react-router-dom'
import {createGlobalStyle} from 'styled-components'
import {useEffect, useState} from 'react'
import Home from './components/Home'
import ProductionForm from './components/ProductionForm'
import ProductionEdit from './components/ProductionEdit'
import Navigation from './components/Navigation'
import ProductionDetail from './components/ProductionDetail'
import NotFound from './components/NotFound'

const baseUrl = 'http://localhost:5555/'
const productionsUrl = baseUrl + 'productions'


function App() {
  const [productions, setProductions] = useState([])
  const [production_edit, setProductionEdit] = useState(false)
  const history = useHistory()
  //5.✅ GET Productions

  useEffect( () => fetchProductions(), [] )

  const fetchProductions = ( ) => 
    fetch( productionsUrl )
    .then( r => r.json() )
    .then( setProductions )
  
  // 6.✅ navigate to client/src/components/ProductionForm.js

  const addProduction = ( production ) => {

    const postRequest = {
      method: 'post',
      headers: {
        'content-type': 'application/json',
        'accept': 'application/json'
      },
      body: JSON.stringify( production )
    }

    fetch( productionsUrl, postRequest )
    .then( r => r.json() )
    .then( newProduction => setProductions( [...productions, newProduction ] ) )
  }


  const updateProduction = (updated_production) => setProductions(productions => productions.map(production =>{
    if(production.id == updated_production.id){
      return updated_production
    } else {
      return production
    }
  } ))


  const deleteProduction = ( id ) => {
    
    const deleteRequest = {
      method: 'DELETE',
    }

    fetch( productionsUrl + `/${ id }` , deleteRequest )
    .then( () => { 
      const removeProduction = productions.filter( production => production.id !== id) 
      setProductions( removeProduction )
      history.push( '/' )
    })

  }

  const handleEdit = (production) => {
    setProductionEdit(production)
    history.push(`/productions/edit/${production.id}`)
  }
  return (
    <>
    <GlobalStyle />
    <Navigation handleEdit={handleEdit}/>
      <Switch>
        <Route  path='/productions/new'>
          <ProductionForm addProduction={addProduction}/>
        </Route>
        <Route  path='/productions/edit/:id'>
          <ProductionEdit updateProduction={updateProduction} production_edit={production_edit}/>
        </Route>
        <Route path='/productions/:id'>
            <ProductionDetail handleEdit={handleEdit} deleteProduction={deleteProduction} productionsUrl = { productionsUrl }/>
        </Route>
        <Route exact path='/'>
          <Home  productions={productions} />
        </Route>
        <Route>
          <NotFound />
        </Route>
      </Switch>
    </>
  )
}

export default App

const GlobalStyle = createGlobalStyle`
    body{
      background-color: black; 
      color:white;
    }
    `

