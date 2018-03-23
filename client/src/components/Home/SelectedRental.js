import React from 'react';
import { Link } from 'react-router-dom';
import { Menu, Container, Header, Image, Grid, Button, Label } from 'semantic-ui-react'
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
            <Container className="selected">
                <Grid>
                    <Grid.Column computer={8} floated="left">
                <Header as='h1'>
                    <Header.Content>
                        {this.props.movie.title}
                        <Header.Subheader>
                            {this.props.movie.releaseDate.substring(0,4)}
                  
                            {this.props.movie.releaseDate.substring(0,4) == 2018 ?
                                <Label color='red'>New Release</Label>
                            :null}

                        </Header.Subheader>
                    </Header.Content>
                </Header>
                <div>
                <p>{this.props.movie.overview}</p>
                <Button>Rent</Button>
                </div>
                </Grid.Column>
                <Grid.Column computer={8} floated="right">
                <Image size="big" className="backdropImage" src={"https://image.tmdb.org/t/p/w500"+this.props.movie.backdropPath}/>
                </Grid.Column >
                </Grid>
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