import jwt from "jsonwebtoken";
import dotenv from "dotenv";

dotenv.config();

async function AuthMiddleWare(req, res, next) {
    try {

        const brower_token = req.cookies.accessToken;

        if (!brower_token) {
            return res.status(401).json({ error: "Unauthorized" });
        }

        const verify_token = jwt.verify(brower_token, process.env.JWT_SECRET);

        req.user = verify_token;

        next();

    } catch (error) {
        console.error(error);
        return res.status(400).json({ error: "Invalid Token" });
    }
}

async function IsAdmin(req, res, next) {
    try {

        if (req.user && req.user.role === "admin") {
            next();
        } else {
            return res.status(403).json({ error: "Access Denied: You are not Admin" });
        }

    } catch (error) {
        console.error(error);
        return res.status(400).json({ error: "Invalid Token" });
    }
}

export { AuthMiddleWare, IsAdmin };