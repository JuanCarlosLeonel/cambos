// Produção

var chart1 = document.getElementById("chartProducao").getContext("2d");
var producao = new Chart(chart1, {
	type: 'line',
	data: {
		labels: labels1,
		datasets : [{	
			label: 'Producao',
			data: data1,
			backgroundColor: [
                'rgba(48, 164, 255, 0.2)',                
            ],
            borderColor: [
                'rgba(48, 164, 255, 1)',                
            ],
            borderWidth: 1
        }]
    },
	options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
		},
		legend: false
    }
});

// Composição do custo

var chart2 = document.getElementById("chartComposicao").getContext("2d");
var composicao = new Chart(chart2, {
	type: 'bar',
	data: {
		labels: labels2,
		datasets : [{	
			label: 'Custo',
			data: data2,
			backgroundColor: 'rgba(255, 206, 86, 0.2)',            
            borderColor: 'rgba(255, 206, 86, 1)',
            borderWidth: 1
		},
		{	
			label: 'Insumo',
			data: data3,
			backgroundColor:'rgba(255, 159, 64, 0.2)',        
            borderColor:'rgba(255, 159, 64, 1)',            
            borderWidth: 1
		},
		{	
			label: 'Material',
			data: data4,
			backgroundColor:'rgba(255, 99, 132, 0.2)',              
            borderColor:'rgba(255, 99, 132, 1)',               
            borderWidth: 1
		}
	]
    },
	options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
		},
    }
});
	
	
	var pieData = [
			{
				value: 300,
				color: "#30a5ff",
				highlight: "#7376df",
				label: "Value 1"
			},
			{
				value: 50,
				color: "#a0a0a0",
				highlight: "#999999",
				label: "Value 2"
			},
			{
				value: 100,
				color:"#dfdfdf",
				highlight: "#cccccc",
				label: "Value 3"
			},
			{
				value: 120,
				color: "#f7f7f7",
				highlight: "#eeeeee",
				label: "Value 4"
			}

		];
			
	var doughnutData = [
			{
				value: 300,
				color: "#30a5ff",
				highlight: "#7376df",
				label: "Value 1"
			},
			{
				value: 50,
				color: "#a0a0a0",
				highlight: "#999999",
				label: "Value 2"
			},
			{
				value: 100,
				color:"#dfdfdf",
				highlight: "#cccccc",
				label: "Value 3"
			},
			{
				value: 120,
				color: "#f7f7f7",
				highlight: "#eeeeee",
				label: "Value 4"
			}
		];
			
	var radarData = {
	    labels: ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"],
	    datasets: [
	        {
	            label: "My First dataset",
	            fillColor: "rgba(220,220,220,0.2)",
	            strokeColor: "rgba(220,220,220,1)",
	            pointColor: "rgba(220,220,220,1)",
	            pointStrokeColor: "#fff",
	            pointHighlightFill: "#fff",
	            pointHighlightStroke: "rgba(220,220,220,1)",
	            data: [65, 59, 90, 81, 56, 55, 40]
	        },
	        {
	            label: "My Second dataset",
	            fillColor : "rgba(48, 164, 255, 0.2)",
	            strokeColor : "rgba(48, 164, 255, 0.8)",
	            pointColor : "rgba(48, 164, 255, 1)",
	            pointStrokeColor : "#fff",
	            pointHighlightFill : "#fff",
	            pointHighlightStroke : "rgba(48, 164, 255, 1)",
	            data: [28, 48, 40, 19, 96, 27, 100]
	        }
	    ]
	};
	
	var polarData = [
	    {
	    	value: 300,
	    	color: "#30a5ff",
	    	highlight: "#7376df",
	    	label: "Value 1"
	    },
	    {
	    	value: 140,
	    	color: "#a0a0a0",
	    	highlight: "#999999",
	    	label: "Value 2"
	    },
	    {
	    	value: 220,
	    	color:"#dfdfdf",
	    	highlight: "#cccccc",
	    	label: "Value 3"
	    },
	    {
	    	value: 250,
	    	color: "#f7f7f7",
	    	highlight: "#eeeeee",
	    	label: "Value 4"
	    }
		
	];
