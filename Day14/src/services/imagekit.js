import ImageKit from "@imagekit/nodejs";
import dotenv from "dotenv";

dotenv.config();

const imagekit = new ImageKit({
    privateKey: process.env.IMAGEKIT_PRIVATE_KEY,
    publicKey: process.env.IMAGEKIT_PUBLIC_KEY,
    urlEndpoint: process.env.IMAGEKIT_URL_ENDPOINT,
});

const upload_file = async (filename, file) => {
    try {
        const result = await imagekit.files.upload({
            file: file.buffer.toString("base64"),
            fileName: filename,
            folder: "/files",
        });

        return { "fileUrl": result.url, "imagekitId": result.fileId };
    } catch (error) {
        console.log(error);
        return error;
    }
};

const delete_file = async (imagekitId) => {
    try {
        const result = await imagekit.files.delete(imagekitId);
        return result;
    } catch (error) {
        console.log(error);
        return error;
    }
};

export { upload_file, delete_file };