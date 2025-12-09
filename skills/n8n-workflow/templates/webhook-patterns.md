# Frontend-to-n8n Webhook Patterns

Patronen voor het verbinden van frontends (React, Next.js, static sites) met n8n workflows.

---

## Overzicht

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│    Frontend     │  POST   │    n8n          │         │    Backend      │
│    (Form/App)   │────────▶│    Webhook      │────────▶│    (Supabase/   │
│                 │         │    Trigger      │         │     API)        │
└─────────────────┘         └─────────────────┘         └─────────────────┘
        │                          │
        │                          ▼
        │                   ┌─────────────────┐
        │◀──────────────────│    Response     │
        │     JSON          │    (Success/    │
                            │     Error)      │
                            └─────────────────┘
```

---

## Pattern 1: Contact Form Submission

### Frontend (React/Next.js)

```typescript
// lib/n8n.ts
const N8N_WEBHOOK_BASE = 'https://n8n.heldlab.be/webhook';

interface ContactFormData {
  name: string;
  email: string;
  phone?: string;
  message: string;
  service?: string;
}

export async function submitContactForm(data: ContactFormData) {
  const response = await fetch(`${N8N_WEBHOOK_BASE}/contact-form`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      ...data,
      source: 'website',
      timestamp: new Date().toISOString(),
    }),
  });

  if (!response.ok) {
    throw new Error('Form submission failed');
  }

  return response.json();
}
```

### n8n Workflow

```
Webhook Trigger → Validate Data → Store in Supabase → Send Notification → Response
```

**Webhook Node Config:**
```json
{
  "httpMethod": "POST",
  "path": "contact-form",
  "responseMode": "responseNode",
  "options": {
    "allowedOrigins": "https://heldlab.be,https://www.heldlab.be"
  }
}
```

---

## Pattern 2: Booking/Appointment Request

### Frontend Component

```typescript
// components/BookingForm.tsx
interface BookingData {
  service: 'cryotherapy' | 'infrared' | 'compression' | 'consultation';
  preferredDate: string;
  preferredTime: string;
  customerName: string;
  customerEmail: string;
  customerPhone: string;
  notes?: string;
}

export async function requestBooking(data: BookingData) {
  const response = await fetch('https://n8n.heldlab.be/webhook/booking-request', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ...data,
      brand: 'held-lab',
      requestedAt: new Date().toISOString(),
    }),
  });

  const result = await response.json();

  if (result.status === 'confirmed') {
    return { success: true, bookingId: result.bookingId };
  } else if (result.status === 'pending') {
    return { success: true, message: 'We nemen contact op ter bevestiging' };
  } else {
    throw new Error(result.error || 'Booking failed');
  }
}
```

### n8n Workflow Structure

```
Webhook → Validate → Check Availability → Create Booking → Send Confirmations → Response
              │              │
              ▼              ▼
         Return Error   Return "pending"
         if invalid     if manual review needed
```

---

## Pattern 3: Lead Capture (Multi-step Form)

### Frontend State Management

```typescript
// hooks/useLeadCapture.ts
interface LeadData {
  step1: { email: string; interest: string };
  step2: { name: string; phone: string };
  step3: { budget: string; timeline: string };
}

export function useLeadCapture() {
  const [leadId, setLeadId] = useState<string | null>(null);

  // Step 1: Create lead with email only
  const captureEmail = async (email: string, interest: string) => {
    const res = await fetch('https://n8n.heldlab.be/webhook/lead-capture', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'create',
        email,
        interest,
        source: window.location.pathname,
      }),
    });
    const { leadId } = await res.json();
    setLeadId(leadId);
    return leadId;
  };

  // Step 2+: Update existing lead
  const updateLead = async (data: Partial<LeadData>) => {
    if (!leadId) throw new Error('No lead ID');

    await fetch('https://n8n.heldlab.be/webhook/lead-capture', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'update',
        leadId,
        ...data,
      }),
    });
  };

  return { captureEmail, updateLead, leadId };
}
```

---

## Pattern 4: Real-time Status Check

### Polling Pattern

```typescript
// Check booking/order status
export async function checkStatus(referenceId: string): Promise<Status> {
  const response = await fetch(
    `https://n8n.heldlab.be/webhook/status-check?id=${referenceId}`,
    { method: 'GET' }
  );
  return response.json();
}

