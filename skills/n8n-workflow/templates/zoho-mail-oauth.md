# Zoho Mail OAuth2 Setup

Complete guide voor Zoho Mail integratie met n8n via OAuth2.

## Prerequisites

- Zoho account met Mail toegang
- Admin toegang tot https://api-console.zoho.eu
- n8n instance met HTTPS (vereist voor OAuth callback)

---

## Stap 1: Zoho API Console Setup

### 1.1 Maak een Server-based Application

1. Ga naar https://api-console.zoho.eu
2. Klik **Add Client**
3. Kies **Server-based Applications**

### 1.2 Client Configuratie

| Veld | Waarde |
|------|--------|
| Client Name | `n8n-heldlab` |
| Homepage URL | `https://n8n.heldlab.be` |
| Authorized Redirect URIs | `https://n8n.heldlab.be/rest/oauth2-credential/callback` |

### 1.3 Noteer Credentials

Na aanmaken krijg je:
- **Client ID**: `1000.XXXXXXXXXX`
- **Client Secret**: `xxxxxxxxxxxxxxxxxxxxxxxx`

---

## Stap 2: n8n Credential Aanmaken

### 2.1 Via n8n UI

1. Ga naar **Settings** → **Credentials**
2. Klik **Add Credential**
3. Zoek **Zoho OAuth2 API**

### 2.2 Credential Configuratie

```json
{
  "clientId": "1000.XXXXXXXXXX",
  "clientSecret": "xxxxxxxxxxxxxxxxxxxxxxxx",
  "authUri": "https://accounts.zoho.eu/oauth/v2/auth",
  "tokenUri": "https://accounts.zoho.eu/oauth/v2/token",
  "scope": "ZohoMail.messages.READ,ZohoMail.messages.CREATE,ZohoMail.folders.READ"
}
```

### 2.3 OAuth Scopes Toelichting

| Scope | Toestemming |
|-------|-------------|
| `ZohoMail.messages.READ` | Emails lezen |
| `ZohoMail.messages.CREATE` | Emails versturen |
| `ZohoMail.folders.READ` | Folders ophalen |
| `ZohoMail.accounts.READ` | Account info |
| `ZohoMail.messages.UPDATE` | Emails markeren (gelezen/ongelezen) |
| `ZohoMail.messages.DELETE` | Emails verwijderen |

**Minimum voor email triage:**
```
ZohoMail.messages.READ,ZohoMail.folders.READ,ZohoMail.messages.UPDATE
```

---

## Stap 3: OAuth Flow Voltooien

### 3.1 Connect Account

1. Klik **Connect** in n8n credential
2. Zoho login popup verschijnt
3. Log in met het email account dat je wilt koppelen
4. Accordeer de gevraagde permissies

### 3.2 Verificatie

Test de connectie met een simpele workflow:
```
Zoho Mail Node → Get Messages → Limit: 1
```

---

## Stap 4: n8n Node Configuratie

### Zoho Mail Trigger (Polling)

```json
{
  "resource": "message",
  "operation": "getAll",
  "accountId": "{{account_id}}",
  "folderId": "INBOX",
  "options": {
    "limit": 50,
    "receivedAfter": "={{$now.minus({hours: 1}).toISO()}}"
  }
}
```

### Account ID Ophalen

Gebruik eerst een **Zoho Mail** node met:
```json
{
  "resource": "account",
  "operation": "getAll"
}
```

Dit geeft je `accountId` die je nodig hebt voor andere operaties.

---

## Stap 5: Folder IDs

### Standaard Folders

| Folder | Zoho ID |
|--------|---------|
| Inbox | Numeriek ID, bv `67890123456` |
| Sent | `sent` of numeriek |
| Drafts | `drafts` of numeriek |
| Spam | `spam` of numeriek |
| Trash | `trash` of numeriek |

### Folder ID Ophalen

```json
{
  "resource": "folder",
  "operation": "getAll",
  "accountId": "{{account_id}}"
}
```

---

## Troubleshooting

### Error: "invalid_client"
- Check Client ID en Secret
- Verify Redirect URI exact matcht (inclusief trailing slash)

### Error: "access_denied"
- User heeft permissies geweigerd
- Probeer opnieuw met juiste account

### Error: "invalid_scope"
- Scope niet toegestaan voor app type
- Check Zoho API Console → Client → Scopes

### Token Expired
n8n refresht automatisch, maar als het faalt:
1. Verwijder credential
2. Maak opnieuw aan
3. Doorloop OAuth flow opnieuw

---

## EU vs COM Datacenter

**Belangrijk:** Zoho heeft aparte datacenters!

| Regio | Auth URL | API URL |
|-------|----------|---------|
| EU | `accounts.zoho.eu` | `mail.zoho.eu` |
| US | `accounts.zoho.com` | `mail.zoho.com` |
| IN | `accounts.zoho.in` | `mail.zoho.in` |

**Held Lab gebruikt EU** → Alle URLs moeten `.eu` zijn.

### In n8n Custom OAuth2

Als je Generic OAuth2 gebruikt:
```json
{
  "authUrl": "https://accounts.zoho.eu/oauth/v2/auth",
  "accessTokenUrl": "https://accounts.zoho.eu/oauth/v2/token",
  "scope": "ZohoMail.messages.READ"
}
```

---

## Rate Limits

| Plan | API Calls/Day | Concurrent |
|------|---------------|------------|
| Free | 5,000 | 5 |
| Standard | 50,000 | 15 |
| Professional | 100,000 | 25 |

**Tip:** Gebruik caching en batch requests waar mogelijk.

---

## Security Best Practices

1. **Gebruik aparte Zoho user** voor n8n (niet persoonlijk account)
2. **Minimale scopes** - alleen wat nodig is
3. **Rotate secrets** periodiek
4. **Log access** - houd bij welke emails verwerkt worden
5. **IP Whitelist** - indien mogelijk in Zoho API Console
