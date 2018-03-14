import React from 'react';
import { Link } from 'react-router-dom';
import { Menu, Container, Dropdown } from 'semantic-ui-react'
import { gql, graphql } from 'react-apollo'

const query = gql`
query SelectedRental($id: Int!) {
    movieReview(id: $id) {
        author,
        content,
        id
  }
}
`
class SelectedRental extends React.Component {

    constructor(props) {
        super(props);
    }
    render() {
        return (
            <Container>
                <span>{this.props.movie.id}</span>
            </Container>
        )
    }
};

const queryOptions = {
    option: props => ({
        variables: {
            id: this.props.movie.id,
        },
    }),
}

SelectedRental = graphql(query, queryOptions)(SelectedRental)
export default SelectedRental;