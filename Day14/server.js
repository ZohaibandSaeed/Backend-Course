import express from "express";
import dotenv from "dotenv";
import fileRoute from "./src/routes/file.route.js";


dotenv.config();

const app = express();

app.use(express.json());

app.use("/file", fileRoute);

app.get("/", async (req, res) => {
    res.send("Hello Word");
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`server is running at ${PORT}`);
    console.log(`localhost:${PORT}`);
})