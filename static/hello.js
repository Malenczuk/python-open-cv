$(document).ready(function(){
    $("#btnSearch").click(function(){
        //var url="http://example.com/results?choice=choice2&choice=choice4"
        var url="camera.html?";
        var flag=false;
        $("input:checkbox[name=choice]:checked").each(function(){
            if(!flag)
            {
                url=url+"choice="+$(this).val();
                flag=true;// To trace if first query string added
            }
            else
            {
                url=url+"&choice="+$(this).val();
            }
        });
        //alert(url);
        window.location = url;
    });
});