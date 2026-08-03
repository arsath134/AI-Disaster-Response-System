AWS.config.update({

region:"ap-southeast-2"

});


const bucketName = "ai-disaster-response-reports-arsath";


const s3=new AWS.S3();



function submitReport(){


let report={


id:Date.now().toString(),

location:
document.getElementById("location").value,


type:
document.getElementById("type").value,


description:
document.getElementById("description").value,


time:
new Date().toISOString()


};



s3.putObject({

Bucket:bucketName,

Key:"reports/"+report.id+".json",

Body:JSON.stringify(report),

ContentType:"application/json"


},function(error,data){


if(error){

alert(error);

}

else{


alert(
"Report submitted successfully"
);


}



});


}
