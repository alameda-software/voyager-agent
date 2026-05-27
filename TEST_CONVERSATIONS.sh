#!/bin/bash

# Wedding Concierge - Conversation Testing Script
# Executes test cases and documents results

API="http://localhost:8000"
CONV_ID=0

echo "=================================================="
echo "Wedding Concierge - Conversation Test Suite"
echo "=================================================="
echo ""

# Create conversation
echo "📝 Creating conversation..."
RESPONSE=$(curl -s -X POST "$API/api/v1/chat/conversations" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test - Conversation Research", "domain": "wedding", "user_id": 1}')

CONV_ID=$(echo $RESPONSE | jq '.conversation.id')
echo "✓ Conversation ID: $CONV_ID"
echo ""

# Helper function to send message and show result
test_message() {
  local test_name=$1
  local message=$2

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "TEST: $test_name"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "👤 User: $message"
  echo ""

  RESPONSE=$(curl -s -X POST "$API/api/v1/chat/send" \
    -H "Content-Type: application/json" \
    -d "{\"conversation_id\": $CONV_ID, \"content\": \"$message\"}")

  # Extract LLM response
  CONTENT=$(echo $RESPONSE | jq -r '.agent_message.content')
  MODE=$(echo $RESPONSE | jq -r '.agent_message.payload.mode')
  CATEGORY=$(echo $RESPONSE | jq -r '.agent_message.payload.category // "N/A"')
  CARDS=$(echo $RESPONSE | jq '.agent_message.payload.cards // []' | jq 'length')

  echo "🤖 System: $CONTENT"
  echo ""
  echo "📊 Metadata:"
  echo "  - Mode: $MODE"
  echo "  - Category detected: $CATEGORY"
  echo "  - Vendors returned: $CARDS"
  echo ""

  # Small pause to avoid API spam
  sleep 1
}

# ============================================
# TEST CASES
# ============================================

echo "TEST SUITE 1: Quick Vendor Searches"
echo ""

test_message "T1.1: Simple Vendor Search" \
  "Necesito fotógrafo en Sevilla"

test_message "T1.2: Search with Category" \
  "Muestra opciones de catering para 150 personas en Sevilla"

test_message "T1.3: Budget Context" \
  "DJ para boda en Sevilla, presupuesto máximo 600€"

test_message "T1.4: Different Vendor Type" \
  "¿Opciones de finca para 200 personas?"

echo ""
echo "TEST SUITE 2: Planning & Context"
echo ""

test_message "T2.1: Full Planning Info" \
  "Casamos en 6 meses, 100 invitados, Sevilla, presupuesto 5000€"

test_message "T2.2: Checklist Request" \
  "¿Me haces un plan de bodas con todas las tareas?"

echo ""
echo "TEST SUITE 3: Comparison & Details"
echo ""

test_message "T3.1: Follow-up Question" \
  "¿Cuál de los fotógrafos tiene mejor precio?"

test_message "T3.2: Filter Request" \
  "¿Opciones de catering más baratas en Sevilla?"

echo ""
echo "TEST SUITE 4: Different Categories"
echo ""

test_message "T4.1: Florist" \
  "Florista para boda en Sevilla"

test_message "T4.2: Beauty" \
  "Maquillaje y peluquería profesional en Sevilla"

test_message "T4.3: Wedding Planner" \
  "¿Hay wedding planners disponibles en Sevilla?"

echo ""
echo "TEST SUITE 5: Edge Cases"
echo ""

test_message "T5.1: Vague Question" \
  "¿Cuál es lo primero que debería hacer?"

test_message "T5.2: Budget Only" \
  "Tengo presupuesto de 3000€ en total"

test_message "T5.3: Clarification" \
  "¿Qué diferencia hay entre DJ y banda?"

echo ""
echo "=================================================="
echo "✓ Test Suite Completed"
echo "=================================================="
echo ""
echo "📋 Next steps:"
echo "1. Review results above"
echo "2. Document in CONVERSATION_RESEARCH.md what worked"
echo "3. Note improvements needed"
echo "4. Implement changes in pack.py if necessary"
echo ""
echo "Conversation ID for reference: $CONV_ID"
echo ""
