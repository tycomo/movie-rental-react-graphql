import React, { Component } from 'react';
import { ApolloClient } from 'apollo-client';
import { BatchHttpLink } from 'apollo-link-batch-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { ApolloProvider } from 'react-apollo';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom'
import './App.css';
import Home from '../Home/Home';
import Login from '../Login/Login';
import Logout from '../Logout/Logout';


const client = new ApolloClient({
  // By default, this client will send queries to the
  //  `/graphql` endpoint on the same host
  // Pass the configuration option { uri: YOUR_GRAPHQL_API_URL } to the `HttpLink` to connect
  // to a different host
  link: new BatchHttpLink({ uri: 'http://localhost:8000/gql' }),
  cache: new InMemoryCache(),
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
            </ul>
            <Route exact path='/' component={Home} />
            <Route exact path='/login/' component={Login} />
            <Route exact path='/logout/' component={Logout} />
          </div>
        </Router>
      </ApolloProvider>
    );
  }
}

export default App;
