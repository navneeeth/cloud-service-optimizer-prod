import { Component } from 'react';
import {Link} from 'react-router-dom'
import { Doughnut, Bar } from 'react-chartjs-2';
import '../styles/Results.css'

class Results extends Component {

    textUtil(filterCompare) {
        var components = [];
        components.push(
            <p className = 'filterHeadingStyle'>Observations</p>
        );
        Object.entries(filterCompare).forEach(item => {
            var instanceName = item[0];
            var instanceValue = item[1];
            components.push(
                <div className = 's3DivStyle'>
                    <div className = 'instanceNameStyle'>{ instanceName }</div>
                    <div className = 'instanceValueStyle'>{ instanceValue + "%" }</div>
                </div>
            );
        })
        return components;
    }

    s3TextUtil(payload) {
        var components = [];
        components.push(
            <p className = 's3FilterHeadingStyle'>Selected Filters</p>
        );
        Object.entries(payload.selectedValues).forEach(item => {
            var filterName = item[0];
            var filterValue = item[1];
            components.push(
                <div className = 's3DivStyle'>
                    <div className = 'selectedS3FilterNameStyle'>{ filterName }</div>
                    <div className = 'selectedS3FilterValueStyle'>{ filterValue }</div>
                </div>
            );
        })
        components.push(
            <p className = 's3FilterHeadingStyle'>Predicted Filter</p>
        );
        Object.entries(payload.predictedValues).forEach(item => {
            var filterName = item[0];
            var filterValue = item[1];
            components.push(
                <div className = 's3DivStyle'>
                    <div className = 'predictedS3FilterNameStyle'>{ filterName }</div>
                    <div className = 'predictedS3FilterValueStyle'>{ filterValue }</div>
                </div>
            );
        })
        return components;
    }

    createData(filterName, filterData) {
        const bgColorMap = {
            "t2.nano": "#B21F00",
            "t2.micro": "#C9DE00",
            "t2.small": "#2FDE00",
            "t2.medium": "#00A6B4",
            "t2.large": "#6800B4",
            "t2.xlarge": "#FF4500",
            "db.t2.micro": "#C9DE00",
            "db.t2.small": "#2FDE00",
            "db.t2.medium": "#00A6B4",
        
        };
        const hvColorMap = {
            "t2.nano": "#501800",
            "t2.micro": "#4B5000",
            "t2.small": "#175000",
            "t2.medium": "#003350",
            "t2.large": "#35014F",
            "t2.xlarge": "#991900",
            "db.t2.micro": "#4B5000",
            "db.t2.small": "#175000",
            "db.t2.medium": "#003350",
        };


        var graphLabels = [];
        var graphData = [];
        var bgColor = [];
        var hvColor = [];

        Object.entries(filterData).forEach(item => {
            var instanceType = item[0];
            var instanceValue = item[1];

            graphLabels.push(instanceType);
            graphData.push(instanceValue);
            bgColor.push(bgColorMap[instanceType]);
            hvColor.push(hvColorMap[instanceType]);
        })

        const data = {
            labels: graphLabels,
            datasets: [
              {
                label: "",
                backgroundColor: bgColor,
                hoverBackgroundColor: hvColor,
                data: graphData
              }
            ]
        }
        
        return data;
    }

    createCharts(data, filterCompare, displayName) {
        return(
            <div>
                <div className = 'doughnutGraphStyle'>
                    <p className = 'filterStyle'>{ displayName }</p>
                    <p className = 'filterRelativeStyle'>Relative Importance of Instance Types</p>
                    <Doughnut
                        data = { data }
                        options = {{
                        title: {
                            display: true,
                            text: displayName,
                            fontSize: 20
                        },
                        legend: {
                            display: true,
                            position: 'right'
                            }
                        }}
                    />
                </div>
                <div className = 'barGraphStyle'>
                    <Bar
                        data={ data }
                        options={{
                            title:{
                                display: false,
                                text: displayName,
                                fontSize: 20
                            },
                            legend: {
                                display: false
                            },
                            tooltips: {
                                enabled: false
                            }
                        }}
                    />
                </div>
                { this.textUtil(filterCompare) }
                <br/>
                <hr className = 'hrStyle'/>
            </div>
        );
    }

    renderGraphs(data) {
        var components = [];
        Object.entries(data).forEach(item => {
            if(item[0] !== "overall") {
                var collectiveData = item[1];
                var filterData = collectiveData.data;
                var filterCompare = collectiveData.filterCompare;
                var displayName = collectiveData.displayName;

                var graphData = this.createData(displayName, filterData);
                var graphs = this.createCharts(graphData, filterCompare, displayName);
                components.push(graphs);
            }
        })
    
        return components;
    }

    renderOverall(data) {
        var collectiveData = data.overall;
        var filterData = collectiveData.data;
        var filterCompare = collectiveData.filterCompare;
        var displayName = collectiveData.displayName;

        var graphData = this.createData(displayName, filterData);
        var graph = this.createCharts(graphData, filterCompare, displayName);

        return graph;
    }
   
    render() {
        var service = this.props.location.state.service;
        var data = this.props.location.state.data;
        console.log(data);
        if(service === "Amazon S3") {
            return(
                <div>
                    <div className = 'titleDivStyle2'>
                        <h1 className = 'titleStyle2'>Results</h1>
                    </div>
                    <Link className = 'linkReturnStyle' to = "/dashboard">Return to Dashboard</Link>
                    <div className = 'graphDivStyleCharts'>
                        { this.s3TextUtil(data) }
                        <p className = 's3FilterHeadingStyle'>About S3</p>
                        <div className = 'aboutS3DivStyle'>

                            <p className = 'aboutS3TextStyle'>S3 is an Object storage built to store and retrieve any amount of data from anywhere. 
                            S3 has no instance types.<br/><br/> Amazon Simple Storage Service (Amazon S3) is an object storage service that offers industry-leading 
                            scalability, data availability, security, and performance.<br/><br/>This means customers of all sizes and industries can use it to store 
                            and protect any amount of data for a range of use cases, such as data lakes, websites, mobile applications, backup and 
                            restore, archive, enterprise applications, IoT devices, and big data analytics.<br/><br/> Amazon S3 provides easy-to-use 
                            management features so you can organize your data and configure finely-tuned access controls to meet your specific business, 
                            organizational, and compliance requirements. <br/><br/>Amazon S3 is designed for 99.999999999% (11 9's) of durability, and stores 
                            data for millions of applications for companies all around the world.<br/><br/><span style = {{color: '#F9CC88'}}>Cloud Service Optimizer</span> runs several consistent 
                            tests on S3's performance.</p>
                        </div>
                    </div> 
                </div>
            );
        }

        return(
            <div>
                <div className = 'titleDivStyle2'>
                    <h1 className = 'titleStyle2'>Results</h1>
                </div>
                <Link className = 'linkReturnStyle' to = "/dashboard">Return to Dashboard</Link>
                <p className = 'serviceTextStyle'>{ service }</p>
                <div className = 'graphDivStyleCharts'>
                    { this.renderOverall(data) }
                    { this.renderGraphs(data) }
                </div>
            </div>
        )
    };
}


export default Results;
