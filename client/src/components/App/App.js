import React, { Component } from 'react';
import {
  ApolloProvider,
  ApolloClient,
  createBatchingNetworkInterface,
} from 'react-apollo'
import { BrowserRouter as Router, Route, Link } from 'react-router-dom'
import './App.css';
import Home from '../Home/Home';
import Login from '../Login/Login';
import Logout from '../Logout/Logout';
import Details from '../Details/Details';
import Navbar from '../Navbar/Navbar';

const networkInterface = createBatchingNetworkInterface({
  uri: 'http://localhost:8000/gql',
  batchInterval: 10,
  opts: {
    credentials: 'same-origin',
  },
})

networkInterface.use([
  {
    applyBatchMiddleware(req, next) {
      if (!req.options.headers) {
        req.options.headers = {}
      }

      const token = localStorage.getItem('token')
        ? localStorage.getItem('token')
        : null
      req.options.headers['authorization'] = `JWT ${token}`
      next()
    },
  },
])

const client = new ApolloClient({
  networkInterface: networkInterface,
})

class App extends Component {
  render() {
    return (
      <ApolloProvider client={client}>
        <Router>
          <div>
            <Navbar/>
            <div className="main">
            <Route exact path='/' component={Home} />
            <Route exact path='/login/' component={Login} />
            <Route exact path='/logout/' component={Logout} />
            <Route exact path='/details/' component={Details} />
            </div>
          </div>
        </Router>
      </ApolloProvider>
    );
  }
}

export default App;
