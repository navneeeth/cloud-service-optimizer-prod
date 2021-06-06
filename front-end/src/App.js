import { Component } from 'react';
import { Router } from 'react-router-dom';
import History from './helpers/History';
import Routes from './Routes';

class App extends Component {
  render() {
    return (
      <Router history = {History}>
        <Routes />
      </Router>
    );
  }
}

export default App;
