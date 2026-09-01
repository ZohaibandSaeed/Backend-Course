import dotenv from "dotenv";
import express from "express";
import userRouter from "./routers.js/users.js";

dotenv.config();

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;

app.use("/api", userRouter);

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});