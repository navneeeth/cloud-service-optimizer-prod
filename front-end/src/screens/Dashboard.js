import { Component } from 'react';
import axios from 'axios'
import { Route } from 'react-router-dom'
import '../styles/Dashboard.css'

class Dashboard extends Component {

    constructor() {
        super();
        var ec2 = "Amazon EC2";
        var s3 = "Amazon S3";
        var rds = "Amazon RDS";

        var defaultJson = {}
        defaultJson[ec2] = {
            "overall": {
                "filterCompare": {
                    "t2.xlarge > t2.large": "72.02",
                    "t2.xlarge > t2.medium": "95.27",
                    "t2.xlarge > t2.small": "112.5",
                    "t2.xlarge > t2.micro": "115.67",
                    "t2.xlarge > t2.nano": "131.2",
                    "t2.large > t2.medium": "13.51",
                    "t2.large > t2.small": "23.53",
                    "t2.large > t2.micro": "25.37",
                    "t2.large > t2.nano": "34.4",
                    "t2.medium > t2.small": "8.82",
                    "t2.medium > t2.micro": "10.45",
                    "t2.medium> t2.nano": "18.4",
                    "t2.small > t2.micro": "1.49",
                    "t2.small > t2.nano": "8.8",
                    "t2.micro > t2.nano": "7.2"
                },
                "data": {
                    "t2.xlarge": 0.289,
                    "t2.large": 0.168,
                    "t2.medium": 0.148,
                    "t2.small": 0.136,
                    "t2.micro": 0.134,
                    "t2.nano": 0.125
                },
                "displayName": "Overall"
            },
            "stdDev": {
                "filterCompare": {
                    "t2.xlarge > t2.micro": "88.59",
                    "t2.xlarge > t2.large": "93.79",
                    "t2.xlarge > t2.small": "96.5",
                    "t2.xlarge > t2.medium": "99.29",
                    "t2.micro > t2.large": "2.76",
                    "t2.micro > t2.small": "4.2",
                    "t2.micro > t2.medium": "5.67",
                    "t2.large > t2.small": "1.4",
                    "t2.large > t2.medium": "2.84",
                    "t2.small > t2.medium": "1.42",
                    "t2.medium > t2.medium": "0.0"
                },
                "data": {
                    "t2.xlarge": 0.281,
                    "t2.micro": 0.149,
                    "t2.large": 0.145,
                    "t2.small": 0.143,
                    "t2.nano": 0.141,
                    "t2.medium": 0.141
                },
                "displayName": "Consistency"
            },
            "errorRate": {
                "filterCompare": {
                    "t2.micro > t2.small": "3.55",
                    "t2.micro > t2.medium": "4.17",
                    "t2.micro > t2.xlarge": "14.38",
                    "t2.small > t2.medium": "0.6",
                    "t2.small > t2.xlarge": "10.46",
                    "t2.medium > t2.medium": "0.0",
                    "t2.medium > t2.xlarge": "9.8"
                },
                "data": {
                    "t2.micro": 0.175,
                    "t2.small": 0.169,
                    "t2.nano": 0.168,
                    "t2.large": 0.168,
                    "t2.medium": 0.168,
                    "t2.xlarge": 0.153
                },
                "displayName": "Error Rate"
            },
            "Throughput": {
                "filterCompare": {
                    "t2.xlarge > t2.large": "53.16",
                    "t2.xlarge > t2.small": "56.13",
                    "t2.xlarge > t2.medium": "61.33",
                    "t2.xlarge > t2.micro": "62.42",
                    "t2.xlarge > t2.nano": "65.75",
                    "t2.large > t2.small": "1.94",
                    "t2.large > t2.medium": "5.33",
                    "t2.large > t2.micro": "6.04",
                    "t2.large > t2.nano": "8.22",
                    "t2.small > t2.medium": "3.33",
                    "t2.small > t2.micro": "4.03",
                    "t2.small > t2.nano": "6.16",
                    "t2.medium > t2.micro": "0.67",
                    "t2.medium > t2.nano": "2.74",
                    "t2.micro > t2.nano": "2.05"
                },
                "data": {
                    "t2.xlarge": 0.242,
                    "t2.large": 0.158,
                    "t2.small": 0.155,
                    "t2.medium": 0.15,
                    "t2.micro": 0.149,
                    "t2.nano": 0.146
                },
                "displayName": "Throughput"
            },
            "elapsed": {
                "filterCompare": {
                    "t2.xlarge > t2.micro": "64.71",
                    "t2.xlarge > t2.small": "65.79",
                    "t2.xlarge > t2.medium": "69.13",
                    "t2.xlarge > t2.nano": "73.79",
                    "t2.micro > t2.small": "0.66",
                    "t2.micro > t2.medium": "2.68",
                    "t2.micro > t2.nano": "5.52",
                    "t2.small > t2.medium": "2.01",
                    "t2.small > t2.nano": "4.83",
                    "t2.medium > t2.medium": "0.0",
                    "t2.medium > t2.nano": "2.76"
                },
                "data": {
                    "t2.xlarge": 0.252,
                    "t2.micro": 0.153,
                    "t2.small": 0.152,
                    "t2.large": 0.149,
                    "t2.medium": 0.149,
                    "t2.nano": 0.145
                },
                "displayName": "Elapsed Time"
            },
            "Latency": {
                "filterCompare": {
                    "t2.xlarge > t2.nano": "111.97",
                    "t2.xlarge > t2.small": "115.0",
                    "t2.xlarge > t2.large": "116.55",
                    "t2.xlarge > t2.medium": "118.12",
                    "t2.nano > t2.small": "1.43",
                    "t2.nano > t2.large": "2.16",
                    "t2.nano > t2.medium": "2.9",
                    "t2.small > t2.small": "0.0",
                    "t2.small > t2.large": "0.72",
                    "t2.small > t2.medium": "1.45",
                    "t2.large > t2.medium": "0.72"
                },
                "data": {
                    "t2.xlarge": 0.301,
                    "t2.nano": 0.142,
                    "t2.micro": 0.14,
                    "t2.small": 0.14,
                    "t2.large": 0.139,
                    "t2.medium": 0.138
                },
                "displayName": "Latency"
            },
            "Connect": {
                "filterCompare": {
                    "t2.xlarge > t2.micro": "61.69",
                    "t2.xlarge > t2.small": "63.82",
                    "t2.xlarge > t2.medium": "67.11",
                    "t2.xlarge > t2.nano": "69.39",
                    "t2.micro > t2.small": "1.32",
                    "t2.micro > t2.medium": "3.36",
                    "t2.micro > t2.nano": "4.76",
                    "t2.small > t2.medium": "2.01",
                    "t2.small > t2.nano": "3.4",
                    "t2.medium > t2.medium": "0.0",
                    "t2.medium > t2.nano": "1.36"
                },
                "data": {
                    "t2.xlarge": 0.249,
                    "t2.micro": 0.154,
                    "t2.small": 0.152,
                    "t2.large": 0.149,
                    "t2.medium": 0.149,
                    "t2.nano": 0.147
                },
                "displayName": "Connection Time"
            },
            "CPU": {
                "filterCompare": {
                    "t2.xlarge > t2.large": "83.25",
                    "t2.xlarge > t2.medium": "114.72",
                    "t2.xlarge > t2.small": "221.1",
                    "t2.xlarge > t2.micro": "243.14",
                    "t2.xlarge > t2.nano": "306.98",
                    "t2.large > t2.medium": "17.18",
                    "t2.large > t2.small": "75.23",
                    "t2.large > t2.micro": "87.25",
                    "t2.large > t2.nano": "122.09",
                    "t2.medium > t2.small": "49.54",
                    "t2.medium > t2.micro": "59.8",
                    "t2.medium > t2.nano": "89.53",
                    "t2.small > t2.micro": "6.86",
                    "t2.small > t2.nano": "26.74",
                    "t2.micro > t2.nano": "18.6"
                },
                "data": {
                    "t2.xlarge": 0.35,
                    "t2.large": 0.191,
                    "t2.medium": 0.163,
                    "t2.small": 0.109,
                    "t2.micro": 0.102,
                    "t2.nano": 0.086
                },
                "displayName": "CPU Utilization"
            },
            "memory": {
                "filterCompare": {
                    "t2.xlarge > t2.large": "96.37",
                    "t2.xlarge > t2.medium": "289.6",
                    "t2.xlarge > t2.small": "616.18",
                    "t2.xlarge > t2.micro": "958.7",
                    "t2.xlarge > t2.nano": "1773.08",
                    "t2.large > t2.medium": "98.4",
                    "t2.large > t2.small": "264.71",
                    "t2.large > t2.micro": "439.13",
                    "t2.large > t2.nano": "853.85",
                    "t2.medium > t2.small": "83.82",
                    "t2.medium > t2.micro": "171.74",
                    "t2.medium > t2.nano": "380.77",
                    "t2.small > t2.micro": "47.83",
                    "t2.small > t2.nano": "161.54",
                    "t2.micro > t2.nano": "76.92"
                },
                "data": {
                    "t2.xlarge": 0.487,
                    "t2.large": 0.248,
                    "t2.medium": 0.125,
                    "t2.small": 0.068,
                    "t2.micro": 0.046,
                    "t2.nano": 0.026
                },
                "displayName": "memory"
            }
        };
        defaultJson[s3] = {
            "predictedValues": {
                "Consistency": "425.82"
            },
            "selectedValues": {
                "Connection Time": 24.0,
                "Elapsed Time": 2116.0,
                "Error Rate": 83.0,
                "Latency": 28.0,
                "Throughput": 36.0
            }     
        };
        defaultJson[rds] = {
            "Connect": {
                "data": {
                    "db.t2.medium": 0.34,
                    "db.t2.micro": 0.32,
                    "db.t2.small": 0.339
                },
                "displayName": "Connection Time",
                "filterCompare": {
                    "db.t2.medium > db.t2.micro": "6.25",
                    "db.t2.medium > db.t2.small": "0.29",
                    "db.t2.small > db.t2.micro": "5.94"
                }
            },
            "Latency": {
                "data": {
                    "db.t2.medium": 0.311,
                    "db.t2.micro": 0.392,
                    "db.t2.small": 0.297
                },
                "displayName": "Latency",
                "filterCompare": {
                    "db.t2.medium > db.t2.small": "4.71",
                    "db.t2.micro > db.t2.medium": "26.05",
                    "db.t2.micro > db.t2.small": "31.99"
                }
            },
            "Throughput": {
                "data": {
                    "db.t2.medium": 0.325,
                    "db.t2.micro": 0.345,
                    "db.t2.small": 0.329
                },
                "displayName": "Throughput",
                "filterCompare": {
                    "db.t2.micro > db.t2.medium": "6.15",
                    "db.t2.micro > db.t2.small": "4.86",
                    "db.t2.small > db.t2.medium": "1.23"
                }
            },
            "elapsed": {
                "data": {
                    "db.t2.medium": 0.341,
                    "db.t2.micro": 0.321,
                    "db.t2.small": 0.338
                },
                "displayName": "Elapsed Time",
                "filterCompare": {
                    "db.t2.medium > db.t2.micro": "6.23",
                    "db.t2.medium > db.t2.small": "0.89",
                    "db.t2.small > db.t2.micro": "5.3"
                }
            },
            "errorRate": {
                "data": {
                    "db.t2.medium": 0.284,
                    "db.t2.micro": 0.403,
                    "db.t2.small": 0.313
                },
                "displayName": "Error Rate",
                "filterCompare": {
                    "db.t2.micro > db.t2.medium": "41.9",
                    "db.t2.micro > db.t2.small": "28.75",
                    "db.t2.small > db.t2.medium": "10.21"
                }
            },
            "overall": {
                "data": {
                    "db.t2.medium": 0.315,
                    "db.t2.micro": 0.361,
                    "db.t2.small": 0.325
                },
                "displayName": "Overall",
                "filterCompare": {
                    "db.t2.micro > db.t2.medium": "14.6",
                    "db.t2.micro > db.t2.small": "11.08",
                    "db.t2.small > db.t2.medium": "3.17"
                }
            },
            "stdDev": {
                "data": {
                    "db.t2.medium": 0.284,
                    "db.t2.micro": 0.383,
                    "db.t2.small": 0.333
                },
                "displayName": "Consistency",
                "filterCompare": {
                    "db.t2.micro > db.t2.medium": "34.86",
                    "db.t2.micro > db.t2.small": "15.02",
                    "db.t2.small > db.t2.medium": "17.25"
                }
            }
        };

        this.ec2 = ec2;
        this.s3 = s3;
        this.rds = rds;
        this.defaultResponse = defaultJson;
        

        this.state = {
          showHideServices: false, showHideFilters: false, showHideInstances: false,
          selectEC2: false, selectS3: false, selectRDS: false,
          selectConsistency: false, selectErrorRate: false, selectLatency: false, selectElapsedTime: false, selectConnectionTime: false, selectThroughput: false, selectCpu: false, selectMemory:false,
          checkbox: true, filterAlert: "", serviceAlert: "", instanceAlert: "",
          selectT2Micro: false, selectT2Nano: false, selectT2Small: false, selectT2Medium: false, selectT2Large: false, selectT2XLarge: false,
          calculateState: 0, response: {}
        };

        this.hideComponent = this.hideComponent.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.handleCalculate = this.handleCalculate.bind(this);
        this.calculateButton = this.calculateButton.bind(this);
    }

