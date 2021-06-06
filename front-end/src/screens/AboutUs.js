import { Component } from 'react';
import '../styles/AboutUs.css'

class AboutUs extends Component {

    render() {
        return(
            
            <div>
                <div className = 'titleDivStyle'>
                    <h1 className = 'titleStyle'>FAQs</h1>
                </div>
                <div className = 'qDivStyle'>
                    <p className = 'qTitleStyle' style = {{color: '#F9CC88'}}>Answer a few questions on the dashboard to get started right now!</p>
                    <p className = 'qTitleStyle' style = {{color: '#F9CC88'}}>For EC2 and RDS:</p>
                    <p className = 'qTextStyle'>1. What AWS Service are you looking for?</p>
                    <p className = 'qTextStyle'>Clicking on the 'Select Service' Button will display the services which are available for comparison and calculation of trustworthy metric. Select the service as per your requirement.</p>
                    <p className = 'qTextStyle'>2. What performance metric do you want us to focus on?</p>
                    <p className = 'qTextStyle'>Select from a wide range of available Filters and assign priority based on how important each attribute is for your business requirement. Checking the 'Assign same priority to all filters' will assign same priority to all attributes. Don't forget to select the filters that you want to apply after this step. Individual priorities can also be assigned by unchecking the above checkbox, clicking on each filter and filling the priority numbers (Integer type in range [1, n]: 1 being the highest priority, n ≤ Total number of Filters available) in the textboxes which appear beside them. To deselect any filter, simply click again on the selected one.</p>
                    <p className = 'qTextStyle'>3. What instance types of the above listed AWS service do you want? </p>
                    <p className = 'qTextStyle'>Select the instance types that you want compare between and click on Save. If no instances are selected all of the shown instances will be automatically chosen for Trustworthiness Evaluation.</p>
                    <p className = 'qTextStyle'>After successfully uploading the above data, click on Show Results to assess the trustworthiness value and graphical results of the comparison.</p>
                    <p className = 'qTitleStyle' style = {{color: '#F9CC88'}}>For S3:</p>
                    <p className = 'qTextStyle'>1. What AWS Service are you looking for?</p>
                    <p className = 'qTextStyle'>Clicking on the 'Select Service' Button will display the services which are available for comparison and calculation of trustworthy metric. Select S3.</p>
                    <p className = 'qTextStyle'>2. What metric should ML Prediction be applied to?</p>
                    <p className = 'qTextStyle'>For S3, Users must choose n-1 (n being the total number of attributes) filters and must provide the values for each of the selected filters. The value of the only 1 remaining filter is predicted. Here, priorities can be positive Integers or Decimal values.</p>
                    <p className = 'qTextStyle'>Allowed values for the selected filters:</p>
                    <p className = 'qTextStyle'>Consistency (stdDev): 100 to 1000. Here, 100 indicates a low level of Consistency and 1000 indicates a high level of Consistency. Knowing the standard deviation of your data set tells you how densely the data points are clustered around the mean. The smaller the standard deviation, the more consistent the data. </p>
                    <p className = 'qTextStyle'>Error Rate (errorRate): 0 to 100. Here, 0 refers to low error rate and 100 refers to high error rate. It is the percentage value of errors caused due to various reasons when connecting to the backend hosted by a service type. Total percentage of errors found for a particular sample request. 0.0% shows that all requests completed successfully. Total equals the percentage of error samples in all samples.</p>
                    <p className = 'qTextStyle'>Latency (Latency): 0 to 300. Here, 0 refers to a low level of Latency and 300 refers to a high level of Latency. JMeter measures the latency from just before sending the request to just after the first response has been received. Thus, the time includes all the processing needed to assemble the request as well as assembling the first part of the response, which in general will be longer than one byte. Protocol analysers (such as Wireshark) measure the time when bytes are actually sent/received over the interface. The JMeter time should be closer to that which is experienced by a browser or other application client.</p>
                    <p className = 'qTextStyle'>Elapsed Time (elapsed): 0 to 300. Here, 0 refers to low Elapsed time and 300 refers to high Elapsed time. JMeter measures the elapsed time from just before sending the request to just after the last response has been received. JMeter does not include the time needed to render the response, nor does JMeter process any client code, for example JavaScript.</p>
                    <p className = 'qTextStyle'>Connection Time (Connect): 0 to 300. Here, 0 refers to the low level of Connection Time and 300 refers to the high level of Connection time. JMeter measures the time it took to establish the connection, including SSL handshake. Note that connect time is not automatically subtracted from latency. In case of connection error, the metric will be equal to the time it took to face the error, for example in case of Timeout, it should be equal to connection timeout.</p>
                    <p className = 'qTextStyle'>Throughput (Throughput): 0 to 5000. Here, 0 refers to a low level of Throughput and 5000 refers to a high level of Throughput. Hits/sec, or total number of requests per unit of time (sec, mins, hr) sent successfully to server during test.</p>
                    <p className = 'qTextStyle' style = {{color: '#F9CC88'}}>After selecting the filters, press Save to upload the data. Click on Show Results to assess the trustworthiness value and graphical results of the comparison.</p>
                </div>
            </div>
        )
    };
}


export default AboutUs;
