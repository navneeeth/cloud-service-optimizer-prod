import { Component, React } from "react";
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom';
import ContactUs from "./screens/ContactUs";
import Home from './screens/Home';
import AboutUs from './screens/AboutUs';
import Dashboard from './screens/Dashboard';
import Results from './screens/Results';

class Routes extends Component {
    render() {
        return (
            <Router>
                <Switch>
                    <Route path = "/" exact component = {Home} />
                    <Route path = "/about-us" component = {AboutUs} />
                    <Route path = "/contact-us" component = {ContactUs} />
                    <Route path = "/dashboard" component = {Dashboard} />
                    <Route path = "/results" component = {Results} />
                </Switch>
            </Router>
            // <Switch>
            //     <Route path="/" exact component={Home} />
            //     <Route component={Home} />
            // </Switch>
        );
    }
}

export default Routes;