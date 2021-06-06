import { Component } from 'react';
import '../styles/ContactUs.css'

class ContactUs extends Component {
    render() {
        return(
           
            <div>
                <div className = 'titleDivStyle1'>
                   <h1 className = 'titleStyle1'>Contact Us</h1>
                </div>
                <div className = 'qDivOverallStyle' >
                    <p className = 'qTitleStyle1' style = {{color: '#F9CC88', display: 'block'}}>Creators:</p>
                    <div className  = 'qDivStyle1'>
                        <div style = {{width: '27%'}}>
                            <p className = 'qTextStyle1' style ={{textAlign: 'right'}}>Navneeth Krishna M</p>
                            <p className = 'qTextStyle1' style ={{textAlign: 'right'}}>Nishchala M</p>
                            <p className = 'qTextStyle1' style ={{textAlign: 'right'}}>Oindrila Chakraborti</p>
                        </div>
                        <div>
                            <p className = 'qTextStyle1'>navneeth.padaki15@gmail.com</p>
                            <p className = 'qTextStyle1'>nishchalamkumar12@gmail.com</p>
                            <p className = 'qTextStyle1'>oindrila2411@gmail.com</p>
                        </div>
                    </div>
                </div>
            </div>
        )};
    }

export default ContactUs;
