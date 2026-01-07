import os
from django.conf import settings
from .models import Manga
import logging

logger = logging.getLogger(__name__)

# Configuration lazily handled in get_ai_response to avoid boot time overhead

def get_shop_context():
    """Obtiene información actualizada del catálogo para dársela a la IA."""
    try:
        recently_added = Manga.objects.filter(vendido=False).order_by('-fecha_de_carga')[:10]
        recently_sold = Manga.objects.filter(vendido=True).order_by('-fecha_venta')[:5]
        
        context = "Eres el Asistente de DERSSG'M Moda. Tu objetivo es ayudar a los clientes a encontrar ropa y responder dudas sobre el catálogo.\n\n"
        context += "CATÁLOGO ACTUAL (DISPONIBLE):\n"
        for m in recently_added:
            image_url = m.front_page.url if m.front_page else "No disponible"
            context += f"- {m.nombre_del_manga}: {m.type_of_manga}, Precio: ${m.precio}, Talla: {m.talla or 'N/A'}, IMAGEN: {image_url}. {'(NUEVO)' if not m.vendido else ''}\n"
        
        context += "\nVENDIDO RECIENTEMENTE (NO DISPONIBLE):\n"
        for m in recently_sold:
            image_url = m.front_page.url if m.front_page else "No disponible"
            context += f"- {m.nombre_del_manga}: {m.type_of_manga}, IMAGEN: {image_url}\n"
            
        context += "\nINSTRUCCIONES:\n"
        context += "1. Sé amable, elegante y servicial.\n"
        context += "2. Si te preguntan por algo que está vendido, sugiere algo similar que esté disponible.\n"
        context += "3. Los precios están en pesos. Si te preguntan por ofertas, menciona que los precios son exclusivos.\n"
        context += "4. Si el usuario pide ver imágenes, 'muéstrame algo' o similares, selecciona un artículo y pon este tag al final (sin negritas ni markdown):\n"
        context += "   MOSTRAR_IMAGEN: URL_DEL_ARTICULO | NOMBRE: NOMBRE_DEL_ARTICULO\n"
        context += "   Importante: COPIA LA URL EXACTA del artículo de la lista anterior, no la resumas ni la cambies. Debe empezar con 'https://res.cloudinary.com/'.\n"
        context += "5. Comando especial 'loginsuperuser': Este comando es manejado por el sistema para permitir el acceso administrativo. Si el usuario lo escribe, no intentes procesarlo tú, el sistema tomará el control.\n"
        context += "6. Si no sabes algo, invita al usuario a esperar a que un humano lo atienda.\n"
        
        return context
    except Exception as e:
        print(f"Error getting context: {e}")
        return "Eres el asistente de DERSSG'M Moda. Ayuda al cliente en lo que necesite."

def get_ai_response(user_message, chat_history=[]):
    """Genera una respuesta usando Gemini Pro."""
    try:
        import google.generativeai as genai
        
        API_KEY = os.environ.get('GEMINI_API_KEY')
        if not API_KEY:
            # Fallback immediato si no hay key
            return "⚠️ El asistente está en mantenimiento (Clave API no configurada)."

        genai.configure(api_key=API_KEY)

        # Use a model that is available in this environment
        # Test showed gemini-2.5-flash works, while 1.5-flash was not found
        model_name = 'gemini-2.5-flash'
        
        # Construir el prompt con contexto e historial
        context = get_shop_context()
        
        # Filtrar historial para solo incluir mensajes relevantes
        history_prompts = []
        for msg in chat_history[-6:]: # Últimos 6 mensajes
            role = "model" if msg['is_from_admin'] else "user"
            history_prompts.append({"role": role, "parts": [msg['message']]})
            
        # Iniciar chat con el contexto como "system instruction"
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=context
        )
        
        chat = model.start_chat(history=history_prompts)
        response = chat.send_message(user_message)
        
        return response.text
    except Exception as e:
        print(f"Error in Gemini: {e}")
        
        # --- MOCK AI FALLBACK ---
        msg = user_message.lower()
        if "hola" in msg or "buenos dias" in msg:
            return "¡Hola! Soy el asistente de DERSSG'M. Por ahora tengo dificultades para procesar mensajes complejos, pero puedo decirte que tenemos prendas exclusivas disponibles. ¿En qué prenda estás interesado?"
        if "precio" in msg or "cuanto cuesta" in msg or "valor" in msg:
            return "Los precios varían según la prenda (entre $200 y $1200 normalmente). Puedes ver el precio exacto haciendo clic en cualquier producto del catálogo."
        if "talla" in msg or "medida" in msg:
            return "Manejamos diferentes tallas según el modelo. En la descripción de cada prenda en el catálogo podrás ver si es S, M, L o XL."
            
        # Fallback inteligente que sugiere el login
        return "⚠️ El asistente está en mantenimiento (Clave API caducada). Si eres el administrador, escribe **'entrar como admin'** o **'loginsuperuser'** para iniciar sesión manualmente."
