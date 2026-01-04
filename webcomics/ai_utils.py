import os
import google.generativeai as genai
from django.conf import settings
from .models import Manga

# Configuration de Gemini
API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyDnIncZ2x9w1V7-QqdvDX3Ot799jKXdrT8')
genai.configure(api_key=API_KEY)

def get_shop_context():
    """Obtiene información actualizada del catálogo para dársela a la IA."""
    try:
        recently_added = Manga.objects.filter(vendido=False).order_by('-fecha_de_carga')[:10]
        recently_sold = Manga.objects.filter(vendido=True).order_by('-fecha_venta')[:5]
        
        context = "Eres el Asistente de DERSSG'M Moda. Tu objetivo es ayudar a los clientes a encontrar ropa y responder dudas sobre el catálogo.\n\n"
        context += "CATÁLOGO ACTUAL (DISPONIBLE):\n"
        for m in recently_added:
            context += f"- {m.nombre_del_manga}: {m.type_of_manga}, Precio: ${m.precio}, Talla: {m.talla or 'N/A'}. {'(NUEVO)' if not m.vendido else ''}\n"
        
        context += "\nVENDIDO RECIENTEMENTE (NO DISPONIBLE):\n"
        for m in recently_sold:
            context += f"- {m.nombre_del_manga}: {m.type_of_manga}\n"
            
        context += "\nINSTRUCCIONES:\n"
        context += "1. Sé amable, elegante y servicial.\n"
        context += "2. Si te preguntan por algo que está vendido, sugiere algo similar que esté disponible.\n"
        context += "3. Los precios están en pesos. Si te preguntan por ofertas, menciona que los precios son exclusivos.\n"
        context += "4. Si no sabes algo, invita al usuario a esperar a que un humano lo atienda.\n"
        
        return context
    except Exception as e:
        print(f"Error getting context: {e}")
        return "Eres el asistente de DERSSG'M Moda. Ayuda al cliente en lo que necesite."

def get_ai_response(user_message, chat_history=[]):
    """Genera una respuesta usando Gemini Pro 1.5."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Construir el prompt con contexto e historial
        context = get_shop_context()
        
        # Filtrar historial para solo incluir mensajes relevantes
        history_prompts = []
        for msg in chat_history[-6:]: # Últimos 6 mensajes
            role = "model" if msg['is_from_admin'] else "user"
            history_prompts.append({"role": role, "parts": [msg['message']]})
            
        # Iniciar chat con el contexto como "system instruction" (simulado en el primer mensaje si no hay system_instruction nativa fácil)
        # Gemini 1.5 soporte system_instruction directamente:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=context
        )
        
        chat = model.start_chat(history=history_prompts)
        response = chat.send_message(user_message)
        
        return response.text
    except Exception as e:
        print(f"Error in Gemini: {e}")
        return "Lo siento, estoy teniendo dificultades técnicas. Un humano te atenderá pronto."