    calculateButton() {
        switch(this.state.calculateState) {
            case 0:
                return(
                    <div className = 'calculateDivStyle'>
                        <button className = 'calculateButtonStyle' onClick={() => {
                            this.handleCalculate(); 
                        }}>Save</button>
                    </div>
                );
            case 1:
                return(
                    <div className = 'calculateDivStyle'>
                        <p className='alertStyle'>Processing...</p>
                    </div>
                );
            case 2:
                return(
                    <Route render={({ history }) => (
                        <div className = 'calculateDivStyle'>
                            <button className = 'calculateButtonStyle' onClick={() => {
                                history.push({
                                    pathname:'./results',
                                    state: { data: this.state.response, service: this.getService() }
                                }) 
                            }}>Show Results</button>
                        </div>
                    )}/>
                );
            case 3:
                return(
                    <div className = 'calculateDivStyle'>
                        <button className = 'calculateButtonStyle' onClick={() => {
                            this.handleCalculate(); 
                        }}>Save</button>
                        <p className='lastAlertStyle'>Processing failed. Try again.</p>
                    </div>
                );
            default: console.log("Invalid calculate button state");

        }
    }

    getService() {
        if(this.state.selectEC2 === true)
            return this.ec2;
        else if(this.state.selectS3 === true)
            return this.s3;
        else if(this.state.selectRDS === true)
            return this.rds;

    }

