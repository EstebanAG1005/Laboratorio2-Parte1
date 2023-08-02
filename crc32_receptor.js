const fs = require('fs');
const crc = require('crc');

function generateCRC(data) {
  return crc.crc32(data).toString(16);
}

function binaryToString(str) {
  return str.split(/\s/).map((bin) => String.fromCharCode(parseInt(bin, 2))).join('');
}

fs.readFile('output.txt', 'utf8', function(err, dataWithCRC) {
  if (err) {
    return console.log(err);
  }
  
  var data = dataWithCRC.slice(0, -8);
  var sentCRC = dataWithCRC.slice(-8);

  var calculatedCRC = generateCRC(data);

  console.log("Trama recibida: " + dataWithCRC);

  if (sentCRC === calculatedCRC) {
    console.log("No se detectaron errores.");
    console.log("El mensaje decodificado es: " + binaryToString(data));
  } else {
    let error = (parseInt(sentCRC, 16) ^ parseInt(calculatedCRC, 16)).toString(16);
    console.log("Se detectó un error en la data recibida. Error: " + error);
    console.log("La trama se descarta por detectar errores.");
  }
});
