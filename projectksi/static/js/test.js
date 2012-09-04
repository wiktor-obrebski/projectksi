(function pKsi( window, undefined ) {
    //let show some stupid message
    this.InternalMessage = function() {
        this.message = function() {
            alert('to jest test 1');
        };
        this.message2 = function() {
            alert('a to test 2');
        };
    };

    window.pKsi = window._ = pKsi;

})( window );
