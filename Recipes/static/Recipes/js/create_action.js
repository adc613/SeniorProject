$(document).ready(function(){
    var $conditional = $('.conditional');
    var $basicReturnText = $('.basic_return_text');
    var $typeSelector = $('#type');

    var conditonalVisible = false;
    makeBasicReturnTextVisible();
    $typeSelector.change(function(){
        console.log('change');
        console.log($typeSelector);
        var value = $typeSelector.val();
        if (value == 'C'){
            makeConditionalVisible();
        } else if (value == 'RT') {
            makeBasicReturnTextVisible();
        }
    });

    function makeConditionalVisible() {
        $conditional.removeClass('hidden');
        $basicReturnText.addClass('hidden');
        conditonalVisible = false;
        console.log('Conditonal is visible');
    }

    function makeBasicReturnTextVisible() {
        $basicReturnText.removeClass('hidden');
        $conditional.addClass('hidden');
        conditonalVisible = true;
        console.log('Conditonal is not visible');
    }

    function toggleVisibility() {
        if(conditonalVisible){
            makeConditionalVisible();
        } else {
            makeBasicReturnTextVisible();
        }
    }
});
