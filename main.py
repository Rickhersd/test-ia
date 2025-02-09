import gzip
import pickle
from fastapi import FastAPI, status, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from keras.preprocessing.image import img_to_array
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with gzip.open('./model_low_size_pkl.gz', 'r') as f:
    model = pickle.load(f)


@app.post("/api/ia-model")
def ia_model(file:  UploadFile):
    try:
        img = Image.open(file.file)
        img = img.resize(size=(200, 200))
        img = img_to_array(img)
        img = img.reshape(1, 200, 200, 3)
        img = img.astype('float32')
        img = img - [123.68, 116.779, 103.939]
        result = model.predict(img)
        num_result = result[0][0]

        return JSONResponse(
            content={
                "status": "success",
                "result": "dog" if num_result == 1 else "cat"
            },
            status_code=status.HTTP_200_OK
        )

    except Exception as ex:
        raise HTTPException(f"Cannot predict the image {str(ex)}") from ex