// Usage with polling
function useStatusPolling(referenceId: string) {
  const [status, setStatus] = useState<Status | null>(null);

  useEffect(() => {
    const poll = async () => {
      const newStatus = await checkStatus(referenceId);
      setStatus(newStatus);

      if (newStatus.status !== 'completed' && newStatus.status !== 'failed') {
        setTimeout(poll, 5000); // Poll every 5 seconds
      }
    };

    poll();
  }, [referenceId]);

  return status;
}
```

---

## Security Patterns

### 1. CORS Configuration

**n8n Webhook Node:**
```json
{
  "options": {
    "allowedOrigins": "https://heldlab.be,https://reconnect-academy.be"
  }
}
```

### 2. Request Validation

**In n8n workflow (Function Node):**
```javascript
// Validate required fields
const required = ['email', 'name', 'message'];
const missing = required.filter(field => !$input.item.json[field]);

if (missing.length > 0) {
  return {
    json: {
      error: true,
      message: `Missing required fields: ${missing.join(', ')}`
    }
  };
}

// Validate email format
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (!emailRegex.test($input.item.json.email)) {
  return {
    json: {
      error: true,
      message: 'Invalid email format'
    }
  };
}

return $input.item;
```

### 3. Rate Limiting

**Frontend:**
```typescript
// Simple client-side rate limiting
const submitTimes: number[] = [];
const RATE_LIMIT = 3; // Max 3 submissions
const RATE_WINDOW = 60000; // Per minute

function checkRateLimit(): boolean {
  const now = Date.now();
  const recentSubmits = submitTimes.filter(t => now - t < RATE_WINDOW);

  if (recentSubmits.length >= RATE_LIMIT) {
    return false;
  }

  submitTimes.push(now);
  return true;
}
```

**n8n (Redis/Memory check):**
```javascript
// In Function Node - track by IP
const clientIP = $input.item.headers['x-forwarded-for'] || 'unknown';
const rateKey = `rate:${clientIP}`;

// Use n8n's built-in rate limiting or external Redis
```

### 4. Honeypot Field (Spam Prevention)

**Frontend:**
```tsx
// Hidden field that bots will fill
<input
  type="text"
  name="website"
  style={{ display: 'none' }}
  tabIndex={-1}
  autoComplete="off"
/>
```

**n8n Validation:**
```javascript
// If honeypot field is filled, it's likely a bot
if ($input.item.json.website && $input.item.json.website.length > 0) {
  return { json: { error: true, message: 'Spam detected' } };
}
```

### 5. Webhook Authentication (API Key)

**Frontend:**
```typescript
const response = await fetch('https://n8n.heldlab.be/webhook/secure-endpoint', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Webhook-Key': process.env.NEXT_PUBLIC_N8N_WEBHOOK_KEY,
  },
  body: JSON.stringify(data),
});
```

**n8n Header Auth:**
```json
{
  "authentication": "headerAuth",
  "headerAuth": {
    "name": "X-Webhook-Key",
    "value": "={{$credentials.webhookKey}}"
  }
}
```

---

## Response Patterns

### Success Response
```json
{
  "success": true,
  "message": "Bedankt voor je bericht!",
  "referenceId": "HLD-2024-001234",
  "nextSteps": "We nemen binnen 24 uur contact op."
}
```

### Validation Error
```json
{
  "success": false,
  "error": "validation_error",
  "message": "Email is verplicht",
  "fields": {
    "email": "Dit veld is verplicht"
  }
}
```

### Server Error
```json
{
  "success": false,
  "error": "server_error",
  "message": "Er ging iets mis. Probeer later opnieuw."
}
```

---

## n8n Response Node Setup

```json
{
  "respondWith": "json",
  "responseBody": "={{ JSON.stringify($json) }}",
  "responseCode": "={{ $json.error ? 400 : 200 }}",
  "responseHeaders": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "https://heldlab.be"
  }
}
```

---

## Testing Webhooks

### cURL Test
```bash
curl -X POST https://n8n.heldlab.be/webhook-test/contact-form \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","message":"Test message"}'
```

### n8n Test Mode
- Gebruik `/webhook-test/` URL tijdens development
- Switch naar `/webhook/` voor productie (alleen actief als workflow actief is)

---

## Held Lab Specifieke Endpoints

| Endpoint | Doel | Method |
|----------|------|--------|
| `/webhook/contact-form` | Algemeen contactformulier | POST |
| `/webhook/booking-request` | Afspraak aanvragen | POST |
| `/webhook/lead-capture` | Multi-step lead form | POST |
| `/webhook/newsletter-signup` | Email lijst | POST |
| `/webhook/status-check` | Status opvragen | GET |
