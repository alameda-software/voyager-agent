# MYPLAN.md — Lo que tiene que tener la app

**Producto:** LiveGate (Wedding + Voyager Concierge)  
**Última actualización:** 2026-05-28

---

## 🏗️ Features del Producto

### ✅ Ya implementado
- Chat con AI (GPT-4o) para planificación de bodas y viajes
- Catálogo de proveedores por categoría (Venue, Catering, Foto, Música, Flores, Tarta, Transporte, Belleza, Invitaciones, Planner)
- Plan de boda: añadir proveedores, marcar preferidos, reservar
- Calendario con checklist por fases
- Browse de proveedores con imágenes Unsplash
- Navegación por pestañas (Inicio, Chats, Vendors, Plan, Calendario)

---

## 🚀 Por Implementar

### 👤 Portal del Proveedor (Vendor Portal)
- **Subir fotos** — el vendor puede añadir/gestionar su galería de imágenes
- **Editar datos** — nombre, descripción, precio, disponibilidad, capacidad
- **Panel propio** — login separado para vendors, dashboard simple
- **Verificación** — badge de proveedor verificado

### 📧 Sistema de Email (Email Relay)
- Cada pareja recibe un alias `nombre1.nombre2@livegate.es`
- Los vendors nunca ven el email personal de la pareja
- La app muestra el hilo de comunicación por vendor
- AI redacta respuestas → pareja aprueba con un tap → enviado
- Forward automático al Gmail real de la pareja
- **Stack**: Resend.com + MX records en `livegate.es`

### 🌐 Página Web Pública (livegate.es)
- Landing page del producto
- Registro de parejas y vendors
- SEO para búsqueda orgánica de proveedores
- Perfil público de cada vendor (URL compartible)

### 🔐 Autenticación de Usuarios
- Login real para parejas (email + contraseña / Google OAuth)
- Login separado para vendors
- Perfil de la pareja: nombre, fecha de boda, ciudad, presupuesto

### 📱 Mejoras de UX
- Notificaciones push (eventos del calendario, respuestas de vendors)
- Modo offline básico
- Compartir plan con pareja / familia

---

## 💡 Ideas a Evaluar
*(Ver también ideas.md)*

- Integración Google Maps para venues y tours
- Presupuesto interactivo (tracker de gastos por categoría)
- Checklist colaborativa (los dos de la pareja)
- Reviews reales de vendors (post-boda)
- Integración con calendario Google/Apple

---

## 📌 Notas
- Dominio: `livegate.es` (a confirmar)
- App actual en: `http://voyager.leafgate.es`
- Repo: `github.com/alameda-software/voyager-agent`
