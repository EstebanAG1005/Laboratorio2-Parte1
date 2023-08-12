const net = require('net');
const crc = require('crc');

const server = net.createServer((socket) => {
    socket.on('data', (dataWithCRC) => {
        var dataWithCRCStr = dataWithCRC.toString();
        var data = dataWithCRCStr.slice(0, -8);
        var sentCRC = dataWithCRCStr.slice(-8);

        var calculatedCRC = crc.crc32(data).toString(16);

        console.log("Trama recibida: " + dataWithCRCStr);

        if (sentCRC === calculatedCRC) {
            console.log("No se detectaron errores.");
            console.log("El mensaje decodificado es: " + data);
        } else {
            let error = (parseInt(sentCRC, 16) ^ parseInt(calculatedCRC, 16)).toString(16);
            console.log("Se detectó un error en la data recibida. Error: " + error);
            console.log("La trama se descarta por detectar errores.");
        }
    });

    socket.on('end', () => {
        console.log('Cliente desconectado');
    });
});

server.listen(12345, '127.0.0.1', () => {
    console.log('Escuchando en el puerto 12345');
});
