import React from 'react'
import { gql, graphql } from 'react-apollo'
import { Container, Card, Image, Header } from 'semantic-ui-react'
import  SelectedRental  from './SelectedRental';


const query = gql`
 query {
    popularMovies{
      id,
      title,
      voteAverage,
      posterPath,
      backdropPath,
      releaseDate,
      overview
    }
  }
`

class Home extends React.Component {

  state = {
    selectedMovie: {},
    showSelected: false
  }

  selectMovie = (movie) => {
    return this.setState({selectedMovie: movie, showSelected: true})
  }

  

  render() {
    let { data } = this.props
    if (data.loading || !data.popularMovies) {
        return <div>Loading</div>
    }
    return(
        <Container>
          {this.state.showSelected ? <SelectedRental movie={this.state.selectedMovie} id={this.state.selectedMovie.id}/> : null}
          <Header as="h2">Popular Rentals</Header>
          <Card.Group itemsPerRow={5}>
            {data.popularMovies.map(movie => (
                <Card key={movie.id} onClick={() => this.selectMovie(movie)}>
                 <Image src={"https://image.tmdb.org/t/p/w500"+movie.posterPath}/>
                 <Card.Header>{movie.title}</Card.Header>
                 </Card>
            ))}
          </Card.Group>
        </Container>
    )
  }
}

export default graphql(query)(Home);