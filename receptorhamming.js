const net = require('net');

function binaryToString(binary) {
    let str = '';
    for (let i = 0; i < binary.length; i += 8) {
        str += String.fromCharCode(parseInt(binary.substr(i, 8), 2));
    }
    return str;
}

function hamming_decode(binaryMessage) {
    const chunks = binaryMessage.match(/.{1,7}/g);
    let decodedMessage = "";

    chunks.forEach(chunk => {
        const [p1, p2, d1, p3, d2, d3, d4] = chunk.split('').map(Number);
        const s1 = (p1 + d1 + d2 + d4) % 2;
        const s2 = (p2 + d1 + d3 + d4) % 2;
        const s3 = (p3 + d2 + d3 + d4) % 2;
        const syndrome = s1 * 4 + s2 * 2 + s3;

        let correctedChunk = chunk.split('');
        if (syndrome !== 0) {
            correctedChunk[syndrome - 1] = correctedChunk[syndrome - 1] === '0' ? '1' : '0';
        }

        decodedMessage += correctedChunk[2] + correctedChunk[4] + correctedChunk[5] + correctedChunk[6];
    });

    return decodedMessage;
}

const server = net.createServer((socket) => {
    console.log('Client connected');

    socket.on('data', (data) => {
        const binaryMessage = data.toString();
        const verifiedMessage = hamming_decode(binaryMessage);
    
        if (verifiedMessage !== null) {
            const decodedMessage = binaryToString(verifiedMessage);
            console.log('Mensaje binario recibido:', binaryMessage);
            console.log('Mensaje decodificado:', decodedMessage);
        } else {
            console.log('Mensaje binario recibido:', binaryMessage);
            console.log('Verificacion fallida. Mensaje no decodificado.');
        }
    });
    
});

server.listen(12345, () => {
    console.log('El servidor esta escuchando el puerto: 12345...');
});
