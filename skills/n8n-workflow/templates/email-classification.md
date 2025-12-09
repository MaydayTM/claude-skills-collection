# AI Email Classification Template

Automatische email triage voor Held Lab met AI-powered classificatie.

## Classificatie Categorieën

| Categorie | Label | Actie |
|-----------|-------|-------|
| Spam/Irrelevant | `spam` | Archiveren, geen actie |
| Bestaande Klant | `existing_customer` | Route naar CRM, prioriteit hoog |
| Nieuwe Aanvraag | `new_inquiry` | Lead pipeline, follow-up starten |
| Dienst Vraag | `service_question` | FAQ check, eventueel doorsturen |
| Urgent | `urgent` | Direct notificatie naar team |

---

## Workflow Structuur

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Zoho Mail   │───▶│  AI Classify │───▶│   Router     │
│  Trigger     │    │  (Claude/    │    │   (Switch)   │
│              │    │   OpenAI)    │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    ▼                          ▼                          ▼
             ┌──────────────┐          ┌──────────────┐          ┌──────────────┐
             │    Spam      │          │   New Lead   │          │  Existing    │
             │  (Archive)   │          │  (Supabase + │          │  Customer    │
             │              │          │   Notify)    │          │  (CRM Update)│
             └──────────────┘          └──────────────┘          └──────────────┘
```

---

## AI Classification Prompt

```
Je bent een email classifier voor Held Lab, een biohacking en recovery therapie centrum.

Analyseer de volgende email en classificeer in EXACT één categorie:

EMAIL:
Van: {{$json.from}}
Onderwerp: {{$json.subject}}
Inhoud: {{$json.body}}

CATEGORIEËN:
- spam: Reclame, irrelevant, automated messages
- existing_customer: Afzender is bekende klant (check email domain/naam)
- new_inquiry: Nieuwe potentiële klant, vraagt info over diensten
- service_question: Vraag over bestaande boeking, openingstijden, etc.
- urgent: Medische vraag, klacht, annulering binnen 24u

RESPONSE FORMAT (alleen JSON):
{
  "category": "category_name",
  "confidence": 0.0-1.0,
  "reasoning": "korte uitleg",
  "suggested_action": "aanbevolen actie"
}
```

---

## Node Configuraties

### 1. Zoho Mail Trigger
```json
{
  "resource": "message",
  "operation": "getAll",
  "folderId": "INBOX",
  "returnAll": false,
  "limit": 10,
  "filters": {
    "isRead": false
  }
}
```

### 2. AI Classification Node (HTTP Request to Claude/OpenAI)
```json
{
  "method": "POST",
  "url": "https://api.anthropic.com/v1/messages",
  "headers": {
    "x-api-key": "{{$credentials.anthropicApiKey}}",
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
  },
  "body": {
    "model": "claude-3-haiku-20240307",
    "max_tokens": 256,
    "messages": [
      {
        "role": "user",
        "content": "{{classification_prompt}}"
      }
    ]
  }
}
```

### 3. Switch Node (Router)
```json
{
  "rules": [
    {
      "output": 0,
      "conditions": {
        "conditions": [
          {
            "leftValue": "={{$json.category}}",
            "rightValue": "spam",
            "operator": "equals"
          }
        ]
      }
    },
    {
      "output": 1,
      "conditions": {
        "conditions": [
          {
            "leftValue": "={{$json.category}}",
            "rightValue": "new_inquiry",
            "operator": "equals"
          }
        ]
      }
    },
    {
      "output": 2,
      "conditions": {
        "conditions": [
          {
            "leftValue": "={{$json.category}}",
            "rightValue": "existing_customer",
            "operator": "equals"
          }
        ]
      }
    }
  ]
}
```

### 4. Supabase Insert (New Lead)
```json
{
  "resource": "row",
  "operation": "create",
  "tableId": "leads",
  "columns": {
    "email": "={{$json.from}}",
    "subject": "={{$json.subject}}",
    "source": "email",
    "status": "new",
    "ai_classification": "={{$json.category}}",
    "ai_confidence": "={{$json.confidence}}"
  }
}
```

---

## Bekende Klanten Check (Optioneel)

Voeg een Supabase lookup toe vóór classificatie:

```json
{
  "resource": "row",
  "operation": "getAll",
  "tableId": "customers",
  "filters": {
    "email": "={{$json.from}}"
  }
}
```

Als resultaat > 0: automatisch `existing_customer` label.

---

## Monitoring & Optimalisatie

### Log elke classificatie
```sql
INSERT INTO email_classifications (
  email_id, from_address, subject,
  ai_category, ai_confidence,
  created_at
) VALUES (...)
```

### Review laag-confidence classificaties
- Filter op `confidence < 0.7`
- Handmatig reviewen
- Gebruik voor prompt verbetering

### Metrics
- Classificatie accuracy per categorie
- Gemiddelde confidence score
- False positive rate voor spam
