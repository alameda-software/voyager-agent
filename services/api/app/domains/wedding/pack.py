from __future__ import annotations
import json
from app.domains.base import DomainReply
from app.models import ConciergeDomain

FUNCTIONS = [
    {
        "name": "search_vendors",
        "description": "Search wedding vendors. Call this when you know the category needed and location.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Vendor category",
                    "enum": ["all", "venue", "catering", "photography", "music",
                             "florist", "cake", "transport", "beauty", "invitations", "planner"],
                },
                "location": {"type": "string"},
                "guest_count": {"type": "integer"},
                "budget": {"type": "integer"},
            },
            "required": ["category"],
        },
    },
    {
        "name": "generate_wedding_checklist",
        "description": "Generate a personalised wedding planning checklist and timeline based on the wedding date and requirements gathered.",
        "parameters": {
            "type": "object",
            "properties": {
                "wedding_date": {"type": "string", "description": "Wedding date or month/year"},
                "months_away": {"type": "integer", "description": "Months until wedding"},
                "guest_count": {"type": "integer"},
                "location": {"type": "string"},
                "budget": {"type": "integer"},
                "priorities": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Most important things to the couple",
                },
            },
            "required": ["wedding_date"],
        },
    },
    {
        "name": "confirm_vendor",
        "description": "Confirm when the user selects a specific vendor to add to their wedding plan.",
        "parameters": {
            "type": "object",
            "properties": {
                "vendor_name": {"type": "string"},
                "vendor_type": {"type": "string"},
                "price": {"type": "string"},
            },
            "required": ["vendor_name", "vendor_type"],
        },
    },
]

SYSTEM_PROMPT = """You are a warm, experienced wedding planning concierge for Spain.
You help couples plan their perfect wedding step by step — fully conversational and personalised.

Your job is to:
1. Gather: location, date, guest count, budget, style/vibe
2. Then work through each category the couple needs:
   venue → catering → photography → music → florist → cake → transport → beauty → invitations → planner
3. Search vendors when you know what category is needed
4. Generate a planning checklist when you have enough info
5. Confirm selections as they choose

Rules:
- Ask one thing at a time — don't overwhelm
- When a category is discussed, call search_vendors with that specific category
- When couple has date + guest count + location → offer to call generate_wedding_checklist
- When couple picks a vendor → call confirm_vendor
- Be warm, celebratory, practical. Use Spanish wedding context naturally (hacienda, aperitivo, barra libre etc.)
- NEVER list vendor results as text — the cards are shown visually
- Keep replies to 1-2 sentences unless giving advice or the checklist"""


def _make_checklist(args: dict) -> dict:
    """Generate a wedding planning checklist."""
    months = args.get("months_away", 12)
    location = args.get("location", "Sevilla")
    guests = args.get("guest_count", 100)
    date = args.get("wedding_date", "")

    checklist = {
        "title": f"Plan de boda · {date}",
        "location": location,
        "guest_count": guests,
        "phases": []
    }

    if months >= 12:
        checklist["phases"].append({
            "phase": "12+ meses antes",
            "emoji": "📅",
            "tasks": [
                "Fijar la fecha de boda",
                "Definir el presupuesto total",
                "Reservar el lugar/hacienda (se agotan rápido)",
                "Elegir wedding planner (opcional)",
                "Hacer lista de invitados preliminar",
            ]
        })
    if months >= 9:
        checklist["phases"].append({
            "phase": "9-12 meses antes",
            "emoji": "📸",
            "tasks": [
                "Contratar fotógrafo y videógrafo",
                "Reservar catering o confirmar menú con la hacienda",
                "Buscar y reservar música/DJ",
                "Empezar búsqueda de vestido de novia",
                "Contratar florista para consulta inicial",
            ]
        })
    if months >= 6:
        checklist["phases"].append({
            "phase": "6-9 meses antes",
            "emoji": "💌",
            "tasks": [
                "Encargar invitaciones",
                "Confirmar transporte (coche novia + autobús invitados)",
                "Reservar hotel de noche de bodas",
                "Elegir pastel de boda",
                "Reservar maquillaje y peluquería",
            ]
        })
    if months >= 3:
        checklist["phases"].append({
            "phase": "3-6 meses antes",
            "emoji": "💍",
            "tasks": [
                "Enviar invitaciones y confirmar asistencias",
                "Organizar seating plan",
                "Planificar luna de miel",
                "Comprar/alquilar traje del novio",
                "Coordinar detalles para invitados",
            ]
        })
    checklist["phases"].append({
        "phase": "Último mes",
        "emoji": "✨",
        "tasks": [
            "Confirmar todos los proveedores",
            "Entrega de arras y anillos",
            "Últimos detalles con wedding planner o coordinador",
            "Ensayo de la ceremonia",
            "¡Disfrutar del gran día! 🎉",
        ]
    })

    return checklist