    validateEntry(checkboxVal, lowerLimit, upperLimit) {
        var reg = new RegExp('^\\d+$');
        var regS3 = new RegExp('^\\d+(\\.\\d+)?$');
        var otherLimit;
        
        if(this.state.selectEC2 === true)
            otherLimit = 8;
        else if(this.state.selectRDS === true)
            otherLimit = 6;
        if(this.state.selectS3  === true) 
            return regS3.test(checkboxVal) && parseFloat(checkboxVal) >= lowerLimit && parseFloat(checkboxVal) <= upperLimit;
        else
            return reg.test(checkboxVal) && parseInt(checkboxVal) > 0 && parseInt(checkboxVal) <= otherLimit;
    }

    hideComponent(name) {
        switch (name) {
            case "showHideServices":
                this.setState({ showHideServices: !this.state.showHideServices });
                break;
            case "showHideFilters":
                this.setState({ showHideFilters: !this.state.showHideFilters });
                break;
            case "showHideInstances":
                this.setState({ showHideInstances: !this.state.showHideInstances });
                break;
            default: console.log("Invalid show and hide scenario");
        }
      }

    handleClick(name) {
        switch(name) {
            case "EC2":
                this.setState({ 
                    selectEC2: !this.state.selectEC2, selectS3:  false, selectRDS: false});
                break;
            case "S3":
                this.setState({ selectS3: !this.state.selectS3, selectEC2:  false, selectRDS: false });
                break;
            case "RDS":
                this.setState({ selectRDS: !this.state.selectRDS, selectEC2:  false, selectS3: false });
                break;
            case "Consistency":
                this.setState({ selectConsistency: !this.state.selectConsistency });
                break;
            case "Error Rate":
                this.setState({ selectErrorRate: !this.state.selectErrorRate });
                break;
            case "Latency":
                this.setState({ selectLatency: !this.state.selectLatency });
                break;
            case "Elapsed Time":
                this.setState({ selectElapsedTime: !this.state.selectElapsedTime });
                break;
            case "Connection Time": 
                this.setState({ selectConnectionTime: !this.state.selectConnectionTime });
                break;
            case "Throughput": 
                this.setState({ selectThroughput: !this.state.selectThroughput });
                break;
            case "CPU Utilization": 
                this.setState({ selectCpu: !this.state.selectCpu });
                break;
            case "Memory": 
                this.setState({ selectMemory: !this.state.selectMemory });
                break;
            case "T2Nano":
                this.setState({ selectT2Nano: !this.state.selectT2Nano });
                break;
            case "T2Micro":
                this.setState({ selectT2Micro: !this.state.selectT2Micro });
                break;
            case "T2Small":
                this.setState({ selectT2Small: !this.state.selectT2Small });
                break;
            case "T2Medium":
                this.setState({ selectT2Medium: !this.state.selectT2Medium });
                break;
            case "T2Large":
                this.setState({ selectT2Large: !this.state.selectT2Large });
                break;
            case "T2XLarge":
                this.setState({selectT2XLarge: !this.state.selectT2XLarge});
                break;
            default: console.log("null");
        }
    }

