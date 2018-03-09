import React from 'react'
import { graphql } from 'react-apollo';
import gql from 'graphql-tag';

const query = gql`
 query {
    allRentals{
      rentalDate,
      id,
      movieId
    }
  }
`

class Home extends React.Component {
  render() {
    let { data } = this.props

    if (data.loading || !data.allRentals) {
        return <div>Loading</div>
    }
    return(
        <div>
            {data.allRentals.map(rental => (
                <p key={rental.id}>{rental.id}</p>
            ))}
        </div>
    )
  }
}

export default graphql(query)(Home);