d3.select("#predict_button").on("click", function(){
    //console.log("you have clicked me");

    var risk_scope = d3.select("#textbox").node().value;
    console.log(risk_scope);

    d3.json("/api/predict",{
        method: "POST",
        body: JSON.stringify({
            "risk_scope": risk_scope
        }),
        headers: {
            "Content-type":"application/json"
        }
    }).then(function(response){
        console.log(response)
        d3.select("#risk_return").text(response.prediction)
    })

})