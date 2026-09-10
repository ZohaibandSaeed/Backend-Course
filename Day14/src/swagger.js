// src/swagger.js
import swaggerJsdoc from 'swagger-jsdoc';
import swaggerUi from 'swagger-ui-express';

const options = {
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'Day14 API Documentation',
            version: '1.0.0',
            description: 'API testing ke liye Swagger documentation',
        },
        servers: [
            {
                url: 'http://localhost:8000', // Aapka local server url
                description: 'Development server',
            },
        ],
    },
    // Yeh un files ka path hai kahan aapne routes banaye hain
    apis: ['./src/docs/*.yaml'],
};

const swaggerSpec = swaggerJsdoc(options);

export const setupSwagger = (app) => {
    app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));
    console.log('Swagger Docs available at http://localhost:8000/api-docs');
};
