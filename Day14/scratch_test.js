import ImageKit from "@imagekit/nodejs";
import dotenv from "dotenv";

dotenv.config();

const imagekit = new ImageKit({
    privateKey: process.env.IMAGEKIT_PRIVATE_KEY,
    publicKey: "dummy",
    urlEndpoint: "https://ik.imagekit.io/dummy"
});

async function run() {
    try {
        console.log("Trying to upload with base64 string...");
        const result = await imagekit.files.upload({
            file: Buffer.from("hello world").toString("base64"),
            fileName: "test.txt"
        });
        console.log("Result:", result);
    } catch (e) {
        console.log("Error:", e);
    }
}
run();
