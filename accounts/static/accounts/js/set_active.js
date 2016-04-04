(function(){
    $("a").each(function(index, obj){
        if(obj.href === window.location.href){
            $(obj).parent().addClass('active');
        }
    });   
})();
