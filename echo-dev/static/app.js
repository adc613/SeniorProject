(function(){
    var inputs = document.getElementById('key-value-inputs');
    var keyValuePairs = 0;
    var addBtn = document.getElementById('add-btn');
    var submitBtn = document.getElementById('submit-btn');

    document.addEventListener("click", function(event){
        if(event.target === addBtn){
            event.preventDefault();
            console.log('test');
            createKeyValueInput();
        }
    });

    createKeyValueInput();
    
    function createKeyValueInput(){
        var keyContainer = document.createElement('div');
        var valueContainer = document.createElement('div');
        var keyInput = document.createElement('input');
        var valueInput = document.createElement('input');
        var keyLabel = document.createElement('label');
        var valueLabel = document.createElement('label');

        keyContainer.className = "col-xs-6";
        valueContainer.className = "col-xs-6";

        keyInput.name = 'key-' + keyValuePairs;
        valueInput.name = 'value-' + keyValuePairs;

        keyLabel.htmlFor = 'key-' + keyValuePairs;
        valueLabel.htmlFor = 'value-' + keyValuePairs;

        keyLabel.textContent = 'Key: '
        valueLabel.textContent = 'Value: '

        keyContainer.appendChild(keyLabel);
        keyContainer.appendChild(keyInput);
        valueContainer.appendChild(valueLabel);
        valueContainer.appendChild(valueInput);

        inputs.insertBefore(valueContainer, inputs.firstChild);
        inputs.insertBefore(keyContainer, valueContainer);

        keyValuePairs++;
    }
})();

(function(){
    var app = angular.module('devApp', []);
});

