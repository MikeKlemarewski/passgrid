(function() {

    // minimum 6 chars long
    var decimalToHexString = function(number) {
        if (number < 0) {
        	number = 0xFFFFFFFF + number + 1;
        }
        var hexStr =  number.toString(16).toUpperCase();
        while (hexStr.length < 6) {
            hexStr = "0" + hexStr;
        }
        return hexStr;
    };

    var generateToken = function(numRows, numCols) {
        var token = [];
        for (i = 0; i < numRows; i++ ) {
            var subTokenArray = [];
            token[i] = subTokenArray;
            for (j = 0; j < numCols; j++) {
                token[i][j] = 64*j * 256*256 * (i == 0 || i == 1) + 64 * j * 256* (i == 0 || i == 2) + 64 * j* (i == 0 || i == 3);
            }
        }
        return token;
    };

    var createGrid = function(token) {
        for (i = 0; i < token.length; i++) {
            for (j = 0; j < token[i].length; j++ ) {
                var blockStr = ".block"+ (i+1) + (j+1);
                var colorValStr = decimalToHexString(token[i][j]);
                // console.log( blockStr + ": #" + colorValStr);
                $(blockStr).css( "background-color", "#" + colorValStr);
            }
        }
    };

    var getToken = function() {
        if (localStorage["token"] == undefined) {
            token = generateToken(4,4);
            localStorage["token"] = JSON.stringify(token);
        }
        var storedToken = localStorage["token"];
        var token = JSON.parse(storedToken);
        return token;
    };

    var token = getToken();
    createGrid(token);

})();