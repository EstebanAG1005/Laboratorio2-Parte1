const net = require('net');
const crc = require('crc');

const PORT = 65432;

function generateCRC(data) {
    return crc.crc32(data).toString(16);
}

function binaryToString(str) {
    let result = "";
    for (let i = 0; i < str.length; i += 8) {
        const byte = str.slice(i, i + 8);
        result += String.fromCharCode(parseInt(byte, 2));
    }
    return result;
}


const server = net.createServer((socket) => {
    socket.on('data', (dataWithCRC) => {
        const strDataWithCRC = dataWithCRC.toString();

        const data = strDataWithCRC.slice(0, -8);
        const sentCRC = strDataWithCRC.slice(-8);

        const calculatedCRC = generateCRC(data);

        console.log("Trama recibida: " + strDataWithCRC);

        if (sentCRC === calculatedCRC) {
            console.log("No se detectaron errores.");
            console.log("El mensaje decodificado es: " + binaryToString(data));
            socket.write('SUCCESS');
        } else {
            let error = (parseInt(sentCRC, 16) ^ parseInt(calculatedCRC, 16)).toString(16);
            console.log("Se detectó un error en la data recibida. Error: " + error);
            console.log("La trama se descarta por detectar errores.");
            socket.write('ERROR');
        }

        socket.end();
    });

    socket.on('error', (error) => {
        if (error.code === 'ECONNRESET') {
            console.log('Client closed connection');
        } else {
            console.error('Unexpected error:', error);
        }
    });
});

server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
});

// To keep the server continuously running and listening
process.on('uncaughtException', function (err) {
    console.error(err.stack);
    console.log("Node NOT Exiting...");
});
