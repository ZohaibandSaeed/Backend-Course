import { Router } from "express";
import { UploadFile, DeleteFile } from "../controllers/file.controller.js";
import { upload } from "../middlewares/upload.multer.js";

const router = Router();

router.post("/upload", upload.single("file"), UploadFile);

router.delete("/delete/:id", DeleteFile);

export default router;