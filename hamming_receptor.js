
const fs = require('fs');

function hammingDecodificar(codeword) {
    let paridad = [
        (parseInt(codeword[0]) ^ parseInt(codeword[2]) ^ parseInt(codeword[4]) ^ parseInt(codeword[6])).toString(),
        (parseInt(codeword[1]) ^ parseInt(codeword[2]) ^ parseInt(codeword[5]) ^ parseInt(codeword[6])).toString(),
        (parseInt(codeword[3]) ^ parseInt(codeword[4]) ^ parseInt(codeword[5]) ^ parseInt(codeword[6])).toString()
    ];
    let error_pos = parseInt(paridad[0]) * 4 + parseInt(paridad[1]) * 2 + parseInt(paridad[2]) * 1;
    if (error_pos !== 0) {
        console.log("Error encontrado en la posición", error_pos);
        codeword = codeword.substr(0, error_pos - 1) + (codeword[error_pos - 1] === '1' ? '0' : '1') + codeword.substr(error_pos);
    }
    return codeword[2] + codeword[4] + codeword[5] + codeword[6];
}

  
  
fs.readFile('output2.txt', 'utf8', (err, codeword) => {
    if (err) throw err;
    console.log("Codeword Hamming:", codeword);
    let data = hammingDecodificar(codeword);
    console.log("Datos decodificados:", data);
});
  