    handleCalculate() {
        
        this.setState({calculateState: 1});
        var timestamp;
        var filters = "";
        var priorities = "";
        var serviceType = "";
        var instanceType = "";
        if(this.state.selectS3!==true && this.state.selectRDS!==true && this.state.selectEC2!==true)
        {  this.setState({ serviceAlert: "Please select at least one service.", calculateState: 0 }); return; }
        else
            this.setState({ serviceAlert: "Service type noted!" }); 
        if(this.state.selectEC2===true)
        {   var ec2 = 0;
           serviceType = "ec2";
            if(this.state.selectT2Micro===true)
             { instanceType += "t2.micro,"; ec2 = ec2 + 1; } 
            if(this.state.selectT2Nano===true)
             { instanceType += "t2.nano,"; ec2 = ec2 + 1; }
            if(this.state.selectT2Small===true)
             { instanceType += "t2.small,"; ec2 = ec2 + 1; }
            if(this.state.selectT2Medium===true)   
             { instanceType += "t2.medium,"; ec2 = ec2 + 1; }
            if(this.state.selectT2Large===true)
             { instanceType += "t2.large,"; ec2 = ec2 + 1; }
            if(this.state.selectT2XLarge===true)
             { instanceType += "t2.xlarge,"; ec2 = ec2 + 1; }
            if(this.state.selectT2Micro===false && this.state.selectT2Nano===false && this.state.selectT2Small===false
                && this.state.selectT2Medium===false && this.state.selectT2Large===false && this.state.selectT2XLarge===false)
             {
                instanceType = "t2.nano,t2.micro,t2.small,t2.medium,t2.large,t2.xlarge,";
                ec2 = 0;
                this.setState({ instanceAlert: "" });
            }
            if(ec2 === 1) {
                this.setState({ instanceAlert: "Please select two or more instance types for comparison.", calculateState: 0 }); 
                return;
            }
            else
                this.setState({ instanceAlert: "Instance types noted!" });
        }
        else if(this.state.selectS3===true) {
            this.setState({ selectCpu: false, selectMemory: false });
            serviceType = "s3";
            instanceType = "na,";
        }
        else if(this.state.selectRDS===true)
        {  
            this.setState({ selectCpu: false, selectMemory: false, selectT2Large: false, selectT2Nano: false, selectT2XLarge: false });
            var rds = 0;
            serviceType = "rds";
            if(this.state.selectT2Micro===true)
            { instanceType += "db.t2.micro,"; rds = rds + 1; } 
            if(this.state.selectT2Small===true)
            { instanceType += "db.t2.small,"; rds = rds + 1; }
            if(this.state.selectT2Medium===true)   
            { instanceType += "db.t2.medium,"; rds = rds + 1; }
            if(this.state.selectT2Micro===false && this.state.selectT2Small===false&& this.state.selectT2Medium===false)
            {
                instanceType = "db.t2.micro,db.t2.small,db.t2.medium,";
                rds = 0;
                this.setState({ instanceAlert: "" });
            }
            if(rds === 1) {
                this.setState({ instanceAlert: "Please select two or more instance types for comparison.", calculateState: 0 }); 
                return;
            }
            else
                this.setState({ instanceAlert: "Instance types noted!" });
        }


        //Filter processing begins

        if(this.state.selectS3===true)
        {
            if(this.state.selectConsistency===true && this.state.selectErrorRate===true && this.state.selectLatency===true 
                && this.state.selectElapsedTime===true && this.state.selectConnectionTime===true && this.state.selectThroughput===true)
            { 
                this.setState({ filterAlert: "Please select all filters except the one that needs to be predicted.", calculateState: 0 }); 
                return; 
            }
        }
        if((document.getElementById("checkbox").checked===true || document.getElementById("checkbox").checked===false) && 
        (this.state.selectConsistency===false && this.state.selectErrorRate===false && this.state.selectLatency===false 
            && this.state.selectElapsedTime===false && this.state.selectConnectionTime===false && this.state.selectThroughput===false
            && this.state.selectCpu===false && this.state.selectMemory===false)) 
        {  
            if(this.state.selectS3===true)
            { 
                this.setState({ filterAlert: "Please select all filters except the one that needs to be predicted.", calculateState: 0 }); 
                return; 
            }
            else
            {
                this.setState({ filterAlert: "Please select at least one filter.", calculateState: 0 }); 
                return; 
            }
        }
        else if (document.getElementById("checkbox").checked===true && (this.state.selectConsistency===true 
            || this.state.selectErrorRate===true || this.state.selectLatency===true || this.state.selectElapsedTime===true 
            || this.state.selectConnectionTime===true || this.state.selectThroughput===true || this.state.selectCpu===true 
            || this.state.selectMemory===true))
        {   
            if (this.state.selectConsistency===true) { filters += "stdDev,"; priorities += "1," }
            if (this.state.selectErrorRate===true) { filters += "errorRate,"; priorities += "1," }
            if (this.state.selectLatency===true)  { filters += "Latency,"; priorities += "1," }
            if (this.state.selectElapsedTime===true) { filters += "elapsed,"; priorities += "1," }
            if (this.state.selectConnectionTime===true) { filters += "Connect,";priorities += "1," }
            if (this.state.selectThroughput===true)  { filters += "Throughput,"; priorities += "1," }
            if (this.state.selectCpu===true) { filters += "CPU,"; priorities += "1," }
            if (this.state.selectMemory===true) { filters += "Memory,";priorities += "1," }
            this.setState({ filterAlert: "Filters noted!" }); 
        }
        else if (document.getElementById("checkbox").checked===false && (this.state.selectConsistency===true 
            || this.state.selectErrorRate===true || this.state.selectLatency===true || this.state.selectElapsedTime===true 
            || this.state.selectConnectionTime===true || this.state.selectThroughput===true || this.state.selectCpu===true 
            || this.state.selectMemory===true))
        {   
            var successText = "Filters with priorities noted!";
            var failureText = "For Amazon EC2, priorities should range from 1 - 8 and for Amazon RDS, priorities should range from 1 - 6 only.";
            var failureTextS3 = "For Amazon S3, priorities can be double / integer values ranging from ";
            var consistencyLimit = 1000, errorLimit = 100, latencyLimit = 300, elapsedLimit = 300, connectionLimit = 300, throughputLimit = 5000, 
            consistencyLowerLimit = 100, lowerLimit = 0;
            var s3FilterCount = 0;

            if (this.state.selectConsistency===true)  { 
                if(this.validateEntry(document.getElementById("PrConsistency").value, consistencyLowerLimit, consistencyLimit)) {
                    filters += "stdDev,"; 
                    s3FilterCount++;
                    priorities += document.getElementById("PrConsistency").value+","; 
                } 
                else {
                    if(this.state.selectS3 === true)
                        this.setState({ filterAlert: failureTextS3 + consistencyLowerLimit + " - " + consistencyLimit + " only for Consistency.", calculateState: 0 }); 
                    else 
                        this.setState({ filterAlert: failureText, calculateState: 0 }); 
                    return;
                }
            }
            if (this.state.selectErrorRate===true) { 
                if(this.validateEntry(document.getElementById("PrError").value, lowerLimit, errorLimit)) {
                    filters += "errorRate,"; 
                    s3FilterCount++;
                    priorities += document.getElementById("PrError").value+","; 
                } 
                else {
                    if(this.state.selectS3 === true)
                        this.setState({ filterAlert: failureTextS3 + lowerLimit + " - " +  errorLimit + " only for Error Rate.", calculateState: 0 }); 
                    else 
                        this.setState({ filterAlert: failureText, calculateState: 0 }); 
                    return;
                }
            }
            if (this.state.selectLatency===true) { 
                if(this.validateEntry(document.getElementById("PrLatency").value, lowerLimit, latencyLimit)) {
                    filters += "Latency,";
                    s3FilterCount++; 
                    priorities += document.getElementById("PrLatency").value+","; 
                } 
                else {
                    if(this.state.selectS3 === true)
                        this.setState({ filterAlert: failureTextS3 + lowerLimit + " - " +  latencyLimit + " only for Latency.", calculateState: 0 }); 
                    else 
                        this.setState({ filterAlert: failureText, calculateState: 0 }); 
                    return;
                }
            }
            if (this.state.selectElapsedTime===true) { 
                if(this.validateEntry(document.getElementById("PrElapsed").value, lowerLimit, elapsedLimit)) {
                    filters += "elapsed,"; 
                    s3FilterCount++;
                    priorities += document.getElementById("PrElapsed").value+","; 
                } else {
                    if(this.state.selectS3 === true)
                        this.setState({ filterAlert: failureTextS3 + lowerLimit + " - " + elapsedLimit + " only for Elapsed Time.", calculateState: 0 }); 
                    else 
                        this.setState({ filterAlert: failureText, calculateState: 0 }); 
                    return;
                }
            }
            if (this.state.selectConnectionTime===true) { 
                if(this.validateEntry(document.getElementById("PrConnection").value, lowerLimit, connectionLimit)) {
                    filters += "Connect,"; 
                    s3FilterCount++;
                    priorities += document.getElementById("PrConnection").value+","; 
                } 
                else {
                    if(this.state.selectS3 === true)
                        this.setState({ filterAlert: failureTextS3 + lowerLimit + " - " + connectionLimit + " only for Connection Time.", calculateState: 0 }); 
                    else 
                        this.setState({ filterAlert: failureText, calculateState: 0 }); 
                    return;
                }
            }
            if (this.state.selectThroughput===true) { 
                if(this.validateEntry(document.getElementById("PrThroughput").value, lowerLimit, throughputLimit)) {
                    filters += "Throughput,";
                    s3FilterCount++; 
                    priorities += document.getElementById("PrThroughput").value+","; 
                } 
                else {
                    if(this.state.selectS3 === true)
                        this.setState({ filterAlert: failureTextS3 + lowerLimit + " - " + throughputLimit + " only for Throughput.", calculateState: 0 }); 
                    else 
                        this.setState({ filterAlert: failureText, calculateState: 0 }); 
                    return;
                }
            }
            if (this.state.selectCpu===true) { 
                if(this.validateEntry(document.getElementById("PrCpu").value, 0, 0)) {
                    filters += "CPU,"; 
                    priorities += document.getElementById("PrCpu").value+","; 
                } 
                else { 
                    this.setState({ filterAlert: failureText, calculateState: 0 }); 
                    return;
                }
            }
            if (this.state.selectMemory===true) { 
                if(this.validateEntry(document.getElementById("PrMemory").value, 0, 0)) {
                    filters += "Memory,"; 
                    priorities += document.getElementById("PrMemory").value+","; 
                } 
                else {
                    this.setState({ filterAlert: failureText, calculateState: 0 }); 
                    return;
                }
            }
            if(this.state.selectS3===true)
            {
                if(s3FilterCount !== 5)
                {
                    this.setState({ filterAlert: "Please select all filters except the one that needs to be predicted.", calculateState: 0  });
                    return;
                }
            }

            this.setState({ filterAlert: successText });    
        }
    
        var moment = require('moment');
        timestamp = moment(Date.now()).format("DD-MM-YYYY h:mm:ss");

        var frontendData = {
            'timestamp': timestamp,
            'filters': filters.substring(0, filters.length - 1),
            'priorities': priorities.substring(0, priorities.length - 1),
            'instanceType': instanceType.substring(0, instanceType.length - 1),
            'serviceType': serviceType
        }
        frontendData = JSON.stringify(frontendData);
        console.log("FrontEndData", frontendData);

        this.getResults(frontendData, 3, 3000)
    }

