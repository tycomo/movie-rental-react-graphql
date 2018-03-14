import React from 'react';
import { Link } from 'react-router-dom';
import { Menu, Container, Dropdown } from 'semantic-ui-react'

let Navbar= ({activeItem}) => {
    return (
        <Menu fixed='top' inverted>
        <Container>
            <Menu.Item header>
            Movie Rental
            </Menu.Item>
            <Menu.Item as={Link} to='/'
            name='PopularMovies'>
            Popular Movies
            </Menu.Item>
            <Menu.Item as={Link} to='/login'
            name='login'>
            Login
            </Menu.Item>
            <Menu.Item as={Link} to='/logout'
            name='logout'>
            Logout
            </Menu.Item>
            <Menu.Item as={Link} to='/details'
            name='details'>
            Details
            </Menu.Item>
        </Container>
      </Menu>
    );
};

export default Navbar;
