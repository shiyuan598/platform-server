const axios = require("axios");

const updateState = (params) => {
    axios
        .post(`http://localhost:9011/monitor/status/update`, params)
        .then((v) => {
            console.info(v.data);
        });
};

setInterval(() => {
    updateState({
        mount_dir: {
            "测试组-001": {
                ip: "127.0.0.1",
                media_dir: "/media/lhz/nvme0n1p1",
                time_stamp: 1690264651.0641866,
                total_size: Math.floor((5 + Math.random() * 2000) * 1024 * 1024),
                progress: Math.ceil(Math.random() * 100),
                upload_status: 0,
                recorders: {}
            },
            "测试组-002": {
                ip: "127.0.0.2",
                media_dir: "/media/lhz/sata",
                time_stamp: 1690264733.2685053,
                total_size: Math.floor((5 + Math.random() * 2000) * 1024 * 1024),
                progress: Math.ceil(Math.random() * 100),
                upload_status: 0,
                recorders: {}
            },
            "集成组": {
                ip: "127.0.0.3",
                media_dir: "/media/lhz/sata",
                time_stamp: 1690264733.2685053,
                total_size: Math.floor((5 + Math.random() * 2000) * 1024 * 1024),
                progress: Math.ceil(Math.random() * 100),
                upload_status: 0,
                recorders: {}
            },
            "HWL4_ORIN": {
                ip: "127.0.0.1",
                media_dir: "/media/lhz/sata",
                time_stamp: 1690264733.2685053,
                total_size: Math.floor((5 + Math.random() * 2000) * 1024 * 1024),
                progress: Math.ceil(Math.random() * 100),
                upload_status: 0,
                recorders: {}
            },
            "HWL4_X86": {
                ip: "127.0.0.2",
                media_dir: "/media/lhz/sata",
                time_stamp: 1690264733.2685053,
                total_size: Math.floor((5 + Math.random() * 2000) * 1024 * 1024),
                progress: Math.ceil(Math.random() * 100),
                upload_status: 0,
                recorders: {}
            },
            "GSL4_X86": {
                ip: "127.0.0.2",
                media_dir: "/media/lhz/sata",
                time_stamp: 1690264733.2685053,
                total_size: Math.floor((5 + Math.random() * 2000) * 1024 * 1024),
                progress: Math.ceil(Math.random() * 100),
                upload_status: 0,
                recorders: {}
            },
            "J7A02": {
                ip: "127.0.0.3",
                media_dir: "/media/lhz/sata",
                time_stamp: 1690264733.2685053,
                total_size: Math.floor((5 + Math.random() * 2000) * 1024 * 1024),
                progress: Math.ceil(Math.random() * 100),
                upload_status: 0,
                recorders: {}
            },
            "J7A01": {
                ip: "127.0.0.3",
                media_dir: "/media/lhz/sata",
                time_stamp: 1690264733.2685053,
                total_size: Math.floor((5 + Math.random() * 2000) * 1024 * 1024),
                progress: Math.ceil(Math.random() * 100),
                upload_status: 0,
                recorders: {}
            },
        },
        log: {
            timestamp: 1690265286,
            ip: "127.0.0.1",
            type: 1,
            content: "Discover a world of possibilities with our innovative products and services."
        }
    })
}, 5000);
