from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

PARTS = {
    "COMPUTADORAS": ["Mouse", "Teclado", "Monitor"],
    "MICROONDAS": ["Buscalo en google"],
    "TELEFONOS": ["Camara", "Pantalla Amoled", ""],
}


@app.get('/')
def index(request: Request):
    result = ""
    return templates.TemplateResponse(
        "index.html",
        context={'request': request, 'result': result}
    )


@app.post("/")
def form_post(request: Request, frase: str = Form(...)):

    response = None

    try:
        genai.configure(api_key="AIzaSyAHg3udnO0f4MKmZIE4YJbHBl4yZJr1SF0")
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(f"""Te proporciono una lista de topicos: ["COMPUTADORAS", "MICROONDAS", "TELEFONOS"]]
            Identifica del siguiente texto "{frase}" si se menciona, habla, se pregunta o se describe algo sobre uno de los topicos que se te
            propocionaron. Debes ser muy preciso. En el caso de que la frase efectivamente hable sobre uno de los topicos, responde unicamente con la palabra del topico.
            en caso contrario, responde con la palabra "UNKWON". Unicamente debes responder una palabra."
        """)

        response_model = str(response.text).strip()

        if response_model == "UNKWON":
            response = "No te entiendo man"
        elif PARTS.get(response_model, None):
            response = ", ".join(PARTS.get(response_model))
        else:
            response = "No se pudo solicitar la pregunta"

    except Exception as ex:
        print(ex)
        response = "Picaron"

    return templates.TemplateResponse(
        'index.html',
        context={'request': request, 'result': response}
    )
