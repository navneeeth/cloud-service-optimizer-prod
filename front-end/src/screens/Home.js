import { Component } from 'react';
import {Link} from 'react-router-dom'
import '../styles/Home.css'
import Cloud from '../resources/cloud.png'

class Home extends Component {
    render() {
        return(
            <div style = {{height: '100%', width: '100%'}}>
                <div className = 'headerDivStyle'>
                    <p className = 'headerStyle'>CLOUD SERVICE OPTIMIZER</p>
                    <img src = { Cloud } alt = "Error" className = 'logoStyle'/>
                </div>
                <div className = 'linkDivStyle'>
                    <Link class = 'linkStyle' to = "/dashboard">Dashboard</Link>
                    <Link className = 'linkStyle' to = "/about-us">FAQs</Link>
                    <Link className = 'linkStyle' to = "/contact-us">Contact Us</Link>
                </div>
                <div className = 'introDivStyle'>
                    <p className = 'introTextStyle'>Cloud Service Selection has progressed as a cloud computing paradigm of entrusting good faith in a Cloud Service Provider (CSP) for the services with specifications that are legally agreed upon by the involved parties.<br/> The abundance of seemingly similar Cloud Services and the enormous range of customized user preferences and requirements have led to difficulty in choosing the optimal CSP. Some of the main issues faced by CC are lack of trust in service providers with respect to availability, reliability and efficiency of services at their time of need, ambiguity in SLAs, non-compliance with SLA, absence of diversified trust elements, and Quality-of-Service guarantee.<br/> Although a number of cloud service e-marketplaces are present, users find it very difficult to manually compare the services of different CSPs: especially new users who must go through each feature’s description separately during Cloud Service Provider selection.<br/><br/> This is where <span style = {{color: '#F9CC88'}}>'Cloud Service Optimizer' </span>comes into the picture to make the job quick, easy and efficient.</p>
                </div>
            </div>
        )};
    }

export default Home;
