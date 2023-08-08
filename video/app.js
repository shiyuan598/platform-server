const NodeMediaServer = require("node-media-server");

const config = {
    rtmp: {
        port: 1935,
        chunk_size: 60000,
        gop_cache: true,
        ping: 60,
        ping_timeout: 30
    },

    http: {
        port: 1936,
        allow_origin: "*"
    }
};
var nms = new NodeMediaServer(config);
nms.run();
