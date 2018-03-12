import React, { Component } from 'react';
import { ApolloClient } from 'apollo-client';
import { BatchHttpLink } from 'apollo-link-batch-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
//import { createHttpLink } from 'apollo-link-http';
import { setContext } from 'apollo-link-context';
import { ApolloProvider } from 'react-apollo';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom'
import './App.css';
import Home from '../Home/Home';
import Login from '../Login/Login';
import Logout from '../Logout/Logout';
import Details from '../Details/Details';

const httpLink = BatchHttpLink({
  uri: 'http://localhost:8000/gql',
});

const authLink = setContext((_, { headers }) => {
  // get the authentication token from local storage if it exists
  const token = localStorage.getItem('token');
  // return the headers to the context so httpLink can read them
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : "",
    }
  }
});

const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache()
});

class App extends Component {
  render() {
    return (
      <ApolloProvider client={client}>
        <Router>
          <div>
            <ul>
              <li><Link to='/'>Home</Link></li>
              <li><Link to='/login/'>Login</Link></li>
              <li><Link to='/logout/'>Logout</Link></li>
              <li><Link to='/details/'>Details</Link></li>
            </ul>
            <Route exact path='/' component={Home} />
            <Route exact path='/login/' component={Login} />
            <Route exact path='/logout/' component={Logout} />
            <Route exact path='/details/' component={Details} />
          </div>
        </Router>
      </ApolloProvider>
    );
  }
}

export default App;
