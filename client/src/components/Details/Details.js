import React from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag';

// This is new:
const mutation = gql`
mutation Details($movieId: Int!) {
  createRental(message: $message) {
    status,
    formErrors,
    message {
      id
    }
  }
}
`
const query = gql`
{
  currentUser {
    id
  }
}
`
class Details extends React.Component {
    componentWillUpdate(nextProps) {
        if (!nextProps.data.loading && nextProps.data.currentUser === null) {
        window.location.replace('/login/')
        }
    }

    handleSubmit(e) {
        e.preventDefault()
        let data = new FormData(this.form)
        this.props
            .mutate({ variables: { message: data.get('message') } })
            .then(res => {
                if (res.data.createMessage.status === 200) {
                    window.location.replace('/')
                }
                if (res.data.createMessage.status === 400) {
                this.setState({
                    formErrors: JSON.parse(res.data.createMessage.formErrors),
                    })
                }
            })
            .catch(err => {
            console.log('Network error')
            })
    }

    render() {
        // This is new:
        let { data } = this.props
        if (data.loading || data.currentUser === null) {
          return <div>Loading...</div>
        }
        return (
          <div>
            <h1>Create Rental</h1>
            <form
              ref={ref => (this.form = ref)}
              onSubmit={e => this.handleSubmit(e)}
            >
              <div>
                <label>Movie Id:</label>
                <input type="text" name="movieId" />
              </div>
              <button type="submit">Rent Movie</button>
            </form>
          </div>
        )
    }
}

Details = graphql(query)(Details)
Details = graphql(mutation)(Details) 
export default Details