class WeddingPack:
    domain = ConciergeDomain.WEDDING

    def initial_state(self, title: str) -> dict:
        return {
            "title": title,
            "status": "collecting_requirements",
            "location": None,
            "event_date": None,
            "guest_count": None,
            "budget": None,
            "vendors_confirmed": [],
            "checklist_generated": False,
        }

    def merge_state(self, state: dict, user_message: str) -> dict:
        return {**state}

    def agent_reply(self, state: dict, history: list | None = None) -> DomainReply:
        from app.config import settings
        from app.services.fake_data import search_vendors
        from openai import OpenAI

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in (history or []):
            messages.append({"role": msg["role"], "content": msg["content"]})

        client = OpenAI(api_key=settings.openai_api_key)

        try:
            response = client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                functions=FUNCTIONS,
                function_call="auto",
                max_tokens=400,
                temperature=0.7,
            )
            msg = response.choices[0].message

            if msg.function_call:
                fn = msg.function_call.name
                args = json.loads(msg.function_call.arguments)

                if fn == "search_vendors":
                    cards = search_vendors(
                        category=args.get("category", "all"),
                        location=args.get("location", "Sevilla"),
                        guest_count=args.get("guest_count", 100),
                        budget=args.get("budget"),
                    )
                    messages.append({"role": "assistant", "content": None,
                                     "function_call": {"name": fn, "arguments": msg.function_call.arguments}})
                    messages.append({"role": "function", "name": fn, "content": json.dumps(cards[:4])})
                    follow_up = client.chat.completions.create(
                        model=settings.llm_model, messages=messages,
                        max_tokens=150, temperature=0.7,
                    )
                    reply_text = follow_up.choices[0].message.content.strip()
                    return DomainReply(
                        content=reply_text,
                        payload={"mode": "vendor_results", "domain": self.domain.value,
                                 "category": args.get("category"), "cards": cards[:4]},
                    )

                elif fn == "generate_wedding_checklist":
                    checklist = _make_checklist(args)
                    messages.append({"role": "assistant", "content": None,
                                     "function_call": {"name": fn, "arguments": msg.function_call.arguments}})
                    messages.append({"role": "function", "name": fn, "content": json.dumps(checklist)})
                    follow_up = client.chat.completions.create(
                        model=settings.llm_model, messages=messages,
                        max_tokens=200, temperature=0.7,
                    )
                    reply_text = follow_up.choices[0].message.content.strip()
                    return DomainReply(
                        content=reply_text,
                        payload={"mode": "checklist", "domain": self.domain.value, "checklist": checklist},
                    )

                elif fn == "confirm_vendor":
                    name = args.get("vendor_name", "el proveedor")
                    vtype = args.get("vendor_type", "")
                    reply_text = f"✅ ¡Perfecto! He añadido **{name}** a tu plan de boda. ¿Qué categoría quieres ver ahora?"
                    return DomainReply(
                        content=reply_text,
                        payload={"mode": "vendor_confirmed", "domain": self.domain.value, "vendor": args},
                    )

            reply_text = msg.content.strip() if msg.content else "¡Hola! Cuéntame sobre vuestra boda. ¿Tenéis ya una fecha en mente?"

        except Exception as e:
            reply_text = f"Tengo un problema de conexión. Inténtalo de nuevo. ({e})"

        return DomainReply(content=reply_text, payload={"mode": "llm", "domain": self.domain.value})


wedding_pack = WeddingPack()
