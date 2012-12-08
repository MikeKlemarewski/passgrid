$(document).ready(function(){
    
    // minimum 6 chars long
    function decimalToHexString(number)
    {
        if (number < 0)
        {
        	number = 0xFFFFFFFF + number + 1;
        }
        hexStr =  number.toString(16).toUpperCase();
        while(hexStr.length < 6){
           hexStr = "0" + hexStr;
         }
        return hexStr;
    }
  
  function generateToken( numRows, numCols) {
  var token = new Array();
  for( i = 0; i < numRows; i++ ) {
    var subTokenArray = new Array();
    token[i] = subTokenArray;
    for( j = 0; j < numCols; j++ ){
      token[i][j] = 64*j * 256*256 * (i == 0 || i == 1) + 64 * j * 256* (i == 0 || i == 2) + 64 * j* (i == 0 || i == 3);
    }
  }
  return token;
}

function createGrid(token) {
  for( i = 0; i < token.length; i++ ) {
     for( j = 0; j < token[i].length; j++ ){
      var blockStr = ".block"+ (i+1) + (j+1);
       var colorValStr = decimalToHexString(token[i][j]);
       // console.log( blockStr + ": #" + colorValStr);
       $(blockStr).css( "background-color", "#" + colorValStr); 
     }
   }     
}
token = generateToken(4,4);
createGrid(token);

});

