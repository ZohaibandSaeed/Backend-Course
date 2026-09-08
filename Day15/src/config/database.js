import mongoose from "mongoose";
import dotenv from "dotenv";

dotenv.config();

const MONGODB_URI = process.env.MONGODB_URI;

async function ConnectDB() {
    try {
        await mongoose.connect(MONGODB_URI);
        console.log("Connection Successfully Created");
    } catch (error) {
        console.log("Error Connecting to DataBase:", error.message);
    }
}

export { ConnectDB };