    getResults(frontendData, retries, backoff) {

        const postDataUrl = "https://cloud-service-optimizer-dev.herokuapp.com/front-end/post-process-filters/";
        const getDataUrl = "https://cloud-service-optimizer-dev.herokuapp.com/front-end/get-results?processingNumber=";

        axios({
            method: 'post',
            url: postDataUrl,
            headers: {
                'Content-type': 'application/json',
            },
            data: frontendData 
        })
        .then(postJsonData => { 
            console.log("pNo. obtained via POST", postJsonData.data);
            
            var postResponse = postJsonData.data

            setTimeout(() => {
                console.log("Initiating a delay of:", backoff);
                axios.get(getDataUrl + postResponse.message)
                .then(getJsonData => { 
                    console.log("GET Response (payload)", getJsonData);
                    
                    var getResponse = getJsonData.data;
        
                    if(getResponse.status === "success") {
                        this.setState({calculateState: 2, response: getResponse.payload})
                    }
                    else {
                        this.setState({calculateState: 2, response: this.defaultResponse[this.getService()]})
                        // this.setState({calculateState: 3})
                    }
                })
                .catch(error => { 
                    console.log(error);
                    if(retries > 0) {
                        var retriesLeft = retries - 1;
                        console.log("Failure in GET, no. of retries left:", retriesLeft);
                        this.getResults(frontendData, retriesLeft, backoff + 500);
                    }
                    else {
                        this.setState({calculateState: 2, response: this.defaultResponse[this.getService()]})
                        // this.setState({calculateState: 3})
                    }
                })
            }, backoff)
        })
        .catch(error => { 
            console.log(error);
            if(retries > 0) {
                var retriesLeft = retries - 1;
                console.log("Failure in POST, no. of retries left:", retriesLeft);
                this.getResults(frontendData, retriesLeft, backoff + 500);
            }
            else {
                this.setState({calculateState: 2, response: this.defaultResponse[this.getService()]})
                // this.setState({calculateState: 3})
            }
        })
    }
  
    
    render() {
        const { showHideServices, showHideFilters, showHideInstances, selectEC2, selectS3, selectRDS,
                selectConsistency, selectErrorRate, selectLatency, selectElapsedTime, selectConnectionTime, selectThroughput, selectCpu, selectMemory,
                filterAlert, serviceAlert, instanceAlert,
                selectT2Micro, selectT2Nano, selectT2Small, selectT2Medium, selectT2Large, selectT2XLarge } = this.state;
        return(
           
            <div>
                <div className = 'titleDivStyle3'>
                   <h1 className = 'titleStyle3'>Dashboard</h1>
                </div>
                <div>
                    <div className = 'questionDivStyle'>
                        <p className = 'questionStyle'>What AWS Service are you looking for?</p>
                        <button className = 'selectButtonStyle' onClick={() => this.hideComponent("showHideServices")}>Select Service</button>
                    </div>
                    { showHideServices && (
                    <div className = 'serviceDivStyle'>
                        <button className={selectEC2 ? "ec2StyleTrue": "ec2StyleFalse"} onClick={() => this.handleClick("EC2")}>{ this.ec2 }</button>
                        <button className={selectS3 ? "s3StyleTrue": "s3StyleFalse"} onClick={() => this.handleClick("S3")}>{ this.s3 }</button>
                        <button className={selectRDS ? "rdsStyleTrue": "rdsStyleFalse"} onClick={() => this.handleClick("RDS")}>{ this.rds }</button>
                        <div>
                        <p className='alertStyle'>{serviceAlert}</p>
                        </div>
                    </div> ) }
                </div>
                <div>
                    <div className = 'questionDivStyle'>
                    <p className = 'questionStyle'>{ !selectS3 ? 'What performance metrics do you want us to focus on?' : 'What metric should ML prediction be applied to?'}</p>
                    <button className = 'selectButtonStyle' onClick={() => this.hideComponent("showHideFilters")}>Select Filters</button>
                    </div>
                    { showHideFilters && (
                    <div className = 'serviceDivStyle'>                    
                            <div>
                                <input type = { selectS3 ? "hidden" : "checkbox"} id = "checkbox"/>
                                <label className='checkboxStyle'>{ selectS3 ?  "" : "Assign same priority to all filters" }</label><br/>
                            </div>
                        <div style={{display: 'inline'}}>
                            <div style={{display: 'inline'}}>
                                <button className={selectConsistency ? "consistencyStyleTrue": "consistencyStyleFalse"} onClick={() => this.handleClick("Consistency")}>Consistency</button>
                                {(selectConsistency && document.getElementById("checkbox").checked!==true &&
                                    <input className='priorityTextStyle' type="text" id="PrConsistency" placeholder="Enter Priority" required/>
                                )}
                            </div>
                            <div style={{display: 'inline'}}>
                                <button className={selectErrorRate ? "errorStyleTrue": "errorStyleFalse"} onClick={() => this.handleClick("Error Rate")}>Error Rate</button>
                                {(selectErrorRate && document.getElementById("checkbox").checked!==true &&
                                    <input className='priorityTextStyle' type="text" id="PrError" placeholder="Enter Priority" required/>
                                )}
                            </div>
                            <div style={{display: 'inline'}}>
                                <button className={selectLatency ? "latencyStyleTrue": "latencyStyleFalse"} onClick={() => this.handleClick("Latency")}>Latency</button>
                                {(selectLatency && document.getElementById("checkbox").checked!==true &&
                                    <input className='priorityTextStyle' type="text" id="PrLatency" placeholder="Enter Priority" required/>
                                )}
                            </div>
                            <div style={{display: 'inline'}} >
                                <button className={selectElapsedTime ? "elapsedStyleTrue": "elapsedStyleFalse"} onClick={() => this.handleClick("Elapsed Time")}>Elapsed Time</button>
                                {(selectElapsedTime && document.getElementById("checkbox").checked!==true &&
                                    <input className='priorityTextStyle' type="text" id="PrElapsed" placeholder="Enter Priority" required/>
                                )}
                            </div>
                            
                            <div style={{display: 'inline'}}>
                                <button className={selectConnectionTime ? "connectionStyleTrue": "connectionStyleFalse"} onClick={() => this.handleClick("Connection Time")}>Connection Time</button>
                                {(selectConnectionTime && document.getElementById("checkbox").checked!==true &&
                                    <input className='priorityTextStyle' type="text" id="PrConnection" placeholder="Enter Priority" required/>
                                )}
                            </div>
                            <div style={{display: 'inline'}}>
                                <button className={selectThroughput ? "throughputStyleTrue": "throughputStyleFalse"} onClick={() => this.handleClick("Throughput")}>Throughput</button>
                                {(selectThroughput && document.getElementById("checkbox").checked!==true &&
                                    <input className='priorityTextStyle' type="text" id="PrThroughput" placeholder="Enter Priority" required/>
                                )}
                            </div>
                            { selectEC2 && (
                            <div style={{display: 'inline'}}>
                                <button className={selectCpu ? "cpuStyleTrue": "cpuStyleFalse"} onClick={() => this.handleClick("CPU Utilization")}>CPU Utilization</button>
                                {(selectCpu && document.getElementById("checkbox").checked!==true &&
                                    <input className='priorityTextStyle' type="text" id="PrCpu" placeholder="Enter Priority" required/>
                                )}
                            </div>
                            )}
                            { selectEC2 && (
                            <div style={{display: 'inline'}}>
                                <button className={selectMemory ? "memoryStyleTrue": "memoryStyleFalse"} onClick={() => this.handleClick("Memory")}>Memory</button>
                                {(selectMemory && document.getElementById("checkbox").checked!==true &&
                                    <input className='priorityTextStyle' type="text" id="PrMemory" placeholder="Enter Priority" required/>
                                )}
                            </div>
                            )}
                        </div>
                        <div>
                            <p className='alertStyle'>{filterAlert}</p>
                            </div>
                    </div> ) }
                </div>
                { !selectS3 && (
                <div>
                    <div className = 'questionDivStyle'>
                        <p className = 'questionStyle'>What Instance type of the above listed AWS Service do you want?</p>
                        <button className = 'selectButtonStyle' onClick={() => this.hideComponent("showHideInstances")}>Select Instance</button>
                    </div>

                    {
                    selectEC2 && showHideInstances && (
                        <div className = 'serviceDivStyle'>
                            <button className={selectT2Nano ? "t2NanoStyleTrue": "t2NanoStyleFalse"} onClick={() => this.handleClick("T2Nano")}>t2.nano</button>
                            <button className={selectT2Micro ? "t2MicroStyleTrue": "t2MicroStyleFalse"} onClick={() => this.handleClick("T2Micro")}>t2.micro</button>
                            <button className={selectT2Small ? "t2SmallStyleTrue": "t2SmallStyleFalse"} onClick={() => this.handleClick("T2Small")}>t2.small</button>
                            <button className={selectT2Medium ? "t2MediumStyleTrue": "t2MediumStyleFalse"} onClick={() => this.handleClick("T2Medium")}>t2.medium</button>
                            <button className={selectT2Large ? "t2LargeStyleTrue": "t2LargeStyleFalse"} onClick={() => this.handleClick("T2Large")}>t2.large</button>
                            <button className={selectT2XLarge ? "t2XLargeStyleTrue": "t2XLargeStyleFalse"} onClick={() => this.handleClick("T2XLarge")}>t2.xlarge</button>
                            <p className='alertStyle'>{instanceAlert}</p>
                        </div>                       
                        )
                    }
                    
                    { selectRDS && showHideInstances && (
                        <div className = 'serviceDivStyle'>
                            <button className={selectT2Micro ? "t2MicroStyleTrue": "t2MicroStyleFalse"} onClick={() => this.handleClick("T2Micro")}>db.t2.micro</button>
                            <button className={selectT2Small ? "t2SmallStyleTrue": "t2SmallStyleFalse"} onClick={() => this.handleClick("T2Small")}>db.t2.small</button>
                            <button className={selectT2Medium ? "t2MediumStyleTrue": "t2MediumStyleFalse"} onClick={() => this.handleClick("T2Medium")}>db.t2.medium</button>
                            <p className='alertStyle'>{instanceAlert}</p>
                        </div>
                        )
                    }
                </div>
                )}
                 { this.calculateButton() }
            </div>

        )};
    }

export default Dashboard;
