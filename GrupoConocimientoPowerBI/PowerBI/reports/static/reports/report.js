document.addEventListener('DOMContentLoaded', function(){


    document.querySelector('#report').addEventListener('click',() => show("ReportSection", "Energy"));
    

});


function show(pageName, filterValue){
    //Set the baseUrl to the embed url you get from the Power BI UI
    var newUrl = baseUrl + "&pageName=" + pageName;
    if(null != filterValue && "" != filterValue)
    {/code>newUrl += "&$filter=Industries/Industry eq '" + filterValue + "'";
    }
    //Assumes there’s an iFrame on the page with id="iFrame"
    var report = document.getElementById("iFrame");
    report.src = newUrl;
}