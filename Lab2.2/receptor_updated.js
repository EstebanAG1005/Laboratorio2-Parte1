const net = require('net');
const zlib = require('zlib');
const crc = require('crc');


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

function compute_crc(binaryMessage) {
    return crc.crc32(binaryMessage).toString(2).padStart(32, '0');
}

function verify_integrity(binaryMessage) {
    const algorithmIndicator = binaryMessage[0];
    const data = binaryMessage.slice(1);

    if (algorithmIndicator === '0') {
        const received_crc = data.slice(-32);
        const message_data = data.slice(0, -32);
        const computed_crc = compute_crc(message_data);

        if (received_crc === computed_crc) {
            return message_data;
    } else {
            console.error("CRC verification failed!");
            return null;
        }
    } else if (algorithmIndicator === '1') {
        return hamming_decode(data);
    } else {
        console.error("Invalid algorithm indicator!");
        return null;
    }
}

const server = net.createServer((socket) => {
    console.log('Client connected');

    socket.on('data', (data) => {
        const binaryMessage = data.toString();
        const verifiedMessage = verify_integrity(binaryMessage);
    
        if (verifiedMessage !== null) {
            const decodedMessage = binaryToString(verifiedMessage);
            console.log('Received binary message:', binaryMessage);
            console.log('Decoded message:', decodedMessage);
            socket.write("success"); // Sending success response
        } else {
            console.log('Received binary message:', binaryMessage);
            console.log('Verification failed. Message not decoded.');
            socket.write("failure"); // Sending failure response
        }
    });
    
});

server.listen(12345, () => {
    console.log('Server is listening on port 12345...');
});
