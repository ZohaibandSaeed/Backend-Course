// import { upload_file } from "../services/imagekit";
// import { db } from "../prisma/db";

import { delete_file, upload_file } from "../services/imagekit.js";

async function UploadFile(req, res) {
    try {

        const file = req.file;

        if (!file) {
            return res.status(400).json({
                "message": "please upload file",
            });
        }

        const uploads = await upload_file(file.originalname, file);

        const file_url = uploads["fileUrl"];
        const imagekit_id = uploads["imagekitId"];

        if (!file_url || !imagekit_id) {
            return res.status(400).json({
                "message": "error in file upload."
            });
        }

        res.status(200).json({
            "message": "File Upload Successfully",
            "file_url": file_url,
            "imagekit_id": imagekit_id,
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({
            message: error.message
        });
    }
}

async function DeleteFile(req, res) {
    try {

        const imagekit_id = req.params;

        if (!imagekit_id.id) {
            return res.status(400).json({
                "message": "please provide imagekit id."
            });
        }

        await delete_file(imagekit_id.id);

        res.status(200).json({
            "message": "File Delete Successfully",
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({
            "message": "Internal Server Error"
        });
    }
}

export { UploadFile, DeleteFile };