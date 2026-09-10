import mongoose from "mongoose";
import dotenv from "dotenv";

dotenv.config();

const mongo_url = process.env.MONGODB_URL;
async function ConnectDB() {
    try {

        const db = await mongoose.connect(mongo_url);
        console.log(db.connection.host);
        console.log(`Connected Successfully`);

    } catch (error) {
        console.error(error);
        throw error;
    }
}

export { ConnectDB };