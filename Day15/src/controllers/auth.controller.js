import { User } from "../models/auth.model.js";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import dotenv from "dotenv";

dotenv.config();

async function Register(req, res) {

    try {

        const payload = req.body;

        const hashpassword = await bcrypt.hash(payload.password, 10);

        const user = await User.create({
            username: payload.username,
            email: payload.email,
            password: hashpassword,
            role: payload.role,
        });

        if (!user) {
            return res.status(400).json({ error: "Failed to register user" });
        }

        res.status(201).json({
            message: "User registered successfully",
            user: user,
        });

    } catch (error) {
        console.log(error);
        return res.status(500).json({ error: "Internal Server Error" });
    }

}

async function Login(req, res) {
    try {

        const payload = req.body;

        const current_user = await User.findOne({ email: payload.email });
        if (!current_user) {
            return res.status(401).json({ error: "Invalid Credential" });
        }

        const comparePassword = await bcrypt.compare(payload.password, current_user.password);

        if (comparePassword == false) {
            return res.status(401).json({ error: "Invalid Credential" });
        }

        const token = jwt.sign({
            _id: current_user._id,
            role: current_user.role,
        }, process.env.JWT_SECRET, {
            expiresIn: "1h",
        });

        res.cookie("accessToken", token, {
            httpOnly: true,
            secure: true,
            sameSite: "strict"
        });

        res.status(200).json({
            message: "Login Successfully",
            user: current_user,
            token: token,
        });

    } catch (error) {
        console.log(error);
        return res.status(500).json({ error: "Internal Server Error" });
    }
}

async function GetUser(req, res) {
    try {
        const users = await User.find();
        res.status(200).json({
            message: "OKAY",
            users: users,
        });
    } catch (error) {
        console.log(error);
        return res.status(500).json({ error: "Internal Server Error" });
    }
}

export { Register, GetUser, Login };
