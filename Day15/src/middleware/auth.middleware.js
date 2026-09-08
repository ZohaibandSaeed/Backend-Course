import jwt from "jsonwebtoken";
import dotenv from "dotenv";

dotenv.config();

async function AuthMiddleWare(req, res, next) {
    try {

    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Internal Server Error" });
    }
}